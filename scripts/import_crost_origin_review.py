#!/usr/bin/env python3
"""Apply the originating-repository qualification of the CROST candidates of release 0.11.4 (21 November 2026).

Usage: python3 scripts/import_crost_origin_review.py <review-dir>

Reads from <review-dir>:
  crost_origin_delta.json     resource_updates (guarded field changes), origin_review blocks and new_section_records
  baseline_fingerprints.json  SHA-256 of the protected data of release 0.11.4
  checksums.json              SHA-256 of the two files above

Only the 69 resources with IDs starting cand-crost- may change. Every resource update names the exact old value: the
field must hold its old value (the change is applied) or its new value (already applied); anything else stops the import.
The origin_review block of each of the 69 resources is written by this script. New section records carry the review
batch below and are rebuilt on every run, so running the script again changes nothing; section records of other batches,
every other cohort object and all TCGA files must keep their release 0.11.4 content. Records keep null patient IDs unless
the source establishes the donor, scanner pixel sizes stay null, no record enters the core tier, and eligibility stays
unknown.
"""
import hashlib
import json
import sys
from pathlib import Path

from vocab import ENUMS

DATA = Path(__file__).resolve().parent.parent / "data"
DATE = "2026-11-21"
BATCH = "crost-origin-2026-11-21"
INPUTS = ("crost_origin_delta.json", "baseline_fingerprints.json")
PROTECTED = ("tcga_counts.json", "tcga_patients.json", "tcga_flags.json", "tcga_reviews.json", "tcga_patient_review.json",
             "tcga_eligibility.json", "tcga_resources.json", "cancers.json", "evidence.json", "leads.json")
FIELDS = {"status", "verification", "verified_on", "linkage", "gates", "preservation", "access", "accession", "description", "notes", "citation",
          "cancers", "compartments", "reported"}
REVIEW_KEYS = {"date", "outcome", "depth", "states", "image_finding", "molecular_finding", "next_step", "sections_checked",
               "sections_listed", "study_local_donors"}


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def stop(msg):
    sys.exit(f"import_crost_origin_review: {msg}")


def main(src):
    src = Path(src)
    sums = json.loads((src / "checksums.json").read_text())
    for name in INPUTS:
        if hashlib.sha256((src / name).read_bytes()).hexdigest() != sums.get(name):
            stop(f"{name} does not match checksums.json")
    delta = json.loads((src / "crost_origin_delta.json").read_text())
    base = json.loads((src / "baseline_fingerprints.json").read_text())
    cohorts = json.loads((DATA / "cohorts.json").read_text())
    captures = json.loads((DATA / "captures.json").read_text())

    for name in PROTECTED:
        if sha(json.loads((DATA / name).read_text())) != base["protected"][name]:
            stop(f"{name} differs from release 0.11.4")
    old_cohorts = [c for c in cohorts if not c["id"].startswith("cand-crost-")]
    if sha(old_cohorts) != base["cohorts_other"]:
        stop("cohort objects outside the CROST candidates differ from release 0.11.4")
    old_caps = [x for x in captures if x.get("review_batch") != BATCH]
    if sha(old_caps) != base["captures_existing"] or len(old_caps) != 767:
        stop("the 767 section records of release 0.11.4 differ")

    by_id = {c["id"]: c for c in cohorts}
    crost = {k for k in by_id if k.startswith("cand-crost-")}
    if len(crost) != 69 or set(delta["origin_review"]) != crost:
        stop("the origin review must cover exactly the 69 CROST candidates")

    changes = 0
    for rid, upd in delta["resource_updates"].items():
        if rid not in crost:
            stop(f"{rid} is not a CROST candidate")
        c = by_id[rid]
        for field, (old, new) in upd.items():
            if field not in FIELDS:
                stop(f"{rid}: field {field} may not be changed by this import")
            cur = c.get(field)
            if cur == new:
                continue
            if cur != old:
                stop(f"{rid}.{field}: holds neither the expected old nor the new value")
            c[field] = new
            changes += 1
    for rid, rv in delta["origin_review"].items():
        if set(rv) - REVIEW_KEYS or rv["date"] != DATE or rv["outcome"] not in ENUMS["backlog_outcome"] \
                or any(s not in ENUMS["route_state"] for s in rv["states"]):
            stop(f"{rid}: invalid origin review")
        by_id[rid]["origin_review"] = rv

    new = delta["new_section_records"]
    for x in new:
        if x.get("review_batch") != BATCH or x["cohort"] not in crost or x["tier"] == "core" or x["stratum"] is not None \
                or x["he_mpp"] is not None or (x["patient"] is not None) != (x["donor_mapping"] != "unresolved"):
            stop(f"section record {x.get('id')}: outside the allowed values")
        if by_id[x["cohort"]]["specimen"] == "clinical-reference" and x["compartment"] not in ("normal", "solid-normal"):
            stop(f"section record {x['id']}: a non-tumour reference keeps a normal or adjacent-normal compartment")
    captures = old_caps + new

    (DATA / "cohorts.json").write_text(json.dumps(cohorts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "captures.json").write_text(json.dumps(captures, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{changes} field changes, {len(delta['origin_review'])} origin reviews, {len(new)} section records in batch {BATCH}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
