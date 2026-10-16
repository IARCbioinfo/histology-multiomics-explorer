#!/usr/bin/env python3
"""Import the TCGA patient review: treatment and diagnosis screen, histology panel revision and analysis cohorts.

Usage: python3 scripts/import_patient_review.py <review-dir>

Reads from <review-dir>:
  tcga_panel_public_review.json      one structured record per audited patient with any retained layer,
                                     including the excluded TCGA-SARC project
  tcga_panel_cohort_counts.json      counts and exact selected patient lists for each analysis cohort
  histology_and_molecular_strata.json  eligible patients by reviewed histology or molecular group
  panel_revision_validation.json     the review's own coverage, totals, lists and normal-reference counts

Writes:
  data/tcga_patient_review.json  per-patient overlay: reason codes, decisions and structured annotations
                                 (no free text, notes or reports)
  data/tcga_eligibility.json     counts per project, per analysis cohort and for the panel, recomputed
                                 here from data/tcga_patients.json plus the overlay

The script stops if any recomputed count, membership list, stratum or normal-reference figure differs
from the review, or if the ESCC/PDAC selections differ from data/tcga_reviews.json. Assay dispositions in
data/tcga_patients.json and data/tcga_flags.json are read, never changed.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
LABELS = {"CRC": "Colorectal adenocarcinoma (COAD + READ)", "ESCC": "Confirmed oesophageal squamous cell carcinoma",
          "PDAC": "Confirmed pancreatic ductal adenocarcinoma", "CSCC": "Cervical squamous cell carcinoma",
          "GLIOMA": "Diffuse glioma classification benchmark (LGG + GBM)"}
ROLE = {"molecular_archetype_discovery": "discovery", "pooled_diffuse_glioma_classification_benchmark": "classification-benchmark",
        "excluded_from_study": "excluded"}
# Projects whose histology was assigned from publication tables in the panel revision.
REVISED = {"CESC", "UCEC", "PCPG", "LGG", "GBM", "SARC"}
# Single-project cohorts named after their histology rather than the project.
HISTOLOGY_COHORT = {"ESCA": "ESCC", "PAAD": "PDAC", "CESC": "CSCC"}
# Cohorts for which reported anatomical site is an analysis annotation.
SITE_COHORTS = {"CRC", "PCPG"}
# Structured annotations summarised per cohort over its selected patients.
ANNOTATIONS = {
    "CSCC": ["histology_evidence", "hpv_status_publication", "endometrial_like_publication"],
    "UCEC": ["histology_stratum", "histology_evidence", "grade_publication", "published_subtype"],
    "PCPG": ["histology_stratum", "histology_evidence", "site_reported", "published_subtype", "adrenal_cortical_admixture"],
    "GLIOMA": ["molecular_group", "idh_status", "codeletion_1p19q", "histology_publication", "grade_publication", "published_subtype"],
}
STRATA_PROJECTS = {"CSCC": ["CESC"], "UCEC": ["UCEC"], "PCPG": ["PCPG"], "GLIOMA": ["LGG", "GBM"]}


def layers(rows):
    rna = sum(r["tumour_rna"] == "retained" for r in rows)
    met = sum(r["tumour_met"] == "retained" for r in rows)
    both = sum(r["tumour_rna"] == "retained" and r["tumour_met"] == "retained" for r in rows)
    return {"total": len(rows), "rna": rna, "met": met, "paired": both, "rna_only": rna - both, "met_only": met - both}


def as_packet(lay):
    return {"patients": lay["total"], "rna": lay["rna"], "450k": lay["met"], "paired": lay["paired"],
            "rna_only": lay["rna_only"], "450k_only": lay["met_only"]}


def admixture(v):
    return None if v is None else {"1.000000": True, "0.000000": False}[v]


def stop(msg):
    sys.exit(f"import stopped: {msg}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    review = json.load(open(src / "tcga_panel_public_review.json", encoding="utf-8"))
    cohort_counts = json.load(open(src / "tcga_panel_cohort_counts.json", encoding="utf-8"))
    strata_ref = json.load(open(src / "histology_and_molecular_strata.json", encoding="utf-8"))
    v = json.load(open(src / "panel_revision_validation.json", encoding="utf-8"))

    tp = json.load(open(DATA / "tcga_patients.json", encoding="utf-8"))
    states = {r[0]: dict(zip(tp["columns"], r)) for r in tp["rows"]}
    tc = json.load(open(DATA / "tcga_counts.json", encoding="utf-8"))
    groups, excluded_projects = tc["meta"]["groups"], tc["meta"]["excluded_projects"]
    hist = json.load(open(DATA / "tcga_reviews.json", encoding="utf-8"))
    hrows = [dict(zip(hist["histology_columns"], r)) for r in hist["histology"]]

    # Coverage and agreement with the site's own assay table.
    by = {r["patient"]: r for r in review}
    if len(by) != len(review) or len({r["case_id"] for r in review}) != len(review):
        stop("duplicate patient or case identifiers")
    any_retained = {p for p, s in states.items()
                    if "retained" in (s["tumour_rna"], s["tumour_met"], s["normal_rna"], s["normal_met"])}
    if set(by) != any_retained:
        stop(f"review covers {len(by)} patients; the site has {len(any_retained)} with a retained layer")
    for p, r in by.items():
        s = states[p]
        if any(r[k] != s[k] for k in ("project", "case_id", "tumour_rna", "tumour_met", "normal_rna", "normal_met",
                                       "normal_rna_he", "normal_rna_he_met")):
            stop(f"{p}: identifiers or assay states differ from the assay table")
        if r["has_retained_tumour"] != ("retained" in (s["tumour_rna"], s["tumour_met"])):
            stop(f"{p}: retained-tumour flag differs from the assay table")
        if r["analysis_group"] != r["selected_histology_cohort"]:
            stop(f"{p}: analysis group and selected cohort differ")
        if (r["analysis_role"] == "excluded_from_study") != (r["project"] in excluded_projects):
            stop(f"{p}: study-role exclusion does not match the excluded projects")
    for c in ("ESCC", "PDAC"):
        members = {h["patient"] for h in hrows if h["analysis_cohort"] == c}
        sel = {p for p, r in by.items() if r["selected_histology_cohort"] == c and r["selected_analysis_eligible"]}
        if sel != members:
            stop(f"{c}: review selection differs from the histology review membership")

    cols = ["patient", "project", "case_id", "analysis_group", "analysis_role", "panel_exclusion_reason", "has_retained_tumour",
            "primary_diagnosis", "morphology", "prior_treatment_field", "treatment_exclusion_reasons", "treatment_hold_reasons",
            "diagnosis_reasons", "covariates", "patient_screen_pass", "tumour_eligible", "selected_cohort", "selected_eligible",
            "normal_donor_eligible", "normal_in_active_scope", "normal_catalogue_eligible", "normal_donor_context",
            "main_disposition", "site_reported", "resection_site_reported", "site_override",
            "histology_stratum", "histology_evidence", "histology_publication", "histology_publication_member",
            "historical_histology_gdc", "histology_label_conflict", "grade_publication", "historical_grade_gdc",
            "molecular_group", "published_subtype", "idh_status", "codeletion_1p19q", "hpv_status_publication",
            "endometrial_like_publication", "adrenal_cortical_admixture", "head_neck_sensitivity_flag",
            "benchmark_subsets", "who_diagnosis_status"]

    def record(r):
        rev = r["project"] in REVISED
        site = r["analysis_group"] in SITE_COHORTS
        return {
            "patient": r["patient"], "project": r["project"], "case_id": r["case_id"], "analysis_group": r["analysis_group"],
            "analysis_role": ROLE[r["analysis_role"]], "panel_exclusion_reason": r["panel_exclusion_reason"],
            "has_retained_tumour": r["has_retained_tumour"], "primary_diagnosis": r["primary_diagnosis"],
            "morphology": r["morphology"], "prior_treatment_field": r["primary_diagnosis_prior_treatment"],
            "treatment_exclusion_reasons": r["treatment_exclusion_reasons"], "treatment_hold_reasons": r["treatment_hold_reasons"],
            "diagnosis_reasons": r["diagnosis_exclusion_or_hold_reasons"], "covariates": r["covariates"],
            "patient_screen_pass": r["patient_screen_pass"], "tumour_eligible": r["tumour_annotation_eligible"],
            "selected_cohort": r["selected_histology_cohort"], "selected_eligible": r["selected_analysis_eligible"],
            "normal_donor_eligible": r["normal_reference_eligible"], "normal_in_active_scope": r["normal_in_active_project_scope"],
            "normal_catalogue_eligible": r["normal_reference_catalogue_eligible"],
            "normal_donor_context": r["normal_donor_diagnosis_context"], "main_disposition": r["main_disposition"],
            "site_reported": r["anatomic_site_reported"] if site else None,
            "resection_site_reported": r["resection_site_reported"] if site else None,
            "site_override": r["anatomic_site_annotation_override"],
            "histology_stratum": r["histology_stratum"] if rev else None,
            "histology_evidence": r["histology_evidence"] if rev else None,
            "histology_publication": r["histology_publication"] if rev else None,
            "histology_publication_member": r["histology_publication_member"] if rev else None,
            "historical_histology_gdc": r["historical_histology_gdc"] if rev else None,
            "histology_label_conflict": r["histology_label_conflict"],
            "grade_publication": r["grade_publication"], "historical_grade_gdc": r["historical_grade_gdc"] if rev else None,
            "molecular_group": r["molecular_diagnostic_group"], "published_subtype": r["published_molecular_subtype"] if rev else None,
            "idh_status": r["IDH_status"], "codeletion_1p19q": r["codeletion_1p19q_status"],
            "hpv_status_publication": r["HPV_status_publication"], "endometrial_like_publication": r["endometrial_like_publication"],
            "adrenal_cortical_admixture": admixture(r["adrenal_cortical_admixture_publication"]),
            "head_neck_sensitivity_flag": r["head_neck_sensitivity_flag"], "benchmark_subsets": r["benchmark_subsets"],
            "who_diagnosis_status": r["who_diagnosis_status"],
        }

    rec = {p: record(r) for p, r in by.items()}
    if any(r["who_integrated_diagnosis"] is not None for r in review):
        stop("an integrated WHO diagnosis is present; the site does not expect any")
    rows = [[rec[p][c] for c in cols] for p in sorted(rec, key=lambda p: (rec[p]["project"], p))]

    active = lambda p: by[p]["project"] not in excluded_projects
    tumour = lambda pts: [p for p in pts if by[p]["has_retained_tumour"]]

    def normal_block(pts, cohort=None):
        # Packages after the patient screen. A package counts towards active totals only when its project is
        # in the study panel; for the excluded project the block is kept for provenance with in_active_scope false.
        n_before = [p for p in pts if states[p]["normal_rna_he"]]
        n_after = [p for p in n_before if by[p]["normal_reference_eligible"]]
        n_after_met = [p for p in n_after if states[p]["normal_rna_he_met"]]
        scope = {by[p]["normal_reference_catalogue_eligible"] for p in n_after}
        if len(scope) > 1 or any(by[p]["normal_in_active_project_scope"] != by[p]["normal_reference_catalogue_eligible"] for p in n_after):
            stop("normal packages with mixed or inconsistent active scope")
        out = {"rna_he_before": len(n_before), "rna_he_after": len(n_after), "rna_he_met_after": len(n_after_met),
               "in_active_scope": scope != {False},
               "withheld": sorted(set(n_before) - set(n_after)),
               "context": dict(Counter(by[p]["normal_donor_diagnosis_context"] for p in n_after)),
               "context_met": dict(Counter(by[p]["normal_donor_diagnosis_context"] for p in n_after_met))}
        if cohort:
            out["outside_cohort"] = sorted(p for p in n_after if by[p]["analysis_group"] != cohort)
            if any(by[p]["project"] in REVISED for p in out["outside_cohort"]):
                out["outside_cohort_histology"] = {p: by[p]["histology_stratum"] for p in out["outside_cohort"]}
        return out

    # Per audited project.
    cohort_of = {}
    for g, ps in groups.items():
        for p in ps:
            cohort_of[p] = HISTOLOGY_COHORT.get(p, g)
    projects = {}
    for project in sorted({r["project"] for r in review}):
        pts = [p for p, r in by.items() if r["project"] == project]
        tum = tumour(pts)
        after = [p for p in tum if by[p]["tumour_annotation_eligible"]]
        sel = [p for p in tum if by[p]["selected_analysis_eligible"]]
        cohort = cohort_of.get(project)
        roles = {by[p]["analysis_role"] for p in pts}
        if len(roles) != 1:
            stop(f"{project}: more than one study role")
        projects[project] = {
            "analysis_cohort": cohort, "role": ROLE[roles.pop()], "reviewed_patients": len(pts),
            "histology_reviewed": project in REVISED or project in ("ESCA", "PAAD"),
            "assay_qc": layers([states[p] for p in tum]), "after_patient_screen": layers([states[p] for p in after]),
            "selected_analysis": layers([states[p] for p in sel]),
            "dispositions": dict(Counter(by[p]["main_disposition"] for p in tum)),
            "normal": normal_block(pts, cohort),
            "label_conflicts": [{"patient": p, "gdc": by[p]["historical_histology_gdc"], "publication": by[p]["histology_publication"],
                                 "stratum": by[p]["histology_stratum"], "selected": by[p]["selected_analysis_eligible"]}
                                for p in sorted(pts) if by[p]["histology_label_conflict"]],
        }
        if project in excluded_projects:
            projects[project]["excluded_from_study"] = True
            projects[project]["exclusion_reason"] = sorted({by[p]["panel_exclusion_reason"] for p in pts})[0]
            if projects[project]["selected_analysis"]["total"]:
                stop(f"{project}: excluded project has selected patients")
        elif cohort is None:
            stop(f"{project}: active project without an analysis cohort")

    # Per analysis cohort: tumour members are selected patients; normal packages follow the donor's analysis group.
    reviews_pdac_flag = {h["patient"] for h in hrows if h["focal_squamous_flag"]}
    cohorts = {}
    for c, rc in sorted(cohort_counts.items()):
        members = sorted(p for p, r in by.items() if r["selected_analysis_eligible"] and r["selected_histology_cohort"] == c)
        if members != sorted(rc["patients_list"]):
            stop(f"{c}: recomputed membership differs from the review's patient list")
        sel = layers([states[p] for p in members])
        if as_packet(sel) != {k: rc[k] for k in ("patients", "rna", "450k", "paired", "rna_only", "450k_only")}:
            stop(f"{c}: recomputed counts {sel} differ from the review")
        projs = [p for ps in groups.values() for p in ps if projects[p]["analysis_cohort"] == c]  # screen-group order
        roles = {by[p]["analysis_role"] for p in members}
        if len(roles) != 1:
            stop(f"{c}: members with different study roles")
        donors = [p for p, r in by.items() if r["analysis_group"] == c]
        entry = {"label": LABELS.get(c, c), "role": ROLE[roles.pop()], "projects": projs, "selected_analysis": sel,
                 "contributions": {p: layers([states[q] for q in members if by[q]["project"] == p]) for p in projs},
                 "normal": normal_block(donors)}
        # Subsets: sensitivity analyses and benchmark subsets, counted within the cohort, never added to totals.
        subsets = []
        def subset(sid, label, pts):
            subsets.append({"id": sid, "label": label, **layers([states[p] for p in pts]), "patients": sorted(pts)})
        if c == "PDAC":
            subset("PDAC-sensitivity", "Without the focal squamous component case", [p for p in members if p not in reviews_pdac_flag])
        if c == "UCEC":
            subset("UCEC-endometrioid", "Endometrioid only", [p for p in members if by[p]["histology_stratum"] == "Endometrioid"])
        if c == "PCPG":
            subset("PCPG-without-neck", "Without the two head and neck paragangliomas", [p for p in members if by[p]["head_neck_sensitivity_flag"] is False])
        if c == "GLIOMA":
            subset("GLIOMA-LGG-only", "TCGA-LGG patients only", [p for p in members if "LGG_only" in (by[p]["benchmark_subsets"] or [])])
            subset("GLIOMA-paired-only", "Patients with both RNA-seq and 450k", [p for p in members if states[p]["tumour_rna"] == states[p]["tumour_met"] == "retained"])
        if subsets:
            entry["subsets"] = subsets
        # Reviewed histology or molecular strata among patients passing the patient screen, by project.
        if c in STRATA_PROJECTS:
            strata = defaultdict(list)
            for p, r in by.items():
                if r["project"] in STRATA_PROJECTS[c] and r["has_retained_tumour"] and r["tumour_annotation_eligible"]:
                    strata[(r["histology_stratum"], r["project"])].append(p)
            entry["strata"] = [{"stratum": s, "project": proj, **layers([states[p] for p in pts]),
                                "publication_members": sum(bool(by[p]["histology_publication_member"]) for p in pts),
                                "selected": sum(by[p]["selected_analysis_eligible"] for p in pts)}
                               for (s, proj), pts in sorted(strata.items(), key=lambda kv: (projs.index(kv[0][1]), -len(kv[1])))]
            for (s, proj), pts in strata.items():
                ref = strata_ref["CESC" if proj == "CESC" else proj][s]
                lay = layers([states[p] for p in pts])
                pub = sum(bool(by[p]["histology_publication_member"]) for p in pts)
                if sorted(pts) != sorted(ref["patients_list"]) or (lay["total"], lay["paired"], pub) != (ref["patients"], ref["paired"], ref["publication_members"]):
                    stop(f"{c} stratum {proj}/{s}: differs from the review's strata table")
            if sum(len(x["patients_list"]) for proj in STRATA_PROJECTS[c] for x in strata_ref[proj].values()) != sum(len(x) for x in strata.values()):
                stop(f"{c}: strata coverage differs from the review")
        if c in ANNOTATIONS:
            ann = {}
            for f in ANNOTATIONS[c]:
                vals = defaultdict(list)
                for p in members:
                    vals[json.dumps(rec[p][f])].append(p)
                ann[f] = [[json.loads(k), len(pts), layers([states[p] for p in pts])["paired"]]
                          for k, pts in sorted(vals.items(), key=lambda kv: -len(kv[1]))]
            entry["annotations"] = ann
        if c in SITE_COHORTS and len(projs) > 1:
            site = defaultdict(Counter)
            for q in members:
                site[by[q]["anatomic_site_reported"] or "Not reported"][by[q]["project"]] += 1
            entry["reported_sites"] = {k: dict(x) for k, x in sorted(site.items(), key=lambda kv: -sum(kv[1].values()))}
            entry["site_overrides"] = [
                {"patient": q, "project": by[q]["project"], "site_reported": by[q]["anatomic_site_reported"],
                 "resection_site_reported": by[q]["resection_site_reported"], "override": by[q]["anatomic_site_annotation_override"],
                 "selected": by[q]["selected_analysis_eligible"],
                 "layers": "both" if states[q]["tumour_rna"] == "retained" and states[q]["tumour_met"] == "retained"
                           else ("rna-only" if states[q]["tumour_rna"] == "retained" else "met-only")}
                for q in sorted(donors) if by[q]["anatomic_site_annotation_override"]]
        if len(projs) > 1:
            entry["withheld"] = [{"patient": q, "project": by[q]["project"], "disposition": by[q]["main_disposition"]}
                                 for q in sorted(donors) if by[q]["has_retained_tumour"] and not by[q]["selected_analysis_eligible"]]
        cohorts[c] = entry

    # Panel: active projects only; the excluded project is reported separately.
    tum_all = [p for p in tumour(by) if active(p)]
    after_all = [p for p in tum_all if by[p]["tumour_annotation_eligible"]]
    sel_all = [p for p in tum_all if by[p]["selected_analysis_eligible"]]
    disc = [p for p in sel_all if by[p]["analysis_role"] == "molecular_archetype_discovery"]
    bench = [p for p in sel_all if by[p]["analysis_role"] == "pooled_diffuse_glioma_classification_benchmark"]
    disp = Counter(by[p]["main_disposition"] for p in tum_all)
    dims = {"treatment_exclusion": sum(bool(by[p]["treatment_exclusion_reasons"]) for p in tum_all),
            "treatment_hold": sum(bool(by[p]["treatment_hold_reasons"]) for p in tum_all),
            "diagnosis_identity_episode": sum(bool(by[p]["diagnosis_exclusion_or_hold_reasons"]) for p in tum_all)}
    normal_all = normal_block([p for p in by if active(p)])
    panel = {"assay_qc": layers([states[p] for p in tum_all]), "after_patient_screen": layers([states[p] for p in after_all]),
             "selected_analysis": layers([states[p] for p in sel_all]), "discovery": layers([states[p] for p in disc]),
             "benchmark": layers([states[p] for p in bench]), "dispositions": dict(disp), "reason_dimensions": dims,
             "normal": normal_all}

    gbm = projects["GBM"]
    checks = [
        ("reviewed patients", len(by), v["retained_cases_reviewed_including_SARC"]),
        ("audited projects", len(projects), v["audited_projects_including_excluded_SARC"]),
        ("active projects", sum(1 for x in projects.values() if not x.get("excluded_from_study")), v["active_contributing_projects"]),
        ("analysis cohorts", len(cohorts), v["selected_analysis_cohorts"]),
        ("GBM assay QC", {k: as_packet(gbm["assay_qc"])[k] for k in ("patients", "rna", "450k", "paired")}, v["GBM_assay_qc"]),
        ("GBM after screen", {**as_packet(gbm["after_patient_screen"]), "patients_list": sorted(p for p in tumour(by) if by[p]["project"] == "GBM" and by[p]["tumour_annotation_eligible"])},
         {**v["GBM_after_patient_screen"], "patients_list": sorted(v["GBM_after_patient_screen"]["patients_list"])}),
        ("GBM dispositions", gbm["dispositions"], v["GBM_patient_dispositions"]),
        ("selected panel", {**as_packet(panel["selected_analysis"]), "patients_list": sorted(sel_all)},
         {**v["selected_panel"], "patients_list": sorted(v["selected_panel"]["patients_list"])}),
        ("discovery panel", {**as_packet(panel["discovery"]), "patients_list": sorted(disc)},
         {**v["discovery_panel_excluding_glioma_benchmark"], "patients_list": sorted(v["discovery_panel_excluding_glioma_benchmark"]["patients_list"])}),
        ("benchmark", as_packet(panel["benchmark"]), {k: cohort_counts["GLIOMA"][k] for k in ("patients", "rna", "450k", "paired", "rna_only", "450k_only")}),
        ("active normal", (normal_all["rna_he_after"], normal_all["rna_he_met_after"]),
         (v["normal_rna_he_active_projects"], v["normal_rna_he_450_active_projects"])),
        ("normal contexts", normal_all["context"], v["normal_donor_context"]),
    ]
    for name, got, exp in checks:
        if got != exp:
            stop(f"{name}: recomputed {str(got)[:200]} differs from the review {str(exp)[:200]}")

    meta = {"date": v["date"], "reviewed_patients": len(by), "audited_projects": len(projects),
            "projects": sum(1 for x in projects.values() if not x.get("excluded_from_study")),
            "analysis_cohorts": len(cohorts), "discovery_cohorts": sum(x["role"] == "discovery" for x in cohorts.values()),
            "benchmark_cohorts": sum(x["role"] == "classification-benchmark" for x in cohorts.values()),
            "excluded_projects": {p: projects[p]["exclusion_reason"] for p in excluded_projects},
            "treated_reference": False, "integrated_who_diagnosis_adjudicated": False}
    with open(DATA / "tcga_patient_review.json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "columns": cols, "rows": rows}, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    with open(DATA / "tcga_eligibility.json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "projects": projects, "cohorts": cohorts, "panel": panel}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    s, d, b = panel["selected_analysis"], panel["discovery"], panel["benchmark"]
    print(f"patients {len(by)}; {len(cohorts)} cohorts ({meta['discovery_cohorts']} discovery, {meta['benchmark_cohorts']} benchmark) "
          f"from {meta['projects']} active projects ({len(projects)} audited); assay QC {panel['assay_qc']['total']}; "
          f"after screen {panel['after_patient_screen']['total']}; selected {s['total']}/{s['paired']} ({s['rna_only']} RNA only, "
          f"{s['met_only']} 450k only); discovery {d['total']}/{d['paired']}; benchmark {b['total']}/{b['paired']}; "
          f"dispositions {dict(disp)}; dimensions {dims}; normal {normal_all['rna_he_after']}/{normal_all['rna_he_met_after']}")


if __name__ == "__main__":
    main()
