#!/usr/bin/env python3
"""Apply the follow-up review of 16 October 2026 to the spatial records of release 0.10.0.

Usage: python3 scripts/import_spatial_followup_review.py <followup-dir>

Run after scripts/import_spatial_backlog_review.py. Reads from <followup-dir>:
  spatial_followup_delta.json  new_section_records, record_updates (guarded field changes), resource_updates, unchanged checks
  scenario_counts.json         the curator's projected counts, used only as a cross-check
  baseline_fingerprints.json   SHA-256 of cohorts.json and captures.json (and index.json) of release 0.10.0
  checksums.json               SHA-256 of every file above

The first run requires data files identical to release 0.10.0. Every record update names the exact old value: a field
must hold its old value (the change is applied) or its new value (already applied); anything else stops the import.
New section records are rebuilt on every run, so running the script again changes nothing. Section records listed here
replace the study-level counts of seven resources; records keep null patient IDs unless the source establishes the
donor, and eligibility stays null. Values are mapped to the site's vocabularies (for example site "Metastatic" to
"Metastasis", an adjacent-normal section to the solid-normal compartment); tier, compartment and the histology field
follow a changed site or diagnosis. Public wording of the resource findings, next steps and open checks is written
here; each changed field keeps its evidence URL in `field_sources`.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from vocab import ENUMS

DATA = Path(__file__).resolve().parent.parent / "data"
DATE = "2026-10-16"
BATCH = "followup-2026-10-16"
INPUTS = ("spatial_followup_delta.json", "scenario_counts.json", "baseline_fingerprints.json")
EXPECTED = {"original_resources": 16, "preview_resources": 29, "candidates": 68, "original_sections": 261, "preview_sections": 500,
            "records": 761, "known_patients": 266, "without_patient": 246, "new_records": 147, "updated_records": 179, "field_changes": 482}
# Resources whose study-level preview counts (public-route review) are now listed one by one.
COUNTED = {"stad-gse270678": 72, "kirc-meylan-gse175540": 24, "cand-dezuani-cvejic-2024": 10, "stad-gse251950": 10,
           "ucec-np137-gse225690": 4, "kirc-treated-gse294006": 3, "ucec-barkley-gse203612": 1}
NEW_ONLY = {"cand-wu2025-zenodo": 22, "cand-yoshihara2026erbt": 1}  # the 23 newly qualified preview sections

SITE = {"primary": ("Primary", "primary-tumour", None), "metastatic": ("Metastasis", "metastatic-tumour", None),
        "adjacent": ("Unknown", "solid-normal", "Adjacent normal"), "unknown": ("Unknown", None, None)}
SITE_UPDATE = {"Primary": ("Primary", "primary-tumour", None), "Metastatic": ("Metastasis", "metastatic-tumour", None),
               "Adjacent normal": ("Unknown", "solid-normal", "Adjacent normal"), "Recurrent": ("Unknown", None, "Recurrent sector")}
TREATMENT = {  # source wording -> (category, note)
    "treatment-naive surgical donors, study-level source statement": ("Untreated", "Treatment-naive surgical donors (study-level source statement)"),
    "treatment-naive, study-level source statement": ("Untreated", "Treatment-naive (study-level source statement)"),
    "post-treatment resection after trial nivolumab +/- ipilimumab": ("Post-treatment", "Resection after trial nivolumab with or without ipilimumab"),
    "pre-treatment biopsy before trial nivolumab +/- ipilimumab": ("Unknown", "Biopsy before trial nivolumab with or without ipilimumab; earlier systemic treatment is not excluded"),
    "Axitinib/Pembrolizumab": ("Post-treatment", "Axitinib and pembrolizumab (GEO series: sampled after systemic treatment)"),
    "Ipilimumab/Nivolumab": ("Post-treatment", "Ipilimumab and nivolumab (GEO series: sampled after systemic treatment)"),
    "at least two previous systemic lines; pre-NP137 baseline": ("Post-treatment", "At least two earlier systemic lines; trial baseline before NP137"),
    "at least two previous systemic lines; on NP137": ("Post-treatment", "At least two earlier systemic lines; on NP137"),
    "unknown": ("Unknown", None),
}
TREATMENT_UPDATE = {"Treatment-naive": ("Untreated", "Treatment-naive (study-level statement in the GEO series)")}
DONOR = {"source-backed clinical/individual label": "source-established", "explicit Factor Value[individual] in public SDRF": "source-established",
         "unresolved": "unresolved", "GEO title explicitly identifies patient": "source-sample-title"}
DONOR_PREFIX_UNRESOLVED = "11 source patient IDs established in object"  # Wu HCC: IDs not public, so no patient field
MOLECULAR = {
    "exact expression-barcode/in-tissue-coordinate agreement, prior complete package check":
        "Expression barcodes match the in-tissue coordinates exactly (complete package check of the public-route review)",
    "complete selected archive: MTX columns/barcodes equal 2078 in-tissue position barcodes; finite coordinates all inside supplied scaled preview":
        "Matrix columns and barcodes equal the 2,078 in-tissue positions; all coordinates fall inside the scaled preview",
}
MOLECULAR_PREFIX = {"source-integrated H5AD": "Source H5AD: the 104,418 expression rows align with the observation index and spatial coordinates; "
                    "each library has unique barcodes, finite positions and a supplied preview scale. The separate position tables are not independently joined"}
DIAGNOSIS = {"hepatocellular carcinoma, source study": "hepatocellular carcinoma"}
CLINICAL = {"anatomical_site": "subsite", "reported_grade": "grade", "reported_stage": "stage", "response_status": "response"}
DIRECT = {"patient", "donor_mapping", "diagnosis", "he_mpp", "he_mpp_basis", "geometry_check", "image_level", "he_file", "links", "tier_reason", "site", "treatment"}

OPEN_CHECKS = {  # public wording of the open checks of new records, by resource
    "default": ["The original H&E scan was not located; registration and calibration are separate checks."],
    "cand-wu2025-zenodo": ["The original H&E of the assayed section was not located; the 36 CODEX-region H&E images are not substituted.",
                           "Qualified by the row, library and scale correspondence within the source H5AD; the separate 28 position tables have not been joined independently.",
                           "The source's patient IDs are not yet mapped to these sections.",
                           "Pre-treatment means before trial therapy; earlier systemic treatment is not excluded."],
    "cand-yoshihara2026erbt": ["Only sample1 of the seven section packages has been checked.",
                               "The original scan of the assayed section and its treatment, histology and site remain to be confirmed.",
                               "The CytAssist instrument TIFF and aligned images are not original scans."],
}
OPEN_CHECK_UPDATES = {  # resource -> (0.10.0 wording, new wording), applied to all its records holding the old wording
    "cand-gse281978-hpv2024": ("The PT and LNMT labels conflict with the primary-tissue metadata; donor and site need joining before the three paired donors are counted.",
                               "Three primary (PT) and three nodal-metastatic (LNMT) sections, as the primary paper states; the generic GEO tissue annotation is not used. Donors still need joining before the three paired donors are counted."),
    "cand-greenwald2024": ("Donor labels and the clinical table conflict; no new eligible patients are inferred.",
                           "Patient labels follow Table S1 where it agrees with the GEO sample label; the two ZH1019/ZH1007 records stay unresolved, and the reported grades of BWH23 and BWH28 conflict with current grading. No eligible patients are inferred."),
    "cand-arora2023-gse208253": ("Patient IDs, treatment and original scans still to be mapped.",
                                 "The primary paper reports 12 spatial samples from 10 patients but no sample-to-patient join, so no patient IDs are assigned; treatment and original scans remain open."),
    "cand-webb2025": ("Recurrent, oligodendroglioma and astrocytoma labels are kept; donor independence and two image-frame checks are pending.",
                      "Recurrent, oligodendroglioma and astrocytoma labels are kept; A1 and A2 are the same patient, as the paper states. Donor independence of the other sections and two image-frame checks are pending."),
}
FOLLOWUP_OUTCOMES = ENUMS["followup_outcome"]
FOLLOWUP = {  # resource -> (findings, next step), public wording of the resource updates
    "cand-wu2025-zenodo": ("The source H5AD holds 104,418 expression rows and 22 named image libraries; rows, observation index and spatial coordinates align, and every coordinate falls inside its supplied preview. The 36 CODEX-region H&E images are not Visium originals.",
                           "Recover the original H&E of the assayed sections, join the 28 separate position tables independently and establish a public alias for the 11 source patients."),
    "cand-yoshihara2026erbt": ("The public DDBJ archive lists seven section packages. Sample1 was read completely: its 2,078 matrix barcodes equal the in-tissue positions, all inside the scaled preview. The CytAssist TIFF is not an original scan.",
                               "Check the six other packages, then recover original scans and the clinical scope."),
    "cand-wang-venet-2024-legacy-st": ("The complete README and clinical archive join 281 arrays to 94 clinical IDs; the count, coordinate and original-image association is not yet verified.",
                                       "Inspect selected array and image members and verify the count, coordinate and image join, keeping arrays and donors separate."),
    "cand-dutreneo": ("The 32 GB archive has 1,457 entries in 20 Xenium sample folders with morphology-focus and per-cycle fluorescence images, which are not H&E; no H&E correspondence is given.",
                      "Join the targeted expression and centroids to H&E if a public H&E is released; fluorescence morphology is not a substitute."),
    "cand-gessain2024-e-mtab-14409": ("One .cloupe file's header and index were decoded: 17,945 features, 3,346 barcodes, a spatial projection of each barcode and an embedded 7,572 × 7,626 brightfield image. The numeric blocks and image tiles are not decoded, and the projection scale is not a scanner calibration.",
                                      "Decode and count-check the expression and spatial blocks and the embedded image transform; transfer of the original whole-slide images needs a separate agreement."),
    "cand-knuch-2026": ("The accession is KAP241022. The linked CELLxGENE collection holds one single-cell dataset of 117,266 cells, not a measured spatial package.",
                        "Locate the released spatial subset and its matched H&E separately from the single-cell data."),
    "cand-simkin2026-gse268014-hd": ("Both Visium HD barcode sets match their in-tissue positions exactly (169,359 and 166,335). In each sample, the main TIFF and the brightfield file names carry opposite patient labels (P5684, P5624). The re-assays add no patients.",
                                     "Confirm the matrix, image, transform and source labels before listing HD sections; keep the source labels and the existing patients."),
    "cand-meti-luad14c": ("The 3,360-row metadata CSV holds barcodes and QC metrics, with no spatial coordinates.",
                          "Find the spot-coordinate table and a source-backed image scale; QC metrics are not coordinates."),
    "cand-beyaert2025-gse289908": ("Each of the three alignment JSON files lists 4,992 grid and image positions without barcode identifiers; the filtered matrices have 1,340, 2,913 and 1,552 barcodes.",
                                   "Find a source-backed barcode-to-grid map and validate the transformed positions."),
    "cand-hoefflin2026": ("The public sample list declares 25 relabelled glioblastoma samples reused from Ravi et al.; the IDH-mutant and glioblastoma archives were not fully read.",
                          "Inspect a selected IDH-mutant package and the source donor map; the reused Ravi samples are not new patients."),
    "cand-arora2023-gse208253": ("The primary paper reports 12 spatial samples from 10 unique patients; GEO does not give the sample-to-patient join.",
                                 "Find the sample-to-patient join; until then the 12 records keep no patient ID, and the 10 patients are reported for the study only."),
    "cand-tang2025": ("The software link now redirects to a public portal; no package-to-section join was inspected.",
                      "Inspect the portal's dataset and file metadata; raw GSA routes and processed spatial data stay separate."),
    "cand-gse281978-hpv2024": ("Zenodo 15226540 holds six original RGB OME-TIFFs whose names match the six GEO section titles. Coordinates fit the originals, the supplied scales reproduce the preview dimensions, and the headers give 0.287545 µm per pixel. Three sections are primary tumour and three are nodal metastases.",
                               "Join the sections to their donors; registration, calibration accuracy and pathology QC remain open."),
    "cand-crc-liu-maru2026": ("The paper links further processed data in Zenodo 19043057, but the record listed no downloadable files when checked; the 37 Visium records are unchanged.",
                              "Check Zenodo 19043057 for a file release and a clinical sample join; no records are added from it yet."),
}
RESOURCE_EXTRAS = {  # links, reported counts and corrections stated by the resource updates
    "cand-gse281978-hpv2024": {"links": [["Original images (Zenodo 15226540)", "https://zenodo.org/records/15226540"]],
                               "compartments": (["tumour-unspecified"], ["primary-tumour", "metastatic-tumour"])},  # (old, new)
    "cand-crc-liu-maru2026": {"links": [["Further processed data (Zenodo 19043057; no files listed)", "https://zenodo.org/records/19043057"]]},
    "cand-tang2025": {"links": [["Public data portal", "http://lfz178.ust.hk:8088/"]]},
    "cand-arora2023-gse208253": {"reported": [[12, "spatial samples", "primary paper Results"], [10, "unique patients", "primary paper Results"]]},
    "cand-wang-venet-2024-legacy-st": {"reported": [[281, "arrays", "Zenodo 8135721 clinical archive"], [94, "clinical IDs", "Zenodo 8135721 clinical archive"]]},
}
CHECKS = {  # unchanged check dimension -> (label, public result)
    "original-scan recovery": ("Original scans", "No further original scan matched to the expression and coordinates in the public listings and data routes checked."),
    "public processed alternative": ("Public processed alternative", "No qualified public processed or image alternative found; declared access restrictions apply only to those files, and retrieval failures are technical gaps."),
    "original-image level / independent registration-calibration sign-off": ("Original level and calibration", "Original level kept. Pixel sizes read from image headers and frame checks are recorded on the sections where available; registration and calibration accuracy are not signed off."),
    "release/final-publication search": ("Release search", "A bounded literature search found no measured spatial package with original images; other routes may still need review."),
}
CHECKS_BY_RESOURCE = {  # unchanged checks without a dimension, by resource
    "cand-zhao-htapp-2025": ("Package join", "Current Zenodo file metadata and the earlier 20-image, eight-prefix inventory do not resolve the spatial_list.Rda row-to-image join."),
    "cand-crc-spatch-ren2025": ("Package join", "The public 36-file image list does not establish which RNA and coordinates belong to each COAD platform."),
    "cand-spatch-hcc": ("Package join", "The same 36-file list does not establish the HCC RNA and coordinate join."),
    "cand-pribus2026": ("Package join", "The 108-entry archive inventory is kept; reading a selected member over the network failed, which is a technical gap."),
    "cand-prjna858545-hcc": ("Package join", "Figshare lists four public images (HCC, HCC-adjacent, CRC and CRC-adjacent); their RNA, coordinate and sample association is unresolved."),
    "cand-causer2023-uq": ("Public route retry", "The UQ DOI and landing page return HTTP 403, a technical gap; the paper states that processed Visium and PhenoCycler data are public and raw reads restricted."),
    "cand-xuzhou2023": ("Public route retry", "NODE still returns HTTP 403; no processed package was inspected."),
    "cand-wu2021-hcc": ("Public route retry", "The Lifeome server refuses connections; no archive was inspected."),
    "cand-gse283406": ("Coordinate join", "GEO sample metadata and positions do not resolve the physical-section, grid and scale association."),
    "cand-jiang2024meti": ("Image scale", "Source-backed scaling is still open; the METI LUAD14C metadata do not supply image coordinates."),
}
KEEP_GATES_OUT = ("package-unverified", "he-unverified", "release-unresolved", "request", "controlled")


def stop(msg):
    sys.exit(f"import_spatial_followup_review: {msg}")


def respace(t):
    """Spacing lost in the delta's compressed text (numbers glued to words)."""
    t = re.sub(r"(?<=[a-z])(?=\d)", " ", t)
    t = re.sub(r"(?<![A-Za-z\d.])(\d+(?:\.\d+)?)([A-Za-z]{2,})\b", r"\1 \2", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section_links(urls):
    data = [u for u in urls if not re.search(r"doi\.org|pmc\.ncbi|nature\.com|/acc\.cgi\?|/studies/E-", u)] or urls
    pick = lambda pat: next((u for u in data if re.search(pat, u, re.I)), data[0])
    return {"he": pick(r"hires_image|\.(tif|tiff|png|jpe?g)(\.gz)?$"), "expression": pick(r"matrix|\.h5$|\.mtx"),
            "coordinates": pick(r"position|spatial\.tar|scalefactors"), "raw": []}


def main():
    if len(sys.argv) != 2:
        stop("usage: import_spatial_followup_review.py <followup-dir>")
    src = Path(sys.argv[1])
    manifest = {f["file"]: f["sha256"] for f in json.loads((src / "checksums.json").read_text())["files"]}
    for name in INPUTS:
        if sha(src / name) != manifest.get(name):
            stop(f"{name} does not match its recorded checksum")
    delta = json.loads((src / INPUTS[0]).read_text())
    scen = json.loads((src / INPUTS[1]).read_text())
    finger = json.loads((src / INPUTS[2]).read_text())
    if delta["baseline_release"] != "0.10.0" or not delta["constraints"]["all_new_eligible_patients_null"]:
        stop("the delta must apply to release 0.10.0 and keep eligibility null")
    # data/index.json is generated from these two files, so only the source files identify the baseline.
    fresh = all(sha(DATA / f"{k}.json") == finger["sha256"][k] for k in ("cohorts", "captures"))

    cohorts = json.loads((DATA / "cohorts.json").read_text(encoding="utf-8"))
    captures = json.loads((DATA / "captures.json").read_text(encoding="utf-8"))
    if not fresh and not any(x.get("review_batch") == BATCH for x in captures):
        stop("data files differ from release 0.10.0 and the follow-up is not applied; restore the 0.10.0 files first")
    if fresh and any(x.get("review_batch") == BATCH for x in captures):
        stop("unexpected follow-up records in the 0.10.0 files")
    by_id = {c["id"]: c for c in cohorts}
    base = [x for x in captures if x.get("review_batch") != BATCH]
    rec = {x["id"]: x for x in base}

    # ---- guarded record updates
    ups = delta["record_updates"]
    if len(ups) != EXPECTED["updated_records"] or sum(map(len, ups.values())) != EXPECTED["field_changes"]:
        stop("expected 482 field changes on 179 records")
    for rid, changes in ups.items():
        x = rec.get(rid)
        if not x:
            stop(f"{rid}: record to update does not exist")
        x.setdefault("field_sources", {})
        for ch in changes:
            f, old, new, url = ch["field"], ch["old_value"], ch["new_value"], ch["evidence_url"]
            if not re.match(r"^https://\S+$", url or ""):
                stop(f"{rid}.{f}: evidence URL {url!r}")
            if f in CLINICAL:
                key, cur = CLINICAL[f], (x.get("clinical") or {}).get(CLINICAL[f])
                if cur not in (old, new):
                    stop(f"{rid}.clinical.{key}: {cur!r} is neither {old!r} nor {new!r}")
                x.setdefault("clinical", {})[key] = new
            elif f == "site":
                site, comp, wording = SITE_UPDATE[new]
                if x["site"] not in (old, site):
                    stop(f"{rid}.site: {x['site']!r} is neither {old!r} nor {site!r}")
                x["site"], x["compartment"] = site, comp
                if wording:
                    x["site_source"] = wording
                if new == "Recurrent":
                    x["sampled_recurrence"] = True
                x["tier"] = "metastatic" if site == "Metastasis" else "review"
            elif f == "treatment":
                cat, note = TREATMENT_UPDATE[new]
                if x["treatment"] not in (old, cat):
                    stop(f"{rid}.treatment: {x['treatment']!r}")
                x["treatment"], x["treatment_note"] = cat, note
            elif f == "donor_mapping":
                if x.get("donor_mapping") not in (old, DONOR[new]):
                    stop(f"{rid}.donor_mapping: {x.get('donor_mapping')!r}")
                x["donor_mapping"] = DONOR[new]
            elif f in DIRECT:
                if x.get(f) not in (old, new):
                    stop(f"{rid}.{f}: {x.get(f)!r} is neither the old nor the new value")
                x[f] = new
                if f == "diagnosis" and x.get("histology") in (None, old):
                    x["histology"] = new
            else:
                stop(f"{rid}: no mapping for field {f}")
            x["field_sources"][f if f not in CLINICAL else f"clinical.{CLINICAL[f]}"] = url
        # a patient label established by the source without its own mapping change
        if x.get("patient") and x.get("donor_mapping") == "unresolved":
            x["donor_mapping"] = "source-established"
        if x.get("patient") is None and x.get("donor_mapping") not in (None, "unresolved"):
            stop(f"{rid}: a donor mapping without a patient ID")
        x["verified_on"] = DATE
    for cid, (old, new) in OPEN_CHECK_UPDATES.items():
        hit = [x for x in base if x["cohort"] == cid and x.get("open_checks") in ([old], [new])]
        if not hit or len(hit) != sum(x["cohort"] == cid for x in base):
            stop(f"{cid}: open checks differ from the 0.10.0 wording")
        for x in hit:
            x["open_checks"] = [new]

    # ---- new section records
    new = []
    for r in delta["new_section_records"]:
        res = by_id.get(r["resource_id"])
        rid = f"{r['resource_id']}:{r['section_id']}"
        if not res or rid in rec or r["eligible_patients"] is not None or r["image_evidence"] != "preview" or r["assay_unit"] != "tissue-section":
            stop(f"{rid}: unknown resource, ID collision, eligibility or level")
        site, comp, wording = SITE[r["site"]]
        cat, note = TREATMENT[r["treatment"]]
        dm = DONOR.get(r["donor_mapping_status"]) or ("unresolved" if r["donor_mapping_status"].startswith(DONOR_PREFIX_UNRESOLVED) else None)
        if not dm or (r["patient"] is None) != (dm == "unresolved"):
            stop(f"{rid}: patient {r['patient']!r} and donor mapping {r['donor_mapping_status']!r} disagree")
        mc = MOLECULAR.get(r["molecular_check"]) or next((v for k, v in MOLECULAR_PREFIX.items() if r["molecular_check"].startswith(k)), None)
        checks = OPEN_CHECKS.get(r["resource_id"], OPEN_CHECKS["default"])
        if not mc or len(checks) != len(r["open_checks"]) or any(not re.match(r"^https://\S+$", u) for u in r["source_urls"]):
            stop(f"{rid}: molecular check, open checks or source URLs without a mapping")
        sr = res.get("spatial_review") or {}
        cancer = res["cancers"][0] if len(res["cancers"]) == 1 else sr.get("analysis_cohort")
        if cancer not in res["cancers"]:
            stop(f"{rid}: cannot assign one cancer code")
        dx = DIAGNOSIS.get(r.get("reported_diagnosis"), r.get("reported_diagnosis"))
        x = {
            "id": rid, "cohort": res["id"], "cancer": cancer, "stratum": None, "patient": r["patient"], "capture": r["section_id"],
            "accession": r["section_id"] if re.match(r"^GSM\d+$", r["section_id"]) else None,
            "tier": "metastatic" if site == "Metastasis" else "review",
            "tier_reason": "Matched data with preview image; the original H&E was not located. Not curated into a histology stratum.",
            "site": site, "site_source": wording, "treatment": cat, "treatment_note": note, "diagnosis": dx, "histology": dx,
            "technique": ", ".join(res.get("techniques") or ["Not specified"]),
            "preservation": res["preservation"][0] if len(res.get("preservation") or []) == 1 else "Unknown",
            "linkage": "listed-together", "registration": "Not yet checked", "he_mpp": None, "he_mpp_basis": "Scanner calibration pending",
            "he_file": None, "links": section_links(r["source_urls"]), "expression_type": mc,
            "access": {"he": res["access"]["category"], "processed": res["access"]["category"], "raw": "unresolved"},
            "verification": "file-checked", "verified_on": DATE, "clinical": {"subsite": r["anatomical_site"].replace("_", " ")} if r.get("anatomical_site") else {},
            "image_level": "preview", "review_batch": BATCH, "compartment": comp, "donor_mapping": dm, "open_checks": checks,
        }
        if r.get("source_sample_title"):
            x["source_name"] = r["source_sample_title"]
        if r.get("expression_subset"):
            x["expression_subset"] = r["expression_subset"]
        if r.get("image_scale") is not None:
            x["geometry_check"] = {"finite_positions": True, "positions_outside_preview": 0, "preview_scale": r["image_scale"],
                                   **({"preview_shape": r["preview_shape"]} if r.get("preview_shape") else {})}
        new.append(x)
    per = {}
    for x in new:
        per[x["cohort"]] = per.get(x["cohort"], 0) + 1
    if per != {**COUNTED, **NEW_ONLY} or len(new) != EXPECTED["new_records"]:
        stop(f"new records per resource {per} differ from the counted sections and the 23 new qualifications")
    for cid, n in COUNTED.items():
        if (by_id[cid]["spatial_review"]["route_review"] or {}).get("sections_with_matching_coordinates") != n or any(x["cohort"] == cid for x in base):
            stop(f"{cid}: the listed records must replace the {n} sections counted at study level")
    owner = {}
    for x in base + new:
        for k in {x["capture"], x.get("accession")} - {None}:
            if owner.setdefault(k, x["cohort"]) != x["cohort"]:
                stop(f"section {k} would belong to {owner[k]} and {x['cohort']}")
    captures = base + new

    # ---- resources
    for cid, u in delta["resource_updates"].items():
        c = by_id[cid]
        if u["outcome"] not in FOLLOWUP_OUTCOMES or cid not in FOLLOWUP or any(s not in ENUMS["route_state"] for s in u["states"]):
            stop(f"{cid}: outcome {u['outcome']!r} or dependencies without a mapping")
        if c["status"] not in (u["baseline_status"], u.get("proposed_status")):
            stop(f"{cid}: status {c['status']!r} is neither {u['baseline_status']!r} nor {u.get('proposed_status')!r}")
        if u.get("proposed_status"):
            level = "original" if u["proposed_status"] == "verified" else "preview"
            c["status"], c["verification"], c["verified_on"] = u["proposed_status"], "file-checked", DATE
            keep = [g for g in c.get("gates") or [] if g not in KEEP_GATES_OUT and not (level == "original" and g == "he-not-located")]
            c["gates"] = keep + [g for g in (["he-not-located"] if level == "preview" else []) + ["image-qc", "calibration"] if g not in keep]
        if u.get("accession_correction"):
            a = u["accession_correction"]
            if c.get("accession") not in (a["old_value"], a["new_value"]):
                stop(f"{cid}: accession {c.get('accession')!r}")
            c["accession"] = a["new_value"]
        extra = RESOURCE_EXTRAS.get(cid, {})
        have = {l for _, l in c["access"].get("links", [])}
        c["access"]["links"] = c["access"].get("links", []) + [l for l in extra.get("links", []) if l[1] not in have]
        if extra.get("compartments"):
            if c.get("compartments") not in (extra["compartments"][0], extra["compartments"][1]):
                stop(f"{cid}: compartments {c.get('compartments')!r}")
            c["compartments"] = extra["compartments"][1]
        if extra.get("reported"):
            rep = c.get("reported") or []
            c["reported"] = rep + [r for r in extra["reported"] if r not in rep]
        findings, nxt = FOLLOWUP[cid]
        c["followup_review"] = {"date": DATE, "outcome": u["outcome"], "depth": respace(u["depth"]), "findings": findings, "next_step": nxt,
                                "states": u["states"], "checks": []}
    for u in delta["unchanged"]:
        c = by_id[u["resource_id"]]
        label, result = CHECKS[u["check"]] if u.get("check") else CHECKS_BY_RESOURCE[u["resource_id"]]
        fr = c.setdefault("followup_review", {"date": DATE, "checks": []})
        item = {"check": label, "depth": respace(u["depth"]), "result": result}
        if item not in fr["checks"]:
            fr["checks"].append(item)
    if set(FOLLOWUP) != set(delta["resource_updates"]):
        stop("public wording must cover exactly the resource updates")

    # ---- cross-checks against the curator's projection (must reconcile, never forced)
    spatial = [c for c in cohorts if c["layer"] == "matched-spatial"]
    known = {(x["cohort"], x["patient"]) for x in captures if x["patient"]}
    got = {"original_resources": sum(c["status"] == "verified" for c in spatial), "preview_resources": sum(c["status"] == "preview" for c in spatial),
           "candidates": sum(c["status"] == "candidate" for c in spatial), "original_sections": sum(x["image_level"] == "original" for x in captures),
           "preview_sections": sum(x["image_level"] == "preview" for x in captures), "records": len(captures), "known_patients": len(known),
           "without_patient": sum(not x["patient"] for x in captures)}
    proj = {"original_resources": scen["original_resources"], "preview_resources": scen["preview_only_resources"], "candidates": scen["candidate_resources"],
            "original_sections": scen["original_section_records"], "preview_sections": scen["preview_section_records"],
            "records": scen["individually_listed_records_after_import"], "known_patients": scen["known_study_local_patients"],
            "without_patient": scen["records_without_patient_id"]}
    if got != proj or any(got[k] != EXPECTED[k] for k in got):
        stop(f"counts {got} do not reconcile with the projection {proj}")
    if any(x["cohort"] in {c["id"] for c in spatial if c["status"] == "preview"} and x["image_level"] != "preview" for x in captures):
        stop("a preview-level resource holds an original-image record")
    if any(c["status"] == "preview" and not any(x["cohort"] == c["id"] for x in captures) for c in spatial):
        stop("every preview-level resource must now list its sections")

    (DATA / "cohorts.json").write_text(json.dumps(cohorts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "captures.json").write_text(json.dumps(captures, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"follow-up review: {len(new)} section records added ({sum(COUNTED.values())} replacing study-level counts, {sum(NEW_ONLY.values())} new); "
          f"{len(ups)} records updated ({EXPECTED['field_changes']} guarded changes); {len(delta['resource_updates'])} resources updated; "
          f"resources {got['original_resources']} original, {got['preview_resources']} preview, {got['candidates']} candidates; "
          f"records {got['original_sections']} original, {got['preview_sections']} preview, {got['records']} in all; "
          f"known study-local patients {got['known_patients']}; records without a patient ID {got['without_patient']}")


if __name__ == "__main__":
    main()
