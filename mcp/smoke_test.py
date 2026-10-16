"""End-to-end check over the MCP protocol: start the server on stdio, list its tools, call them and compare with the data.

Usage (from mcp/): uv run python smoke_test.py
"""
import asyncio
import json
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from explorer_mcp.catalogue import TOOLS, Catalogue


def payload(result):
    if result.is_error:
        raise AssertionError(result.content[0].text)
    return json.loads(result.content[0].text)


async def main():
    expected = Catalogue()
    elig = expected._data("tcga_eligibility")
    params = StdioServerParameters(command=sys.executable, args=["-m", "explorer_mcp.server"])
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        init = await session.initialize()
        tools = {t.name: t for t in (await session.list_tools()).tools}
        assert set(tools) == {n for n, _ in TOOLS}, sorted(tools)
        assert all(t.annotations and t.annotations.read_only_hint for t in tools.values())
        o = payload(await session.call_tool("catalogue_overview", {}))
        assert o["tcga"]["selected_patients"] == elig["panel"]["selected_analysis"]["total"]
        for cohort, c in elig["cohorts"].items():
            r = payload(await session.call_tool("search_tcga_patients", {"cohort": cohort, "selected": True, "limit": 1}))
            assert (r["patients"], r["with_both"]) == (c["selected_analysis"]["total"], c["selected_analysis"]["paired"]), cohort
        s = payload(await session.call_tool("search_spatial_sections", {"cancer": "PDAC", "strict": True}))
        assert s["sections"] == sum(1 for x in expected._data("captures") if x["cancer"] == "PDAC" and x["tier"] == "core" and x["treatment"] == "Untreated")
        caps = expected._data("captures")
        for level in ("original", "preview"):
            r = payload(await session.call_tool("search_spatial_sections", {"image_level": level, "limit": 1}))
            assert r["sections"] == sum(x["image_level"] == level for x in caps), level
        sp = o["spatial"]
        assert (sp["section_records_original_he"], sp["section_records_preview_image"] + sp["preview_sections_counted_without_records"]) == (
            sum(x["image_level"] == "original" for x in caps), sum(x["image_level"] == "preview" for x in caps) + sp["preview_sections_counted_without_records"])
        assert sp["known_study_local_patients"] == len({(x["cohort"], x["patient"]) for x in caps if x["patient"]}) and sp["eligible_patients"] is None
        bad = payload(await session.call_tool("get_cancer_type", {"code": "XYZ"}))
        assert "error" in bad
        guide = await session.read_resource("explorer://llms.txt")
        assert guide.contents[0].text.startswith("# Tumour Histology and Multi-omics Explorer")
        print(f"MCP smoke test passed: server {init.server_info.name} {init.server_info.version}, {len(tools)} read-only tools, "
              f"{len(elig['cohorts'])} cohort totals match, release {o['release']}")


asyncio.run(main())
