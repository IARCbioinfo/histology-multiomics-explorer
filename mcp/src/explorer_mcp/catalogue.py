"""Read-only queries over the Tumour Histology and Multi-omics Explorer metadata.

Standard library only, so scripts/check.py can verify the answers without the MCP SDK.
Each public method of Catalogue listed in TOOLS is exposed as one MCP tool by server.py.
"""
import hashlib
import json
import os
import urllib.request
from pathlib import Path

# Published site URL, ending with "/": the default source when the server does not run from a checkout.
DEFAULT_SITE_URL = "https://iarcbioinfo.github.io/histology-multiomics-explorer/"

INSTRUCTIONS = (
    "Read-only access to the Tumour Histology and Multi-omics Explorer: curated public metadata for TCGA patients "
    "with RNA-seq and 450k methylation (a dated selected analysis panel and broader availability) and published spatial "
    "omics studies with matched H&E, at two image levels (original H&E located, or matched data with a preview image only). "
    "Start with catalogue_overview. Keep the selected panel and broader availability apart, "
    "never add counts across studies or units, and remember that spatial studies involve patients other than those in TCGA. "
    "The underlying data stay at their original repositories; listing a dataset does not mean access has been granted."
)

TOOLS = [  # (method, description shown to agents)
    ("catalogue_overview", "Release, the points to read before using any count, headline figures and every cancer page with its TCGA and spatial summary. Call this first."),
    ("get_cancer_type", "One cancer page by code (for example BRCA, CRC, GLIOMA, PDAC): TCGA selected-panel and availability counts, normal reference, spatial resources, located tissue sections by stratum, other resources, selection evidence and gaps."),
    ("search_resources", "Search catalogued studies and resources by text, cancer code, data layer, status (for spatial studies the image level: verified = original H&E located, preview = matched data with preview image, candidate = not yet verified), access category, technique, package-review result or open dependency from the spatial reviews (public-download, download-failure, vendor-terms, account-registration, dac-approval, author-release, local-qc). Pooled codes (CRC, GLIOMA) include their constituent cancers. Returns compact records and the total."),
    ("get_resource", "Full record of one study or resource by id, with its located tissue sections counted by tier and image level, and known study-local patients."),
    ("search_spatial_sections", "Located spatial transcriptomics tissue section records (measured spatial RNA and coordinates with the original H&E or only a preview image), filtered by cancer, resource, image level (original or preview), histology stratum, primary or metastatic site, treatment before sampling, curation tier or technique. strict=true keeps core primary sections documented as untreated. Preview-level sections do not support whole-slide or tile models, morphology or distances. Returns totals (section records, known study-local patients, sections without a patient ID, resources) and compact rows; records are not globally unique physical sections or eligible patients."),
    ("get_spatial_section", "Full record of one located tissue section by id (<resource>:<section>), with links, source wording and reported clinical fields."),
    ("get_tcga_cohort", "One TCGA analysis cohort (for example BRCA, CRC, ESCC, GLIOMA, PDAC): study role, contributing projects, selected-panel counts, per-project contributions, normal reference, sensitivity or benchmark subsets, strata and annotation value counts. Without an id, lists the cohorts."),
    ("search_tcga_patients", "TCGA patients joined across assay states and the patient screen, filtered by analysis cohort, project, selection, retained tumour assays, normal reference, screen disposition, subset, histology stratum or glioma molecular group. Returns totals (patients, RNA-seq, 450k, both) and compact rows."),
    ("get_tcga_patient", "One TCGA patient by barcode (TCGA-XX-XXXX): assay states, screen decision with reason codes, analysis cohort, subsets, published annotations and every excluded or unresolved aliquot."),
    ("explain_term", "Definitions of the terms used for counts and curation (for example selected analysis panel, original H&E located, matched data with preview image, section record, strict subset) and the meaning of any vocabulary code shown in the other tools."),
]

