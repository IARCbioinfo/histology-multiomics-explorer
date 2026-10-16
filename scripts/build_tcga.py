#!/usr/bin/env python3
"""Build the TCGA molecular-screen tables from public GDC and PanCanAtlas metadata.

Usage: python3 scripts/build_tcga.py <input-dir> [--date YYYY-MM-DD]

Writes data/tcga_counts.json, data/tcga_patients.json and data/tcga_flags.json.
Curated text (cancer summaries, Hausser status, histology caveats) lives in
cancers.json and cohorts.json and is not touched. Standard library only.

Inputs, all public metadata (not molecular values):

  merged_sample_quality_annotations.tsv
      PanCanAtlas sample-quality annotations,
      https://api.gdc.cancer.gov/data/1a7d7be8-675d-4e60-a105-19d4121bdebf
  tcga_RNA_aliquot_metadata.json
      GDC files endpoint, cases.project.program.name=TCGA,
      data_type=Gene Expression Quantification, experimental_strategy=RNA-Seq
  tcga_450_aliquot_metadata.json
      GDC files endpoint, cases.project.program.name=TCGA,
      data_type=Methylation Beta Value, platform=Illumina Human Methylation 450
  tcga_normal_slide_metadata.json
      GDC files endpoint, TCGA slide images linked to Solid Tissue Normal samples
  pancanatlas_RNA_header.tsv, pancanatlas_450_header.tsv
      First line only of the final harmonized RNA and 450k-only matrices

For the GDC queries, request fields cases.case_id, cases.submitter_id,
cases.project.project_id, cases.samples.sample_id, cases.samples.submitter_id,
cases.samples.sample_type and
cases.samples.portions.analytes.aliquots.submitter_id.

Rules:
  * Tumour assays: sample_type "Primary Tumor"; normal reference: "Solid Tissue Normal".
  * Join each assay aliquot to the quality table by the full aliquot barcode and a
    compatible platform (RNA: IlluminaHiSeq_RNASeqV2 or IlluminaGA_RNASeqV2;
    450k: HumanMethylation450).
  * Exclude an aliquot if Do_not_use is True OR AWG_excluded_because_of_pathology is 1.
  * An aliquot without an exact match is unresolved: neither excluded nor retained.
  * Patient layers are counted from retained aliquots only, after exclusions.
  * Normal reference: a retained normal RNA aliquot whose sample also has a normal
    slide image; "with 450k" additionally needs a retained 450k aliquot on that sample.
  * Molecular screen: >= 150 patients with tumour RNA and/or 450k, >= 100 with both, applied to
    each analysis group. Colorectal adenocarcinoma (CRC) pools TCGA-COAD and TCGA-READ, and the
    glioma classification benchmark (GLIOMA) pools TCGA-LGG and TCGA-GBM, so READ and GBM
    contribute without passing the screen on their own.
  * TCGA-SARC passes the screen as a project but is outside the study: it combines several sarcoma
    types, each below the threshold. Its patients and flagged aliquots are still written here for
    validation and are removed afterwards by scripts/remove_excluded_projects.py; it is outside the
    panel and the panel totals.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"
RNA_PLATFORMS = {"IlluminaHiSeq_RNASeqV2", "IlluminaGA_RNASeqV2"}
MET_PLATFORMS = {"HumanMethylation450"}
COMPARTMENT = {"Primary Tumor": "tumour", "Solid Tissue Normal": "normal"}
MIN_TOTAL, MIN_PAIRED = 150, 100
# Analysis groups at the assay stage and the TCGA projects that feed them.
GROUPS = {"BLCA": ["BLCA"], "BRCA": ["BRCA"], "CESC": ["CESC"], "CRC": ["COAD", "READ"], "ESCA": ["ESCA"],
          "GLIOMA": ["LGG", "GBM"], "HNSC": ["HNSC"], "KIRC": ["KIRC"], "KIRP": ["KIRP"], "LIHC": ["LIHC"],
          "LUAD": ["LUAD"], "LUSC": ["LUSC"], "PAAD": ["PAAD"], "PCPG": ["PCPG"], "PRAD": ["PRAD"], "STAD": ["STAD"],
          "THCA": ["THCA"], "UCEC": ["UCEC"]}
PANEL = sorted(p for ps in GROUPS.values() for p in ps)
GROUP_OF = {p: g for g, ps in GROUPS.items() for p in ps}
# Projects audited with the panel but excluded from the study; kept in the patient and flag tables.
EXCLUDED = {"SARC": "excluded_from_study"}
AUDITED = sorted(PANEL + list(EXCLUDED))
NON_SOLID = {"LAML"}


def load_hits(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)["data"]
    hits = data["hits"]
    total = data.get("pagination", {}).get("total")
    if total is not None and total != len(hits):
        sys.exit(f"{path.name}: {len(hits)} records but pagination total {total}")
    return hits


def flag(value):
    return str(value).strip().lower() in {"true", "1", "1.0"}


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    src = Path(args[0])
    date = args[args.index("--date") + 1] if "--date" in args else None

    quality = defaultdict(list)
    with open(src / "merged_sample_quality_annotations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            quality[row["aliquot_barcode"]].append(row)

    aliquots = []  # one record per assay aliquot
    cases = {}
    for layer, fname, platforms in (("rna", "tcga_RNA_aliquot_metadata.json", RNA_PLATFORMS),
                                    ("met", "tcga_450_aliquot_metadata.json", MET_PLATFORMS)):
        for hit in load_hits(src / fname):
            if layer == "met" and hit.get("platform") != "Illumina Human Methylation 450":
                continue
            for case in hit["cases"]:
                project = case["project"]["project_id"].removeprefix("TCGA-")
                cases[case["submitter_id"]] = (project, case["case_id"])
                for sample in case["samples"]:
                    comp = COMPARTMENT.get(sample["sample_type"])
                    if not comp:
                        continue
                    for portion in sample.get("portions", []):
                        for analyte in portion.get("analytes", []):
                            for al in analyte.get("aliquots", []):
                                barcode = al["submitter_id"]
                                rows = [r for r in quality.get(barcode, []) if r["platform"] in platforms]
                                rec = {"project": project, "patient": case["submitter_id"],
                                       "sample": sample["submitter_id"], "sample_id": sample["sample_id"],
                                       "aliquot": barcode, "layer": layer, "compartment": comp}
                                if not rows:
                                    rec["disposition"] = "unresolved"
                                else:
                                    dnu = any(flag(r["Do_not_use"]) for r in rows)
                                    awg = any(flag(r["AWG_excluded_because_of_pathology"]) for r in rows)
                                    r = rows[0]
                                    rec.update({
                                        "disposition": "excluded" if (dnu or awg) else "retained",
                                        "do_not_use": dnu, "awg_pathology": awg,
                                        "pathology_reason": r["AWG_pathology_exclusion_reason"].strip() or None,
                                        "patient_annotation": r["patient_annotation"].strip() or None,
                                        "sample_annotation": r["sample_annotation"].strip() or None,
                                        "aliquot_annotation": (r["aliquot_annotation_updated"].strip()
                                                               or r["aliquot_annotation"].strip() or None),
                                        "reviewed_by_epc": flag(r["Reviewed_by_EPC"]),
                                    })
                                aliquots.append(rec)

    normal_slide_samples = set()
    for hit in load_hits(src / "tcga_normal_slide_metadata.json"):
        for case in hit["cases"]:
            for sample in case["samples"]:
                if sample["sample_type"] == "Solid Tissue Normal":
                    normal_slide_samples.add(sample["sample_id"])

    def header(name):
        with open(src / name, encoding="utf-8") as f:
            return [c.strip('"') for c in f.readline().rstrip("\n").split("\t")[1:]]

    historical = {}
    held_historical = {"rna": 0, "met": 0}
    for layer, name, platforms in (("rna", "pancanatlas_RNA_header.tsv", RNA_PLATFORMS),
                                   ("met", "pancanatlas_450_header.tsv", MET_PLATFORMS)):
        for barcode in header(name):
            if barcode[13:15] != "01":  # primary solid tumour
                continue
            rows = [r for r in quality.get(barcode, []) if r["platform"] in platforms]
            if not rows:
                held_historical[layer] += 1
                continue
            if any(flag(r["Do_not_use"]) or flag(r["AWG_excluded_because_of_pathology"]) for r in rows):
                continue
            historical.setdefault(rows[0]["cancer type"], {"rna": set(), "met": set()})[layer].add(barcode[:12])

    # Per patient, per compartment and layer: retained > unresolved > excluded.
    state = defaultdict(lambda: defaultdict(set))
    for a in aliquots:
        state[a["patient"]][(a["compartment"], a["layer"])].add(a["disposition"])
    retained_normal = defaultdict(lambda: defaultdict(set))  # patient -> layer -> sample_ids
    for a in aliquots:
        if a["compartment"] == "normal" and a["disposition"] == "retained":
            retained_normal[a["patient"]][a["layer"]].add(a["sample_id"])

    def summarise(dispositions):
        for s in ("retained", "unresolved", "excluded"):
            if s in dispositions:
                return s
        return "absent"

    patients = []
    by_project = defaultdict(list)
    for pid, layers in state.items():
        project, case_id = cases[pid]
        rec = {"patient": pid, "project": project, "case_id": case_id}
        for comp in ("tumour", "normal"):
            for layer in ("rna", "met"):
                rec[f"{comp}_{layer}"] = summarise(layers.get((comp, layer), set()))
        he_rna = retained_normal[pid]["rna"] & normal_slide_samples
        rec["normal_rna_he"] = bool(he_rna)
        rec["normal_rna_he_met"] = bool(he_rna & retained_normal[pid]["met"])
        patients.append(rec)
        by_project[project].append(rec)

    def counts(recs):
        tr = {r["patient"] for r in recs if r["tumour_rna"] == "retained"}
        tm = {r["patient"] for r in recs if r["tumour_met"] == "retained"}
        pre_r = {r["patient"] for r in recs if r["tumour_rna"] != "absent"}
        pre_m = {r["patient"] for r in recs if r["tumour_met"] != "absent"}
        n1 = {r["patient"] for r in recs if r["normal_rna_he"]}
        n2 = {r["patient"] for r in recs if r["normal_rna_he_met"]}
        tumour = tr | tm
        return {
            "pre_qc": {"union": len(pre_r | pre_m), "paired": len(pre_r & pre_m),
                       "rna_only": len(pre_r - pre_m), "met_only": len(pre_m - pre_r)},
            "post_qc": {"union": len(tumour), "paired": len(tr & tm),
                        "rna_only": len(tr - tm), "met_only": len(tm - tr)},
            "normal": {"rna_he": len(n1), "rna_he_met": len(n2),
                       "also_in_tumour_union": len(n1 & tumour), "normal_only": len(n1 - tumour)},
            "patients_either_compartment": len(tumour | n1),
        }

    project_counts = {}
    for project, recs in sorted(by_project.items()):
        if project in NON_SOLID:
            continue
        c = counts(recs)
        al = [a for a in aliquots if a["project"] == project]
        c["aliquots"] = {comp: {layer: {d: sum(1 for a in al if a["compartment"] == comp and a["layer"] == layer
                                               and a["disposition"] == d)
                                        for d in ("retained", "excluded", "unresolved")}
                                for layer in ("rna", "met")}
                         for comp in ("tumour", "normal")}
        h = historical.get(project)
        c["historical_matrix"] = ({"union": len(h["rna"] | h["met"]), "paired": len(h["rna"] & h["met"])}
                                  if h else None)
        c["passes_screen"] = c["post_qc"]["union"] >= MIN_TOTAL and c["post_qc"]["paired"] >= MIN_PAIRED
        c["in_panel"] = project in PANEL
        c["group"] = GROUP_OF.get(project)
        if project in EXCLUDED:
            c["excluded_from_study"] = True
        project_counts[project] = c

    group_counts = {}
    for g, ps in GROUPS.items():
        recs = [r for p in ps for r in by_project[p]]
        gc = counts(recs)
        gc["projects"] = ps
        gc["passes_screen"] = gc["post_qc"]["union"] >= MIN_TOTAL and gc["post_qc"]["paired"] >= MIN_PAIRED
        group_counts[g] = gc
    failing_groups = [g for g, c in group_counts.items() if not c["passes_screen"]]
    passing_outside = [p for p, c in project_counts.items() if c["passes_screen"] and p not in PANEL and p not in EXCLUDED]
    if failing_groups or passing_outside:
        sys.exit(f"Groups do not match the screen: failing {failing_groups}, passing outside {passing_outside}")

    panel = [r for r in patients if r["project"] in PANEL]
    totals = counts(panel)
    meta = {
        "date": date, "rule": {"min_total": MIN_TOTAL, "min_paired": MIN_PAIRED},
        "representation": "Current GDC file metadata (RNA-seq gene expression quantification; "
                          "Illumina 450k methylation beta values), joined to PanCanAtlas quality annotations",
        "historical_representation": "PanCanAtlas final harmonized RNA and 450k-only matrices, header-level membership",
        "historical_unmatched_primary_columns": held_historical,
        "panel": PANEL, "groups": GROUPS, "excluded_projects": EXCLUDED,
    }

    def write(name, obj):
        with open(OUT / name, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":") if name != "tcga_counts.json" else None,
                      indent=None if name != "tcga_counts.json" else 1)
            f.write("\n")

    write("tcga_counts.json", {"meta": meta, "panel_totals": totals, "groups": group_counts, "projects": project_counts})

    # Patient table for the panel projects and the excluded, audited ones, as compact rows.
    cols = ["patient", "project", "case_id", "tumour_rna", "tumour_met", "normal_rna", "normal_met",
            "normal_rna_he", "normal_rna_he_met"]
    audited = [r for r in patients if r["project"] in AUDITED]
    rows = [[r[c] for c in cols] for r in sorted(audited, key=lambda r: (r["project"], r["patient"]))]
    write("tcga_patients.json", {"meta": meta, "columns": cols, "rows": rows})

    # Excluded and unresolved aliquots in audited projects, with retained layers for context.
    retained_layers = defaultdict(set)
    for a in aliquots:
        if a["disposition"] == "retained":
            retained_layers[(a["patient"], a["compartment"])].add(a["layer"])
    fcols = ["aliquot", "patient", "sample", "project", "compartment", "layer", "disposition",
             "do_not_use", "awg_pathology", "pathology_reason", "patient_annotation", "sample_annotation",
             "aliquot_annotation", "reviewed_by_epc", "retained_layers_same_compartment"]
    flagged = []
    for a in sorted(aliquots, key=lambda a: (a["project"], a["aliquot"])):
        if a["project"] not in AUDITED or a["disposition"] == "retained":
            continue
        a = dict(a, retained_layers_same_compartment=sorted(retained_layers[(a["patient"], a["compartment"])]))
        flagged.append([a.get(c) for c in fcols])
    write("tcga_flags.json", {"meta": meta, "columns": fcols, "rows": flagged})

    print(f"audited patient rows {len(rows)}; panel patients {len(panel)}; tumour union {totals['post_qc']['union']}, paired {totals['post_qc']['paired']}; "
          f"normal RNA+H&E {totals['normal']['rna_he']}, with 450k {totals['normal']['rna_he_met']}; "
          f"flagged aliquots {len(flagged)}")


if __name__ == "__main__":
    main()
