#!/usr/bin/env python3
"""Import the TCGA histology adjudication and patient-scope review into data/tcga_reviews.json.

Usage: python3 scripts/import_tcga_review.py <review-dir>

Reads these files from <review-dir>:
  tcga_escc_pdac_final_adjudication.json  one record per registered TCGA-ESCA/TCGA-PAAD case
  tcga_patient_scope_review.json          patient-scope review of annotated, excluded assays
  tcga_329_aliquot_scope_review.json      the reviewed aliquots behind that patient review

Only structured public fields are exported: GDC identifiers and labels, published
histology fields, links to GDC pathology reports, cohort decisions and review actions.
Report text and free-text annotation notes are not copied. Standard library only.
"""
import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "tcga_reviews.json"

ESCA_SOURCE = "TCGA oesophageal carcinoma study (Nature 2017), Supplementary Table 1"
PAAD_SOURCE = "TCGA pancreatic study (Cancer Cell 2017), pathology review table (Histological type by RHH)"
REPORT_SOURCE = "Original GDC pathology report"
GDC_SOURCE = "GDC primary diagnosis only"

# Specimen detail documented in the review for the one patient with separate primary and metastatic samples.
SPECIMEN_NOTES = {
    "TCGA-HZ-A9TJ": "Primary pancreatic tumour samples 01A and 01Z (slides TCGA-HZ-A9TJ-01A-01-TS1 and "
                    "TCGA-HZ-A9TJ-01Z-00-DX1) are in the cohort. The metastatic sample 06A and its slide "
                    "TCGA-HZ-A9TJ-06A-01-TS1 are kept out of the primary-tumour cohort.",
}


COHORTS = [
    {"id": "ESCC", "project": "ESCA", "label": "Confirmed oesophageal squamous cell carcinoma",
     "status": "approved", "exception": "Approved smaller cohort: below both the 150-patient total and the 100-patient paired thresholds of the general screen.",
     "definition": "TCGA-ESCA patients classified as oesophageal squamous cell carcinoma in the TCGA oesophageal study's Supplementary Table 1, with retained primary-tumour assays after quality exclusions. Squamous carcinomas labelled only in GDC metadata are kept outside the cohort as provisional."},
    {"id": "PDAC", "project": "PAAD", "label": "Confirmed pancreatic ductal adenocarcinoma",
     "status": "proposed", "exception": "Proposed cohort one patient below the general 150-patient total threshold; the paired threshold is met. The general screen is unchanged.",
     "definition": "TCGA-PAAD patients with retained primary-tumour assays whose diagnosis is ductal adenocarcinoma in the TCGA pancreatic study's pathology review table (Histological type by RHH), plus patients absent from that table whose original GDC pathology report confirms invasive pancreatic ductal adenocarcinoma. Membership is an explicit patient list, not a morphology-code filter."},
    {"id": "PDAC-sensitivity", "project": "PAAD", "parent": "PDAC", "label": "Confirmed PDAC, sensitivity subset",
     "status": "sensitivity", "exception": None,
     "definition": "The PDAC cohort without the one patient whose pathology report describes a focal squamous component (TCGA-L1-A7W4)."},
]


def relation(r):
    """How the reviewed histology relates to the GDC label."""
    stratum, morph = r["histology_stratum"], r["morphology"]
    if r["project"] == "ESCA":
        return {
            "escc_publication_reviewed": "concordant", "eac_definite_oesophageal": "concordant",
            "eac_probable_oesophageal": "refined", "gej_adenocarcinoma_indeterminate_origin": "refined",
            "gastric_or_probably_gastric_adenocarcinoma": "differs", "unclassified_publication_histology": "unconfirmed",
        }.get(stratum, "not-reviewed")
    rhh = r.get("publication_RHH_histology")
    if r["analysis_reason"] == "pathology_report_confirmed_ductal":
        return "concordant"
    if not rhh:
        return "not-reviewed"
    if rhh == "Ductal adenocarcinoma":
        return "concordant" if morph == "8500/3" else ("differs" if morph == "8480/3" else "refined")
    if morph in ("8140/3", "8255/3"):  # unspecific GDC label made specific
        return "refined"
    if morph == "8480/3" and rhh.startswith("Colloid"):
        return "refined"
    return "differs"


