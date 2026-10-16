#!/usr/bin/env python3
"""Apply the 16 October 2026 spatial backlog package review: image levels, section records and study outcomes.

Usage: python3 scripts/import_spatial_backlog_review.py <backlog-review-dir>

Run after scripts/import_spatial_review.py and scripts/import_spatial_route_review.py. Reads from <backlog-review-dir>:
  spatial_backlog_public_corrections.json  outcome of each of the 77 candidates never package-reviewed before
  spatial_section_record_proposals.json    410 proposed section records (25 of those studies and Greenwald)
  scenario_counts.json                     the curator's projected counts, used only as a cross-check
  checksums.json                           SHA-256 of the three files above

Two image levels are recorded per section and per study: "original" (Original H&E located) and "preview" (Matched data
with preview image). A study counts once, at its best level, with the supported subset stated. New section records keep
null patient IDs unless the source establishes them, null eligibility and the "review" or "metastatic" tier (no core
promotion). Shared assay areas keep `assay_area_id` and the source region. Seven studies reviewed on 15 October hold
checked preview packages without individual records in these inputs; they move to the preview level with their checked
section counts, and no rows are invented for them. Text from the ledger is respaced mechanically and stripped of process
notes; next steps for the imported studies and the public wording of the section open checks are written here. Running the script again gives the same files; it stops if an input, count or join
disagrees with the expectations below.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from vocab import ENUMS

DATA = Path(__file__).resolve().parent.parent / "data"
DATE = "2026-10-16"
BATCH = "backlog-2026-10-16"
INPUTS = ("spatial_backlog_public_corrections.json", "spatial_section_record_proposals.json", "scenario_counts.json")
# Reviewed on 15 October: checked preview packages, no individual records in these inputs.
PREVIEW_FROM_ROUTE_REVIEW = {"stad-gse270678": 72, "kirc-meylan-gse175540": 24, "cand-dezuani-cvejic-2024": 10, "stad-gse251950": 10,
                             "ucec-np137-gse225690": 4, "kirc-treated-gse294006": 3, "ucec-barkley-gse203612": 1}
EXPECTED = {"original_resources": 15, "preview_resources": 28, "original_sections": 255, "preview_sections": 483, "listed_new": 410}

OUTCOME_STATES = {  # ledger outcome -> open dependencies (vocabulary route_state)
    "original-ready": ["public-download", "local-qc"], "preview-ready": ["public-download", "author-release", "local-qc"],
    "bounded-public-work": ["public-download", "local-qc"], "technical-gap": ["download-failure"],
    "release-unresolved": ["author-release"], "author-release": ["author-release"], "release-gap": ["author-release"],
    "code-only-lead": ["author-release"], "coordinate-gap": ["author-release", "local-qc"], "registration-gap": ["author-release", "local-qc"],
    "linkage-gap": ["local-qc"], "account-route": ["account-registration"], "unspecified-vendor-lead": ["vendor-terms"],
    "vendor-boundary": ["vendor-terms"]}
DEPTH = {"original-ready": "downloaded components checked", "preview-ready": "downloaded components checked",
         "coordinate-gap": "components inspected; join incomplete", "registration-gap": "components inspected; join incomplete",
         "linkage-gap": "components inspected; join incomplete", "bounded-public-work": "public listing or archive inventoried",
         "technical-gap": "public download failed", "access-dependent": "access boundary reached"}

# Next steps for the studies whose sections are imported (the ledger's own text describes the import itself).
NEXT = {
    "schmitt-2026": "Original scans; clinical and image QC.",
    "cand-wu-2021": "Original scans and the provenance of the image PDF; filter the out-of-tissue spots in three sections explicitly.",
    "cand-bassiouni-gse210616": "Treatment, original scans and registration QC.",
    "cand-crc-orgares-gse283052": "Map donor IDs and primary or metastatic site before counting patients; keep the shared barcode-vector provenance.",
    "cand-crc-mahidol-gse267401": "Original scans and treatment; the primary and metastatic sections of patients 21 and 17 stay separate sites.",
    "cand-crc-liu-maru2026": "Donor count and treatment; all 37 tissues are colorectal metastases.",
    "cand-liao-2025-gse250521": "Original scans; four anaplastic thyroid carcinoma sections and nine single-cell samples stay outside this selection.",
    "cand-tourneur-2026-legacyst": "Overlay and calibration QC for the legacy arrays; section treatment and site unknown; 12 anaplastic sections excluded.",
    "cand-yu2026atlas": "Clinical adjudication against the reported 22-patient denominator; one preview has an out-of-frame spot flagged.",
    "cand-ziblat2024": "Original-image overlay and calibration QC; the ten smaller-image regions share eight array areas and need multi-specimen review.",
    "cand-zheng2025": "Donor, site and treatment from the source; original image QC.",
    "cand-webb2025": "Donor independence and two image-frame checks; recurrent, oligodendroglioma and astrocytoma labels are kept.",
    "cand-ritternepsta2025": "Donor independence; 15 gliosarcoma sections are kept as glioblastoma variants, unrelated to TCGA-SARC; other CNS tumour types excluded.",
    "cand-longitudinal2026": "Same-patient timeline and the crosswalk of a fourth sample.",
    "cand-he2024": "Original scans and the donor, histology, grade and reuse crosswalk.",
    "cand-gse238264": "Original scans; all seven donors were treated with cabozantinib and nivolumab.",
    "cand-gse281759": "Donor total (the B0013 and B013 aliases conflict); regions, recurrent versus primary labels and one normal section are kept.",
    "cand-takano-suzuki-2024": "Only LUAD3B is checked; the rest of the study and image calibration remain (the 72 DPI tag is not a micron scale).",
    "cand-peng-kadara-2025": "Only the 30 invasive or minimally invasive sections are tumour; 25 precursor lesions and one normal stay separate; repeated sections of a patient stay linked.",
    "cand-chen-liu-2024": "Original pathology scans and the image transform; the donor relation of the solid and lepidic sections is unknown.",
    "cand-arora2023-gse208253": "Patient IDs, treatment and original scans.",
    "cand-cheng2022-gse181300": "Original scans and treatment; repeated invasive-front and inner sections of two patients.",
    "cand-gse281978-hpv2024": "Donor and site join before counting the three paired donors; the PT and LNMT labels conflict with the primary-tissue metadata.",
    "cand-frontiers2026-zenodo18238293": "Treatment and timing; 11 tissue blocks from ten donors share four array areas, and the recurrence field is a later outcome.",
    "cand-gse301720-ici2026": "Clinical timing and source site; response labels do not show that samples were taken after immunotherapy.",
}
OUTCOME_LABEL_CHECK = set(OUTCOME_STATES) | {"access-dependent"}
LINK_FIXES = {  # access and provenance corrections from the ledger
    "cand-wang-venet-2024-legacy-st": dict(relabel={"https://zenodo.org/records/13867935": "Code (Zenodo 13867935)"},
                                           add=[["Data record (Zenodo 8135721)", "https://zenodo.org/records/8135721"]]),
    "cand-dutreneo": dict(access="open", add=[["Targeted RNA data (Zenodo 19693316)", "https://zenodo.org/records/19693316"]],
                          route="Public targeted-RNA data in Zenodo 19693316; the earlier request-only label is corrected"),
    "cand-gessain2024-e-mtab-14409": dict(access="open", route="Public processed .cloupe files in E-MTAB-14409; sharing of the original institutional whole-slide images needs a separate agreement"),
    "cand-crc-spatch-ren2025": dict(relabel={"https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1900": "Images (BioImage Archive S-BIAD1900)"},
                                    add=[["Code (Zenodo 16992659)", "https://zenodo.org/records/16992659"]]),
    "cand-spatch-hcc": dict(relabel={"https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1900": "Images (BioImage Archive S-BIAD1900)"},
                            add=[["Code (Zenodo 16992659)", "https://zenodo.org/records/16992659"]]),
}
SITE = {"primary": ("Primary", "primary-tumour"), "primary tumour": ("Primary", "primary-tumour"), "metastatic": ("Metastasis", "metastatic-tumour"),
        "precursor": ("Unknown", "precursor"), "normal": ("Unknown", "normal"), "tumour, exact site unconfirmed": ("Unknown", "tumour-unspecified"),
        "unknown": ("Unknown", None)}
TREATMENT = {"without pretreatment, source-reported": "Untreated", "cabozantinib+nivolumab, source-reported treated": "Post-treatment",
             "none reported": "Unknown", "unknown": "Unknown"}
ESTABLISHED = {"established within source", "source patientid column checked"}
DONOR = {"established within source": "source-established", "source patientid column checked": "source-patient-column", "unresolved": "unresolved"}
# Public wording of the open check of each study's section records, by study and image level (the proposals word them
# as curation instructions; the input checksums pin that wording).
OPEN_CHECKS = {
    ("cand-arora2023-gse208253", "preview"):
        "Patient IDs, treatment and original scans still to be mapped.",
    ("cand-bassiouni-gse210616", "preview"):
        "One of 43 primary TNBC sections from 22 numbered patients; treatment, original scans and registration QC remain.",
    ("cand-chen-liu-2024", "preview"):
        "The CytAssist instrument TIFF is not an original pathology scan.",
    ("cand-cheng2022-gse181300", "preview"):
        "Repeated invasive-front and inner sections from two patients identified by UPN; original scans and treatment remain open.",
    ("cand-crc-liu-maru2026", "preview"):
        "All 37 deposited tissues are colorectal metastases; the donor count is unknown and treatment unresolved.",
    ("cand-crc-mahidol-gse267401", "preview"):
        "The paired primary and metastatic sections of patients 21 and 17 are separate sites; original scans and treatment remain open.",
    ("cand-crc-orgares-gse283052", "preview"):
        "The 12 matrices share one series barcode vector; donor IDs and primary or metastatic site need mapping before patients are counted.",
    ("cand-frontiers2026-zenodo18238293", "original"):
        "The publication describes 11 separately sectioned tissue blocks on four multiplexed array areas; area R3 holds two blocks. Recurrence is a later outcome, not a sampled recurrence.",
    ("cand-greenwald2024", "original"):
        "Donor labels and the clinical table conflict; no new eligible patients are inferred.",
    ("cand-greenwald2024", "preview"):
        "Donor labels and the clinical table conflict; no new eligible patients are inferred.",
    ("cand-gse238264", "preview"):
        "The source reports treatment with cabozantinib and nivolumab.",
    ("cand-gse281759", "preview"):
        "Region, recurrent-versus-primary and normal labels are kept; the B0013 and B013 aliases conflict, so no donor total is given.",
    ("cand-gse281978-hpv2024", "preview"):
        "The PT and LNMT labels conflict with the primary-tissue metadata; donor and site need joining before the three paired donors are counted.",
    ("cand-gse301720-ici2026", "preview"):
        "Response labels do not show that the sample was taken after immunotherapy; clinical timing and source site need confirmation.",
    ("cand-he2024", "preview"):
        "Provenance and geometry of the RAW PNG files, donor, histology, grade and overlap with reused data remain to be checked.",
    ("cand-liao-2025-gse250521", "preview"):
        "Eight PTC or locally advanced PTC sections and four normal sections; four ATC sections are kept separate. GEO records treatment as none.",
    ("cand-longitudinal2026", "preview"):
        "One of three checked longitudinal astrocytoma sections; the same-patient timeline and the crosswalk of a fourth record remain open.",
    ("cand-peng-kadara-2025", "preview"):
        "Only the 30 invasive or minimally invasive sections are tumour; precursor and normal sections stay separate, and a patient's repeated sections stay linked.",
    ("cand-takano-suzuki-2024", "original"):
        "The selected component files are complete, but the archive's tail is truncated; the donor or block identifier needs confirming from the source clinical table before patients are counted.",
    ("cand-webb2025", "preview"):
        "Recurrent, oligodendroglioma and astrocytoma labels are kept; donor independence and two image-frame checks are pending.",
    ("cand-wu-2021", "preview"):
        "Coordinate rows missing from the filtered matrix have no expression values, and none are imputed.",
    ("cand-yu2026atlas", "preview"):
        "Primary MIBC section; the boundary QC flag is kept, and the study's reported 22-patient denominator still needs clinical adjudication.",
    ("cand-zheng2025", "preview"):
        "Donor, site and treatment are unknown until joined to the source; original image QC remains.",
    ("cand-ziblat2024", "original"):
        "Barcodes renamed by R (.1_) are normalised explicitly to -1_; the retained matrix is a subset of the in-tissue coordinates.",
    ("cand-ziblat2024", "preview"):
        "Several specimen sections can share one array and image; the array identifier and the source region's expression subset are kept. The donor order within an array is unresolved.",
}
# Public text for studies whose ledger text carries process notes or a correction already applied here.
NEXT_OTHER = {
    "cand-dutreneo": "Inspect the targeted expression and centroids and their relation to the H&E; do not infer 20 independent patients.",
    "cand-gessain2024-e-mtab-14409": "Decode the counts, positions and preview inside the .cloupe files; transfer of the original whole-slide images needs a separate agreement.",
    "cand-meti-luad14c": "Inspect the metadata CSV for coordinates and an original-image or scale route; the released image is not an original scan.",
    "cand-zhao-htapp-2025": "Extract spatial_list and join the exact 20 sections and 8 reported donor labels to the image members; a directory listing alone does not verify the study.",
}
IMAGE_OTHER = {
    "cand-crc-colonmap-heiser2023": "HTAN public manifest behind a free account",
    "cand-crc-cottam-htan2025": "HTAN public portal behind a free account",
    "cand-10x-post-xenium-hd": "Official vendor source behind registration and terms",
}
DIAGNOSIS = {"Gliosarkom": "gliosarcoma"}  # source wording in German
MOLECULAR = {  # section-level molecular check, in words
    "exact-barcode-set": "Expression barcodes match the tissue coordinates exactly",
    "exact-in-tissue-barcode-set": "Expression barcodes match the in-tissue coordinates exactly",
    "matrix-header-and-barcode-vector; in-tissue selection": "Matrix headers and barcode vector match all array positions; in-tissue spots are selected explicitly",
    "shared-barcode-vector": "A barcode vector shared across the series matches all array positions; in-tissue spots must be selected",
    "unfiltered-matrix-in-tissue-filter-required": "Unfiltered matrix: every expression barcode has a position; in-tissue spots must be selected",
    "source-filtered-matrix; all expression barcodes have coordinates; explicit in-tissue selection required":
        "Source-filtered matrix: every expression barcode has coordinates; in-tissue spots must be selected explicitly",
}
CHECKED = {"original-ready", "preview-ready"}  # outcomes whose downloaded components were checked
# Assay of a section where the proposals name it; otherwise the study's technique, or all of them when it lists several
# (a section is not assigned one of them without evidence), and its preservation only when the study has one.
ASSAY = {"legacy-ST": "Spatial Transcriptomics (legacy arrays)"}


def stop(msg):
    sys.exit(f"import_spatial_backlog_review: {msg}")


def respace(t):
    """Restore the spacing lost in the ledger's compressed text (numbers glued to words, missing spaces after punctuation)."""
    if not t:
        return t
    t = t.replace("spatial_list.Rda2.70GB", "spatial_list.Rda (2.70 GB)")
    t = re.sub(r"\b(Import|All|Two|Zenodo|Public)(?=\d)", r"\1 ", t)
    t = re.sub(r"\b([a-z]{2,})(?=\d)", r"\1 ", t)
    t = re.sub(r"(?<=[A-Za-z\)])\(", " (", t)
    t = re.sub(r"(?<=[A-Za-z]),(?=[A-Za-z\d])", ", ", t)
    t = re.sub(r";(?=\S)", "; ", t)
    t = re.sub(r"(?<=\d)x(?=\d)", " × ", t)
    t = re.sub(r"(?<=\d)(GB|px)\b", r" \1", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def tidy_next(t):
    """Next-step text for the studies that are not imported, without process notes."""
    t = respace(t)
    for drop in ("; no contact made", "; no enquiry made", "; no application made", "; do not request now", "; no current matched increment",
                 "; no current matched gain"):
        t = t.replace(drop, "")
    return t[0].upper() + t[1:] + ("" if t.endswith(".") else ".")


def https(u):
    return re.sub(r"^ftp://ftp\.ncbi\.nlm\.nih\.gov/", "https://ftp.ncbi.nlm.nih.gov/", u)


def pick(urls, pattern, fallback):
    hit = next((u for u in urls if re.search(pattern, u, re.I)), None)
    return https(hit or fallback)


def section_links(r):
    pc = r.get("package_components") or {}
    urls = [u for u in r["source_urls"] if "doi.org" not in u and "frontiersin.org" not in u and "nature.com" not in u]
    data = https(urls[0] if urls else r["source_urls"][0])
    return {"he": https(pc["preview"]) if pc.get("preview") else pick(urls, r"\.(tif|tiff|png|jpe?g)(\.gz)?(/content)?$|image", data),
            "expression": https(pc["matrix"]) if pc.get("matrix") else pick(urls, r"matrix|counts|seurat|\.rds|\.h5|\.mtx", data),
            "coordinates": https(pc["coordinates"]) if pc.get("coordinates") else pick(urls, r"position|coords|spatial", data),
            "raw": []}


def section_cancer(resource, r):
    codes = resource["cancers"]
    dx = (r.get("reported_diagnosis") or r.get("histology") or "").lower()
    if set(codes) & {"LGG", "GBM"}:
        if "glioblastoma" in dx or "gliosark" in dx or "gliosarc" in dx:
            return "GBM"
        if "idh-mutant" in dx or "oligodendro" in dx:
            return "LGG"
        return "GLIOMA" if (len(set(codes) & {"LGG", "GBM"}) > 1 or dx) else codes[0]
    if set(codes) >= {"COAD", "READ"}:
        return "CRC"
    if len(codes) != 1:
        stop(f"{resource['id']}: cannot assign one cancer code from {codes}")
    return codes[0]


def main():
    if len(sys.argv) != 2:
        stop("usage: import_spatial_backlog_review.py <backlog-review-dir>")
    src = Path(sys.argv[1])
    manifest = {Path(f["file"] if "file" in f else f["path"]).name: f["sha256"] for f in json.loads((src / "checksums.json").read_text())["files"]}
    for name in INPUTS:
        if hashlib.sha256((src / name).read_bytes()).hexdigest() != manifest.get(name):
            stop(f"{name} does not match its recorded checksum")
    ledger = json.loads((src / INPUTS[0]).read_text())
    props = json.loads((src / INPUTS[1]).read_text())
    scen = json.loads((src / INPUTS[2]).read_text())
    if ledger["counts_are_eligible"] or not props["all_eligible_counts_null"] or ledger["cross_study_physical_section_deduplication_complete"]:
        stop("the inputs must keep eligibility null and say that physical-section deduplication is incomplete")

    cohorts = json.loads((DATA / "cohorts.json").read_text(encoding="utf-8"))
    captures = json.loads((DATA / "captures.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in cohorts}
    L = {r["id"]: r for r in ledger["resources"]}
    backlog = {c["id"] for c in cohorts if c["layer"] == "matched-spatial" and not c.get("spatial_review")
               and (c["status"] == "candidate" or c.get("backlog_review"))}
    if set(L) != backlog or len(L) != 77:
        stop(f"the ledger's 77 studies differ from the catalogue's never-reviewed candidates: {sorted(set(L) ^ backlog)[:6]}")
    if any(r["eligible_patients"] is not None or r["strict_core_promoted"] for r in L.values()):
        stop("the ledger must leave eligible patients unknown and promote nothing")
    unknown = ({r["outcome"] for r in L.values()} - OUTCOME_LABEL_CHECK) | ({r["outcome"] for r in L.values()} - ENUMS["backlog_outcome"])
    if any(x not in ENUMS["route_state"] for v in OUTCOME_STATES.values() for x in v):
        stop("an outcome maps to a dependency outside the route_state vocabulary")
    if unknown:
        stop(f"unmapped ledger outcomes {sorted(unknown)}")

    recs = props["records"]
    if len(recs) != EXPECTED["listed_new"] or len({(r["resource_id"], r["section_id"]) for r in recs}) != len(recs):
        stop("expected 410 proposed section records with unique study and section IDs")
    per = {}
    for r in recs:
        per.setdefault(r["resource_id"], []).append(r)
        if r["eligible_patients"] is not None or r["image_evidence"] not in ("original", "preview") or r["assay_unit"] != "tissue-section":
            stop(f"{r['section_id']}: eligibility must be null and the image level original or preview")
        if (r["patient"] is not None) != (r["donor_mapping_status"] in ESTABLISHED):
            stop(f"{r['section_id']}: a patient ID needs a source-backed donor mapping, and an unresolved mapping no patient ID")
        if len(r.get("open_checks") or []) > 1 or bool(r.get("open_checks")) != ((r["resource_id"], r["image_evidence"]) in OPEN_CHECKS):
            stop(f"{r['section_id']}: open checks differ from the public wording kept for its study and level")
        if r["site"] not in SITE or r["treatment"] not in TREATMENT:
            stop(f"{r['section_id']}: unmapped site or treatment {r['site']!r} / {r['treatment']!r}")
    if any(len({x for r in recs if (r["resource_id"], r["image_evidence"]) == k for x in r["open_checks"]}) != 1 for k in OPEN_CHECKS):
        stop("each study and level with public open-check wording must have exactly one open check in the proposals")
    imported = {rid for rid, r in L.items() if r["proposed_single_section_records"]}
    if set(per) != imported | {"cand-greenwald2024"} or set(NEXT) != imported:
        stop("proposed records must cover exactly the 25 studies with selections and Greenwald")
    for rid in imported - {"cand-ziblat2024"}:
        if len(per[rid]) != L[rid]["proposed_single_section_records"]:
            stop(f"{rid}: {len(per[rid])} proposed records but the ledger lists {L[rid]['proposed_single_section_records']}")
        if L[rid]["established_study_local_donors"] is not None and len({x["patient"] for x in per[rid] if x["patient"]}) != L[rid]["established_study_local_donors"]:
            stop(f"{rid}: patient IDs do not match the ledger's established donors")
    zb = per["cand-ziblat2024"]
    if sum(x["image_evidence"] == "original" for x in zb) != L["cand-ziblat2024"]["proposed_single_section_records"] or len({x.get("assay_area_id") for x in zb if x["image_evidence"] == "preview"}) != 8:
        stop("Ziblat: two original sections and ten preview regions on eight array areas expected")
    hn = per["cand-frontiers2026-zenodo18238293"]
    if len({x["assay_area_id"] for x in hn}) != 4 or len({x["patient"] for x in hn}) != 10:
        stop("Frontiers HNSC: 11 sections on four array areas from ten donors expected")
    gw = per["cand-greenwald2024"]
    if (sum(x["image_evidence"] == "original" for x in gw), sum(x["image_evidence"] == "preview" for x in gw)) != (12, 7):
        stop("Greenwald: 12 direct original matches and 7 preview-level sections expected")
    # Cross-study overlap: a source section ID must not already be a catalogued section of another study.
    have = {c["capture"]: c["cohort"] for c in captures if not c.get("review_batch")}
    have |= {c["accession"]: c["cohort"] for c in captures if c.get("accession") and not c.get("review_batch")}
    clash = [(r["resource_id"], r["section_id"], have[r["section_id"]]) for r in recs if r["section_id"] in have and have[r["section_id"]] != r["resource_id"]]
    if clash:
        stop(f"proposed sections already catalogued under another study: {clash[:5]}")
    for rid in PREVIEW_FROM_ROUTE_REVIEW:
        rr = (by_id[rid].get("spatial_review") or {}).get("route_review") or {}
        if rr.get("sections_with_matching_coordinates") != PREVIEW_FROM_ROUTE_REVIEW[rid]:
            stop(f"{rid}: the route review does not hold {PREVIEW_FROM_ROUTE_REVIEW[rid]} checked sections")

    # ---- section records
    base = [c for c in captures if c.get("review_batch") != BATCH]
    for c in base:
        c.setdefault("image_level", "original")
    new = []
    for r in recs:
        res = by_id[r["resource_id"]]
        site, comp = SITE[r["site"]]
        dx = r.get("reported_diagnosis") or r.get("histology")
        dx = DIAGNOSIS.get(dx, dx)
        checks = [OPEN_CHECKS[(r["resource_id"], r["image_evidence"])]] if r.get("open_checks") else []
        mc = r.get("molecular_check")
        if mc and mc not in MOLECULAR:
            stop(f"{r['section_id']}: molecular check {mc!r} has no wording")
        molecular = MOLECULAR[mc] if mc else (f"Checked for the study: {respace(L[res['id']]['molecular_finding'])}" if res["id"] in L else None)
        level = ("Original H&E located; registration and scanner calibration not yet checked." if r["image_evidence"] == "original"
                 else "Matched data with preview image; the original H&E was not located.")
        rec = {
            "id": f"{res['id']}:{r['section_id']}", "cohort": res["id"], "cancer": section_cancer(res, r), "stratum": None,
            "patient": r["patient"], "capture": r["section_id"], "accession": r["section_id"] if re.match(r"^GSM\d+$", r["section_id"]) else None,
            "tier": "metastatic" if site == "Metastasis" else "review",
            "tier_reason": f"{level} Not curated into a histology stratum.",
            "site": site, "site_source": None if r["site"] == "unknown" else r["site"], "treatment": TREATMENT[r["treatment"]],
            "treatment_note": None if r["treatment"] == "unknown" else r["treatment"],
            "diagnosis": dx, "histology": dx, "technique": ASSAY.get(r.get("assay")) or ", ".join(res.get("techniques") or ["Not specified"]),
            "preservation": res["preservation"][0] if len(res.get("preservation") or []) == 1 else "Unknown", "linkage": "listed-together",
            "registration": "Not yet checked", "he_mpp": None, "he_mpp_basis": "Scanner calibration pending",
            "he_file": r.get("original_filename"), "links": section_links(r), "expression_type": molecular,
            "access": {"he": res["access"]["category"], "processed": res["access"]["category"], "raw": "unresolved"},
            "verification": "file-checked" if r.get("molecular_check") or L.get(res["id"], {}).get("outcome") in CHECKED else "metadata-checked",
            "verified_on": DATE, "clinical": {},
            "image_level": r["image_evidence"], "review_batch": BATCH, "compartment": comp,
            "donor_mapping": DONOR[r["donor_mapping_status"]], "open_checks": checks,
        }
        for k in ("assay_area_id", "region_label", "expression_subset", "out_of_tissue_expression_spots", "original_crosswalk_inferred", "recurrence_outcome"):
            if r.get(k) is not None:
                rec[k] = r[k]
        new.append(rec)
    captures = base + new

    # ---- studies
    def gates(c, level):
        keep = [g for g in c.get("gates") or [] if g not in ("package-unverified", "he-unverified", "release-unresolved", "request", "controlled")]
        add = (["he-not-located"] if level == "preview" else []) + ["image-qc", "calibration"]
        return keep + [g for g in add if g not in keep]

    for rid, r in L.items():
        c = by_id[rid]
        rows = per.get(rid, [])
        levels = {x["image_evidence"] for x in rows}
        outcome = r["outcome"]
        states = OUTCOME_STATES.get(outcome) or (["dac-approval"] if r["baseline_access"] == "controlled" else ["author-release"])
        c["backlog_review"] = {
            "date": DATE, "outcome": outcome, "depth": DEPTH.get(outcome, "source or metadata only"), "states": states,
            "image_finding": IMAGE_OTHER.get(rid) or respace(r["image_finding"]), "molecular_finding": respace(r["molecular_finding"]),
            "next_step": NEXT.get(rid) or NEXT_OTHER.get(rid) or tidy_next(r["next_dependency"]),
            "sections_listed": len(rows) or None, "study_local_donors": r["established_study_local_donors"],
        }
        fix = LINK_FIXES.get(rid, {})
        if fix.get("access"):
            c["access"]["category"] = fix["access"]
        if fix.get("route"):
            c["access"]["route"] = fix["route"]
        links = [[fix.get("relabel", {}).get(u, lbl), u] for lbl, u in c["access"].get("links", [])]
        c["access"]["links"] = links + [l for l in fix.get("add", []) if l[1] not in {u for _, u in links}]
        if rows:
            level = "original" if "original" in levels else "preview"
            c["status"] = "verified" if level == "original" else "preview"
            c["verification"] = "file-checked"
            c["verified_on"] = DATE
            c["gates"] = gates(c, level)
            c["cancers"] = c["cancers"] + sorted({x["cancer"] for x in new if x["cohort"] == rid and x["cancer"] in ("LGG", "GBM")} - set(c["cancers"]))
        elif outcome in ("bounded-public-work", "coordinate-gap", "registration-gap", "linkage-gap") and c["verification"] == "source-described":
            c["verification"] = "metadata-checked"
        if rid == "cand-simkin2026-gse268014-hd":
            c["derived_from"] = ["simkin-2026"]
            note = "HD re-assays of the existing Simkin patients P5684 and P5624; they add no patients"
            c["notes"] = (c.get("notes") or []) + ([note] if note not in (c.get("notes") or []) else [])

    gw_c = by_id["cand-greenwald2024"]
    gw_c["status"], gw_c["gates"] = "verified", gates(gw_c, "original")
    note = "Twelve sections have directly matched original images; the two with inferred crossed labels and the five without originals are shown at preview level"
    gw_c["notes"] = gw_c["notes"] + ([note] if note not in gw_c["notes"] else [])
    for rid, n in PREVIEW_FROM_ROUTE_REVIEW.items():
        c = by_id[rid]
        c["status"], c["gates"] = "preview", gates(c, "preview")
        note = f"Matched data with preview image: {n} checked section packages, not yet listed as individual section records"
        c["notes"] = c["notes"] + ([note] if note not in c["notes"] else [])

    # ---- cross-checks against the curator's projection (must reconcile, never forced)
    spatial = [c for c in cohorts if c["layer"] == "matched-spatial"]
    orig = [c for c in spatial if c["status"] == "verified"]
    prev = [c for c in spatial if c["status"] == "preview"]
    n_orig = sum(1 for x in captures if x["image_level"] == "original")
    n_prev = sum(1 for x in captures if x["image_level"] == "preview") + sum(PREVIEW_FROM_ROUTE_REVIEW.values())
    got = {"original_resources": len(orig), "preview_resources": len(prev), "original_sections": n_orig, "preview_sections": n_prev}
    tl = scen["two_level_option"]
    proj = {"original_resources": tl["resources_with_original"], "preview_resources": tl["resources_preview_only"],
            "original_sections": tl["single_section_records_original"], "preview_sections": tl["single_section_records_preview"]}
    if got != proj or any(got[k] != EXPECTED[k] for k in got):
        stop(f"counts {got} do not reconcile with the projection {proj}")
    if any(x["cohort"] in {c["id"] for c in prev} and x["image_level"] != "preview" for x in captures):
        stop("a preview-level study holds an original-image section record")

    (DATA / "cohorts.json").write_text(json.dumps(cohorts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "captures.json").write_text(json.dumps(captures, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    known = len({(x["cohort"], x["patient"]) for x in captures if x["patient"]})
    print(f"backlog review: 77 studies updated; {len(new)} section records added ({sum(x['image_level'] == 'original' for x in new)} original, "
          f"{sum(x['image_level'] == 'preview' for x in new)} preview); studies {len(orig)} original and {len(prev)} preview; "
          f"section records {n_orig} original and {n_prev} preview ({sum(PREVIEW_FROM_ROUTE_REVIEW.values())} counted without individual rows); "
          f"known study-local patients {known}; sections without a patient ID {sum(1 for x in captures if not x['patient'])}")


if __name__ == "__main__":
    main()