KEY_NOTES = {
    "tcga": "Selected-panel counts and broader availability are different selections; report which one you use.",
    "spatial": ("Spatial studies involve patients other than those in TCGA. Original H&E located and matched data with preview image are separate image levels; "
                "preview-level sections do not support whole-slide or tile models, morphology or physical distances. Registration, calibration and tissue QC "
                "may be pending at either level. Patients are study-local IDs given by the source; sections without one are not counted as patients, "
                "and section records are not globally unique physical sections or eligible patients."),
    "reported": "Study-reported counts keep the study's own unit and are never added across studies; an unknown count is absent, not zero.",
    "normal": "Normal tissue comes from patients with cancer, not healthy donors.",
    "treated": "Withheld patients are not a treated reference set.",
    "glioma": "GLIOMA is a classification benchmark; integrated WHO CNS5 diagnoses are not adjudicated.",
}
RESOURCE_FIELDS = ("id", "label", "cancers", "layer", "status", "access", "techniques", "linkage", "compartments", "reported", "verification")
SECTION_FIELDS = ("id", "cohort", "cancer", "stratum", "patient", "capture", "image_level", "tier", "site", "treatment", "technique", "preservation",
                  "linkage", "registration", "he_mpp", "verification", "assay_area_id", "donor_mapping")
PATIENT_FIELDS = ("patient", "project", "analysis_cohort", "role", "selected", "tumour_assays", "normal_reference", "disposition",
                  "reasons", "subsets", "histology_stratum", "molecular_group", "published_subtype", "flagged_aliquots")


class SourceError(Exception):
    """The catalogue files cannot be found, read or verified."""


def find_checkout():
    """The repository checkout containing this package, when run from one."""
    for p in Path(__file__).resolve().parents:
        if (p / "data" / "index.json").exists():
            return p
    return None


def views(x):
    """RNA-seq, 450k, both and total patients from either count format."""
    if "rna" in x:
        return {"rna_seq": x["rna"], "methylation_450k": x["met"], "both": x["paired"], "total": x["total"]}
    return {"rna_seq": x["paired"] + x["rna_only"], "methylation_450k": x["paired"] + x["met_only"], "both": x["paired"], "total": x["union"]}


def known_patients(caps):
    """Study-local patients given by the source; records without a patient ID add none."""
    return len({(x["cohort"], x["patient"]) for x in caps if x.get("patient")})


def counted_preview(c, caps):
    """Checked preview packages counted for a resource without individual section records."""
    if c.get("status") != "preview" or any(x["cohort"] == c["id"] for x in caps):
        return 0
    return (((c.get("spatial_review") or {}).get("route_review") or {}).get("sections_with_matching_coordinates")) or 0


def page(items, limit, offset):
    limit = max(1, min(int(limit), 500))
    offset = max(0, int(offset))
    return items[offset:offset + limit], {"total": len(items), "offset": offset, "returned": len(items[offset:offset + limit])}


