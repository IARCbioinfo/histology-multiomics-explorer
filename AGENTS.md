# Instructions for coding agents

This repository is the Tumour Histology and Multi-omics Explorer, a static site that catalogues public tumour datasets linking histology with molecular data. `README.md` describes the site and `data/README.md` defines every data field. `llms.txt` is for agents reading the published site, not for editing it.

If an untracked `AGENTS.local.md` exists, read it too. It holds a maintainer's local instructions and is never committed.

## Layout

- Pages are HTML files at the root, styled by `assets/css/site.css` and rendered by vanilla ES modules in `assets/js/`. `common.js` holds the shared helpers and the display labels (`LABELS`). There is no build step and no dependency.
- Curated metadata are in `data/*.json`: `cancers.json`, `evidence.json`, `cohorts.json`, `captures.json`, `release.json` and `tcga_resources.json` are maintained by hand.
- Script-written data: `scripts/build_tcga.py` writes `tcga_counts.json`, `tcga_patients.json` and `tcga_flags.json`; `scripts/import_tcga_review.py` writes `tcga_reviews.json`; `scripts/import_patient_review.py` writes `tcga_patient_review.json` and `tcga_eligibility.json`, and `scripts/remove_excluded_projects.py`, run after the TCGA imports, removes projects outside the study from the patient-level files; `scripts/import_spatial_review.py` updates the reviewed spatial records in `cohorts.json`, and `scripts/import_spatial_route_review.py`, run after it, applies the public-route review and writes `leads.json`. Change these through their scripts, not by hand.
- Generated agent files: `llms.txt`, `md/`, `data/by-cancer/`, `data/index.json`, `data/glossary.json`, `schemas/` and the block between the `agent:dataset-jsonld` markers in `index.html`. `scripts/build_agent_files.py` writes them; never edit them by hand.
- `mcp/` is the read-only MCP server. Its queries live in `mcp/src/explorer_mcp/catalogue.py` (standard library only, also used by `scripts/check.py`); `server.py` registers them as tools. A new or renamed tool must be documented in `agents.html` and `README.md`, which the checks verify.
- Controlled vocabularies are in `scripts/vocab.py`. A new value also needs a display label in `LABELS`.

## Commands

Python 3.10 or later. The site scripts use the standard library only; the MCP server is run with uv.

```bash
python3 scripts/build_agent_files.py          # after any change in data/
python3 scripts/check.py                      # must pass before a commit
uv run --directory mcp python smoke_test.py   # after any change to mcp/
python3 -m http.server 8000                   # local preview at http://localhost:8000/
```

The browser may keep an old copy of a page after an edit; reload with the cache bypassed before judging a layout.

## Rules

- Public metadata only. Do not add clinical notes, pathology report text, free-text annotations, local file paths, credentials or unpublished data to `data/`, the pages or the Git history.
- Preserve hand edits in `data/`. Do not regenerate it from the original seed export, which would overwrite later curation.
- `scripts/check.py` pins the approved panel counts and cohort memberships. A change to them is a scientific decision for the maintainer, not a fix to make the check pass.
- Keep the meaning of counts: the selected analysis panel and general availability are reported separately; spatial studies involve patients other than those in TCGA; counts reported by different studies, or in different units, are never added; an unknown count is absent or null, not zero; there is no treated TCGA reference set; integrated WHO diagnoses for glioma are not adjudicated.
- Some page wording is mirrored in `scripts/build_agent_files.py` (the points in `KEY_POINTS`, table captions and page introductions). Change both.
- After a data or page change, update `version` and `date` in `data/release.json`.
- Every page has the same header with six links, the current one marked `aria-current="page"`, and must not scroll sideways at 375 px.
- Write plain scientific British English (tumour, oesophageal), keep stated caveats and avoid em dashes.
- Do not deploy, publish or push without the maintainer's approval.
