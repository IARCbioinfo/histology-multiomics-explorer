#!/usr/bin/env python3
"""Generate the agent-readable layer of the explorer from data/*.json.

Writes llms.txt, Markdown versions of the TCGA, spatial and cancer pages (md/),
one JSON file per cancer page (data/by-cancer/), JSON Schemas for every data
file (schemas/) and the data index (data/index.json), and refreshes the
schema.org Dataset block in index.html. Do not edit these files by hand.

Usage: python3 scripts/build_agent_files.py          # write the files
       python3 scripts/build_agent_files.py --check  # list stale files, exit 1 if any
Standard library only. scripts/check.py runs the same comparison.
"""
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from vocab import ENUMS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mcp" / "src"))
from explorer_mcp.catalogue import TOOLS as MCP_TOOLS  # noqa: E402  (standard library module)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NAME = "Tumour Histology and Multi-omics Explorer"
# Published base URL, ending with "/". While empty, every link stays relative to the site root.
SITE_URL = "https://iarcbioinfo.github.io/histology-multiomics-explorer/"
REPO = "https://github.com/IARCbioinfo/histology-multiomics-explorer"
# Licence of the curated metadata (name, URL). While None, no licence is stated in llms.txt or the Dataset block.
LICENCE = ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/")

SOURCE_FILES = {  # file: (description, how records are counted)
    "release.json": ("Release version, date and the dates on which sources were checked", None),
    "cancers.json": ("Cancer types: page codes, panel rationale, linked TCGA project and analysis cohort, histology strata, summary and gaps", "list"),
    "evidence.json": ("Published archetype studies used as the panel's selection history", "list"),
    "cohorts.json": ("Studies and resources in every data layer, with linkage, access, open checks, reported counts and the spatial review details", "list"),
    "captures.json": ("Located spatial transcriptomics tissue sections with original H&E, expression and coordinates, one record per section", "list"),
    "tcga_counts.json": ("TCGA molecular screen: patients with RNA-seq and 450k methylation per project, before and after assay-quality exclusions, with normal tissue", "projects"),
    "tcga_eligibility.json": ("TCGA selected analysis panel: counts per project after assay QC, after the patient screen and selected, and the 18 analysis cohorts", "cohorts"),
    "tcga_patients.json": ("Per-patient RNA-seq and 450k states (retained, excluded, unresolved, absent) for tumour and normal tissue", "rows"),
    "tcga_patient_review.json": ("Per-patient treatment and diagnosis screen, analysis cohort, study role and published annotations, as reason codes", "rows"),
    "tcga_flags.json": ("Every excluded or unresolved TCGA aliquot with its reason and the layers still retained", "rows"),
    "tcga_reviews.json": ("Histology review of TCGA-ESCA and TCGA-PAAD cases, cohort definitions and the patient scope review", "histology"),
    "tcga_resources.json": ("Links to current GDC data, PanCanAtlas files, histology sources and reference publications", "list"),
    "leads.json": ("Related leads that add no resources or patients: unassigned releases, precursor studies and reuse records", "list"),
}

KEY_POINTS = [
    "The selected analysis panel is one selection for one study design. General availability per TCGA project is reported separately and is larger; do not mix the two.",
    "Spatial studies come from patients other than those in TCGA. They add tissue context, not measurements for TCGA patients.",
    "\"Matched data located\" means the image and molecular files were found; image registration and tissue QC may still be pending.",
    "Counts reported by a study keep that study's own unit (sections, slides, samples, donors) and are never added across studies. An unknown count is absent, not zero.",
    "Normal tissue comes from patients with cancer, not healthy donors.",
    "There is no treated TCGA reference set: treatment-flagged patients were withheld, not collected as a treated group.",
    "The pooled glioma cohort (TCGA-LGG and TCGA-GBM) is a classification benchmark; integrated WHO CNS5 diagnoses are not adjudicated.",
    "Data remain at their original repositories. Listing a dataset does not mean access has been granted or requested.",
]


CONCEPTS = [  # terms agents most often need, in the site's own definitions (see methods.html)
    ("selected analysis panel", "A selection of TCGA primary-tumour patients for studies of tumour heterogeneity: assay-quality exclusions, a patient treatment and diagnosis screen, histology-defined and pooled cohorts, and a minimum cohort size of 150 patients with RNA-seq or 450k and 100 with both."),
    ("broader availability", "What each TCGA project provides after assay-quality exclusions only, before the patient screen and histology selection. It is larger than the selected panel and must not be mixed with it."),
    ("analysis cohort", "The unit of the selected panel: usually one TCGA project; CRC pools TCGA-COAD and TCGA-READ, GLIOMA pools TCGA-LGG and TCGA-GBM, and ESCC, PDAC and CSCC are histology-defined cohorts within TCGA-ESCA, TCGA-PAAD and TCGA-CESC. Each patient belongs to one cohort."),
    ("classification benchmark", "The pooled glioma cohort (TCGA-LGG and TCGA-GBM), used to test whether a molecular target recovers historical or integrated WHO CNS5 diagnoses. Integrated diagnoses are not adjudicated."),
    ("patient screen", "A review of treatment, diagnosis, identity and recurrence annotations for every retained TCGA patient. It withholds patients by exclusion or reversible hold and never changes assay states. Withheld patients do not form a treated reference set."),
    ("TCGA patient counts", "Unique patients with a retained primary-tumour assay: the union of RNA-seq and 450k, the intersection (both, or paired) and the single-assay remainders. Patients with both assays also appear in each single-assay column."),
    ("normal reference", "TCGA patients with same-sample normal RNA-seq and an H&E image (and, where counted, normal 450k). Normal tissue comes from patients with cancer, not healthy donors."),
    ("spatial resource", "A published spatial omics study or vendor example with matched H&E. Spatial studies come from patients other than those in TCGA."),
    ("matched data located", "The original H&E image, measured expression and spot or cell coordinates were found for a resource. Image registration and tissue QC may still be pending."),
    ("tissue section", "One assayed section or capture area with its own expression matrix, coordinates and H&E image (a capture). Repeated or serial sections add sections, not patients."),
    ("strict subset", "Located tissue sections in the core tier (primary tumour within a defined histology stratum) documented as untreated before sampling."),
    ("reported counts", "Counts in a study's own units (sections, slides, samples, donor labels) for resources not verified at section level. They are not patient counts unless stated, are never added across studies, and an unknown count is absent, not zero."),
    ("size threshold", "The minimum cohort size of the selected panel: at least 150 patients with a primary-tumour RNA-seq or 450k methylation profile and at least 100 with both, counted after assay-quality exclusions and before the patient screen. It applies to analysis cohorts, not TCGA projects; ESCC (90 patients) and PDAC (149) are explicit exceptions, and TCGA-SARC is not in the panel because each of its sarcoma types is below the threshold."),
    ("pooled page", "A cancer page combining others (CRC from COAD and READ, GLIOMA from LGG and GBM). It reuses the resources of its constituent cancers, so its counts must not be added to theirs."),
]