def reviewed_histology(r):
    if r["project"] == "ESCA":
        if r.get("publication_histology") in ("ESCC", "AC"):
            site = r.get("publication_gej_category")
            return f"{'Squamous cell carcinoma' if r['publication_histology'] == 'ESCC' else 'Adenocarcinoma'}" + (
                f"; site: {site.replace('_', ' ').lower()}" if site and site != "NA" else "")
        if r.get("publication_histology") == "NA":
            return "Not classified in the publication table"
        return None
    if r["analysis_reason"] == "pathology_report_confirmed_ductal":
        return "Ductal adenocarcinoma (pathology report)"
    return r.get("publication_RHH_histology")


def evidence(r):
    if r["project"] == "ESCA":
        return ESCA_SOURCE if r.get("publication_histology") else GDC_SOURCE
    srcs = []
    if r.get("publication_150_member"):
        srcs.append(PAAD_SOURCE)
    if r.get("pathology_report_url"):
        srcs.append(REPORT_SOURCE)
    return "; ".join(srcs) or GDC_SOURCE


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    adj = json.load(open(src / "tcga_escc_pdac_final_adjudication.json", encoding="utf-8"))
    scope = json.load(open(src / "tcga_patient_scope_review.json", encoding="utf-8"))
    aliquots = json.load(open(src / "tcga_329_aliquot_scope_review.json", encoding="utf-8"))

    hcols = ["patient", "project", "stratum", "evidence", "evidence_level", "gdc_primary_diagnosis", "gdc_morphology",
             "gdc_diagnosis_id", "gdc_site", "publication_histology", "publication_site_category",
             "publication_table_member", "publication_review_histology", "publication_notes", "pathology_report_url",
             "reviewed_histology", "gdc_label_relation", "tumour_rna_retained", "tumour_450k_retained",
             "normal_rna_he", "normal_rna_he_450k", "analysis_cohort", "analysis_reason",
             "focal_squamous_flag", "primary_metastatic_separated", "specimen_note"]
    hrows = []
    for r in sorted(adj, key=lambda r: (r["project"], r["patient"])):
        hrows.append([
            r["patient"], r["project"], r["histology_stratum"], evidence(r), r["histology_evidence_level"],
            r["primary_diagnosis"], r["morphology"], r["primary_diagnosis_id"], r["tissue_or_organ_of_origin"],
            r.get("publication_histology") if r["project"] == "ESCA" else None,
            r.get("publication_gej_category") if r["project"] == "ESCA" else None,
            bool(r.get("publication_150_member")) if r["project"] == "PAAD" else None,
            r.get("publication_RHH_histology"), (r.get("publication_notes") or None),
            r.get("pathology_report_url"), reviewed_histology(r), relation(r),
            r["tumour_rna_retained"], r["tumour_450_retained"], r["normal_rna_he"], r["normal_rna_he_450"],
            r["analysis_cohort"], r["analysis_reason"],
            bool(r.get("focal_squamous_sensitivity_flag")), bool(r.get("primary_and_metastatic_samples_separate")),
            SPECIMEN_NOTES.get(r["patient"]),
        ])

    reviewed = Counter(a["patient"] for a in aliquots)
    scols = ["patient", "project", "summary_action", "reviewed_aliquots", "annotations"]
    srows = []
    for p in sorted(scope, key=lambda x: (x["project"], x["patient"])):
        anns = [{"category": a.get("category"), "entity_type": a.get("entity_type"), "entity": a.get("entity_barcode"),
                 "scope": a.get("scope"), "action": a.get("action"), "annotation_id": a.get("annotation_id")}
                for a in p["reviewed_annotations"]]
        srows.append([p["patient"], p["project"], p["summary_review_action"], reviewed[p["patient"]], anns])

    out = {
        "meta": {
            "date": "2026-10-14",
            "histology": "Documented diagnosis review of all registered TCGA-ESCA and TCGA-PAAD cases using published "
                         "pathology tables and original GDC pathology reports; not a new expert slide review.",
            "scope": "Metadata review of excluded assay aliquots carrying patient annotations, against live GDC case "
                     "annotations. Review categories are not additional exclusions.",
            "reviewed_aliquots": len(aliquots), "reviewed_patients": len(scope),
            "cohorts": COHORTS,
        },
        "histology_columns": hcols, "histology": hrows,
        "scope_columns": scols, "scope": srows,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    c = Counter(r[21] for r in hrows)
    print(f"histology records {len(hrows)} (cohorts {dict(c)}); scope patients {len(srows)}; reviewed aliquots {len(aliquots)}")


if __name__ == "__main__":
    main()
