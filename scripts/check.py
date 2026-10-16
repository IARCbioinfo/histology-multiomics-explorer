#!/usr/bin/env python3
"""Validate the catalogue metadata and print summary counts.

Usage: python3 scripts/check.py
Exits with status 1 if any error is found. Standard library only.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

from vocab import ENUMS  # noqa: E402  (scripts/ is on the path when run as a script)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
errors = []


def err(msg):
    errors.append(msg)


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def check_url(where, url):
    if url is not None and not re.match(r"^https?://\S+$", url):
        err(f"{where}: malformed URL {url!r}")


release = load("release.json")
cancers = load("cancers.json")
evidence = load("evidence.json")
cohorts = load("cohorts.json")
captures = load("captures.json")
tcga = load("tcga_counts.json")
tcga_patients = load("tcga_patients.json")
tcga_flags = load("tcga_flags.json")
tcga_resources = load("tcga_resources.json")
reviews = load("tcga_reviews.json")
patient_review = load("tcga_patient_review.json")
eligibility = load("tcga_eligibility.json")

if not DATE.match(release.get("date", "")):
    err("release.json: date must be YYYY-MM-DD")

codes = {c["code"] for c in cancers}
for c in cancers:
    if c.get("group") not in ENUMS["group"]:
        err(f"cancer {c['code']}: invalid group {c.get('group')!r}")
    if c.get("hausser") not in ENUMS["hausser"]:
        err(f"cancer {c['code']}: invalid hausser {c.get('hausser')!r}")
    tp = c.get("tcga_project")
    if tp and tp not in tcga["projects"]:
        err(f"cancer {c['code']}: unknown TCGA project {tp}")
    for tp in c.get("tcga_projects", []):
        if tp not in tcga["projects"]:
            err(f"cancer {c['code']}: unknown TCGA project {tp}")
    if c.get("analysis_cohort") and c["analysis_cohort"] not in eligibility["cohorts"]:
        err(f"cancer {c['code']}: unknown analysis cohort {c['analysis_cohort']}")
strata = {s[0]: c["code"] for c in cancers for s in c["strata"]}

for e in evidence:
    for code in e["cancers"]:
        if code not in codes:
            err(f"evidence {e['id']}: unknown cancer {code}")

ids = Counter(c["id"] for c in cohorts)
for k, n in ids.items():
    if n > 1:
        err(f"cohorts: duplicate id {k}")
cohort_by_id = {c["id"]: c for c in cohorts}

for c in cohorts:
    w = f"cohort {c['id']}"
    for code in c["cancers"]:
        if code not in codes:
            err(f"{w}: unknown cancer {code}")
    for field, enum in (("layer", "layer"), ("status", "status"), ("verification", "verification"),
                        ("linkage", "linkage"), ("specimen", "specimen")):
        if c.get(field) not in ENUMS[enum]:
            err(f"{w}: invalid {field} {c.get(field)!r}")
    if c["access"]["category"] not in ENUMS["access"]:
        err(f"{w}: invalid access {c['access']['category']!r}")
    for g in c.get("gates", []):
        if g not in ENUMS["gate"]:
            err(f"{w}: invalid gate {g!r}")
    comps = c.get("compartments")
    if not comps or any(x not in ENUMS["compartment"] for x in comps):
        err(f"{w}: missing or invalid compartments {comps!r}")
    if c["status"] == "screened" and not c.get("tcga_project"):
        err(f"{w}: screened entries must name a TCGA project")
    if c["status"] == "candidate" and not c.get("gates"):
        err(f"{w}: candidate without an open check")
    if c.get("verified_on") and not DATE.match(c["verified_on"]):
        err(f"{w}: bad verified_on")
    if c["status"] != "listed" and not c.get("verified_on"):
        err(f"{w}: missing verified_on")
    for parent in c.get("derived_from", []):
        if parent not in cohort_by_id:
            err(f"{w}: derived_from unknown cohort {parent}")
    for label, url in c["access"].get("links", []):
        check_url(w, url)
    check_url(w, (c.get("citation") or {}).get("url"))
    for item in c.get("reported") or []:
        if not (isinstance(item[0], int) and item[0] >= 0 and item[1] and item[2]) or len(item) > 4 or (len(item) == 4 and item[3] not in c["cancers"]):
            err(f"{w}: reported counts need value, unit, basis and an optional cancer scope from the entry's cancers")

cap_ids = Counter(c["id"] for c in captures)
for k, n in cap_ids.items():
    if n > 1:
        err(f"captures: duplicate id {k}")

for c in captures:
    w = f"capture {c['id']}"
    co = cohort_by_id.get(c["cohort"])
    if not co:
        err(f"{w}: unknown cohort {c['cohort']}")
        continue
    if co["status"] not in ("verified", "preview"):
        err(f"{w}: section records must belong to a study at one of the two image levels")
    if c.get("image_level") not in ENUMS["image_level"] or (co["status"] == "preview" and c["image_level"] != "preview"):
        err(f"{w}: image level must be original or preview, and a preview-level study holds only preview sections")
    if c["cancer"] not in codes:
        err(f"{w}: unknown cancer {c['cancer']}")
    if c["stratum"] is not None and strata.get(c["stratum"]) != c["cancer"]:
        err(f"{w}: stratum {c['stratum']} does not belong to {c['cancer']}")
    for field in ("tier", "treatment", "site", "verification", "linkage"):
        if c[field] not in ENUMS[field]:
            err(f"{w}: invalid {field} {c[field]!r}")
    for k, v in c["access"].items():
        if v not in ENUMS["access"]:
            err(f"{w}: invalid access.{k} {v!r}")
    if c["tier"] == "core":
        if c["site"] != "Primary":
            err(f"{w}: core captures must be primary")
        if not c["stratum"]:
            err(f"{w}: core captures need a histology stratum")
    for k in ("he", "expression", "coordinates"):
        if not c["links"].get(k):
            err(f"{w}: missing {k} link")
        check_url(w, c["links"].get(k))
    for u in c["links"].get("raw", []):
        check_url(w, u)
    if not c.get("patient") and c["tier"] == "core":
        err(f"{w}: core capture without patient ID")
    if c.get("review_batch") == "backlog-2026-10-16":
        if c["tier"] not in ("review", "metastatic") or c["stratum"] or (c["tier"] == "metastatic") != (c["site"] == "Metastasis"):
            err(f"{w}: backlog sections stay outside the core and any histology stratum")
        if c.get("donor_mapping") not in ENUMS["donor_mapping"] or (c["patient"] is not None) != (c["donor_mapping"] != "unresolved"):
            err(f"{w}: a patient ID needs a source-backed donor mapping, and an unresolved mapping has none")
        if c["registration"] != "Not yet checked" or c["he_mpp"] is not None or not c["tier_reason"].startswith(
                "Original H&E located" if c["image_level"] == "original" else "Matched data with preview image"):
            err(f"{w}: registration and calibration stay unchecked, and the tier reason states the image level")
    elif c.get("image_level") != "original" or "donor_mapping" in c:
        err(f"{w}: section records before the backlog review are at the original level")
    if "ftp://" in json.dumps(c["links"]):
        err(f"{w}: links must use https")

# Section records imported before the backlog review keep their maintained values (image_level was added).
import hashlib  # noqa: E402
_base = [{k: v for k, v in c.items() if k != "image_level"} for c in captures if not c.get("review_batch")]
if len(_base) != 204 or hashlib.sha256(json.dumps(_base, sort_keys=True, ensure_ascii=False).encode()).hexdigest() != \
        "be1d9cc7e17a79699213b75938adf6fa2c756f2ac50fe54597f3d9b0b729e630":
    err("captures: the 204 section records from before the backlog review changed; update this pin only for a deliberate edit")
# A source section (GEO sample or capture ID) belongs to one study.
_owner = defaultdict(set)
for c in captures:
    for k in {c["capture"], c.get("accession")} - {None}:
        _owner[k].add(c["cohort"])
for k, v in _owner.items():
    if len(v) > 1:
        err(f"captures: section {k} is listed under several studies {sorted(v)}")

# Spatial resources reviewed on 15 October 2026 (candidates only)
SPATIAL_REVIEW = {
    "cscc-10x-ffpe": "CSCC", "cscc-hpv-gse208654": "CSCC", "cscc-ou-stereo": "CSCC", "escc-hra000776-omix009524": "ESCC",
    "escc-hra007162": "ESCC", "escc-precancer-geomx": "ESCC", "kirc-meylan-gse175540": "KIRC", "kirc-egad00001008781": "KIRC",
    "kirc-treated-gse294006": "KIRC", "kirc-10x-xenium-protein": "KIRC", "kirp-10x-xenium-preview": "KIRP", "kirp-macrophage-abstract": "KIRP",
    "lusc-10x-cytassist": "LUSC", "lusc-emtab13530": "LUSC", "pcpg-ling-ssrn": "PCPG", "pcpg-developmental-preprint": "PCPG",
    "prad-10x-acinar": "PRAD", "prad-10x-invasive": "PRAD", "prad-hirz-slideseq": "PRAD", "prad-erickson-clonal": "PRAD",
    "stad-gse251950": "STAD", "stad-gse270678": "STAD", "ucec-barkley-gse203612": "UCEC", "ucec-np137-gse225690": "UCEC",
    "glioma-greenwald-gse237183": "GLIOMA", "glioma-2026-niche-atlas": "GLIOMA"}
SPATIAL_EXISTING = {"lusc-emtab13530": "cand-dezuani-cvejic-2024", "glioma-greenwald-gse237183": "cand-greenwald2024",
                    "glioma-2026-niche-atlas": "cand-snu2026"}
SCOPE_CANCERS = {"CSCC": {"CESC"}, "ESCC": {"ESCA"}, "GLIOMA": {"LGG", "GBM"}}
# Checked preview packages counted at study level, without individual section records (backlog review of 16 October 2026).
PREVIEW_COUNTED = {"stad-gse270678": 72, "kirc-meylan-gse175540": 24, "lusc-emtab13530": 10, "stad-gse251950": 10,
                   "ucec-np137-gse225690": 4, "kirc-treated-gse294006": 3, "ucec-barkley-gse203612": 1}
SR = {c["spatial_review"]["id"]: c for c in cohorts if c.get("spatial_review")}
if set(SR) != set(SPATIAL_REVIEW) or len(SR) != len([c for c in cohorts if c.get("spatial_review")]):
    err(f"spatial review: {len(SR)} records differ from the 26 reviewed")
if {SR[k]["id"] for k in SPATIAL_EXISTING if k in SR} != set(SPATIAL_EXISTING.values()):
    err("spatial review: the three existing entries must keep their IDs and carry the review")
for rid, scope in SPATIAL_REVIEW.items():
    c = SR.get(rid)
    if not c:
        continue
    w, sr = f"spatial {rid}", c["spatial_review"]
    if c["id"] != SPATIAL_EXISTING.get(rid, rid):
        err(f"{w}: catalogue ID {c['id']} is not the expected one")
    if sr["analysis_cohort"] != scope or not (SCOPE_CANCERS.get(scope, {scope}) & set(c["cancers"])) or "SARC" in c["cancers"]:
        err(f"{w}: analysis scope or cancer pages do not match {scope}")
    level = "verified" if rid == "glioma-greenwald-gse237183" else "preview" if rid in PREVIEW_COUNTED else "candidate"
    if c["layer"] != "matched-spatial" or c["status"] != level or not c.get("gates"):
        err(f"{w}: must stay a gated matched-spatial entry with status {level}")
    if sr["eligible_patients"] is not None or sr["strict_core_promoted"] or (rid != "glioma-greenwald-gse237183" and any(x["cohort"] == c["id"] for x in captures)):
        err(f"{w}: no eligible-patient count, core promotion or (apart from Greenwald) section records are allowed")
    if not sr["assay_classes"] or any(a not in ENUMS["assay_class"] for a in sr["assay_classes"]) or sr["treatment_class"] not in ENUMS["treatment_class"]:
        err(f"{w}: invalid assay or treatment class")
    if sr["date"] != "2026-10-15" or c["verified_on"] != "2026-10-15":
        err(f"{w}: review date")
# Public-route review of 15 October 2026 (scripts/import_spatial_route_review.py): every reviewed record carries it.
ROUTE_VENDOR = {"cscc-10x-ffpe", "kirc-10x-xenium-protein", "kirp-10x-xenium-preview", "lusc-10x-cytassist", "prad-10x-acinar", "prad-10x-invasive"}
route_sections = 0
for rid, c in SR.items():
    w, rr = f"spatial {rid}", c["spatial_review"].get("route_review")
    if not rr:
        err(f"{w}: missing route review; run scripts/import_spatial_route_review.py after import_spatial_review.py")
        continue
    if rr["date"] != "2026-10-15" or not rr["status"] or not rr["next_step"] or not rr["states"] or any(x not in ENUMS["route_state"] for x in rr["states"]):
        err(f"{w}: route review needs a date, status, next step and valid states")
    if ("vendor-terms" in rr["states"]) != (rid in ROUTE_VENDOR) or (rid in ROUTE_VENDOR and c["access"]["category"] != "account"):
        err(f"{w}: the six vendor pages, and only they, need registration and terms")
    if ("dac-approval" in rr["states"]) != (c["access"]["category"] == "controlled"):
        err(f"{w}: data access committee approval and controlled access must agree")
    n = rr["sections_with_matching_coordinates"]
    if n is not None and (not isinstance(n, int) or n <= 0):
        err(f"{w}: invalid number of checked section packages")
    route_sections += n or 0
if route_sections != 144:
    err(f"spatial route review: {route_sections} checked section packages, expected 144")
leads = load("leads.json")
if len({x["id"] for x in leads}) != len(leads) or {x["id"] for x in leads} & set(cohort_by_id):
    err("leads.json: lead IDs must be unique and distinct from resource IDs")
for x in leads:
    check_url(f"lead {x['id']}", x["url"])
    for _, u in x.get("links", []):
        check_url(f"lead {x['id']}", u)
    if "cancers" in x or not x["not_counted"] or not DATE.match(x["checked_on"]):
        err(f"lead {x['id']}: leads are not assigned to cancer pages and must say why they are not counted")


def units(rid):
    return {u: n for n, u, *_ in SR[rid].get("reported") or []} if rid in SR else {}
def unit(rid, start):
    hits = [n for u, n in units(rid).items() if u.startswith(start)]
    return hits[0] if len(hits) == 1 else None
ARITH = [
    ("lusc-emtab13530", [unit("lusc-emtab13530", "LUSC donors"), unit("lusc-emtab13530", "LUSC tumour"), unit("lusc-emtab13530", "LUSC adjacent"), unit("lusc-emtab13530", "sections in the complete")], [2, 6, 4, 40]),
    ("cscc-hpv-gse208654", [unit("cscc-hpv-gse208654", "squamous"), unit("cscc-hpv-gse208654", "adenocarcinoma"), unit("cscc-hpv-gse208654", "HPV-positive"), unit("cscc-hpv-gse208654", "sections in the complete")], [1, 1, 2, 4]),
    ("kirc-meylan-gse175540", [unit("kirc-meylan-gse175540", "spatial samples"), unit("kirc-meylan-gse175540", "FFPE") + unit("kirc-meylan-gse175540", "fresh-frozen")], [24, 24]),
    ("kirp-10x-xenium-preview", [unit("kirp-10x-xenium-preview", "papillary"), unit("kirp-10x-xenium-preview", "non-diseased"), unit("kirp-10x-xenium-preview", "donors")], [1, 1, 2]),
    ("stad-gse251950", [unit("stad-gse251950", "donor labels"), unit("stad-gse251950", "primary") + unit("stad-gse251950", "metastasis"), unit("stad-gse251950", "spatial samples")], [9, 10, 10]),
    ("stad-gse270678", [unit("stad-gse270678", "deposited sections"), unit("stad-gse270678", "donor labels"), unit("stad-gse270678", "patients with main"), unit("stad-gse270678", "main sections") + unit("stad-gse270678", "repeat sections")], [72, 20, 19, 72]),
    ("ucec-barkley-gse203612", [unit("ucec-barkley-gse203612", "endometrial")], [1]),
    ("ucec-np137-gse225690", [unit("ucec-np137-gse225690", "metastasis"), unit("ucec-np137-gse225690", "patients") * unit("ucec-np137-gse225690", "timepoints")], [4, 4]),
    ("prad-hirz-slideseq", [unit("prad-hirz-slideseq", "prostate cancer"), unit("prad-hirz-slideseq", "control") + unit("prad-hirz-slideseq", "prostate cancer"), unit("prad-hirz-slideseq", "Slide-seqV2")], [2, 4, 12]),
    ("glioma-greenwald-gse237183", [unit("glioma-greenwald-gse237183", "IDH-wildtype glioblastoma") + unit("glioma-greenwald-gse237183", "IDH-mutant glioma"), unit("glioma-greenwald-gse237183", "IDH-wildtype donor"), unit("glioma-greenwald-gse237183", "IDH-mutant donor")], [19, 5, 6]),
    ("glioma-2026-niche-atlas", [unit("glioma-2026-niche-atlas", "Visium sections"), unit("glioma-2026-niche-atlas", "FFPE") + unit("glioma-2026-niche-atlas", "fresh-frozen"), unit("glioma-2026-niche-atlas", "Xenium"),
                                 unit("glioma-2026-niche-atlas", "patients in all"), unit("glioma-2026-niche-atlas", "patients with glioblastoma") + unit("glioma-2026-niche-atlas", "patients with IDH-mutant") + unit("glioma-2026-niche-atlas", "normal-brain control"),
                                 unit("glioma-2026-niche-atlas", "glioblastoma sections") + unit("glioma-2026-niche-atlas", "IDH-mutant astrocytoma sections") + unit("glioma-2026-niche-atlas", "normal-brain control")], [32, 32, 4, 17, 17, 32]),
    ("kirc-egad00001008781", [unit("kirc-egad00001008781", "patients"), unit("kirc-egad00001008781", "sections"), unit("kirc-egad00001008781", "spots")], [8, 16, 38836]),
    ("escc-precancer-geomx", [unit("escc-precancer-geomx", "patients in the study"), unit("escc-precancer-geomx", "patients with invasive") + unit("escc-precancer-geomx", "patients with intraepithelial"), unit("escc-precancer-geomx", "ROIs")], [19, 19, 42]),
    ("cscc-ou-stereo", [unit("cscc-ou-stereo", "tumour patients"), unit("cscc-ou-stereo", "tumour slides")], [14, 15]),
]
for rid, got, exp in ARITH:
    if got != exp:
        err(f"spatial {rid}: reported units {got} differ from {exp}")
if unit("glioma-greenwald-gse237183", "sections in the study") != 19:
    err("spatial Greenwald: study sections must be 19")
lusc_ids = SR["lusc-emtab13530"]["spatial_review"]["sample_ids"] if "lusc-emtab13530" in SR else {}
if sorted(lusc_ids.get("tumour_sample_ids", [])) != ["P11_T1", "P11_T2", "P11_T3", "P11_T4", "P19_T1", "P19_T2"] or sorted(lusc_ids.get("adjacent_sample_ids", [])) != ["P11_B1", "P11_B2", "P19_B1", "P19_B2"]:
    err("spatial E-MTAB-13530: LUSC selection must be Patients 11 and 19 (six tumour, four adjacent sections)")
if "cscc-hpv-gse208654" in SR and (SR["cscc-hpv-gse208654"]["spatial_review"]["sample_ids"].get("sample_ids") != ["GSM6360691"]
                                   or "GSM6360692" not in SR["cscc-hpv-gse208654"]["spatial_review"]["sample_ids"].get("exclude_sample_ids", [])):
    err("spatial GSE208654: only the SCC section GSM6360691 is selected; the adenocarcinoma is excluded")
if "ucec-barkley-gse203612" in SR and SR["ucec-barkley-gse203612"]["spatial_review"]["sample_ids"].get("sample_ids") != ["GSM6177623"]:
    err("spatial GSE203612: only GSM6177623 is the UCEC spatial sample")
for rid, cls in (("kirc-treated-gse294006", "treated"), ("ucec-np137-gse225690", "baseline-and-on-treatment")):
    if rid in SR and (SR[rid]["spatial_review"]["treatment_class"] != cls or "treated" not in SR[rid]["gates"]):
        err(f"spatial {rid}: must stay a treated, gated resource")
if "ucec-np137-gse225690" in SR and SR["ucec-np137-gse225690"]["compartments"] != ["metastatic-tumour"]:
    err("spatial NP137: all captures are metastatic biopsies")
if "pcpg-ling-ssrn" in SR and (SR["pcpg-ling-ssrn"].get("reported") or SR["pcpg-ling-ssrn"]["spatial_review"]["assay_classes"] != ["unverified"]):
    err("spatial pcpg-ling-ssrn: the manuscript lead carries no count and no verified platform")
if "pcpg-developmental-preprint" in SR and ([x[:2] for x in SR["pcpg-developmental-preprint"].get("reported") or []] != [[2, "human PPGL specimens"]]
                                             or SR["pcpg-developmental-preprint"]["access"]["category"] != "unreleased"):
    err("spatial pcpg-developmental-preprint: two human PPGL specimens only, with no released accession")
# Deduplicate by accession, Zenodo record, vendor dataset and DOI across the whole catalogue.
def ident(c):
    text = " ".join([c.get("accession") or ""] + [u for _, u in c["access"].get("links", [])])
    out = {k.upper() for k in re.findall(r"\b(GSE\d+|E-MTAB-\d+|EGA[DS]\d+|HRA\d+|OMIX\d+|CNP\d+|PRJNA\d+)\b", text)}
    out |= {f"ZENODO:{z}" for z in re.findall(r"zenodo(?:\.org/records/|\s+)(\d+)", text, re.I)}
    out |= {f"10X:{v}" for v in re.findall(r"10xgenomics\.com/datasets/([\w-]+)", text)}
    if (c.get("citation") or {}).get("doi"):
        out.add(c["citation"]["doi"].lower())
    return out
# Older entries may deliberately split one study by cancer or assay; reviewed records must not overlap anything.
reviewed_ids = {c["id"] for c in SR.values()}
owner = {}
for c in sorted(cohorts, key=lambda c: c["id"] not in reviewed_ids):
    for k in ident(c):
        if k in owner and owner[k] != c["id"] and (owner[k] in reviewed_ids or c["id"] in reviewed_ids):
            err(f"spatial review: {k} appears in both {owner[k]} and {c['id']}")
        owner.setdefault(k, c["id"])
# Backlog review of 16 October 2026 (scripts/import_spatial_backlog_review.py): two image levels.
spatial = [c for c in cohorts if c["layer"] == "matched-spatial"]
BL = [c for c in spatial if c.get("backlog_review")]
if len(BL) != 77 or any(c.get("spatial_review") for c in BL):
    err(f"backlog review: {len(BL)} studies carry it, expected the 77 never package-reviewed before")
for c in BL:
    w, b = f"backlog {c['id']}", c["backlog_review"]
    rows = [x for x in captures if x["cohort"] == c["id"]]
    if b["date"] != "2026-10-16" or b["outcome"] not in ENUMS["backlog_outcome"] or not b["states"] or any(x not in ENUMS["route_state"] for x in b["states"]) \
            or not all(b.get(k) for k in ("depth", "image_finding", "molecular_finding", "next_step")):
        err(f"{w}: backlog review needs a date, a known outcome, valid dependencies and its findings")
    sel = [x for x in rows if x["image_level"] == "original"] if len({x["image_level"] for x in rows}) > 1 else rows
    if rows and b["study_local_donors"] is not None and len({x["patient"] for x in sel if x["patient"]}) != b["study_local_donors"]:
        err(f"{w}: {b['study_local_donors']} established donors in the review, but the records give a different number")
    if (b["sections_listed"] or 0) != len(rows):
        err(f"{w}: {len(rows)} section records but {b['sections_listed']} listed")
    want = ("verified" if any(x["image_level"] == "original" for x in rows) else "preview") if rows else "candidate"
    if c["status"] != want or (rows and c["verified_on"] != "2026-10-16"):
        err(f"{w}: status {c['status']} does not follow its section records ({want})")
    if ("dac-approval" in b["states"]) and c["access"]["category"] != "controlled":
        err(f"{w}: data access committee approval needs controlled access")
    if re.search(r"\b(no (new )?account|registration created|contact made|terms accepted)\b", " ".join(str(v) for v in b.values()), re.I):
        err(f"{w}: process notes must not appear in the public review text")
orig = [c for c in spatial if c["status"] == "verified"]
prev = [c for c in spatial if c["status"] == "preview"]
n_orig = sum(x["image_level"] == "original" for x in captures)
n_prev_rows = sum(x["image_level"] == "preview" for x in captures)
n_prev_counted = sum((c["spatial_review"]["route_review"]["sections_with_matching_coordinates"] or 0) for c in prev if not any(x["cohort"] == c["id"] for x in captures))
if {c["id"] for c in prev if not any(x["cohort"] == c["id"] for x in captures)} != {SR[k]["id"] for k in PREVIEW_COUNTED if k in SR} \
        or any(SR[k]["spatial_review"]["route_review"]["sections_with_matching_coordinates"] != n for k, n in PREVIEW_COUNTED.items() if k in SR):
    err("spatial: the preview studies without section records must be the seven route-reviewed packages, with their checked counts")
if (len(orig), len(prev), n_orig, n_prev_rows, n_prev_counted) != (15, 28, 255, 359, 124):
    err(f"spatial: {len(orig)} original-level and {len(prev)} preview-level studies, {n_orig} original and {n_prev_rows} + {n_prev_counted} preview sections; "
        "expected 15, 28, 255 and 359 + 124 (738 study–section records)")
for cid, n_sec, n_area in (("cand-frontiers2026-zenodo18238293", 11, 4),):
    rows = [x for x in captures if x["cohort"] == cid]
    if len(rows) != n_sec or len({x.get("assay_area_id") for x in rows}) != n_area or len({x["patient"] for x in rows}) != 10:
        err(f"spatial {cid}: {n_sec} sections from ten donors on {n_area} shared array areas expected")
zb = [x for x in captures if x["cohort"] == "cand-ziblat2024"]
if sum(x["image_level"] == "original" for x in zb) != 2 or len([x for x in zb if x["image_level"] == "preview"]) != 10 \
        or len({x.get("assay_area_id") for x in zb if x["image_level"] == "preview"}) != 8:
    err("spatial Ziblat: two original sections and ten preview regions on eight array areas expected")
gw = [x for x in captures if x["cohort"] == "cand-greenwald2024"]
if (sum(x["image_level"] == "original" for x in gw), sum(x["image_level"] == "preview" for x in gw)) != (12, 7):
    err("spatial Greenwald: 12 direct original matches and 7 preview-level sections expected")
if any(c["cancers"] == ["SARC"] or "SARC" in c["cancers"] for c in spatial):
    err("spatial: no resource is assigned to TCGA-SARC")

# TCGA molecular screen
meta = tcga["meta"]
rule = meta["rule"]
panel = meta["panel"]
excluded_projects = meta.get("excluded_projects", {})
# Patient-level files cover the panel projects only; scripts/remove_excluded_projects.py drops the excluded ones,
# whose project-level availability stays in tcga_counts.json.
audited = sorted(panel)
if set(excluded_projects) != {"SARC"} or len(panel) != 20 or "GBM" not in panel or "SARC" in panel:
    err(f"tcga: expected 20 panel projects including GBM, with TCGA-SARC outside the panel")
for name, d in (("tcga_patients", tcga_patients), ("tcga_flags", tcga_flags), ("tcga_patient_review", patient_review)):
    i = d["columns"].index("project")
    if any(r[i] in excluded_projects for r in d["rows"]) or "excluded_projects" in d["meta"]:
        err(f"{name}: projects outside the study must be removed; run scripts/remove_excluded_projects.py")
if set(eligibility["projects"]) != set(panel) or "excluded_projects" in eligibility["meta"]:
    err("tcga_eligibility: projects outside the study must be removed; run scripts/remove_excluded_projects.py")
if any(c["group"] == "excluded" for c in cancers) or any(c["status"] == "excluded" for c in cohorts):
    err("cancer pages and resources must not include projects outside the study")
for p, x in tcga["projects"].items():
    w = f"tcga {p}"
    for stage in ("pre_qc", "post_qc"):
        q = x[stage]
        if q["union"] != q["paired"] + q["rna_only"] + q["met_only"]:
            err(f"{w}: {stage} union is not paired + RNA-only + 450k-only")
    if x["post_qc"]["union"] > x["pre_qc"]["union"] or x["post_qc"]["paired"] > x["pre_qc"]["paired"]:
        err(f"{w}: post-QC count exceeds pre-QC count")
    n = x["normal"]
    if n["rna_he_met"] > n["rna_he"] or n["also_in_tumour_union"] + n["normal_only"] != n["rna_he"]:
        err(f"{w}: inconsistent normal-reference counts")
    if x["patients_either_compartment"] != x["post_qc"]["union"] + n["normal_only"]:
        err(f"{w}: distinct patients across compartments do not add up")
    passes = x["post_qc"]["union"] >= rule["min_total"] and x["post_qc"]["paired"] >= rule["min_paired"]
    if passes != x["passes_screen"] or x["in_panel"] != (p in panel):
        err(f"{w}: screen result disagrees with the rule or the panel list")
    if (x.get("group") is not None) != (p in panel) or (passes and p not in panel and p not in excluded_projects):
        err(f"{w}: project passes the screen or has an analysis group but is not in the panel, or the reverse")
    if bool(x.get("excluded_from_study")) != (p in excluded_projects):
        err(f"{w}: study exclusion flag disagrees with the excluded projects")
# The threshold applies to the analysis group: one project, or a pooled group (CRC, GLIOMA).
groups = tcga["groups"]
if sorted(p for g in groups.values() for p in g["projects"]) != sorted(panel) or len(groups) != 18:
    err(f"tcga: analysis groups do not partition the 20-project panel into 18 groups")
for g, ps in (("CRC", ["COAD", "READ"]), ("GLIOMA", ["LGG", "GBM"])):
    if groups[g]["projects"] != ps or meta["groups"][g] != ps:
        err(f"tcga: {g} must pool exactly {ps}")
for g, x in groups.items():
    if any(tcga["projects"][p]["group"] != g for p in x["projects"]):
        err(f"tcga group {g}: project group labels disagree")
    if not x["passes_screen"] or x["passes_screen"] != (x["post_qc"]["union"] >= rule["min_total"] and x["post_qc"]["paired"] >= rule["min_paired"]):
        err(f"tcga group {g}: screen result disagrees with the rule, or the group is below it")

tcga_entries = {c["tcga_project"]: c for c in cohorts if c.get("tcga_project")}
if set(tcga_entries) != set(audited):
    err(f"TCGA cohort entries {sorted(tcga_entries)} differ from the audited projects {audited}")
for p, c in tcga_entries.items():
    if c["status"] != ("excluded" if p in excluded_projects else "screened"):
        err(f"cohort {c['id']}: status {c['status']} does not match its study scope")

cols = tcga_patients["columns"]
prow = [dict(zip(cols, r)) for r in tcga_patients["rows"]]
if len({r["patient"] for r in prow}) != len(prow):
    err("tcga_patients: duplicate patient rows")
if sorted({r["project"] for r in prow}) != audited:
    err("tcga_patients: projects differ from the panel plus excluded projects")
recount = defaultdict(lambda: {"union": 0, "paired": 0, "rna_only": 0, "met_only": 0, "rna_he": 0, "rna_he_met": 0})
for r in prow:
    for k in ("tumour_rna", "tumour_met", "normal_rna", "normal_met"):
        if r[k] not in ENUMS["tcga_state"]:
            err(f"tcga patient {r['patient']}: invalid {k} {r[k]!r}")
    if r["normal_rna_he_met"] and not r["normal_rna_he"]:
        err(f"tcga patient {r['patient']}: normal 450k counted without normal RNA + H&E")
    if r["normal_rna_he"] and r["normal_rna"] != "retained":
        err(f"tcga patient {r['patient']}: normal reference without a retained normal RNA aliquot")
    t = recount[r["project"]]
    tr, tm = r["tumour_rna"] == "retained", r["tumour_met"] == "retained"
    t["union"] += tr or tm
    t["paired"] += tr and tm
    t["rna_only"] += tr and not tm
    t["met_only"] += tm and not tr
    t["rna_he"] += bool(r["normal_rna_he"])
    t["rna_he_met"] += bool(r["normal_rna_he_met"])
for p in audited:
    x, t = tcga["projects"][p], recount[p]
    got = {k: t[k] for k in ("union", "paired", "rna_only", "met_only")}
    if got != x["post_qc"] or (t["rna_he"], t["rna_he_met"]) != (x["normal"]["rna_he"], x["normal"]["rna_he_met"]):
        err(f"tcga {p}: patient table does not reproduce the project counts")
for g, x in groups.items():
    got = {k: sum(recount[p][k] for p in x["projects"]) for k in ("union", "paired", "rna_only", "met_only")}
    if got != x["post_qc"] or sum(recount[p]["rna_he"] for p in x["projects"]) != x["normal"]["rna_he"]:
        err(f"tcga group {g}: patient table does not reproduce the group counts")
for g, exp, alone in (("CRC", (599, 379), "READ"), ("GLIOMA", (756, 565), "GBM")):
    if (groups[g]["post_qc"]["union"], groups[g]["post_qc"]["paired"]) != exp or tcga["projects"][alone]["passes_screen"]:
        err(f"tcga {g}: expected {exp[0]} / {exp[1]} after assay QC, with {alone} below the screen on its own")
sx = tcga["projects"]["SARC"]
if (sx["post_qc"]["union"], sx["post_qc"]["paired"], sx["passes_screen"], sx["in_panel"]) != (225, 223, True, False):
    err("tcga SARC: expected 225 / 223, passing the screen but outside the panel")
totals = tcga["panel_totals"]
for k in ("union", "paired", "rna_only", "met_only"):
    if sum(tcga["projects"][p]["post_qc"][k] for p in panel) != totals["post_qc"][k]:
        err(f"tcga: panel tumour {k} is not the sum of the panel projects")
if (totals["post_qc"]["union"], totals["normal"]["rna_he"], totals["normal"]["rna_he_met"]) != (8139, 663, 378):
    err("tcga: panel totals differ from 8,139 tumour and 663 / 378 normal patients after assay QC")

fcols = tcga_flags["columns"]
patient_ids = {r["patient"] for r in prow}
for row in tcga_flags["rows"]:
    f = dict(zip(fcols, row))
    if f["patient"] not in patient_ids:
        err(f"tcga flag {f['aliquot']}: patient not in the patient table")
    if f["disposition"] == "excluded" and not (f["do_not_use"] or f["awg_pathology"]):
        err(f"tcga flag {f['aliquot']}: excluded without a flag")
    if f["disposition"] not in ("excluded", "unresolved"):
        err(f"tcga flag {f['aliquot']}: unexpected disposition {f['disposition']}")
for x in tcga_resources:
    check_url(f"tcga resource {x['id']}", x["url"])

# Histology review and analysis cohorts
H = [dict(zip(reviews["histology_columns"], r)) for r in reviews["histology"]]
pstate = {r["patient"]: r for r in prow}
if len(H) != len({h["patient"] for h in H}):
    err("tcga_reviews: duplicate histology records")
by_proj = Counter(h["project"] for h in H)
if by_proj != Counter({"ESCA": 185, "PAAD": 185}):
    err(f"tcga_reviews: expected 185 ESCA and 185 PAAD registered cases, found {dict(by_proj)}")
for h in H:
    w = f"histology {h['patient']}"
    if not h["stratum"]:
        err(f"{w}: no histology stratum")
    st = pstate.get(h["patient"])
    rna = bool(st) and st["tumour_rna"] == "retained"
    met = bool(st) and st["tumour_met"] == "retained"
    if (rna, met) != (h["tumour_rna_retained"], h["tumour_450k_retained"]):
        err(f"{w}: retained layers disagree with tcga_patients")
    if st and (bool(st["normal_rna_he"]), bool(st["normal_rna_he_met"])) != (h["normal_rna_he"], h["normal_rna_he_450k"]):
        err(f"{w}: normal-reference flags disagree with tcga_patients")
    if h["analysis_cohort"] and not (rna or met):
        err(f"{w}: cohort member without a retained tumour assay")
    if h["analysis_cohort"] == "ESCC" and (h["project"] != "ESCA" or h["publication_histology"] != "ESCC"):
        err(f"{w}: ESCC member not publication-reviewed ESCC")
    if h["analysis_cohort"] == "PDAC":
        ok = (h["publication_review_histology"] == "Ductal adenocarcinoma") or (
            h["analysis_reason"] == "pathology_report_confirmed_ductal" and h["pathology_report_url"])
        if h["project"] != "PAAD" or not ok:
            err(f"{w}: PDAC member without ductal review or report confirmation")

def cohort_counts(rows):
    rna = sum(h["tumour_rna_retained"] for h in rows)
    met = sum(h["tumour_450k_retained"] for h in rows)
    both = sum(h["tumour_rna_retained"] and h["tumour_450k_retained"] for h in rows)
    return {"patients": len(rows), "rna": rna, "met": met, "both": both,
            "rna_only": rna - both, "met_only": met - both,
            "normal": sum(bool(h["normal_rna_he"]) for h in rows), "normal_met": sum(bool(h["normal_rna_he_450k"]) for h in rows)}

EXPECT = {
    "ESCC": {"patients": 90, "rna": 90, "met": 90, "both": 90, "rna_only": 0, "met_only": 0, "normal": 2, "normal_met": 2},
    "PDAC": {"patients": 149, "rna": 143, "met": 149, "both": 143, "rna_only": 0, "met_only": 6, "normal": 4, "normal_met": 4},
    "PDAC-sensitivity": {"patients": 148, "rna": 142, "met": 148, "both": 142, "rna_only": 0, "met_only": 6, "normal": 4, "normal_met": 4},
}
members = {"ESCC": [h for h in H if h["analysis_cohort"] == "ESCC"],
           "PDAC": [h for h in H if h["analysis_cohort"] == "PDAC"]}
members["PDAC-sensitivity"] = [h for h in members["PDAC"] if not h["focal_squamous_flag"]]
for k, exp in EXPECT.items():
    got = cohort_counts(members[k])
    if got != exp:
        err(f"cohort {k}: {got} differs from the reviewed definition {exp}")
    if got["patients"] != got["both"] + got["rna_only"] + got["met_only"]:
        err(f"cohort {k}: patients is not paired + single-layer")
pdac_reasons = Counter(h["analysis_reason"] for h in members["PDAC"])
if pdac_reasons != Counter({"publication_reviewed_ductal": 142, "pathology_report_confirmed_ductal": 7}):
    err(f"PDAC evidence split {dict(pdac_reasons)} is not 142 publication + 7 report-confirmed")
paad_out = [h for h in H if h["project"] == "PAAD" and not h["analysis_cohort"] and (h["tumour_rna_retained"] or h["tumour_450k_retained"])]
if len(paad_out) != 8 or any(h["publication_review_histology"] in (None, "Ductal adenocarcinoma") for h in paad_out):
    err(f"PAAD: expected 8 retained cases excluded or held after review, found {len(paad_out)}")
if sum(h["focal_squamous_flag"] for h in H) != 1 or sum(h["primary_metastatic_separated"] for h in H) != 1:
    err("expected exactly one focal-squamous flag and one primary/metastatic separation")
proj_counts = {p: tcga["projects"][p]["post_qc"] for p in ("ESCA", "PAAD")}
for p, q in proj_counts.items():
    rows = [h for h in H if h["project"] == p and (h["tumour_rna_retained"] or h["tumour_450k_retained"])]
    both = sum(h["tumour_rna_retained"] and h["tumour_450k_retained"] for h in rows)
    if (len(rows), both) != (q["union"], q["paired"]):
        err(f"{p}: reviewed cases with retained assays ({len(rows)}/{both}) differ from project counts")
cohort_ids = {c["id"] for c in reviews["meta"]["cohorts"]}
if cohort_ids != set(EXPECT):
    err(f"tcga_reviews: cohort definitions {sorted(cohort_ids)} do not match {sorted(EXPECT)}")
S = [dict(zip(reviews["scope_columns"], r)) for r in reviews["scope"]]
if len(S) != reviews["meta"]["reviewed_patients"] or sum(x["reviewed_aliquots"] for x in S) != reviews["meta"]["reviewed_aliquots"]:
    err("tcga_reviews: scope review totals are inconsistent")
flag_patients = {dict(zip(fcols, r))["patient"] for r in tcga_flags["rows"]}
missing = [x["patient"] for x in S if x["patient"] not in flag_patients]
if missing:
    err(f"tcga_reviews: scope-reviewed patients without flagged aliquots: {missing[:5]}")

# Patient treatment and diagnosis screen, histology panel revision and analysis cohorts
EXPECTED_SELECTED = {  # approved selected contributions per project: total, paired
    "BLCA": (388, 382), "BRCA": (1062, 762), "CESC": (249, 248), "COAD": (427, 279), "READ": (154, 92), "ESCA": (90, 90),
    "GBM": (225, 46), "HNSC": (514, 506), "KIRC": (494, 305), "KIRP": (275, 261), "LGG": (502, 502), "LIHC": (357, 351),
    "LUAD": (457, 403), "LUSC": (471, 358), "PAAD": (149, 143), "PCPG": (178, 178), "PRAD": (402, 401),
    "STAD": (414, 348), "THCA": (495, 493), "UCEC": (523, 413)}
EXPECTED_COHORTS = {  # cohort: total, rna, 450k, paired, rna_only, 450k_only, role
    "BLCA": (388, 382, 388, 382, 0, 6), "BRCA": (1062, 1060, 764, 762, 298, 2), "CRC": (581, 579, 373, 371, 208, 2),
    "CSCC": (249, 248, 249, 248, 0, 1), "ESCC": (90, 90, 90, 90, 0, 0), "GLIOMA": (727, 643, 632, 548, 95, 84),
    "HNSC": (514, 506, 514, 506, 0, 8), "KIRC": (494, 493, 306, 305, 188, 1), "KIRP": (275, 274, 262, 261, 13, 1),
    "LIHC": (357, 351, 357, 351, 0, 6), "LUAD": (457, 453, 407, 403, 50, 4), "LUSC": (471, 471, 358, 358, 113, 0),
    "PCPG": (178, 178, 178, 178, 0, 0), "PDAC": (149, 143, 149, 143, 0, 6), "PRAD": (402, 401, 402, 401, 0, 1),
    "STAD": (414, 385, 377, 348, 37, 29), "THCA": (495, 493, 495, 493, 0, 2), "UCEC": (523, 521, 415, 413, 108, 2)}
EXPECTED_NORMAL_CHANGED = {"HNSC": (39, 20), "LUAD": (56, 19), "LUSC": (45, 8)}
COHORT_OF = {p: ("CRC" if p in ("COAD", "READ") else "GLIOMA" if p in ("LGG", "GBM") else "ESCC" if p == "ESCA"
                 else "PDAC" if p == "PAAD" else "CSCC" if p == "CESC" else p) for p in panel}
ROLE_OF = {p: "excluded" if p in excluded_projects else "classification-benchmark" if COHORT_OF[p] == "GLIOMA" else "discovery" for p in audited}
PR = {r[0]: dict(zip(patient_review["columns"], r)) for r in patient_review["rows"]}
if len(PR) != len(patient_review["rows"]):
    err("tcga_patient_review: duplicate patients")
retained_any = {r["patient"] for r in prow if "retained" in (r["tumour_rna"], r["tumour_met"], r["normal_rna"], r["normal_met"])}
if set(PR) != retained_any or len(PR) != 8187:
    err(f"tcga_patient_review covers {len(PR)} patients; {len(retained_any)} have a retained layer (expected 8,187)")
REASON_ORDER = [("diagnosis_reasons", "diagnosis_identity_or_episode_exclusion_hold"),
                ("treatment_exclusion_reasons", "known_treatment_exclusion"),
                ("treatment_hold_reasons", "treatment_unknown_hold")]
NARRATIVE_FIELDS = re.compile(r"(^|_)(notes?|texts?|comments?|narrative|report_text)(_|$)", re.I)
if any(NARRATIVE_FIELDS.search(c) for c in patient_review["columns"]):
    err("tcga_patient_review: a free-text field name appears in the public overlay")
for pid, r in PR.items():
    st = pstate[pid]
    tum = "retained" in (st["tumour_rna"], st["tumour_met"])
    if r["has_retained_tumour"] != tum or r["project"] != st["project"] or r["case_id"] != st["case_id"]:
        err(f"patient review {pid}: retained tumour, project or case ID disagrees with the assay table")
    expected = next((d for k, d in REASON_ORDER if r[k]), "pass_annotation_screen")
    if r["main_disposition"] != expected:
        err(f"patient review {pid}: main disposition {r['main_disposition']} does not follow reason precedence")
    if tum and r["tumour_eligible"] != (r["main_disposition"] == "pass_annotation_screen"):
        err(f"patient review {pid}: tumour eligibility disagrees with disposition")
    if r["selected_eligible"] and not (tum and r["tumour_eligible"]):
        err(f"patient review {pid}: selected without an eligible retained tumour")
    p = r["project"]
    if r["analysis_role"] != ROLE_OF[p]:
        err(f"patient review {pid}: study role {r['analysis_role']} is not {ROLE_OF[p]}")
    g = r["analysis_group"]
    if p in excluded_projects:
        if g or r["selected_eligible"] or r["panel_exclusion_reason"] != "SARC_entirely_excluded_individual_entities_too_small":
            err(f"patient review {pid}: excluded-project patient has a cohort, a selection or no exclusion reason")
        if r["normal_catalogue_eligible"] or r["normal_in_active_scope"]:
            err(f"patient review {pid}: excluded-project normal package counted in active totals")
        continue
    if g not in (COHORT_OF[p], None) or (g is None and p not in ("ESCA", "PAAD", "CESC")):
        err(f"patient review {pid}: analysis group {g} does not match project {p}")
    if r["selected_eligible"] and r["selected_cohort"] != g:
        err(f"patient review {pid}: selected cohort {r['selected_cohort']} differs from analysis group {g}")
    if r["normal_donor_eligible"] != r["normal_catalogue_eligible"] or not r["normal_in_active_scope"]:
        err(f"patient review {pid}: active-project normal scope inconsistent")
    cesc_out = p == "CESC" and r["histology_stratum"] in ("Adenocarcinoma", "Adenosquamous")
    if (r["panel_exclusion_reason"] is not None) != cesc_out or (cesc_out and r["panel_exclusion_reason"] != "cervical_glandular_or_adenosquamous_outside_squamous_core"):
        err(f"patient review {pid}: study-scope exclusion does not match cervical histology")
    if p == "CESC" and (g == "CSCC") != (r["histology_stratum"] == "Squamous"):
        err(f"patient review {pid}: CSCC membership does not follow squamous histology")
    if r["site_override"] and g != "CRC":
        err(f"patient review {pid}: site override outside CRC")
    if r["site_reported"] is not None and g not in ("CRC", "PCPG"):
        err(f"patient review {pid}: reported site exported outside CRC and PCPG")
    if g == "CRC" and not r["site_reported"]:
        err(f"patient review {pid}: CRC patient without a reported site")
    glioma = p in ("LGG", "GBM")
    if glioma != (r["who_diagnosis_status"] == "requires_independent_integrated_diagnosis_and_grade") or (glioma and not r["molecular_group"]):
        err(f"patient review {pid}: glioma WHO status or molecular group inconsistent")
    if glioma and ("LGG_only" in (r["benchmark_subsets"] or [])) != (p == "LGG"):
        err(f"patient review {pid}: LGG-only benchmark subset does not follow the project")
    if (r["histology_stratum"] is not None) != (p in ("CESC", "UCEC", "PCPG", "LGG", "GBM")):
        err(f"patient review {pid}: reviewed histology present outside the revised projects, or missing")
for c, cohort_set in (("ESCC", {h["patient"] for h in H if h["analysis_cohort"] == "ESCC"}),
                      ("PDAC", {h["patient"] for h in H if h["analysis_cohort"] == "PDAC"})):
    sel = {p for p, r in PR.items() if r["selected_cohort"] == c and r["selected_eligible"]}
    if sel != cohort_set:
        err(f"patient review: {c} selection differs from the histology-review membership")
if PR["TCGA-EK-A2H0"]["tumour_eligible"] or not PR["TCGA-ZJ-A8QQ"]["tumour_eligible"]:
    err("CESC duplicate: expected TCGA-ZJ-A8QQ retained and TCGA-EK-A2H0 excluded")
case_ids = [r["case_id"] for r in PR.values()]
if len(set(case_ids)) != len(case_ids) or not all(case_ids):
    err("tcga_patient_review: GDC case IDs missing or not unique")

def stage_counts(rows):
    rna = sum(r["tumour_rna"] == "retained" for r in rows)
    met = sum(r["tumour_met"] == "retained" for r in rows)
    both = sum(r["tumour_rna"] == "retained" and r["tumour_met"] == "retained" for r in rows)
    return {"total": len(rows), "rna": rna, "met": met, "paired": both, "rna_only": rna - both, "met_only": met - both}

def lay_of(p):
    st = pstate[p]
    return "both" if st["tumour_rna"] == st["tumour_met"] == "retained" else "rna-only" if st["tumour_rna"] == "retained" else "met-only"

# Every analysis cohort: exact membership from the overlay, counts, role, normal scope; no patient in two cohorts.
EC = eligibility["cohorts"]
if set(EC) != set(EXPECTED_COHORTS) or set(COHORT_OF.values()) != set(EXPECTED_COHORTS):
    err(f"tcga_eligibility: cohorts {sorted(EC)} differ from the 18 expected")
cohort_members = {}
for c, exp in EXPECTED_COHORTS.items():
    m = sorted(p for p, r in PR.items() if r["selected_eligible"] and r["selected_cohort"] == c)
    cohort_members[c] = m
    got = stage_counts([pstate[p] for p in m])
    if tuple(got[k] for k in ("total", "rna", "met", "paired", "rna_only", "met_only")) != exp or got != EC.get(c, {}).get("selected_analysis"):
        err(f"cohort {c}: {got} differs from the approved {exp}")
    if EC[c]["role"] != ("classification-benchmark" if c == "GLIOMA" else "discovery"):
        err(f"cohort {c}: role {EC[c]['role']}")
    if sorted(EC[c]["projects"]) != sorted(p for p in panel if COHORT_OF[p] == c):
        err(f"cohort {c}: contributing projects differ")
    for p, x in EC[c]["contributions"].items():
        if x != stage_counts([pstate[q] for q in m if PR[q]["project"] == p]):
            err(f"cohort {c}: contribution of {p} differs from the overlay")
    for sub in EC[c].get("subsets", []):
        if not set(sub["patients"]) <= set(m) or {k: sub[k] for k in got} != stage_counts([pstate[p] for p in sub["patients"]]):
            err(f"cohort {c}: subset {sub['id']} is not inside the cohort or its counts differ")
all_members = [p for m in cohort_members.values() for p in m]
if len(all_members) != len(set(all_members)) or set(all_members) != {p for p, r in PR.items() if r["selected_eligible"]}:
    err("cohorts: a selected patient is missing from, or counted in more than one, analysis cohort")
if len(all_members) != 7826:
    err(f"cohorts: {len(all_members)} selected patients, expected 7,826")
for p in audited:
    e = eligibility["projects"].get(p)
    if not e:
        err(f"tcga_eligibility: missing project {p}")
        continue
    sel = e["selected_analysis"]
    if (sel["total"], sel["paired"]) != EXPECTED_SELECTED[p]:
        err(f"tcga_eligibility {p}: selected {sel['total']}/{sel['paired']} differs from the approved {EXPECTED_SELECTED[p]}")
    if e["analysis_cohort"] != COHORT_OF.get(p) or e["role"] != ROLE_OF[p]:
        err(f"tcga_eligibility {p}: analysis cohort or role differs")

# Subsets and sensitivity analyses.
sub = {s["id"]: s for c in EC.values() for s in c.get("subsets", [])}
for sid, exp in (("PDAC-sensitivity", (148, 142)), ("UCEC-endometrioid", (398, 303)), ("PCPG-without-neck", (176, 176)),
                 ("GLIOMA-LGG-only", (502, 502)), ("GLIOMA-paired-only", (548, 548))):
    if sid not in sub or (sub[sid]["total"], sub[sid]["paired"]) != exp:
        err(f"subset {sid}: expected {exp[0]} / {exp[1]}")
if set(sub) != {"PDAC-sensitivity", "UCEC-endometrioid", "PCPG-without-neck", "GLIOMA-LGG-only", "GLIOMA-paired-only"}:
    err(f"subsets {sorted(sub)} differ from the five approved")
if set(sub["PDAC-sensitivity"]["patients"]) != set(cohort_members["PDAC"]) - {h["patient"] for h in H if h["focal_squamous_flag"]}:
    err("PDAC sensitivity subset differs from the histology review")
if set(sub["UCEC-endometrioid"]["patients"]) != {p for p in cohort_members["UCEC"] if PR[p]["histology_stratum"] == "Endometrioid"}:
    err("UCEC endometrioid subset does not follow reviewed histology")
neck = sorted(p for p, r in PR.items() if r["head_neck_sensitivity_flag"])
if neck != ["TCGA-RM-A68T", "TCGA-RM-A68W"] or not set(neck) <= set(cohort_members["PCPG"]) or set(sub["PCPG-without-neck"]["patients"]) != set(cohort_members["PCPG"]) - set(neck):
    err("PCPG: the two neck paragangliomas must be in the cohort and outside the 176-patient subset")
if set(sub["GLIOMA-LGG-only"]["patients"]) != {p for p in cohort_members["GLIOMA"] if PR[p]["project"] == "LGG"}:
    err("GLIOMA: LGG-only subset differs from the LGG contribution")
if set(sub["GLIOMA-paired-only"]["patients"]) != {p for p in cohort_members["GLIOMA"] if lay_of(p) == "both"}:
    err("GLIOMA: paired-only subset differs from patients with both assays")

# Reviewed histology and annotations.
def strata_of(projects, select=False):
    out = Counter()
    for p, r in PR.items():
        if r["project"] in projects and r["has_retained_tumour"] and r["tumour_eligible"] and (r["selected_eligible"] or not select):
            out[(r["histology_stratum"], lay_of(p) == "both")] += 1
    return {k: (sum(v for (s, b), v in out.items() if s == k), sum(v for (s, b), v in out.items() if s == k and b)) for k in {s for s, _ in out}}
if strata_of(["CESC"]) != {"Squamous": (249, 248), "Adenocarcinoma": (46, 46), "Adenosquamous": (6, 5)}:
    err(f"CESC histology {strata_of(['CESC'])} differs from 249/248, 46/46 and 6/5")
if strata_of(["UCEC"]) != {"Endometrioid": (398, 303), "Serous": (112, 98), "Mixed": (12, 11), "Other": (1, 1)}:
    err(f"UCEC histology {strata_of(['UCEC'])} differs from the review")
if strata_of(["PCPG"]) != {"pheochromocytoma": (146, 146), "paraganglioma": (32, 32)}:
    err(f"PCPG histology {strata_of(['PCPG'])} differs from 146 / 32")
if strata_of(["LGG", "GBM"]) != {"IDHmut-non-codel": (254, 243), "IDHmut-codel": (163, 163), "IDHwt": (295, 135), "unassigned": (15, 7)}:
    err(f"glioma molecular groups {strata_of(['LGG', 'GBM'])} differ from 254/243, 163/163, 295/135 and 15/7")
conf = {p: (r["project"], r["selected_eligible"]) for p, r in PR.items() if r["histology_label_conflict"]}
if Counter(v[0] for v in conf.values()) != Counter({"CESC": 3, "UCEC": 19, "PCPG": 2}) or not all(s for p, (proj, s) in conf.items() if proj == "UCEC"):
    err("publication/GDC histology conflicts differ from 3 CESC, 19 UCEC (all selected) and 2 PCPG")
if {p: s for p, (proj, s) in conf.items() if proj in ("CESC", "PCPG")} != {"TCGA-DG-A2KK": True, "TCGA-EA-A5ZF": False, "TCGA-HM-A6W2": False, "TCGA-QR-A6GT": True, "TCGA-SR-A6MQ": True}:
    err("CESC and PCPG histology conflicts differ from the reviewed cases")

# Glioma benchmark details.
gbm = eligibility["projects"]["GBM"]
if gbm["dispositions"] != {"pass_annotation_screen": 225, "known_treatment_exclusion": 3, "treatment_unknown_hold": 4, "diagnosis_identity_or_episode_exclusion_hold": 10} \
        or (gbm["assay_qc"]["total"], gbm["assay_qc"]["rna"], gbm["assay_qc"]["met"], gbm["assay_qc"]["paired"]) != (242, 154, 139, 51):
    err("GBM: assay QC 242 (154 RNA, 139 450k, 51 paired) or dispositions 225 / 3 / 4 / 10 differ")
for p, test, why in (("TCGA-27-2523", lambda r: r["selected_eligible"] and any(c.startswith("supportive_") for c in r["covariates"]) and not r["treatment_exclusion_reasons"], "supportive medication covariate, selected"),
                     ("TCGA-06-1804", lambda r: r["selected_eligible"] and "GBM_submitted_LGG_corrected_retained_in_pooled_glioma" in r["covariates"], "LGG annotation kept, selected"),
                     ("TCGA-15-1444", lambda r: not r["selected_eligible"] and "diagnosis_or_specimen_eligibility_hold" in r["diagnosis_reasons"], "pathology hold"),
                     ("TCGA-27-2526", lambda r: not r["selected_eligible"] and "qualification_in_error_patient_hold" in r["diagnosis_reasons"], "qualification in error")):
    if not test(PR[p]):
        err(f"GBM {p}: expected {why}")

# Pooled colorectal cohort.
crc_rows = {p: r for p, r in PR.items() if r["project"] in ("COAD", "READ")}
crc_sel = set(cohort_members["CRC"])
if crc_sel != {p for p, r in crc_rows.items() if r["has_retained_tumour"] and r["tumour_eligible"]}:
    err("CRC: selected set is not every COAD and READ patient passing the patient screen")
ec = EC["CRC"]
SITE_OVERRIDES = {"TCGA-AY-4071": ("COAD", "rectum", "Sigmoid colon", "Colon, NOS", "rna-only"),
                  "TCGA-CM-4750": ("COAD", "rectum", "Rectosigmoid junction", "Colon, NOS", "both"),
                  "TCGA-AF-2692": ("READ", "colon_unspecified", "Rectum, NOS", "Not Reported", "rna-only"),
                  "TCGA-AF-2693": ("READ", "colon_unspecified", "Rectosigmoid junction", "Sigmoid colon", "both")}
got_over = {p: r for p, r in PR.items() if r["site_override"]}
if set(got_over) != set(SITE_OVERRIDES):
    err(f"CRC site overrides {sorted(got_over)} differ from the four approved corrections")
for p, (proj, over, site, resection, layers) in SITE_OVERRIDES.items():
    r = PR[p]
    if (r["project"], r["site_override"], r["site_reported"], r["resection_site_reported"], lay_of(p)) != (proj, over, site, resection, layers) or p not in crc_sel:
        err(f"CRC site correction {p}: expected {proj}, {over}, reported {site} / {resection}, {layers}, selected")
    o = next((x for x in ec["site_overrides"] if x["patient"] == p), None)
    if not o or (o["project"], o["override"], o["site_reported"], o["resection_site_reported"], o["layers"], o["selected"]) != (proj, over, site, resection, layers, True):
        err(f"CRC site correction {p}: eligibility summary disagrees")
if PR["TCGA-CI-6620"]["main_disposition"] != "known_treatment_exclusion" or "TCGA-CI-6620" in crc_sel:
    err("CRC: TCGA-CI-6620 must be a treatment exclusion")
f5 = PR["TCGA-F5-6810"]
if f5["main_disposition"] != "diagnosis_identity_or_episode_exclusion_hold" or not f5["treatment_hold_reasons"] or "TCGA-F5-6810" in crc_sel:
    err("CRC: TCGA-F5-6810 must be held for missing diagnosis and treatment history")
withheld = sorted(p for p, r in crc_rows.items() if r["has_retained_tumour"] and not r["tumour_eligible"])
if sorted(w["patient"] for w in ec["withheld"]) != withheld or len(withheld) != 18:
    err(f"CRC: withheld list differs from the patient review ({len(withheld)})")
sites = defaultdict(Counter)
for p in crc_sel:
    sites[PR[p]["site_reported"]][PR[p]["project"]] += 1
if {k: dict(v) for k, v in sites.items()} != ec["reported_sites"]:
    err("CRC: reported-site table differs from the patient review")

# Stages per project and for the panel (active projects only).
panel_stage = defaultdict(list)
for p in audited:
    rows_p = [pstate[x] for x, r in PR.items() if r["project"] == p]
    tum = [s for s in rows_p if PR[s["patient"]]["has_retained_tumour"]]
    after = [s for s in tum if PR[s["patient"]]["tumour_eligible"]]
    sel = [s for s in tum if PR[s["patient"]]["selected_eligible"]]
    e = eligibility["projects"][p]
    for name, rows_s in (("assay_qc", tum), ("after_patient_screen", after), ("selected_analysis", sel)):
        if stage_counts(rows_s) != e[name]:
            err(f"tcga_eligibility {p} {name}: stored counts differ from the patient tables")
        if p in panel:
            panel_stage[name] += rows_s
    tq = tcga["projects"][p]["post_qc"]
    if (e["assay_qc"]["total"], e["assay_qc"]["paired"]) != (tq["union"], tq["paired"]):
        err(f"tcga_eligibility {p}: assay-QC stage differs from tcga_counts")
    n_before = [s for s in rows_p if s["normal_rna_he"]]
    n_after = [s for s in n_before if PR[s["patient"]]["normal_donor_eligible"]]
    n_after_met = [s for s in n_after if s["normal_rna_he_met"]]
    if (len(n_after), len(n_after_met), p in panel) != (e["normal"]["rna_he_after"], e["normal"]["rna_he_met_after"], e["normal"]["in_active_scope"]):
        err(f"tcga_eligibility {p}: normal-reference counts or scope differ from the patient tables")
    expected_n = EXPECTED_NORMAL_CHANGED.get(p, (tcga["projects"][p]["normal"]["rna_he"], tcga["projects"][p]["normal"]["rna_he_met"]))
    if (len(n_after), len(n_after_met)) != expected_n:
        err(f"tcga_eligibility {p}: normal reference {len(n_after)}/{len(n_after_met)} differs from the approved {expected_n}")
    if len(n_before) != tcga["projects"][p]["normal"]["rna_he"]:
        err(f"tcga_eligibility {p}: normal packages before screening differ from tcga_counts")
ep = eligibility["panel"]
for name, total, paired, r_only, m_only in (("assay_qc", 8139, 6808, 1169, 162), ("after_patient_screen", 7970, 6703, 1110, 157),
                                             ("selected_analysis", 7826, 6561, 1110, 155)):
    got = stage_counts(panel_stage[name])
    if (got["total"], got["paired"], got["rna_only"], got["met_only"]) != (total, paired, r_only, m_only) or got != ep[name]:
        err(f"panel {name}: {got} differs from the approved {total}/{paired}/{r_only}/{m_only}")
disc = stage_counts([pstate[p] for c, m in cohort_members.items() if c != "GLIOMA" for p in m])
if (disc["total"], disc["paired"]) != (7099, 6013) or disc != ep["discovery"] or ep["benchmark"] != EC["GLIOMA"]["selected_analysis"]:
    err(f"panel discovery {disc['total']}/{disc['paired']} or benchmark totals differ from 7,099 / 6,013 and the GLIOMA cohort")
tum_review = [r for r in PR.values() if r["has_retained_tumour"] and r["project"] in panel]
disp = Counter(r["main_disposition"] for r in tum_review)
if disp != Counter({"pass_annotation_screen": 7970, "known_treatment_exclusion": 67, "treatment_unknown_hold": 40,
                    "diagnosis_identity_or_episode_exclusion_hold": 62}) or dict(disp) != ep["dispositions"]:
    err(f"patient screen dispositions {dict(disp)} differ from the approved split")
dims = {"treatment_exclusion": sum(bool(r["treatment_exclusion_reasons"]) for r in tum_review),
        "treatment_hold": sum(bool(r["treatment_hold_reasons"]) for r in tum_review),
        "diagnosis_identity_episode": sum(bool(r["diagnosis_reasons"]) for r in tum_review)}
if dims != {"treatment_exclusion": 74, "treatment_hold": 47, "diagnosis_identity_episode": 62} or dims != ep["reason_dimensions"]:
    err(f"overlapping reason dimensions {dims} differ from 74/47/62")

# Normal reference: active projects only; cohort scope separate from project scope.
nrows = [pstate[p] for p, r in PR.items() if r["project"] in panel and pstate[p]["normal_rna_he"] and r["normal_donor_eligible"]]
ctx = Counter(PR[s["patient"]]["normal_donor_context"] for s in nrows)
ctx_met = Counter(PR[s["patient"]]["normal_donor_context"] for s in nrows if s["normal_rna_he_met"])
if (len(nrows), sum(ctx_met.values())) != (656, 377) or ctx != Counter({"target_project_donor": 634, "organ_specific_control": 12,
        "non_target_or_uncertain_or_recurrent_donor": 5, "normal_only_donor_primary_diagnosis_unreported": 5}) or ctx_met != Counter(
        {"target_project_donor": 362, "organ_specific_control": 12, "non_target_or_uncertain_or_recurrent_donor": 2, "normal_only_donor_primary_diagnosis_unreported": 1}):
    err(f"normal reference after screening {len(nrows)}/{sum(ctx_met.values())} or its donor contexts differ from 656/377 (634/362, 12/12, 5/2, 5/1)")
if (ep["normal"]["rna_he_after"], ep["normal"]["rna_he_met_after"]) != (656, 377):
    err("panel normal reference differs from 656 / 377")
unrep = sorted(p for p, r in PR.items() if r["normal_donor_context"] == "normal_only_donor_primary_diagnosis_unreported" and pstate[p]["normal_rna_he"])
if len(unrep) != 5 or any(PR[p]["project"] != "GBM" or PR[p]["has_retained_tumour"] for p in unrep):
    err("normal-only donors without a reported diagnosis must be the five GBM normal-only packages")
for c, exp in (("CRC", (47, 19)), ("CSCC", (2, 2)), ("ESCC", (2, 2)), ("PDAC", (4, 4)), ("GLIOMA", (5, 1))):
    if (EC[c]["normal"]["rna_he_after"], EC[c]["normal"]["rna_he_met_after"]) != exp:
        err(f"cohort {c}: normal reference differs from {exp}")
if EC["CRC"]["normal"]["context"] != {"target_project_donor": 46, "non_target_or_uncertain_or_recurrent_donor": 1}:
    err("CRC: normal donor context differs from 46 target and 1 other (TCGA-AA-3525)")
if eligibility["projects"]["CESC"]["normal"]["outside_cohort"] != ["TCGA-FU-A3EO"] or PR["TCGA-FU-A3EO"]["histology_stratum"] != "Adenocarcinoma":
    err("CESC: the one normal donor outside CSCC should be the adenocarcinoma donor TCGA-FU-A3EO")

F = [dict(zip(fcols, x)) for x in tcga_flags["rows"]]
grp_flag = lambda f: f["project"] if f["project"] in ("READ", "GBM") else "other"
if Counter((grp_flag(f), f["disposition"]) for f in F) != Counter({("other", "excluded"): 725, ("other", "unresolved"): 105,
                                                                   ("READ", "excluded"): 14, ("GBM", "excluded"): 1, ("GBM", "unresolved"): 216}):
    err("tcga_flags: assay exclusions changed (expected 725 excluded and 105 unresolved before READ and GBM; 14 READ excluded; 1 excluded and 216 unresolved GBM)")
if eligibility["meta"]["treated_reference"] or eligibility["meta"]["integrated_who_diagnosis_adjudicated"]:
    err("tcga_eligibility: no treated reference and no adjudicated integrated WHO diagnosis are expected")

# Summary
def tally(rows):
    return len({(r["cohort"], r["patient"]) for r in rows if r["patient"]}), len(rows)

print(f"Release {release['version']} ({release['date']})")
print(f"Cohorts: {len(cohorts)}  " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(c['status'] for c in cohorts).items())))
p, n = tally(captures)
print(f"Spatial review: {len(SR)} records ({sum(SR[k]['id'] != k for k in SR)} enriching existing entries) across {len(set(SPATIAL_REVIEW.values()))} tumour groups; eligible patients unknown for all")
print(f"Captures: {n} section records, {p} known study-local patients, {sum(not c['patient'] for c in captures)} without a patient ID  "
      + ", ".join(f"{k}={v}" for k, v in sorted(Counter(c['tier'] for c in captures).items())))
print(f"Image levels: original H&E located {len(orig)} studies / {n_orig} sections; matched data with preview image {len(prev)} studies / "
      f"{n_prev_rows + n_prev_counted} sections ({n_prev_counted} counted without records); {len(spatial) - len(orig) - len(prev)} candidates")
print()
print(f"{'stratum':<16}{'core':>10}{'untreated':>12}{'post':>10}{'unknown':>10}")
by = defaultdict(list)
for c in captures:
    if c["tier"] == "core":
        by[c["stratum"]].append(c)
for s in strata:
    rows = by.get(s, [])
    cells = [tally(rows)] + [tally([r for r in rows if r["treatment"] == t]) for t in ("Untreated", "Post-treatment", "Unknown")]
    print(f"{s:<16}" + "".join(f"{f'{a}/{b}':>{w}}" for (a, b), w in zip(cells, (10, 12, 10, 10))))

print()
t = tcga["panel_totals"]
print(f"TCGA screen {meta['date']}: {len(groups)} screen groups from {len(panel)} panel projects (+ {', '.join(excluded_projects)} excluded); tumour {t['post_qc']['union']} patients "
      f"({t['post_qc']['paired']} both, {t['post_qc']['rna_only']} RNA only, {t['post_qc']['met_only']} 450k only); "
      f"normal RNA+H&E {t['normal']['rna_he']} ({t['normal']['rna_he_met']} with 450k); "
      f"distinct across compartments {t['patients_either_compartment']}; flagged aliquots {len(tcga_flags['rows'])}")

print(f"Patient screen {patient_review['meta']['date']}: {len(PR)} patients reviewed; tumour {ep['assay_qc']['total']} -> {ep['after_patient_screen']['total']} -> "
      f"{ep['selected_analysis']['total']} selected ({ep['selected_analysis']['paired']} paired, {ep['selected_analysis']['rna_only']} RNA only, "
      f"{ep['selected_analysis']['met_only']} 450k only); withheld {dict((k, v) for k, v in ep['dispositions'].items() if k != 'pass_annotation_screen')}; "
      f"normal {ep['normal']['rna_he_after']}/{ep['normal']['rna_he_met_after']}")
print(f"Analysis cohorts: {len(EC)} ({sum(c['role'] == 'discovery' for c in EC.values())} discovery, {sum(c['role'] == 'classification-benchmark' for c in EC.values())} benchmark); "
      f"discovery {ep['discovery']['total']}/{ep['discovery']['paired']}; GLIOMA {ep['benchmark']['total']}/{ep['benchmark']['paired']} "
      f"(LGG-only {sub['GLIOMA-LGG-only']['total']}, paired-only {sub['GLIOMA-paired-only']['total']}); CSCC {EC['CSCC']['selected_analysis']['total']}/{EC['CSCC']['selected_analysis']['paired']}; "
      f"UCEC {EC['UCEC']['selected_analysis']['total']}/{EC['UCEC']['selected_analysis']['paired']} (endometrioid {sub['UCEC-endometrioid']['total']}/{sub['UCEC-endometrioid']['paired']}); "
      f"PCPG {EC['PCPG']['selected_analysis']['total']} (without neck {sub['PCPG-without-neck']['total']})")
print(f"Pooled CRC: {ec['selected_analysis']['total']} selected ({ec['selected_analysis']['paired']} paired, {ec['selected_analysis']['rna_only']} RNA only, {ec['selected_analysis']['met_only']} 450k only); "
      f"COAD {ec['contributions']['COAD']['total']}/{ec['contributions']['COAD']['paired']}, READ {ec['contributions']['READ']['total']}/{ec['contributions']['READ']['paired']}; "
      f"withheld {len(withheld)}; site corrections {len(got_over)}; normal {ec['normal']['rna_he_after']}/{ec['normal']['rna_he_met_after']}")
print(f"Histology review: {len(H)} registered ESCA/PAAD cases; "
      + "; ".join(f"{k} {v['patients']} ({v['both']} paired, {v['met_only']} 450k only)" for k, v in ((k, cohort_counts(m)) for k, m in members.items()))
      + f"; PAAD retained cases outside the cohort {len(paad_out)}; scope review {len(S)} patients / {sum(x['reviewed_aliquots'] for x in S)} aliquots")

# Agent-readable files: generated from the data by build_agent_files.py and validated against their schemas.
import build_agent_files  # noqa: E402
for path in build_agent_files.stale():
    err(f"{path} is out of date; run python3 scripts/build_agent_files.py")
errors += build_agent_files.schema_errors()
print(f"Agent files: llms.txt, {len(list((DATA.parent / 'md').rglob('*.md')))} Markdown pages, {len(list((DATA / 'by-cancer').glob('*.json')))} per-cancer files, "
      f"{len(list((DATA.parent / 'schemas').glob('*.json')))} schemas" + ("" if build_agent_files.LICENCE else "; licence not yet set"))

# MCP server queries (mcp/src/explorer_mcp/catalogue.py, standard library): answers must match the data, and every tool must be documented.
sys.path.insert(0, str(DATA.parent / "mcp" / "src"))
from explorer_mcp.catalogue import TOOLS as MCP_TOOLS, Catalogue, SourceError  # noqa: E402
mcp_cat = Catalogue(DATA.parent)
try:
    mcp_overview = mcp_cat.catalogue_overview()
except SourceError as e:
    err(f"MCP catalogue: {e}")
    mcp_overview = {"tcga": {"selected_patients": ep["selected_analysis"]["total"]}}
if mcp_overview["tcga"]["selected_patients"] != ep["selected_analysis"]["total"]:
    err("MCP catalogue_overview: selected panel total differs from tcga_eligibility.json")
for cid, c in (EC.items() if not any(e.startswith("MCP catalogue") for e in errors) else []):
    r = mcp_cat.search_tcga_patients(cohort=cid, selected=True, limit=1)
    if (r["patients"], r["with_both"]) != (c["selected_analysis"]["total"], c["selected_analysis"]["paired"]):
        err(f"MCP search_tcga_patients {cid}: {r['patients']}/{r['with_both']} differs from the cohort's selected counts")
if not any(e.startswith("MCP catalogue") for e in errors) and mcp_cat.search_spatial_sections(limit=1)["sections"] != len(captures):
    err("MCP search_spatial_sections: total differs from captures.json")
for c in (cancers if not any(e.startswith("MCP catalogue") for e in errors) else []):
    bc = json.loads((DATA / "by-cancer" / f"{c['code']}.json").read_text(encoding="utf-8"))
    if mcp_cat.search_resources(cancer=c["code"], layer="matched-spatial", limit=1)["total"] != len(bc["spatial_resources"]):
        err(f"MCP search_resources {c['code']}: spatial resources differ from the cancer page")
for doc in ("agents.html", "README.md"):
    text = (DATA.parent / doc).read_text(encoding="utf-8")
    for name, _ in MCP_TOOLS:
        if name not in text:
            err(f"MCP tool {name} is not documented in {doc}")
print(f"MCP queries: {len(MCP_TOOLS)} tools; panel total, {len(EC)} cohort totals, {len(captures)} sections and {len(cancers)} cancer pages match")

if errors:
    print(f"\n{len(errors)} error(s):", file=sys.stderr)
    for e in errors:
        print("  " + e, file=sys.stderr)
    sys.exit(1)
print("\nAll checks passed.")