# ---------------------------------------------------------------- helpers

def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def js_labels():
    """Display labels from assets/js/common.js (every block of plain string labels), so the text versions use the site's wording."""
    src = (ROOT / "assets/js/common.js").read_text(encoding="utf-8")
    body = src[src.index("export const LABELS = {"):]
    body = body[:body.index("\n};")]
    out = {}
    for m in re.finditer(r"\n  (\w+): \{([^{}]*)\},?", body):
        pairs = re.findall(r'(?:"([^"]+)"|([A-Za-z_][\w-]*))\s*:\s*"((?:[^"\\]|\\.)*)"', m.group(2))
        if pairs:
            out[m.group(1)] = {(a or b): v.replace('\\"', '"') for a, b, v in pairs}
    return out


def fmt(n):
    return "—" if n is None else f"{n:,}"


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def plural(n, one, many):
    return f"{fmt(n)} {one if n == 1 else many}"


def cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(" --- " for _ in head) + "|"]
    out += ["| " + " | ".join(cell(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def link(path, frm=""):
    """A link from a file at `frm` (relative to the site root) to `path`."""
    if SITE_URL:
        return SITE_URL + path
    return "../" * frm.count("/") + path


def views(x):
    if "rna" in x:
        return x["rna"], x["met"], x["paired"], x["total"]
    return x["paired"] + x["rna_only"], x["paired"] + x["met_only"], x["paired"], x["union"]


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


# ---------------------------------------------------------------- site model

class Site:
    def __init__(self):
        self.release = load("release.json")
        self.cancers = load("cancers.json")
        self.evidence = load("evidence.json")
        self.cohorts = load("cohorts.json")
        self.captures = load("captures.json")
        self.counts = load("tcga_counts.json")
        self.elig = load("tcga_eligibility.json")
        self.L = js_labels()
        self.by_code = {c["code"]: c for c in self.cancers}
        self.pages = [c for c in self.cancers if c["group"] not in ("aggregate", "excluded")]
        self.excluded = [c for c in self.cancers if c["group"] == "excluded"]
        self.spatial = [c for c in self.cohorts if c["layer"] == "matched-spatial"]
        self.leads = load("leads.json")

    def codes(self, page):
        return [page["code"], *page.get("includes", [])]

    def spatial_for(self, page):
        codes = self.codes(page)
        return [x for x in self.spatial if any(k in codes for k in x["cancers"])]

    def others_for(self, page):
        codes = self.codes(page)
        return [x for x in self.cohorts if x["layer"] != "matched-spatial" and any(k in codes for k in x["cancers"])]

    def captures_for(self, page):
        codes = self.codes(page)
        return [x for x in self.captures if x["cancer"] in codes]

    @staticmethod
    def patients(caps):
        return len({(c["cohort"], c.get("patient") or c["capture"]) for c in caps})

    def projects_of(self, page):
        return page.get("tcga_projects") or ([page["tcga_project"]] if page.get("tcga_project") else [])

    def panel_status(self, p):
        """As panelStatus in assets/js/common.js."""
        x, e = self.counts["projects"][p], self.elig["projects"].get(p)
        if p in self.counts["meta"].get("excluded_projects", {}):
            return self.L["projectExclusion"].get(p, "No: outside the study")
        if not x.get("in_panel") or not e:
            return "No: below the size threshold"
        cid, c = e["analysis_cohort"], self.elig["cohorts"][e["analysis_cohort"]]
        if len(c["projects"]) > 1:
            others = " and ".join(f"TCGA-{q}" for q in c["projects"] if q != p)
            return f"Yes: pooled with {others} as {self.L['pooledName'].get(cid, cid)} ({cid})"
        if cid != p:
            return f"Yes: {self.L['cohortScope'].get(cid, cid)} ({cid})"
        return "Yes"

    def cohort_scope(self, cid):
        return f"{self.L['cohortScope'][cid]} ({cid})" if cid in self.L["cohortScope"] else ""

    def reported_for(self, c, codes):
        """A count reported by the source: one scoped to this page, or the study total when the study spans several of the page's cancers."""
        rep = c.get("reported") or []
        spans = sum(k in codes for k in c["cancers"]) > 1
        r = (None if spans else next((x for x in rep if len(x) > 3 and x[3] in codes), None)) or next((x for x in rep if len(x) < 4 or not x[3]), None)
        if not r:
            return ""
        return f"{fmt(r[0])} {r[1]}" + (" (all cancer sites)" if (len(r) < 4 or not r[3]) and any(k not in codes for k in c["cancers"]) else "")

    def notes_for(self, c, codes):
        out, comps = [], c.get("compartments") or []
        caps = [x for x in self.captures if x["cohort"] == c["id"] and x["cancer"] in codes]
        tc = (c.get("spatial_review") or {}).get("treatment_class")
        if tc in ("treated", "baseline-and-on-treatment") or any(x["treatment"] == "Post-treatment" for x in caps):
            out.append("includes treated tissue")
        if comps and all(x == "metastatic-tumour" for x in comps):
            out.append("metastases only")
        elif "metastatic-tumour" in comps or any(x["site"] == "Metastasis" for x in caps):
            out.append("includes metastases")
        if any(x in ("solid-normal", "normal", "peritumoral") for x in comps):
            out.append("includes normal or adjacent tissue")
        if "precursor" in comps:
            out.append("includes precursor lesions")
        if c.get("linkage") == "serial-section":
            out.append("H&E from serial sections")
        return out

    def rationale(self, c):
        if c["group"] == "hausser":
            return self.L["hausser"][c["hausser"]]
        if c.get("rationale"):
            return c["rationale"]
        if c["group"] == "tcga-panel":
            h = self.L["hausser"][c["hausser"]]
            return f"Molecular screen; {h[0].lower()}{h[1:]}"
        if c["group"] == "pooled":
            return f"Pooled analysis cohort ({' + '.join(c.get('includes', []))})"
        return "Separate published archetype study"

    def finding(self, page, e):
        if page.get("evidence_notes", {}).get(e["id"]):
            return page["evidence_notes"][e["id"]]
        if e["id"] != "hausser-2019":
            return e["finding"]
        name = page["name"]
        if page["hausser"] == "significant":
            return (f"{name} was one of six cancer types with significant within-type structure under the authors' strong criterion, "
                    f"and was included in the pooled six-cancer analysis. {'. '.join(e['finding'].split('. ')[2:])}")
        if page["hausser"] == "borderline":
            return f"{name} was described as borderline under the authors' significance criterion and was not part of the pooled analysis."
        return (f"{name} was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. "
                "This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.")

    def tcga_summary(self, page):
        """Short text used in indexes: the page's patients in the selected panel."""
        E, EC = self.elig["projects"], self.elig["cohorts"]
        if page.get("tcga_projects"):
            return f"{fmt(EC[page['code']]['selected_analysis']['total'])} TCGA patients in the selected panel (pooled {' + '.join('TCGA-' + p for p in page['tcga_projects'])})"
        e = E.get(page.get("tcga_project")) if page.get("tcga_project") else None
        if not e:
            return "No TCGA cohort"
        if e.get("excluded_from_study"):
            return "TCGA project excluded from the selected panel"
        if len(EC[e["analysis_cohort"]]["projects"]) > 1:
            return f"{fmt(e['selected_analysis']['total'])} TCGA patients in the selected panel, within pooled {e['analysis_cohort']}"
        return f"{fmt(e['selected_analysis']['total'])} TCGA patients in the selected panel" + (f", {self.cohort_scope(e['analysis_cohort'])}" if self.cohort_scope(e["analysis_cohort"]) else "")

    def spatial_summary(self, page):
        lst = self.spatial_for(page)
        if not lst:
            return "no spatial resources catalogued yet"
        n = sum(x["status"] == "verified" for x in lst)
        return f"{plural(len(lst), 'spatial resource', 'spatial resources')}, " + (f"{fmt(n)} with matched data located" if n else "verification pending")


# ---------------------------------------------------------------- per-cancer JSON and Markdown

# Located sections in the per-cancer files keep the fields needed to select data; links, source wording
# and clinical fields stay in data/captures.json under the same id.
SECTION_FIELDS = ("id", "cohort", "cancer", "stratum", "patient", "capture", "tier", "site", "treatment", "technique",
                  "preservation", "linkage", "registration", "he_mpp", "access", "verification")


def cancer_json(S, page):
    E, EC, C = S.elig["projects"], S.elig["cohorts"], S.counts["projects"]
    projects = S.projects_of(page)
    cid = page["code"] if page.get("tcga_projects") else page.get("analysis_cohort")
    return {
        "release": S.release,
        "code": page["code"],
        "page": f"cancers.html?c={page['code']}",
        "markdown": f"md/cancers/{page['code']}.md",
        "notes": KEY_POINTS[:5] + ["located_sections lists selection fields only; the full record with links, source wording and clinical fields is in data/captures.json under the same id."],
        "cancer": page,
        "tcga": {
            "panel_date": S.elig["meta"]["date"],
            "availability_date": S.counts["meta"]["date"],
            "analysis_cohort": {"id": cid, **EC[cid]} if cid and cid in EC else None,
            "projects": {p: {"selected_panel": E.get(p), "availability": {k: C[p][k] for k in ("pre_qc", "post_qc", "normal", "passes_screen", "in_panel", "group") if k in C[p]}} for p in projects},
        },
        "spatial_resources": S.spatial_for(page),
        "located_sections": [{k: x.get(k) for k in SECTION_FIELDS} for x in S.captures_for(page)],
        "other_resources": S.others_for(page),
        "evidence": [e for e in S.evidence if page["code"] in e["cancers"]],
    }


def cancer_md(S, page):
    code, frm = page["code"], f"md/cancers/{page['code']}.md"
    E, EC, C = S.elig["projects"], S.elig["cohorts"], S.counts["projects"]
    rel, codes = S.release, S.codes(page)
    excluded = page["group"] == "excluded"
    lines = [f"# {page['name']}", "",
             f"Code `{code}`. {S.rationale(page)}. Release {rel['version']}, {long_date(rel['date'])}. "
             f"Web page: [cancers.html?c={code}]({link(f'cancers.html?c={code}', frm)}). Data: [data/by-cancer/{code}.json]({link(f'data/by-cancer/{code}.json', frm)}).", "",
             page["summary"], ""]
    if excluded:
        lines += ["This cancer type is not in the selected analysis panel, and no patient is selected from it. Its TCGA data are listed below for provenance and can still be used for other questions.", ""]

    # TCGA
    lines += ["## TCGA reference", ""]
    projects = S.projects_of(page)
    head = ["", "Patients with RNA-seq", "Patients with methylation (450k)", "Patients with both", "Total patients"]
    e = E.get(page.get("tcga_project")) if page.get("tcga_project") else None
    if not projects:
        lines += ["No TCGA project is linked to this page.", ""]
    else:
        if e and e.get("excluded_from_study"):
            lines += [f"TCGA-{page['tcga_project']} is excluded from the selected analysis panel by decision, so no patient is selected. The table below shows the data available for it.", ""]
        else:
            if page.get("tcga_projects"):
                c = EC[code]
                rows = [[f"{code}, all contributing projects", *views(c["selected_analysis"])]] + [[f"submitted as TCGA-{p}", *views(c["contributions"][p])] for p in c["projects"]]
                cohort = c
            else:
                cohort = EC[e["analysis_cohort"]]
                rows = ([[f"Contribution of TCGA-{page['tcga_project']}", *views(e["selected_analysis"])], [f"Pooled {e['analysis_cohort']} cohort, all projects", *views(cohort["selected_analysis"])]]
                        if len(cohort["projects"]) > 1 else
                        [[e["analysis_cohort"] + (f": {cohort['label']}" if e["analysis_cohort"] != page["tcga_project"] else ""), *views(e["selected_analysis"])]])
            role = S.L["role"].get(cohort["role"], cohort["role"])
            lines += [f"Selected analysis panel ({role.lower()}). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection."
                      + (" Each patient counts once in the pooled cohort; project rows show where patients were submitted." if len(rows) > 1 else ""), "",
                      table(["Selected analysis panel", *head[1:]], [[r[0], *map(fmt, r[1:])] for r in rows]), ""]
            n = cohort["normal"]
            lines += [f"Normal reference of the cohort after screening: {plural(n['rna_he_after'], 'patient', 'patients')} with same-sample normal RNA-seq and H&E, "
                      f"{fmt(n['rna_he_met_after'])} of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.", ""]
        lines += [f"Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.", "",
                  table(["Broader availability", *head[1:]], [[f"TCGA-{p} project", *map(fmt, views(C[p]["post_qc"]))] for p in projects]), ""]

    # Spatial
    spatial = S.spatial_for(page)
    caps = S.captures_for(page)
    nloc = sum(x["status"] == "verified" for x in spatial)
    lines += ["## Spatial studies", ""]
    if not spatial:
        lines += ["No spatial resources are catalogued for this cancer type yet.", ""]
    else:
        head_s = f"{plural(len(spatial), 'spatial resource is', 'spatial resources are')} catalogued"
        sent = (f"{head_s}. Verification of the matched image and molecular data is pending." if not nloc else
                f"{head_s}, and matched image and molecular data have been located for {'it' if nloc == 1 else 'all of them'}." if nloc == len(spatial) else
                f"{head_s}; matched image and molecular data have been located for {fmt(nloc)}. Verification is pending for the others.")
        lines += [sent + " These studies usually involve patients other than those in TCGA.", ""]
        dependent = {"controlled", "request", "unreleased", "unresolved"}
        ranked = sorted(spatial, key=lambda c: 0 if c["status"] == "verified" else 2 if c["access"]["category"] in dependent else 1)
        rows = []
        for c in ranked:
            notes = S.notes_for(c, codes)
            pts = S.patients([x for x in S.captures if x["cohort"] == c["id"] and x["cancer"] in codes])
            located = ("Yes" + (f", for {plural(pts, 'patient', 'patients')}" if pts else "")) if c["status"] == "verified" else "Verification pending"
            rows.append([f"{c['label']} (`{c['id']}`)" + (f"; {'; '.join(notes)}" if notes else ""), ", ".join(c.get("techniques") or []) or "Not specified",
                         S.L["access"][c["access"]["category"]], S.reported_for(c, codes) or "No count reported", located])
        lines += [table(["Study", "Assay", "Access", "Reported by the study", "Matched data located"], rows), "",
                  "Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.", ""]
    if caps:
        lines += [f"Located tissue sections: {plural(len(caps), 'section', 'sections')} from {plural(S.patients(caps), 'patient', 'patients')}, "
                  f"each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.", ""]
        if page.get("includes"):
            groups = [(page.get("unstated_label") or "Not stated") if k == code else S.by_code[k]["name"] for k in [*page["includes"], code]]
            sels = [lambda x, k=k: x["cancer"] == k for k in [*page["includes"], code]]
            label = "Stated site"
        else:
            groups = [lab for _, lab in page["strata"]] + ["No stratum assigned"]
            sels = [lambda x, i=i: x["stratum"] == i for i, _ in page["strata"]] + [lambda x: not x["stratum"]]
            label = "Histology stratum"
        rows = []
        for g, sel in zip(groups, sels):
            in_g = [x for x in caps if sel(x)]
            if not in_g and g == "No stratum assigned":
                continue
            prim = [x for x in in_g if x["tier"] == "core"]
            rows.append([g, fmt(S.patients(prim)), fmt(len(prim)), fmt(len(in_g) - len(prim))])
        lines += [table([label, "Patients, primary tumour", "Sections, primary tumour", "Other sections"], rows), ""]

    # Selection history
    ev = [e for e in S.evidence if code in e["cancers"]]
    lines += ["## Selection history: published archetype evidence", ""]
    if not ev:
        lines += ["No archetype analysis specific to this cancer type is catalogued.", ""]
    for e in ev:
        lines += [f"### {e['short']}", "", f"- Scale: {e['scale']}", f"- Definition: {e['definition']}", f"- Finding: {S.finding(page, e)}",
                  f"- Limits: {e['limits']}", f"- Citation: {e['citation']} [doi:{e['doi']}]({e['url']})", ""]

    # Other resources
    others = S.others_for(page)
    lines += ["## Other resources", ""]
    if not others:
        lines += ["No other resources are catalogued yet.", ""]
    for layer, lab in S.L["layer"].items():
        in_l = [x for x in others if x["layer"] == layer]
        if layer == "matched-spatial" or not in_l:
            continue
        lines += [f"### {lab}", ""]
        for x in in_l:
            rep = S.reported_for(x, codes)
            extra = "; ".join(filter(None, [", ".join(x.get("techniques") or []), rep and f"reported by the source: {rep}"]))
            lines.append(f"- {x['label']} (`{x['id']}`): {S.L['status'][x['status']].lower()}; {S.L['access'][x['access']['category']].lower()}."
                         + (f" {x['description']}" if x.get("description") else "") + (f" {extra[0].upper()}{extra[1:]}." if extra else ""))
        lines.append("")

    lines += ["## Gaps and cautions", ""] + [f"- {g}" for g in page.get("gaps") or []] + [""]
    return "\n".join(lines)


def cancers_index_md(S):
    frm = "md/cancers/index.md"
    rows = [[f"[{p['name']}]({p['code']}.md)", p["code"], S.tcga_summary(p), S.spatial_summary(p)] for p in S.pages]
    ex = ", ".join(f"[{x['name']}]({x['code']}.md)" for x in S.excluded)
    return "\n".join([
        "# Cancer types", "",
        f"Release {S.release['version']}, {long_date(S.release['date'])}. Web page: [cancers.html]({link('cancers.html', frm)}).", "",
        "Each page brings together the TCGA data and the spatial studies for one cancer type, with its selection history, other resources and open checks. "
        "Colorectal cancer (CRC) and diffuse glioma (GLIOMA) also have pooled pages; the glioma cohort is a classification benchmark.", "",
        table(["Cancer type", "Code", "TCGA", "Spatial studies"], rows), "",
        "TCGA counts are patients in the selected analysis panel with RNA-seq, methylation or both. "
        "Spatial counts are resources, not patients; pooled pages reuse the resources of their constituent cancers, so the column should not be summed. "
        + (f"Excluded from the panel and not listed above: {ex}." if ex else ""), ""])


def tcga_md(S):
    frm = "md/tcga.md"
    m, ep, EC = S.elig["meta"], S.elig["panel"], S.elig["cohorts"]
    rule = S.counts["meta"]["rule"]
    G = {g: S.counts["groups"][g]["post_qc"] for g in ("CRC", "GLIOMA")}
    P = {p: S.counts["projects"][p]["post_qc"] for p in ("READ", "GBM", "SARC")}
    rows = []
    for cid, c in sorted(EC.items()):
        page = S.by_code.get(cid) or next((p for p in S.cancers if p.get("analysis_cohort") == cid and p.get("tcga_project")), None)
        name = page["name"] if page and page["code"] == cid else c["label"]
        sub = " + ".join(f"TCGA-{p}" for p in c["projects"])
        sa = c["selected_analysis"]
        rows.append([f"{name} ({cid}; {sub})", *map(fmt, (sa["rna"], sa["met"], sa["paired"], sa["total"], c["normal"]["rna_he_after"], c["normal"]["rna_he_met_after"]))])
    sa = ep["selected_analysis"]
    rows.append([f"All {m['analysis_cohorts']} cohorts ({m['projects']} TCGA projects)", *map(fmt, (sa["rna"], sa["met"], sa["paired"], sa["total"], ep["normal"]["rna_he_after"], ep["normal"]["rna_he_met_after"]))])
    order = sorted(S.counts["projects"].items(), key=lambda kv: (not kv[1].get("in_panel"), not S.elig["projects"].get(kv[0], {}).get("excluded_from_study"), kv[0]))
    prow = [[f"TCGA-{p}", *map(fmt, views(x["post_qc"])), fmt(x["normal"]["rna_he"]), S.panel_status(p)] for p, x in order]
    d = ep["dispositions"]
    withheld = ep["assay_qc"]["total"] - ep["after_patient_screen"]["total"]
    return "\n".join([
        "# TCGA reference", "",
        f"Release {S.release['version']}, {long_date(S.release['date'])}. Web page: [tcga.html]({link('tcga.html', frm)}). "
        f"Data: [tcga_eligibility.json]({link('data/tcga_eligibility.json', frm)}), [tcga_counts.json]({link('data/tcga_counts.json', frm)}), "
        f"[tcga_patient_review.json]({link('data/tcga_patient_review.json', frm)}), [tcga_patients.json]({link('data/tcga_patients.json', frm)}).", "",
        "The Cancer Genome Atlas (TCGA) holds tumour and normal tissue from thousands of patients across many cancer types, with slide images and molecular measurements released through the NCI Genomic Data Commons. "
        "TCGA is reported in two ways here. Data availability is what each project provides after assay-quality exclusions. "
        "The selected analysis panel is a selection for studies of tumour heterogeneity, which adds a patient treatment and diagnosis screen, histology-defined and pooled cohorts, and a minimum cohort size.", "",
        "## Size threshold", "",
        f"A cohort enters the panel only if it has enough patients for the planned RNA-seq and methylation analyses: at least {rule['min_total']} patients with a primary-tumour RNA-seq or 450k methylation profile, and at least {rule['min_paired']} of them with both. "
        "Patients are counted once, after assay-quality exclusions and before the treatment and diagnosis screen.", "",
        f"- It applies to the analysis cohort, not to the TCGA project. Colorectal cancer (CRC: {fmt(G['CRC']['union'])} patients, {fmt(G['CRC']['paired'])} with both) and diffuse glioma (GLIOMA: {fmt(G['GLIOMA']['union'])} and {fmt(G['GLIOMA']['paired'])}) are pooled cohorts; "
        f"TCGA-READ ({fmt(P['READ']['union'])} and {fmt(P['READ']['paired'])}) and TCGA-GBM ({fmt(P['GBM']['union'])} and {fmt(P['GBM']['paired'])}) would not pass on their own.",
        "- Where a project mixes distinct diseases, the cohort is the histology analysed: oesophageal squamous cell carcinoma (ESCC) from TCGA-ESCA, which also contains adenocarcinoma; cervical squamous cell carcinoma (CSCC) from TCGA-CESC, which also contains adenocarcinoma; and pancreatic ductal adenocarcinoma (PDAC) from TCGA-PAAD, which also contains a few adenosquamous, colloid and other carcinomas.",
        f"- Two cohorts are explicit exceptions: ESCC has {fmt(EC['ESCC']['selected_analysis']['total'])} patients, below both limits, and PDAC has {fmt(EC['PDAC']['selected_analysis']['total'])}, one patient below the total limit.",
        f"- Sarcoma is not in the panel. TCGA-SARC passes as a project ({fmt(P['SARC']['union'])} patients, {fmt(P['SARC']['paired'])} with both), but it combines several distinct sarcoma types, each below the threshold: the largest, soft-tissue leiomyosarcoma, has 53 patients, and all leiomyosarcomas together 87.", "",
        "## Selected analysis panel", "",
        f"{m['analysis_cohorts']} analysis cohorts from {m['projects']} TCGA projects: {m['discovery_cohorts']} discovery cohorts and {m['benchmark_cohorts']} glioma classification benchmark. "
        f"{fmt(sa['total'])} patients, {fmt(sa['paired'])} with both RNA-seq and 450k methylation.", "",
        table(["Cancer cohort", "Patients with RNA-seq", "Patients with methylation (450k)", "Patients with both", "Total patients", "Normal RNA-seq + H&E", "Normal with 450k"], rows), "",
        "Each patient belongs to one cohort, so the rows add up to the total. Patients with both assays also appear in the RNA-seq and methylation columns. "
        "Normal columns count the cohort's own donors with same-sample normal RNA-seq and H&E after screening.", "",
        "## Patient screen", "",
        f"Of {fmt(ep['assay_qc']['total'])} primary-tumour patients after assay QC in the panel projects, the treatment and diagnosis screen withholds {fmt(withheld)}: "
        f"{d['known_treatment_exclusion']} treatment exclusions, {d['treatment_unknown_hold']} treatment holds and {d['diagnosis_identity_or_episode_exclusion_hold']} diagnosis, identity, recurrence or specimen cases. "
        "Reasons can overlap; each patient is counted once under its main disposition. Not all withheld patients were treated, and they do not form a treated reference set. "
        f"Histology selection then keeps {fmt(sa['total'])} of the {fmt(ep['after_patient_screen']['total'])} patients who pass the screen. "
        "", "## Coverage by project", "",
        "Broader availability: primary-tumour patients in each project after exact assay-quality exclusions, not the selected panel. The last column shows how each project contributes to the panel, if at all.", "",
        table(["TCGA project", "Patients with RNA-seq", "Patients with methylation (450k)", "Patients with both", "Total patients", "Normal RNA-seq + H&E", "In the selected panel"], prow), "",
        f"Patient-level data: [tcga_patients.json]({link('data/tcga_patients.json', frm)}) gives the assay states of every patient; "
        f"[tcga_patient_review.json]({link('data/tcga_patient_review.json', frm)}) gives the screen decisions as reason codes, the analysis cohort and published annotations. "
        f"Field definitions are in [data/README.md]({link('data/README.md', frm)}).", ""])


def spatial_md(S):
    frm = "md/spatial.md"
    located = sum(c["status"] == "verified" for c in S.spatial)
    codes = {k for c in S.spatial for k in c["cancers"]}
    for p in S.pages:
        if p.get("includes") and p["code"] in codes and any(k in codes for k in p["includes"]):
            codes.discard(p["code"])
    represented = sum(p["code"] in codes for p in S.pages)
    rows = []
    for p in S.pages:
        lst = S.spatial_for(p)
        n = sum(x["status"] == "verified" for x in lst)
        md = link("md/cancers/" + p["code"] + ".md", frm)
        rows.append([f"[{p['name']}]({md})", p["code"], fmt(len(lst)) if lst else "None catalogued",
                     ("—" if not lst else fmt(n) if n else "Verification pending")])
    reviewed = [c for c in S.spatial if (c.get("spatial_review") or {}).get("route_review")]
    route_counts = {k: sum(k in c["spatial_review"]["route_review"]["states"] for c in reviewed) for k in S.L["routeState"]}
    res = [[c["label"], f"`{c['id']}`", ", ".join(c["cancers"]), S.L["status"][c["status"]], S.L["access"][c["access"]["category"]], ", ".join(c.get("techniques") or []) or "Not specified"]
           for c in sorted(S.spatial, key=lambda c: (c["status"] != "verified", c["label"].lower()))]
    return "\n".join([
        "# Spatial studies", "",
        f"Release {S.release['version']}, {long_date(S.release['date'])}. Web page: [spatial.html]({link('spatial.html', frm)}). "
        f"Data: [cohorts.json]({link('data/cohorts.json', frm)}) (resources with layer `matched-spatial`) and [captures.json]({link('data/captures.json', frm)}) (located tissue sections).", "",
        "Published spatial omics studies show where molecular programmes and cell states sit within a tumour and how they relate to its morphology. "
        "They usually come from patients other than those in TCGA, so they add tissue context to the reference but no measurements for TCGA patients.", "",
        f"{fmt(len(S.spatial))} catalogued spatial resources, {fmt(located)} with matched data located, {fmt(represented)} cancer types represented. "
        f"{plural(len(S.captures), 'tissue section', 'tissue sections')} with an original H&E image, measured spatial RNA and coordinates are located.", "",
        "## By cancer type", "",
        table(["Cancer type", "Code", "Catalogued resources", "With matched data located"], rows), "",
        "Catalogued resources are all listed spatial studies and vendor examples, including those not yet verified and those that need an access request. "
        "A resource counts as having matched data located once its image and molecular files have been found; image registration and tissue QC may still be pending. "
        "The pooled colorectal and glioma rows reuse the resources of their constituent cancers, and some studies cover several cancers, so the rows should not be summed.", "",
        "## Public-route review", "",
        f"The {len(reviewed)} reviewed resources were followed to a retrieved result, a registration or controlled-access boundary, a missing release or a reproducible download failure. "
        "The open dependencies below are kept apart: a download failure is a technical gap, not a permission requirement. "
        f"{fmt(sum(c['spatial_review']['route_review']['sections_with_matching_coordinates'] or 0 for c in reviewed))} section packages have expression barcodes that match their tissue coordinates exactly; "
        "this is not a patient count or final QC, and no eligible-patient total is established.", "",
        table(["Open dependency", "Resources"], [[S.L["routeState"][k], fmt(v)] for k, v in route_counts.items()]), "",
        table(["Resource", "ID", "Status", "Next step"], [[c["label"], f"`{c['id']}`", c["spatial_review"]["route_review"]["status"], c["spatial_review"]["route_review"]["next_step"]] for c in reviewed]), "",
        "## Related leads, not counted", "",
        "These releases add no resources or patients to the totals above.", ""]
        + [f"- [{x['label']}]({x['url']}): {x['description']} {x['not_counted']} Next: {x['next']}" for x in S.leads] + ["",
        "## All spatial resources", "",
        table(["Resource", "ID", "Cancer codes", "Status", "Access", "Assay"], res), ""])


def llms_txt(S):
    rel, ep = S.release, S.elig["panel"]["selected_analysis"]
    sp_loc = sum(c["status"] == "verified" for c in S.spatial)
    lines = [f"# {NAME}", "",
             f"> A curated catalogue of public tumour datasets that link histology with molecular measurements: TCGA patients with RNA-seq and DNA methylation (450k), "
             f"and published spatial omics studies with matched H&E images. Release {rel['version']}, {long_date(rel['date'])}.", "",
             f"The selected TCGA analysis panel has {fmt(ep['total'])} patients in {S.elig['meta']['analysis_cohorts']} analysis cohorts, {fmt(ep['paired'])} with both RNA-seq and 450k methylation. "
             f"{fmt(len(S.spatial))} spatial omics resources are catalogued, {fmt(sp_loc)} with matched image and molecular data located, and {len(S.pages)} cancer types have their own page. "
             "The web pages draw their tables with JavaScript; the Markdown and JSON files below hold the same content as text.", "",
             "Read these points before using any count:", ""] + [f"- {k}" for k in KEY_POINTS] + [""]
    if LICENCE:
        lines += [f"Licence: the curated metadata and these text files are [{LICENCE[0]}]({LICENCE[1]}); the code is GPL-3.0. "
                  f"The underlying datasets keep their own terms: cite the original publications and repositories for each dataset. "
                  f"Maintainer: Matthieu Foll (IARC); questions and corrections through [GitHub issues]({REPO}/issues).", ""]
    else:
        lines += ["Cite the original publications and repositories for each dataset (see Sources).", ""]
    lines += ["## Pages as Markdown", "",
              f"- [TCGA reference]({link('md/tcga.md')}): the selected analysis panel by cohort, the patient screen and coverage by TCGA project",
              f"- [Spatial studies]({link('md/spatial.md')}): spatial resources by cancer type, with status, access and assay for each",
              f"- [Cancer types]({link('md/cancers/index.md')}): one page per cancer type with its TCGA data, spatial studies, selection history and gaps",
              f"- [Curation and methods]({link('methods.html')}): definitions of count units, linkage levels, exclusions, pooling and limitations (static HTML)",
              f"- [Research applications]({link('applications.html')}): study designs the data can support, with their limits (static HTML)", "",
              "## Agent interfaces", "",
              f"- [MCP server]({link('agents.html#mcp')}): a read-only Model Context Protocol server with {len(MCP_TOOLS)} tools "
              f"({', '.join(f'`{n}`' for n, _ in MCP_TOOLS)}). It runs on the user's computer: "
              f"`uvx --from \"git+{REPO}#subdirectory=mcp\" histology-multiomics-explorer-mcp` reads the published site, and `uv run --directory mcp histology-multiomics-explorer-mcp` reads a copy of the repository. Setup for Claude Code and Claude Desktop is on the linked page.",
              f"- [AGENTS.md]({REPO}/blob/main/AGENTS.md): instructions for coding agents working on the [repository]({REPO})", "",
              "## Data", "",
              f"- [Data index]({link('data/index.json')}): every data file with its description, record count, size, SHA-256 checksum and JSON Schema",
              f"- [Field reference]({link('data/README.md')}): meaning of every field and controlled vocabulary",
              f"- [Per-cancer JSON]({link('data/by-cancer/BRCA.json')}): one file per cancer page, `data/by-cancer/<CODE>.json`, with the cancer record, TCGA counts, spatial resources, located sections, other resources and evidence"]
    lines.append(f"- [Glossary]({link('data/glossary.json')}): {FILE_DOCS['glossary']}")
    for name, (desc, _) in SOURCE_FILES.items():
        lines.append(f"- [{name}]({link('data/' + name)}): {desc}")
    lines += ["", "## Cancer pages", ""]
    for p in S.pages + S.excluded:
        md = link("md/cancers/" + p["code"] + ".md")
        lines.append(f"- [{p['name']}]({md}) (`{p['code']}`): {S.tcga_summary(p)}; {S.spatial_summary(p)}")
    lines += ["", "## Optional", "",
              f"- [Sources]({link('sources.html')}): citations and access routes for every dataset",
              f"- [Data explorer]({link('explore.html')}): interactive filters and CSV or JSON export (needs JavaScript)", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- JSON Schemas

ENUM_AT = {  # (file, path) -> vocabulary; [] marks list items, {} map values
    ("cancers", "[].group"): "group", ("cancers", "[].hausser"): "hausser",
    ("cohorts", "[].layer"): "layer", ("cohorts", "[].status"): "status", ("cohorts", "[].compartments[]"): "compartment",
    ("cohorts", "[].specimen"): "specimen", ("cohorts", "[].linkage"): "linkage", ("cohorts", "[].gates[]"): "gate",
    ("cohorts", "[].access.category"): "access", ("cohorts", "[].verification"): "verification",
    ("cohorts", "[].spatial_review.assay_classes[]"): "assay_class", ("cohorts", "[].spatial_review.treatment_class"): "treatment_class",
    ("captures", "[].tier"): "tier", ("captures", "[].site"): "site", ("captures", "[].treatment"): "treatment",
    ("captures", "[].linkage"): "linkage", ("captures", "[].verification"): "verification",
    ("captures", "[].access.he"): "access", ("captures", "[].access.processed"): "access", ("captures", "[].access.raw"): "access",
}
MAPS = {  # objects keyed by identifiers rather than fixed field names
    ("glossary", "vocabularies"), ("glossary", "vocabularies{}"),
    ("tcga_counts", "groups"), ("tcga_counts", "projects"), ("tcga_eligibility", "projects"), ("tcga_eligibility", "cohorts"),
    ("tcga_eligibility", "cohorts{}.contributions"), ("tcga_eligibility", "cohorts{}.annotations"), ("tcga_eligibility", "cohorts{}.annotations{}"),
    ("tcga_eligibility", "cohorts{}.reported_sites"),
    ("cancers", "[].evidence_notes"), ("by-cancer", "tcga.projects"), ("by-cancer", "cancer.evidence_notes"),
    ("by-cancer", "tcga.analysis_cohort.contributions"), ("by-cancer", "tcga.analysis_cohort.annotations"),
    ("by-cancer", "tcga.analysis_cohort.annotations{}"), ("by-cancer", "tcga.analysis_cohort.reported_sites"),
}
DEPTH = {"tcga_counts": 4, "tcga_eligibility": 4, "tcga_reviews": 3, "by-cancer": 6}
DOCS = {
    ("cancers", "[].code"): "Short code, following TCGA where one exists; CRC and GLIOMA are pooled pages",
    ("cancers", "[].group"): "Why the cancer type is in the explorer; excluded types are kept for provenance only",
    ("cancers", "[].tcga_project"): "TCGA project linked to this page, or null; pooled pages list tcga_projects",
    ("cancers", "[].analysis_cohort"): "TCGA analysis cohort the page's patients belong to; null for an excluded project",
    ("cancers", "[].strata"): "[id, label] pairs for the histology strata used by located sections",
    ("cohorts", "[].layer"): "Data layer: matched H&E and spatial RNA, whole-slide images with bulk data, bulk RNA, single-cell or image only",
    ("cohorts", "[].status"): "verified means matched packages were located; candidate means not yet verified",
    ("cohorts", "[].reported"): "[value, unit, basis] or [value, unit, basis, cancer] in the source's own units; never added across studies",
    ("cohorts", "[].gates"): "Open checks: what prevents inclusion, or the curation still to do",
    ("cohorts", "[].linkage"): "Level of H&E to RNA linkage",
    ("captures", "[].id"): "<cohort>:<capture>",
    ("captures", "[].tier"): "core: primary tumour within the histology stratum; other tiers are metastatic, under review, outside the stratum or held for QC",
    ("captures", "[].treatment"): "Treatment before sampling",
    ("captures", "[].he_mpp"): "Image resolution in micrometres per pixel, where established",
}
FILE_DOCS = {**{Path(k).stem: v[0] for k, v in SOURCE_FILES.items()},
             "by-cancer": "One cancer page: the cancer record, its TCGA panel and availability counts, spatial resources, located sections, other resources and evidence",
             "index": "Index of the explorer's data files with checksums and schemas",
             "glossary": "Definitions of the terms used for counts and curation, and every display vocabulary of the site"}
TABLES = {"tcga_patients": "rows", "tcga_patient_review": "rows", "tcga_flags": "rows"}


def jtype(v):
    return ("null" if v is None else "boolean" if isinstance(v, bool) else "integer" if isinstance(v, int) else "number" if isinstance(v, float)
            else "string" if isinstance(v, str) else "array" if isinstance(v, list) else "object")


def infer(samples, file, path, depth=0):
    types = {jtype(v) for v in samples}
    if {"integer", "number"} <= types:
        types.discard("integer")
    s = {"type": sorted(types)[0] if len(types) == 1 else sorted(types)}
    if (file, path) in DOCS:
        s["description"] = DOCS[(file, path)]
    if (file, path) in ENUM_AT:
        s["enum"] = sorted(ENUMS[ENUM_AT[(file, path)]]) + ([None] if "null" in types else [])
    objs = [v for v in samples if isinstance(v, dict)]
    arrs = [v for v in samples if isinstance(v, list)]
    if objs and depth < DEPTH.get(file, 8):
        if (file, path) in MAPS:
            vals = [x for o in objs for x in o.values()]
            if vals:
                s["additionalProperties"] = infer(vals, file, path + "{}", depth + 1)
        else:
            keys = list(dict.fromkeys(k for o in objs for k in o))
            s["properties"] = {k: infer([o[k] for o in objs if k in o], file, f"{path}.{k}".lstrip("."), depth + 1) for k in keys}
            s["required"] = [k for k in keys if all(k in o for o in objs)]
            s["additionalProperties"] = False
    if arrs and depth < DEPTH.get(file, 8):
        items = [x for a in arrs for x in a]
        if items:
            s["items"] = infer(items, file, path + "[]", depth + 1)
    return s


def schema_for(file, data, samples=None):
    if file in TABLES:
        cols = data["columns"]
        rows = data["rows"]
        s = infer([{k: v for k, v in data.items() if k != "rows"}], file, "")
        row = {"type": "array", "minItems": len(cols), "maxItems": len(cols), "items": False,
               "prefixItems": [{"title": c, **{k: v for k, v in infer([r[i] for r in rows], file, f"rows[].{c}").items()}} for i, c in enumerate(cols)]}
        if file in ("tcga_patients",):
            for item in row["prefixItems"]:
                if item["title"] in ("tumour_rna", "tumour_met", "normal_rna", "normal_met"):
                    item["enum"] = sorted(ENUMS["tcga_state"])
        s["properties"]["columns"] = {"const": cols, "description": "Column names of each row"}
        s["properties"]["rows"] = {"type": "array", "items": row, "description": "One row per record, in the column order above"}
        s["required"] = list(data)
    else:
        s = infer(samples or [data], file, "")
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"schemas/{file}.schema.json",
            "title": file, "description": FILE_DOCS.get(file, ""), **s}


def validate(inst, s, path="$"):
    """Errors from validating `inst` against the subset of JSON Schema used in schemas/."""
    if s is False:
        return [f"{path}: not allowed"]
    errs = []
    t = s.get("type")
    if t is not None:
        ok = jtype(inst) in (t if isinstance(t, list) else [t]) or (jtype(inst) == "integer" and "number" in (t if isinstance(t, list) else [t]))
        if not ok:
            return [f"{path}: expected {t}, found {jtype(inst)}"]
    if "const" in s and inst != s["const"]:
        errs.append(f"{path}: differs from the expected constant")
    if "enum" in s and inst not in s["enum"]:
        errs.append(f"{path}: {inst!r} is not in the vocabulary")
    if isinstance(inst, dict):
        for k in s.get("required", []):
            if k not in inst:
                errs.append(f"{path}: missing {k}")
        props = s.get("properties", {})
        for k, v in inst.items():
            if k in props:
                errs += validate(v, props[k], f"{path}.{k}")
            elif s.get("additionalProperties") is False and "properties" in s:
                errs.append(f"{path}: unexpected field {k}")
            elif isinstance(s.get("additionalProperties"), dict):
                errs += validate(v, s["additionalProperties"], f"{path}.{k}")
    if isinstance(inst, list):
        pre = s.get("prefixItems", [])
        if "minItems" in s and len(inst) < s["minItems"] or "maxItems" in s and len(inst) > s["maxItems"]:
            errs.append(f"{path}: wrong length {len(inst)}")
        for i, v in enumerate(inst):
            if i < len(pre):
                errs += validate(v, pre[i], f"{path}[{i}]")
            elif "items" in s:
                errs += validate(v, s["items"], f"{path}[{i}]")
    return errs[:20]


# ---------------------------------------------------------------- index.html Dataset block

JSONLD_START, JSONLD_END = "<!-- agent:dataset-jsonld -->", "<!-- /agent:dataset-jsonld -->"


def dataset_jsonld(S):
    rel = S.release
    d = {"@context": "https://schema.org", "@type": "Dataset", "name": NAME,
         "description": ("Curated public metadata linking tumour histology with molecular measurements: TCGA patients with RNA-seq and 450k DNA methylation, "
                         "assay and patient exclusions and an analysis panel of 18 cohorts, and published spatial omics studies with matched H&E images, "
                         "with their linkage, access route and verification status. The underlying data remain at their original repositories."),
         "version": rel["version"], "dateModified": rel["date"],
         "keywords": ["TCGA", "histology", "H&E", "spatial transcriptomics", "RNA-seq", "DNA methylation", "tumour heterogeneity", "cancer"],
         "isAccessibleForFree": True,
         "distribution": [{"@type": "DataDownload", "name": "Data index", "encodingFormat": "application/json", "contentUrl": link("data/index.json")},
                          {"@type": "DataDownload", "name": "Agent guide", "encodingFormat": "text/markdown", "contentUrl": link("llms.txt")}]}
    if SITE_URL:
        d["url"] = SITE_URL
        d["codeRepository"] = REPO
    if LICENCE:
        d["license"] = LICENCE[1]
    d["creator"] = {"@type": "Person", "name": "Matthieu Foll", "affiliation": {"@type": "Organization", "name": "International Agency for Research on Cancer"}}
    return d


def index_html(S, current):
    block = (f'{JSONLD_START}\n<script type="application/ld+json">\n{json.dumps(dataset_jsonld(S), ensure_ascii=False, indent=1)}\n</script>\n{JSONLD_END}')
    if JSONLD_START in current:
        return re.sub(re.escape(JSONLD_START) + r".*?" + re.escape(JSONLD_END), lambda _: block, current, flags=re.S)
    return current.replace("</head>", block + "\n</head>", 1)


# ---------------------------------------------------------------- build

def build():
    """Return {relative path: text} for every generated file."""
    S = Site()
    out = {"llms.txt": llms_txt(S), "md/tcga.md": tcga_md(S), "md/spatial.md": spatial_md(S), "md/cancers/index.md": cancers_index_md(S)}
    by_cancer = {}
    for p in S.pages + S.excluded:
        out[f"md/cancers/{p['code']}.md"] = cancer_md(S, p)
        by_cancer[p["code"]] = cancer_json(S, p)
        out[f"data/by-cancer/{p['code']}.json"] = dump(by_cancer[p["code"]])
    sources = {Path(n).stem: load(n) for n in SOURCE_FILES}
    for stem, data in sources.items():
        out[f"schemas/{stem}.schema.json"] = dump(schema_for(stem, data))
    out["schemas/by-cancer.schema.json"] = dump(schema_for("by-cancer", None, list(by_cancer.values())))

    files = []
    for name, (desc, unit) in SOURCE_FILES.items():
        raw = (DATA / name).read_bytes()
        data = sources[Path(name).stem]
        records = (len(data) if unit == "list" else len(data["rows"]) if unit == "rows" else len(data[unit]) if unit else None)
        files.append({"path": f"data/{name}", "description": desc, "records": records, "bytes": len(raw),
                      "sha256": hashlib.sha256(raw).hexdigest(), "schema": f"schemas/{Path(name).stem}.schema.json"})
    for code in by_cancer:
        raw = out[f"data/by-cancer/{code}.json"].encode()
        files.append({"path": f"data/by-cancer/{code}.json", "description": f"Cancer page {code}: {S.by_code[code]['name']}", "records": None,
                      "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "schema": "schemas/by-cancer.schema.json"})
    index = {"name": NAME, "release": S.release, "description": FILE_DOCS["index"], "agent_guide": "llms.txt", "field_reference": "data/README.md",
             "notes": KEY_POINTS, "files": files}
    glossary = {"release": S.release, "concepts": [{"term": t, "definition": d} for t, d in CONCEPTS], "vocabularies": S.L}
    out["data/glossary.json"] = dump(glossary)
    raw = out["data/glossary.json"].encode()
    files.append({"path": "data/glossary.json", "description": FILE_DOCS["glossary"], "records": len(CONCEPTS),
                  "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "schema": "schemas/glossary.schema.json"})
    out["schemas/glossary.schema.json"] = dump(schema_for("glossary", glossary))
    out["data/index.json"] = dump(index)
    out["schemas/index.schema.json"] = dump(schema_for("index", index))
    out["index.html"] = index_html(S, (ROOT / "index.html").read_text(encoding="utf-8"))
    return out


def stale(out=None):
    """Generated files that are missing or differ from a fresh build, and leftover generated files."""
    out = out or build()
    bad = [p for p, text in out.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding="utf-8") != text]
    for d in ("md", "data/by-cancer", "schemas"):
        for f in (ROOT / d).rglob("*") if (ROOT / d).exists() else []:
            if f.is_file() and str(f.relative_to(ROOT)) not in out:
                bad.append(f"{f.relative_to(ROOT)} (no longer generated)")
    return bad


def schema_errors():
    """Validation errors of every data file against its committed schema."""
    errs = []
    for name in SOURCE_FILES:
        sp = ROOT / "schemas" / f"{Path(name).stem}.schema.json"
        if sp.exists():
            errs += [f"data/{name} {e}" for e in validate(load(name), json.loads(sp.read_text(encoding="utf-8")))]
    sp = ROOT / "schemas/by-cancer.schema.json"
    if sp.exists():
        s = json.loads(sp.read_text(encoding="utf-8"))
        for f in sorted((DATA / "by-cancer").glob("*.json")):
            errs += [f"{f.relative_to(ROOT)} {e}" for e in validate(json.loads(f.read_text(encoding="utf-8")), s)]
    return errs


def main():
    out = build()
    if "--check" in sys.argv:
        bad = stale(out)
        for b in bad:
            print(f"stale: {b}")
        sys.exit(1 if bad else 0)
    for d in ("md", "data/by-cancer", "schemas"):
        for f in (ROOT / d).rglob("*") if (ROOT / d).exists() else []:
            if f.is_file() and str(f.relative_to(ROOT)) not in out:
                f.unlink()
    for p, text in out.items():
        (ROOT / p).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / p).write_text(text, encoding="utf-8")
    errs = schema_errors()
    for e in errs:
        print(e)
    print(f"Wrote {len(out)} files; schema errors: {len(errs)}")


if __name__ == "__main__":
    main()
