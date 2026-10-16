"""Controlled vocabularies shared by check.py and build_agent_files.py."""

ENUMS = {
    "group": {"hausser", "tcga-panel", "extension", "additional", "pooled", "excluded", "aggregate"},
    "layer": {"matched-spatial", "wsi-bulk", "bulk-rna", "single-cell", "image-only"},
    "status": {"verified", "candidate", "reference", "listed", "screened", "excluded"},
    "compartment": {"primary-tumour", "metastatic-tumour", "tumour-unspecified", "solid-normal", "peritumoral", "normal", "precursor"},
    "assay_class": {"whole-transcriptome", "targeted-rna", "rna-protein", "roi", "protein-imaging", "unverified"},
    "treatment_class": {"unknown", "reported-untreated", "treated", "baseline-and-on-treatment"},
    "hausser": {"significant", "borderline", "no-geometry", "not-screened"},
    "tcga_state": {"retained", "excluded", "unresolved", "absent"},
    "access": {"open", "account", "controlled", "request", "unreleased", "unresolved"},
    "verification": {"source-described", "metadata-checked", "file-checked", "qc-complete", "not-audited"},
    "linkage": {"same-section", "same-section-mapping-pending", "listed-together", "serial-section", "same-patient", "unverified", "none"},
    "specimen": {"clinical-tumour", "cell-line", "mouse"},
    "tier": {"core", "metastatic", "review", "outside-stratum", "held"},
    "treatment": {"Untreated", "Post-treatment", "Unknown"},
    "site": {"Primary", "Metastasis", "Unknown"},
    "route_state": {"public-download", "download-failure", "vendor-terms", "dac-approval", "author-release", "local-qc"},
    "gate": {"coordinates", "he-not-located", "he-unverified", "not-released", "controlled", "request", "release-unresolved",
             "pathology-review", "identity", "treated", "package-unverified", "serial-section", "calibration", "platform",
             "histology-strata", "treatment-review", "tumour-slide-linkage", "image-qc", "integrated-diagnosis", "count-reconciliation"},
}