class Catalogue:
    def __init__(self, source=None):
        source = source or os.environ.get("EXPLORER_SOURCE") or find_checkout() or DEFAULT_SITE_URL
        if not source:
            raise SourceError("No catalogue source. Pass --source with a checkout of the Explorer repository or the published site URL.")
        source = str(source)
        self.remote = source.startswith(("http://", "https://"))
        if self.remote:
            self.base = source if source.endswith("/") else source + "/"
        else:
            p = Path(source).expanduser().resolve()
            if p.name == "data" and (p / "index.json").exists():
                p = p.parent
            if not (p / "data" / "index.json").exists():
                raise SourceError(f"{p} is not an Explorer checkout: data/index.json is missing.")
            self.base = p
        self._cache = {}
        self.index = self._json("data/index.json", verify=False)
        self.hashes = {f["path"]: f["sha256"] for f in self.index["files"]}
        self.release = self.index["release"]

    # ------------------------------------------------------------ loading

    def _json(self, rel, verify=True):
        if rel not in self._cache:
            try:
                if self.remote:
                    with urllib.request.urlopen(self.base + rel, timeout=60) as r:
                        raw = r.read()
                else:
                    raw = (self.base / rel).read_bytes()
            except OSError as e:
                raise SourceError(f"Could not read {rel}: {e}") from e
            if verify and rel in self.hashes and hashlib.sha256(raw).hexdigest() != self.hashes[rel]:
                raise SourceError(f"{rel} does not match the checksum in data/index.json; the source is inconsistent.")
            self._cache[rel] = json.loads(raw)
        return self._cache[rel]

    def _data(self, name):
        return self._json(f"data/{name}.json")

    def text(self, rel):
        """A text file of the site, such as llms.txt."""
        try:
            if self.remote:
                with urllib.request.urlopen(self.base + rel, timeout=60) as r:
                    return r.read().decode("utf-8")
            return (self.base / rel).read_text(encoding="utf-8")
        except OSError as e:
            raise SourceError(f"Could not read {rel}: {e}") from e

    def _envelope(self, result, *notes):
        out = {"release": f"{self.release['version']} ({self.release['date']})", **result}
        if notes:
            out["notes"] = [KEY_NOTES[n] for n in notes]
        return out

    @property
    def cancers(self):
        return {c["code"]: c for c in self._data("cancers")}

    @property
    def pages(self):
        return [c for c in self._data("cancers") if c["group"] not in ("aggregate",)]

    def _codes(self, code):
        c = self.cancers.get(code.upper()) if code else None
        return [c["code"], *c.get("includes", [])] if c else [code.upper()]

    def _patients(self):
        """TCGA patients joined as in the explorer's TCGA view."""
        if "patients" in self._cache:
            return self._cache["patients"]
        tp, pr, fl = self._data("tcga_patients"), self._data("tcga_patient_review"), self._data("tcga_flags")
        elig = self._data("tcga_eligibility")
        review = {r[0]: dict(zip(pr["columns"], r)) for r in pr["rows"]}
        flags = {}
        for r in fl["rows"]:
            f = dict(zip(fl["columns"], r))
            flags.setdefault(f["patient"], []).append(f)
        subsets = {}
        for c in elig["cohorts"].values():
            for s in c.get("subsets", []):
                for p in s["patients"]:
                    subsets.setdefault(p, []).append(s["id"])
        out = {}
        for r in tp["rows"]:
            x = dict(zip(tp["columns"], r))
            cl = review.get(x["patient"])
            tr, tm = x["tumour_rna"] == "retained", x["tumour_met"] == "retained"
            layers = "both" if tr and tm else "rna-only" if tr else "met-only" if tm else "none"
            normal = "rna-he-met" if x["normal_rna_he_met"] else "rna-he" if x["normal_rna_he"] else "none"
            if normal != "none" and not (cl and cl["normal_donor_eligible"]):
                normal = "withheld"
            elif normal != "none" and not cl["normal_catalogue_eligible"]:
                normal = "inactive"
            out[x["patient"]] = {
                "patient": x["patient"], "project": x["project"], "case_id": x["case_id"],
                "analysis_cohort": (cl["analysis_group"] or ("excluded" if cl["analysis_role"] == "excluded" else "outside")) if cl else "none",
                "role": cl["analysis_role"] if cl else "none",
                "selected": ("yes" if cl and cl["selected_eligible"] else "no") if layers != "none" else "na",
                "tumour_assays": layers, "tumour_rna": x["tumour_rna"], "tumour_met": x["tumour_met"],
                "normal_reference": normal, "normal_rna": x["normal_rna"], "normal_met": x["normal_met"],
                "disposition": cl["main_disposition"] if cl else "not-reviewed",
                "reasons": (cl["treatment_exclusion_reasons"] + cl["treatment_hold_reasons"] + cl["diagnosis_reasons"]) if cl else [],
                "subsets": subsets.get(x["patient"], []),
                "histology_stratum": cl.get("histology_stratum") if cl else None,
                "molecular_group": cl.get("molecular_group") if cl else None,
                "published_subtype": cl.get("published_subtype") if cl else None,
                "flagged_aliquots": len(flags.get(x["patient"], [])),
                "_review": cl, "_flags": flags.get(x["patient"], []),
            }
        self._cache["patients"] = out
        return out

    # ------------------------------------------------------------ tools

    def catalogue_overview(self) -> dict:
        """Release, key points, headline figures and every cancer page."""
        elig, cohorts, captures = self._data("tcga_eligibility"), self._data("cohorts"), self._data("captures")
        sa, m = elig["panel"]["selected_analysis"], elig["meta"]
        spatial = [c for c in cohorts if c["layer"] == "matched-spatial"]
        pages = []
        for c in self.pages:
            bc = self._json(f"data/by-cancer/{c['code']}.json")
            sp = bc["spatial_resources"]
            ac = bc["tcga"]["analysis_cohort"]
            proj = bc["tcga"]["projects"]
            sel = (ac["selected_analysis"]["total"] if c.get("tcga_projects") else
                   next((v["selected_panel"]["selected_analysis"]["total"] for v in proj.values() if v["selected_panel"] and not v["selected_panel"].get("excluded_from_study")), None))
            pages.append({"code": c["code"], "name": c["name"], "in_panel": c["group"] != "excluded",
                          "tcga_analysis_cohort": ac["id"] if ac else None, "tcga_selected_patients": sel,
                          "spatial_resources": len(sp), "spatial_with_original_he": sum(x["status"] == "verified" for x in sp),
                          "spatial_with_preview_image_only": sum(x["status"] == "preview" for x in sp)})
        layers = {}
        for c in cohorts:
            layers[c["layer"]] = layers.get(c["layer"], 0) + 1
        return self._envelope({
            "name": self.index["name"],
            "key_points": self.index["notes"],
            "tcga": {"panel_date": m["date"], "analysis_cohorts": m["analysis_cohorts"], "projects": m["projects"],
                     "selected_patients": sa["total"], "selected_with_both_assays": sa["paired"],
                     "normal_reference_rna_he": elig["panel"]["normal"]["rna_he_after"], "normal_reference_with_450k": elig["panel"]["normal"]["rna_he_met_after"]},
            "spatial": {"resources": len(spatial), "with_original_he_located": sum(c["status"] == "verified" for c in spatial),
                        "with_matched_data_and_preview_image": sum(c["status"] == "preview" for c in spatial),
                        "candidates": sum(c["status"] == "candidate" for c in spatial),
                        "section_records": len(captures), "section_records_original_he": sum(x["image_level"] == "original" for x in captures),
                        "section_records_preview_image": sum(x["image_level"] == "preview" for x in captures),
                        "preview_sections_counted_without_records": sum(counted_preview(c, captures) for c in spatial),
                        "known_study_local_patients": known_patients(captures),
                        "sections_without_patient_id": sum(not x.get("patient") for x in captures),
                        "eligible_patients": None,
                        "units": "Resources count once at their best image level. Section records are per study, not globally unique physical sections. Patients are study-local IDs given by the source; no eligible-patient total is established."},
            "resources_by_layer": layers,
            "related_leads": [{"id": x["id"], "label": x["label"], "url": x["url"], "not_counted": x["not_counted"]} for x in self._data("leads")],
            "cancer_pages": pages,
            "files": {"agent_guide": "llms.txt", "data_index": "data/index.json", "glossary": "data/glossary.json", "field_reference": "data/README.md"},
        }, "tcga", "spatial")

    def get_cancer_type(self, code: str) -> dict:
        """One cancer page by code."""
        code = code.strip().upper()
        if code not in self.cancers:
            return self._envelope({"error": f"Unknown cancer code {code}.", "codes": sorted(self.cancers)})
        bc = self._json(f"data/by-cancer/{code}.json")
        c, t = bc["cancer"], bc["tcga"]
        ac = t["analysis_cohort"]
        caps = bc["located_sections"]
        strata = dict(c.get("strata") or [])
        groups = {}
        for x in caps:
            key = x["cancer"] if c.get("includes") else (strata.get(x["stratum"], "No stratum assigned") if x["stratum"] else "No stratum assigned")
            g = groups.setdefault(key, {"sections": 0, "original": 0, "primary_sections": 0, "_p": set(), "_pp": set()})
            g["sections"] += 1
            g["original"] += x.get("image_level") == "original"
            if x["patient"]:
                g["_p"].add((x["cohort"], x["patient"]))
            if x["tier"] == "core":
                g["primary_sections"] += 1
                g["_pp"].add((x["cohort"], x["patient"]))
        by_group = [{"group": k, "sections": v["sections"], "sections_original_he": v["original"], "sections_preview_image": v["sections"] - v["original"],
                     "known_patients": len(v["_p"]), "primary_tumour_sections": v["primary_sections"],
                     "primary_tumour_patients": len(v["_pp"])} for k, v in groups.items()]
        return self._envelope({
            "code": code, "name": c["name"], "in_panel": c["group"] != "excluded", "summary": c["summary"],
            "hausser_2019_result": c["hausser"],
            "web_page": bc["page"], "markdown": bc["markdown"],
            "tcga": {
                "analysis_cohort": ac["id"] if ac else None, "role": ac["role"] if ac else None,
                "selected_panel": views(ac["selected_analysis"]) if ac else None,
                "contributions": {p: views(v) for p, v in ac.get("contributions", {}).items()} if ac else None,
                "normal_reference": {"rna_he": ac["normal"]["rna_he_after"], "with_450k": ac["normal"]["rna_he_met_after"]} if ac else None,
                "availability_by_project": {p: views(v["availability"]["post_qc"]) for p, v in t["projects"].items()},
                "panel_date": t["panel_date"], "availability_date": t["availability_date"],
            },
            "spatial_resources": [self._resource_row(x, caps) for x in bc["spatial_resources"]],
            "located_sections": {"sections": len(caps), "sections_original_he": sum(x.get("image_level") == "original" for x in caps),
                                 "sections_preview_image": sum(x.get("image_level") == "preview" for x in caps),
                                 "known_patients": known_patients(caps), "sections_without_patient_id": sum(not x["patient"] for x in caps), "by_group": by_group},
            "other_resources": [self._resource_row(x) for x in bc["other_resources"]],
            "selection_evidence": [{"study": e["short"], "citation": e["citation"], "doi": e["doi"],
                                    "finding": (c.get("evidence_notes") or {}).get(e["id"], e["finding"]), "limits": e["limits"]} for e in bc["evidence"]],
            "gaps": c.get("gaps", []),
        }, "tcga", "spatial", "reported", "normal")

    def _resource_row(self, c, caps=None):
        row = {k: (c["access"]["category"] if k == "access" else c.get(k)) for k in RESOURCE_FIELDS}
        if c.get("spatial_review"):
            row["treatment_class"] = c["spatial_review"].get("treatment_class")
            row["assay_classes"] = c["spatial_review"].get("assay_classes")
            rr = c["spatial_review"].get("route_review")
            if rr:
                row["route_review"] = {"status": rr["status"], "open_dependencies": rr["states"], "next_step": rr["next_step"]}
        if c.get("backlog_review"):
            b = c["backlog_review"]
            row["package_review"] = {"result": b["outcome"], "open_dependencies": b["states"], "next_step": b["next_step"]}
        if (c.get("citation") or {}).get("doi"):
            row["doi"] = c["citation"]["doi"]
        if c["layer"] == "matched-spatial":
            allcaps = self._data("captures")
            mine = [x for x in (caps if caps is not None else allcaps) if x["cohort"] == c["id"]]
            row["located_sections"] = len(mine)
            row["sections_original_he"] = sum(x.get("image_level") == "original" for x in mine)
            row["sections_preview_image"] = sum(x.get("image_level") == "preview" for x in mine) + counted_preview(c, allcaps)
            if counted_preview(c, allcaps):
                row["preview_sections_counted_without_records"] = counted_preview(c, allcaps)
            row["known_patients"] = known_patients(mine)
        return row

    def search_resources(self, text: str | None = None, cancer: str | None = None, layer: str | None = None, status: str | None = None,
                         access: str | None = None, technique: str | None = None, open_dependency: str | None = None,
                         package_review_result: str | None = None, limit: int = 50, offset: int = 0) -> dict:
        """Search catalogued studies and resources."""
        codes = self._codes(cancer) if cancer else None
        hits = []
        for c in self._data("cohorts"):
            if codes and not any(k in codes for k in c["cancers"]):
                continue
            if layer and c["layer"] != layer or status and c["status"] != status or access and c["access"]["category"] != access:
                continue
            if technique and not any(technique.lower() in t.lower() for t in c.get("techniques") or []):
                continue
            states = (c.get("backlog_review") or {}).get("states") or ((c.get("spatial_review") or {}).get("route_review") or {}).get("states", [])
            if open_dependency and open_dependency not in states:
                continue
            if package_review_result and (c.get("backlog_review") or {}).get("outcome") != package_review_result:
                continue
            if text:
                cit = c.get("citation") or {}
                blob = " ".join(str(v) for v in [c["label"], c.get("title"), c.get("description"), c.get("accession"), cit.get("authors"),
                                                 cit.get("title"), cit.get("doi"), *c["cancers"], *(c.get("techniques") or [])] if v).lower()
                if not all(w in blob for w in text.lower().split()):
                    continue
            hits.append(c)
        rows, meta = page(hits, limit, offset)
        return self._envelope({**meta, "resources": [self._resource_row(c) for c in rows]}, "spatial", "reported")

    def get_resource(self, resource_id: str) -> dict:
        """Full record of one study or resource."""
        c = next((x for x in self._data("cohorts") if x["id"] == resource_id), None)
        if not c:
            return self._envelope({"error": f"Unknown resource id {resource_id}. Use search_resources to find ids."})
        allcaps = self._data("captures")
        caps = [x for x in allcaps if x["cohort"] == resource_id]
        tiers, levels = {}, {}
        for x in caps:
            tiers[x["tier"]] = tiers.get(x["tier"], 0) + 1
            levels[x["image_level"]] = levels.get(x["image_level"], 0) + 1
        out = {"resource": c, "located_sections": len(caps), "known_patients": known_patients(caps),
               "sections_without_patient_id": sum(not x["patient"] for x in caps),
               "located_sections_by_tier": tiers, "located_sections_by_image_level": levels}
        if counted_preview(c, allcaps):
            out["preview_sections_counted_without_records"] = counted_preview(c, allcaps)
        return self._envelope(out, "spatial", "reported")

    def search_spatial_sections(self, cancer: str | None = None, resource: str | None = None, image_level: str | None = None,
                                stratum: str | None = None, site: str | None = None, treatment: str | None = None, tier: str | None = None,
                                technique: str | None = None, strict: bool = False, text: str | None = None, limit: int = 50, offset: int = 0) -> dict:
        """Located tissue sections with totals."""
        codes = self._codes(cancer) if cancer else None
        hits = []
        for x in self._data("captures"):
            if codes and x["cancer"] not in codes or resource and x["cohort"] != resource or image_level and x["image_level"] != image_level:
                continue
            if stratum and (x["stratum"] or "none") != stratum or site and x["site"].lower() != site.lower():
                continue
            if treatment and x["treatment"].lower() != treatment.lower() or tier and x["tier"] != tier:
                continue
            if technique and technique.lower() not in (x["technique"] or "").lower():
                continue
            if strict and not (x["tier"] == "core" and x["treatment"] == "Untreated"):
                continue
            if text and not all(w in " ".join(str(v) for v in (x["capture"], x["patient"], x.get("accession"), x.get("diagnosis"), x.get("histology")) if v).lower()
                                for w in text.lower().split()):
                continue
            hits.append(x)
        rows, meta = page(hits, limit, offset)
        total = meta.pop("total")
        return self._envelope({"sections": total, **meta,
                               "known_patients": known_patients(hits), "sections_without_patient_id": sum(not x["patient"] for x in hits),
                               "sections_original_he": sum(x["image_level"] == "original" for x in hits),
                               "sections_preview_image": sum(x["image_level"] == "preview" for x in hits),
                               "resources": len({x["cohort"] for x in hits}),
                               "rows": [{k: x.get(k) for k in SECTION_FIELDS} | {"he_access": x["access"]["he"]} for x in rows]}, "spatial")

    def get_spatial_section(self, section_id: str) -> dict:
        """Full record of one located tissue section."""
        x = next((c for c in self._data("captures") if c["id"] == section_id), None)
        if not x:
            return self._envelope({"error": f"Unknown section id {section_id}. Ids look like <resource>:<section>; use search_spatial_sections."})
        return self._envelope({"section": x}, "spatial")

    def get_tcga_cohort(self, cohort: str | None = None) -> dict:
        """One TCGA analysis cohort, or the list of cohorts."""
        ec = self._data("tcga_eligibility")["cohorts"]
        if not cohort or cohort.upper() not in ec:
            listing = [{"id": k, "label": v["label"], "role": v["role"], "projects": v["projects"], "selected_patients": v["selected_analysis"]["total"]}
                       for k, v in sorted(ec.items())]
            return self._envelope({**({"error": f"Unknown cohort {cohort}."} if cohort else {}), "cohorts": listing}, "tcga")
        k = cohort.upper()
        c = ec[k]
        out = {"id": k, "label": c["label"], "role": c["role"], "projects": c["projects"],
               "selected_panel": views(c["selected_analysis"]),
               "contributions": {p: views(v) for p, v in c["contributions"].items()},
               "normal_reference": {"rna_he": c["normal"]["rna_he_after"], "with_450k": c["normal"]["rna_he_met_after"], "donor_context": c["normal"].get("context")},
               "subsets": [{"id": s["id"], "label": s["label"], **views(s), "note": "already counted in the cohort; never added to totals"} for s in c.get("subsets", [])],
               "strata": c.get("strata", []),
               "annotations": {f: [{"value": v, "patients": n, "selected": s} for v, n, s in vals] for f, vals in c.get("annotations", {}).items()}}
        if c.get("withheld"):
            out["withheld_patients"] = len(c["withheld"])
        return self._envelope(out, "tcga", "normal", "treated", *(["glioma"] if k == "GLIOMA" else []))

    def search_tcga_patients(self, cohort: str | None = None, project: str | None = None, selected: bool | None = None,
                             tumour_assays: str | None = None, normal_reference: str | None = None, disposition: str | None = None,
                             subset: str | None = None, histology_stratum: str | None = None, molecular_group: str | None = None,
                             limit: int = 50, offset: int = 0) -> dict:
        """TCGA patients with totals."""
        hits = []
        for x in self._patients().values():
            if cohort and x["analysis_cohort"] != cohort.upper() or project and x["project"] != project.upper().removeprefix("TCGA-"):
                continue
            if selected is not None and (x["selected"] == "yes") != bool(selected):
                continue
            if tumour_assays and x["tumour_assays"] != tumour_assays or normal_reference and x["normal_reference"] != normal_reference:
                continue
            if disposition and x["disposition"] != disposition or subset and subset not in x["subsets"]:
                continue
            if histology_stratum and x["histology_stratum"] != histology_stratum or molecular_group and x["molecular_group"] != molecular_group:
                continue
            hits.append(x)
        hits.sort(key=lambda x: x["patient"])
        rows, meta = page(hits, limit, offset)
        total = meta.pop("total")
        t = [x["tumour_assays"] for x in hits]
        return self._envelope({"patients": total, **meta,
                               "with_rna_seq": sum(v in ("both", "rna-only") for v in t), "with_450k": sum(v in ("both", "met-only") for v in t),
                               "with_both": t.count("both"),
                               "rows": [{k: x[k] for k in PATIENT_FIELDS} for x in rows]}, "tcga", "treated")

    def get_tcga_patient(self, barcode: str) -> dict:
        """One TCGA patient by barcode."""
        b = barcode.strip().upper()[:12]
        x = self._patients().get(b)
        if not x:
            return self._envelope({"error": f"No patient {b} in the 20 panel projects."})
        rec = {k: v for k, v in x.items() if not k.startswith("_")}
        rec["screen_review"] = x["_review"]
        rec["flagged_aliquot_details"] = [{k: f[k] for k in ("aliquot", "sample", "compartment", "layer", "disposition", "pathology_reason", "retained_layers_same_compartment")}
                                          for f in x["_flags"]]
        return self._envelope({"patient": rec}, "tcga", "treated", "normal")

    def explain_term(self, term: str) -> dict:
        """Definitions and vocabulary codes matching a term."""
        g = self._data("glossary")
        q = term.strip().lower()
        concepts = [c for c in g["concepts"] if q in c["term"].lower() or c["term"].lower() in q]
        if not concepts:
            concepts = [c for c in g["concepts"] if q in c["definition"].lower()]
        codes = [{"vocabulary": v, "code": k, "label": lab} for v, m in g["vocabularies"].items() for k, lab in m.items()
                 if q == k.lower() or q in lab.lower()][:30]
        return self._envelope({"term": term, "concepts": concepts[:10], "vocabulary_codes": codes,
                               "more": "methods.html defines count units, linkage levels, exclusions and limitations."})
