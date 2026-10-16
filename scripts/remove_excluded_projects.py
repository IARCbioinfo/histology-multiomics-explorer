#!/usr/bin/env python3
"""Remove projects excluded from the study from the public patient-level files.

Usage: python3 scripts/remove_excluded_projects.py

Run after scripts/build_tcga.py, scripts/import_tcga_review.py and scripts/import_patient_review.py, which keep
the excluded projects (currently TCGA-SARC) for their own validation against the source reviews. The explorer
presents only the panel projects, so this script drops the excluded projects' rows from tcga_patients.json,
tcga_flags.json and tcga_patient_review.json, their rows from the scope review in tcga_reviews.json and their
entries from tcga_eligibility.json, and updates the patient counts in the metadata. Project-level availability in
tcga_counts.json is kept, so every TCGA project's coverage, and the reason a project is outside the panel, stay
visible. Running it again changes nothing; scripts/check.py fails if an excluded project reappears.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj, compact):
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(obj, ensure_ascii=False, indent=1)
    (DATA / name).write_text(text + "\n", encoding="utf-8")


def main():
    excluded = set(load("tcga_counts.json")["meta"].get("excluded_projects", {}))
    removed = {}
    for name in ("tcga_patients.json", "tcga_flags.json", "tcga_patient_review.json"):
        d = load(name)
        i = d["columns"].index("project")
        before = len(d["rows"])
        d["rows"] = [r for r in d["rows"] if r[i] not in excluded]
        d["meta"].pop("excluded_projects", None)
        if name == "tcga_patient_review.json":
            d["meta"]["reviewed_patients"] = len(d["rows"])
            d["meta"]["audited_projects"] = len({r[i] for r in d["rows"]})
        removed[name] = before - len(d["rows"])
        save(name, d, compact=True)

    rv = load("tcga_reviews.json")
    i = rv["scope_columns"].index("project")
    n = rv["scope_columns"].index("reviewed_aliquots")
    before = len(rv["scope"])
    rv["scope"] = [r for r in rv["scope"] if r[i] not in excluded]
    rv["meta"]["reviewed_patients"] = len(rv["scope"])
    rv["meta"]["reviewed_aliquots"] = sum(r[n] for r in rv["scope"])
    removed["tcga_reviews.json (scope review)"] = before - len(rv["scope"])
    save("tcga_reviews.json", rv, compact=True)

    el = load("tcga_eligibility.json")
    review = load("tcga_patient_review.json")["meta"]
    removed["tcga_eligibility.json (projects)"] = sum(p in el["projects"] for p in excluded)
    el["projects"] = {p: v for p, v in el["projects"].items() if p not in excluded}
    el["meta"].pop("excluded_projects", None)
    el["meta"]["reviewed_patients"] = review["reviewed_patients"]
    el["meta"]["audited_projects"] = len(el["projects"])
    save("tcga_eligibility.json", el, compact=False)
    print(f"excluded projects {sorted(excluded)} removed from patient-level files: {removed}")


if __name__ == "__main__":
    main()
