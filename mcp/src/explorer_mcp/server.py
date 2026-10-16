"""MCP server exposing the read-only catalogue queries over stdio.

Usage: histology-multiomics-explorer-mcp [--source PATH_OR_URL]
The source is an Explorer checkout or the published site URL; inside a checkout it is found automatically.
"""
import argparse
import sys

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from . import __version__
from .catalogue import INSTRUCTIONS, TOOLS, Catalogue, SourceError

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


def build_server(source=None):
    cat = Catalogue(source)
    server = MCPServer(name="histology-multiomics-explorer", title="Tumour Histology and Multi-omics Explorer",
                       instructions=INSTRUCTIONS, version=__version__)
    for name, description in TOOLS:
        server.add_tool(getattr(cat, name), name=name, description=description, annotations=READ_ONLY)

    @server.resource("explorer://llms.txt", name="llms.txt", description="Agent guide to the Explorer: key points and links", mime_type="text/markdown")
    def llms_txt() -> str:
        return cat.text("llms.txt")

    return server


def main():
    parser = argparse.ArgumentParser(description="Read-only MCP server for the Tumour Histology and Multi-omics Explorer.")
    parser.add_argument("--source", help="Explorer checkout path or published site URL (default: the checkout containing this package, or $EXPLORER_SOURCE)")
    args = parser.parse_args()
    try:
        server = build_server(args.source)
    except SourceError as e:
        sys.exit(f"histology-multiomics-explorer-mcp: {e}")
    server.run("stdio")


if __name__ == "__main__":
    main()
