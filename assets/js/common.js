// Shared data loading, vocabulary and rendering helpers.

// Site navigation collapses behind a Menu button on narrow screens; without scripts it stays visible.
{
  const header = document.querySelector(".site-header"), toggle = header?.querySelector(".nav-toggle");
  if (toggle) {
    const set = open => { toggle.setAttribute("aria-expanded", String(open)); header.classList.toggle("nav-open", open); };
    toggle.hidden = false;
    header.classList.add("has-toggle");
    toggle.addEventListener("click", () => set(toggle.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", e => { if (e.key === "Escape" && header.classList.contains("nav-open")) { set(false); toggle.focus(); } });
  }
}

export const LABELS = {
  layer: {
    "matched-spatial": "Matched H&E and spatial RNA",
    "wsi-bulk": "Whole-slide images with bulk RNA and methylation",
    "bulk-rna": "Bulk RNA reference",
    "single-cell": "Single-cell or single-nucleus RNA",
    "image-only": "Histology images only",
  },
  status: {
    verified: "Original H&E located",
    preview: "Matched data with preview image",
    candidate: "Candidate, not yet verified",
    reference: "Published reference",
    listed: "Listed, not yet curated",
    screened: "In the molecular screen panel",
    excluded: "Excluded from the study panel",
  },
  tier: {
    core: "Core primary",
    metastatic: "Metastatic site",
    review: "Under review",
    "outside-stratum": "Outside histology stratum",
    held: "Held for QC",
  },
  access: {
    open: "Open download",
    account: "Free account",
    controlled: "Controlled access",
    request: "Author request",
    unreleased: "Not released",
    unresolved: "Unresolved",
  },
  verification: {
    "source-described": "Source-described",
    "metadata-checked": "Metadata checked",
    "file-checked": "File/header checked",
    "qc-complete": "Image/registration QC complete",
    "not-audited": "Not yet audited",
  },
  linkage: {
    "same-section": "Same section: H&E imaged on the assayed section",
    "same-section-mapping-pending": "Same section; capture area still to be located on the slide scan",
    "listed-together": "H&E and expression released for the same capture; section identity not separately checked",
    "serial-section": "Serial section, not the assayed section",
    "same-patient": "Same patient: assays and slides come from one patient; sample, block and region equivalence not established",
    "unverified": "Linkage not verified",
    none: "No matched modality",
  },
  linkageShort: {
    "same-section": "Same section",
    "same-section-mapping-pending": "Same section, mapping pending",
    "listed-together": "Released together",
    "serial-section": "Serial section",
    "same-patient": "Same patient",
    unverified: "Not verified",
    none: "None",
  },
  modality: {
    "he-original": "Original-resolution H&E",
    "he-downsampled": "Downsampled H&E only",
    "he-wsi": "H&E whole-slide images",
    "he-tma": "H&E tissue microarray",
    "spatial-rna": "Spatial RNA",
    "spatial-protein": "Spatial protein",
    "bulk-rna": "Bulk RNA",
    "single-cell-rna": "Single-cell RNA",
    "raw-reads": "Raw sequencing reads",
    ihc: "Immunohistochemistry",
    proteomics: "Proteomics",
    wes: "Whole-exome sequencing",
    signature: "Archetype gene signature",
    "methylation-450k": "450k DNA methylation",
    "normal-reference": "Normal tissue reference",
    wgs: "Whole-genome sequencing",
  },
  compartment: {
    "primary-tumour": "Primary tumour",
    "metastatic-tumour": "Metastatic tumour",
    "tumour-unspecified": "Tumour, site not curated",
    "solid-normal": "Solid normal (tumour-adjacent)",
    peritumoral: "Peritumoral tissue",
    normal: "Normal tissue, not tumour-adjacent or adjacency not stated",
    precursor: "Precursor lesion",
  },
  assayClass: {
    "whole-transcriptome": "Whole-transcriptome (spot, bin or bead)",
    "targeted-rna": "Targeted RNA panel",
    "rna-protein": "Targeted RNA plus protein",
    roi: "ROI-based (GeoMx)",
    "protein-imaging": "Protein imaging only (not spatial RNA)",
    unverified: "Platform not verified",
    "not-classified": "Not classified (earlier entry)",
    na: "Not a spatial resource",
  },
  treatmentClass: {
    unknown: "Treatment unknown",
    "reported-untreated": "Reported untreated by the source, not verified",
    treated: "Treated before sampling",
    "baseline-and-on-treatment": "Trial baseline and on treatment; prior treatment not excluded",
    na: "Not in the spatial review",
  },
  tcgaState: {
    retained: "Retained",
    excluded: "Excluded",
    unresolved: "Unresolved",
    absent: "Not available",
  },
  tumourLayers: {
    both: "RNA-seq and 450k",
    "rna-only": "RNA-seq only",
    "met-only": "450k only",
    none: "None retained",
  },
  normalRef: {
    "rna-he-met": "Normal RNA + H&E + 450k",
    "rna-he": "Normal RNA + H&E, no 450k",
    withheld: "Normal package withheld by patient screen",
    inactive: "Normal package in a project excluded from the study",
    none: "Not in normal reference",
  },
  disposition: {
    pass_annotation_screen: "Passes patient screen",
    known_treatment_exclusion: "Excluded: documented treatment",
    treatment_unknown_hold: "Hold: treatment history unresolved",
    diagnosis_identity_or_episode_exclusion_hold: "Excluded or held: diagnosis, identity, recurrence or specimen",
    "not-reviewed": "No retained layer (not reviewed)",
  },
  dispositionShort: {
    pass_annotation_screen: "Passes",
    known_treatment_exclusion: "Treatment exclusion",
    treatment_unknown_hold: "Treatment hold",
    diagnosis_identity_or_episode_exclusion_hold: "Diagnosis/identity/episode",
    "not-reviewed": "Not reviewed",
  },
  reason: {
    neoadjuvant_therapy_annotation: "Neoadjuvant treatment documented in a case annotation",
    primary_diagnosis_prior_treatment_yes: "Study-primary diagnosis records treatment before sampling",
    systemic_treatment_for_prior_other_malignancy: "Systemic treatment for another malignancy",
    unacceptable_prior_other_malignancy_treatment: "Prior treatment for another malignancy annotated as unacceptable",
    previous_local_treatment_same_organ: "Earlier local treatment of the same organ",
    prior_malignancy_treatment_details_unresolved: "Prior malignancy with unresolved treatment details",
    primary_diagnosis_treatment_unreported: "Treatment before sampling not reported",
    possible_chemotherapy_unverified: "Possible chemotherapy, unverified",
    neoadjuvant_timing_unverified: "Neoadjuvant timing unverified",
    coded_lineage_variant_or_mismatch_needs_pathology_adjudication: "Diagnosis code suggests another lineage or variant: pathology hold",
    recurrence_or_progression_not_initial_primary: "Recurrence or progression, not the initial primary",
    diagnosis_or_specimen_eligibility_hold: "Diagnosis or specimen eligibility unresolved",
    primary_diagnosis_missing_or_unreported: "Study-primary diagnosis missing or unreported",
    wrong_target_primary_site_or_histology: "Wrong primary site or histology for the project",
    sample_identity_or_tumour_normal_integrity_hold: "Sample identity or tumour–normal integrity concern",
    no_tumour_in_submitted_specimen: "No tumour in the submitted specimen",
    duplicate_patient_second_biopsy_excluded: "Duplicate patient: second biopsy record excluded",
    prior_or_synchronous_malignancy: "Prior or synchronous malignancy",
    prior_other_malignancy_local_treatment: "Local treatment of another malignancy",
    distant_brain_radiation_lung_primary_explicitly_untreated: "Brain radiation; the lung primary is explicitly untreated",
    prior_lung_local_radiation_remote_from_sampled_kidney: "Lung radiation, remote from the sampled kidney",
    prior_remote_local_radiation_not_sampled_kidney_treatment: "Remote local radiation, not treatment of the sampled kidney",
    childhood_radiation_exposure_not_cancer_pretreatment: "Childhood radiation exposure, not cancer pretreatment",
    canonical_first_biopsy_duplicate_crosswalk_EK_A2H0: "Canonical record of a duplicate patient (second biopsy TCGA-EK-A2H0 excluded)",
    COAD_submitted_rectal_primary_recovered_in_CRC: "Submitted as COAD, rectal primary by annotation; included in CRC",
    READ_submitted_colon_primary_retained_in_CRC: "Submitted as READ, colon primary by annotation; included in CRC",
    GBM_submitted_LGG_corrected_retained_in_pooled_glioma: "Submitted as GBM, annotated as lower-grade glioma; both labels kept in the glioma benchmark",
    qualification_in_error_patient_hold: "Patient qualified in error",
    supportive_dexamethasone_phenytoin_before_procurement_not_anticancer_neoadjuvant: "Dexamethasone and phenytoin before procurement: supportive medication, not antineoplastic treatment",
  },
  treatmentContext: {
    "sampled-cancer": "Treatment of the sampled cancer before sampling",
    "same-organ-local": "Earlier local treatment of the same organ",
    "other-systemic": "Systemic treatment for another malignancy",
    unresolved: "Treatment history unresolved",
    "remote-radiation": "Remote local radiation (covariate)",
    "other-local": "Local treatment of another malignancy (covariate)",
    "childhood-exposure": "Childhood radiation exposure (covariate)",
    "supportive-medication": "Supportive steroid or anticonvulsant before procurement (covariate)",
    "none-documented": "No pretreatment documented",
    "not-reviewed": "Not reviewed",
  },
  normalContext: {
    target_project_donor: "Donor with a target-project tumour diagnosis",
    organ_specific_control: "Organ-specific control, no reported tumour diagnosis",
    non_target_or_uncertain_or_recurrent_donor: "Non-target, uncertain or recurrent donor diagnosis",
    normal_only_donor_primary_diagnosis_unreported: "Normal-only donor, primary diagnosis unreported (not a verified matched control)",
    na: "No normal package after screening",
  },
  selected: { yes: "In the selected analysis set", no: "Retained tumour assays, not selected", na: "No retained tumour assay" },
  siteOverride: { rectum: "Rectum (case annotation)", colon_unspecified: "Colon, segment not specified (case annotation)", none: "No override" },
  sampleIds: {
    sample_ids: "Selected", exclude_sample_ids: "Excluded from this scope", normal_or_precursor_ids: "Normal or precursor, kept separate",
    tumour_sample_ids: "Tumour sections", adjacent_sample_ids: "Adjacent-normal sections", metastatic_sample_ids: "Metastatic",
  },
  spatialScope: {
    CSCC: "Cervical squamous cell carcinoma (CSCC), shown on the CESC page", ESCC: "Oesophageal squamous cell carcinoma (ESCC), shown on the ESCA page",
    KIRC: "Clear-cell renal cell carcinoma", KIRP: "Papillary renal cell carcinoma", LUSC: "Lung squamous cell carcinoma",
    PCPG: "Pheochromocytoma and paraganglioma", PRAD: "Prostate adenocarcinoma", STAD: "Gastric adenocarcinoma",
    UCEC: "Endometrial carcinoma", GLIOMA: "Diffuse glioma, including GBM (pooled GLIOMA)",
  },
  role: { discovery: "Discovery cohort", "classification-benchmark": "Classification benchmark", excluded: "Excluded from the study panel", none: "Not reviewed" },
  panelExclusion: {
    cervical_glandular_or_adenosquamous_outside_squamous_core: "Cervical adenocarcinoma or adenosquamous: outside the squamous cohort",
    none: "None",
  },
  // Why a TCGA project that passes the size threshold as a whole is still outside the panel.
  projectExclusion: {
    SARC: "No: it combines several sarcoma types, each below the size threshold",
  },
  // The histology analysed when a cohort is one part of a TCGA project.
  cohortScope: {
    ESCC: "squamous cell carcinoma only",
    PDAC: "ductal adenocarcinoma only",
    CSCC: "squamous cell carcinoma only",
  },
  pooledName: { CRC: "colorectal cancer", GLIOMA: "diffuse glioma" },
  whoStatus: {
    not_adjudicated: "Not adjudicated",
    requires_independent_integrated_diagnosis_and_grade: "Needs an independent integrated diagnosis and grade; not adjudicated",
  },
  subset: {
    "PDAC-sensitivity": "PDAC sensitivity subset",
    "UCEC-endometrioid": "UCEC endometrioid only",
    "PCPG-without-neck": "PCPG without head and neck paragangliomas",
    "GLIOMA-LGG-only": "Glioma benchmark: LGG only",
    "GLIOMA-paired-only": "Glioma benchmark: RNA-seq and 450k",
    none: "Not in a subset",
  },
  histStratum: {
    Squamous: "Cervical squamous cell carcinoma", Adenocarcinoma: "Cervical adenocarcinoma", Adenosquamous: "Cervical adenosquamous carcinoma",
    Endometrioid: "Endometrial: endometrioid", Serous: "Endometrial: serous", Mixed: "Endometrial: mixed", Other: "Endometrial: other",
    pheochromocytoma: "Pheochromocytoma", paraganglioma: "Paraganglioma",
    IDHwt: "Glioma: IDH-wildtype group", "IDHmut-non-codel": "Glioma: IDH-mutant, non-codeleted group",
    "IDHmut-codel": "Glioma: IDH-mutant, 1p/19q-codeleted group", unassigned: "Glioma: no complete published group",
    na: "Not part of the histology revision",
  },
  annotationField: {
    histology_stratum: "Reviewed histology", histology_evidence: "Histology source", grade_publication: "Grade (publication)",
    published_subtype: "Published molecular subtype", site_reported: "Reported tumour site (GDC)",
    adrenal_cortical_admixture: "Adrenal-cortical admixture (publication)", hpv_status_publication: "HPV status (publication)",
    endometrial_like_publication: "Endometrial-like group (publication)", molecular_group: "Published molecular group",
    idh_status: "IDH status (raw call)", codeletion_1p19q: "1p/19q status (raw call)", histology_publication: "Historical histology (publication)",
  },
  stratum: {
    escc_publication_reviewed: "Squamous cell carcinoma, publication-reviewed",
    escc_gdc_only_provisional: "Squamous cell carcinoma, GDC label only (provisional)",
    eac_definite_oesophageal: "Oesophageal adenocarcinoma, definite",
    eac_probable_oesophageal: "Oesophageal adenocarcinoma, probable",
    gej_adenocarcinoma_indeterminate_origin: "Junctional adenocarcinoma, origin indeterminate",
    gastric_or_probably_gastric_adenocarcinoma: "Gastric or probably gastric adenocarcinoma",
    unclassified_publication_histology: "Unclassified in the publication table",
    adenocarcinoma_gdc_only_origin_unresolved: "Adenocarcinoma, GDC label only, origin unresolved",
    ductal_labelled_gdc: "GDC label: infiltrating duct carcinoma",
    adenocarcinoma_nos_gdc: "GDC label: adenocarcinoma NOS",
    mucinous_adenocarcinoma_gdc: "GDC label: mucinous adenocarcinoma",
    adenocarcinoma_mixed_subtypes_gdc: "GDC label: adenocarcinoma with mixed subtypes",
    neuroendocrine_gdc: "GDC label: neuroendocrine carcinoma",
    undifferentiated_carcinoma_gdc: "GDC label: undifferentiated carcinoma",
  },
  relation: {
    concordant: "Agrees with GDC label",
    refined: "More specific than GDC label",
    differs: "Differs from GDC label",
    unconfirmed: "Not confirmed by review",
    "not-reviewed": "GDC label only",
    na: "Not part of the histology review",
  },
  analysisGroup: {
    outside: "Outside the histology-defined cohort",
    none: "Not reviewed: no retained RNA-seq or 450k",
  },
  siteReported: { na: "Not imported for this project" },
  analysisCohort: {
    ESCC: "Confirmed ESCC (90)",
    PDAC: "Confirmed PDAC (149, proposed)",
    outside: "Reviewed, outside the cohort",
    none: "No histology-defined cohort",
  },
  analysisReason: {
    confirmed_ESCC_smaller_cohort_exception: "Publication-reviewed ESCC with retained assays",
    outside_confirmed_ESCC_core: "Not publication-reviewed ESCC",
    publication_reviewed_ductal: "Ductal adenocarcinoma in the publication pathology review",
    pathology_report_confirmed_ductal: "Ductal adenocarcinoma confirmed by the original pathology report",
    other_or_unconfirmed_histology_or_no_retained_assay: "Other or unconfirmed histology, or no retained tumour assay",
  },
  sens: {
    included: "In the 148-patient sensitivity subset",
    excluded: "Excluded: focal squamous component",
    na: "Not applicable",
  },
  scopeAction: {
    exclude_untreated_core_prior_treatment: "Prior treatment: outside untreated core",
    hold_untreated_core_treatment_unknown: "Treatment history unknown: untreated eligibility on hold",
    retain_existing_assay_exclusion_review_histology_or_region: "Histology, site or region issue: assay exclusion kept",
    exclude_hcc_tumour_stratum_keep_organ_normal_separate_donor_stratum: "Non-HCC liver tumour: normal tissue is a separate donor stratum",
    record_covariate_no_new_global_exclusion: "Prior or synchronous malignancy: recorded as a covariate",
    exclude_untreated_core_keep_treated_resource: "Neoadjuvant treatment: treated resource only",
    exclude_primary_core_keep_recurrence_resource: "Recurrence: outside primary-tumour core",
    hold_affected_assay_keep_other_covered_layer: "Qualification metrics changed: affected assay held",
    keep_exact_assay_exclusion_no_patient_blacklist: "Assay-specific technical issue: exact assay exclusion only",
    none: "Not in the scope review",
  },
  tcgaCompartment: {
    "primary-tumour": "Primary tumour assays retained",
    "solid-normal": "Normal reference retained",
    none: "Nothing retained",
  },
  specimen: {
    "clinical-tumour": "Clinical tumour tissue",
    "cell-line": "Cell lines",
    mouse: "Mouse models",
  },
  routeState: {
    "public-download": "Public download works",
    "download-failure": "Public files listed, download failed (technical)",
    "vendor-terms": "Vendor registration and terms",
    "account-registration": "Free account registration",
    "dac-approval": "Data access committee approval",
    "author-release": "Author release or metadata needed",
    "local-qc": "Local scientific QC remaining",
  },
  // Image level of a study (its best level) or of one section record.
  imageLevel: {
    original: "Original H&E located",
    preview: "Matched data with preview image",
  },
  imageLevelNote: {
    original: "The original H&E scan, measured expression and coordinates were located. Registration and scanner calibration are separate checks.",
    preview: "Measured expression and coordinates match a preview image released with them (such as a Space Ranger image). The original H&E scan was not located, so the section supports molecular spatial maps but not whole-slide or tile models, cell morphology, physical distances or registration sign-off.",
  },
  backlogOutcome: {
    "original-ready": "Original H&E and matched data checked",
    "preview-ready": "Matched data checked; preview image only",
    "bounded-public-work": "Public files listed; inspection not finished",
    "access-dependent": "Access needs approval or permission",
    "release-unresolved": "Data release not identified",
    "author-release": "Release by the authors needed",
    "release-gap": "Public record without downloadable files",
    "code-only-lead": "Code only; no data package identified",
    "technical-gap": "Public download failed (technical)",
    "coordinate-gap": "Coordinates or image scale missing",
    "registration-gap": "Original image or its transform missing",
    "linkage-gap": "Image and expression files not yet joined",
    "account-route": "Free account needed",
    "unspecified-vendor-lead": "Vendor catalogue without a specific dataset",
    "vendor-boundary": "Vendor registration and terms",
  },
  followupOutcome: {
    "original-ready": "Original H&E and matched data checked",
    "preview-ready": "Matched data checked; preview image only",
    "preview-ready-partial": "Part of the study checked; preview image only",
    "preview-clinical-correction": "Clinical details corrected",
    "preview-additional-route": "Further data route found; no files listed",
    "bounded-public-work": "Public files listed; inspection not finished",
    "bounded-public-work-reuse-known": "Public files listed; reused data identified",
    "image-linkage-gap": "No H&E correspondence for the measured data",
    "image-alias-review": "Image and sample labels conflict",
    "public-processed-decoding-gap": "Public processed files not yet decoded",
    "spatial-release-unresolved": "Spatial data release not identified",
    "public-portal-link-resolved": "Public portal found; files not yet inspected",
    "coordinate-gap": "Coordinates or image scale missing",
    "barcode-grid-gap": "Barcode-to-grid map missing",
  },
  donorMapping: {
    "source-established": "Established within the source",
    "source-patient-column": "From the source's patient ID column",
    "source-sample-title": "From the source sample title",
    unresolved: "Not mapped: the source does not establish the donor",
  },
  gate: {
    "coordinates": "Spot or bead coordinates missing or defective",
    "he-not-located": "Original-resolution H&E not located",
    "he-unverified": "Original H&E content or resolution unverified",
    "not-released": "Data not yet released",
    controlled: "Controlled access; package contents unverified",
    request: "Available on request only",
    "release-unresolved": "Release route unresolved",
    "pathology-review": "Histology or primary-site review needed",
    identity: "Image identity, crosswalk or registration unresolved",
    treated: "Post-treatment cohort",
    "package-unverified": "Public package contents not fully verified",
    "serial-section": "Serial rather than same-section H&E",
    calibration: "Image calibration unresolved",
    platform: "Legacy, targeted or ROI-based spatial platform",
    "count-reconciliation": "Reported and deposited counts disagree",
    "histology-strata": "Histology strata not yet curated",
    "treatment-review": "Treatment history not yet reviewed",
    "tumour-slide-linkage": "Tumour slide linkage for retained assays not yet checked",
    "image-qc": "Image QC not done",
  },
  hausser: {
    significant: "Significant geometry in Hausser et al. 2019",
    borderline: "Borderline in Hausser et al. 2019",
    "no-geometry": "No geometry detected in Hausser et al. 2019",
    "not-screened": "Not screened by Hausser et al. 2019",
  },
  treatment: { Untreated: "Untreated", "Post-treatment": "Post-treatment", Unknown: "Unknown" },
  site: { Primary: "Primary", Metastasis: "Metastasis", Unknown: "Unknown" },
};

const TONE = {
  status: { verified: "ok", preview: "accent", candidate: "warn", reference: "accent", listed: "", screened: "accent", excluded: "" },
  imageLevel: { original: "ok", preview: "accent" },
  tcgaState: { retained: "ok", excluded: "eosin", unresolved: "warn", absent: "" },
  tumourLayers: { both: "ok", "rna-only": "accent", "met-only": "accent", none: "" },
  normalRef: { "rna-he-met": "ok", "rna-he": "accent", none: "", withheld: "warn", inactive: "" },
  disposition: { pass_annotation_screen: "ok", known_treatment_exclusion: "eosin", treatment_unknown_hold: "warn", diagnosis_identity_or_episode_exclusion_hold: "warn", "not-reviewed": "" },
  tier: { core: "ok", metastatic: "accent", review: "warn", "outside-stratum": "", held: "warn" },
  access: { open: "ok", account: "ok", controlled: "accent", request: "warn", unreleased: "", unresolved: "" },
  treatment: { Untreated: "ok", "Post-treatment": "eosin", Unknown: "" },
  verification: { "file-checked": "ok", "metadata-checked": "ok", "source-described": "", "not-audited": "", "qc-complete": "ok" },
};

let cache = null;
export async function loadData() {
  if (cache) return cache;
  const names = ["release", "cancers", "evidence", "cohorts", "captures", "tcga_counts", "tcga_resources", "tcga_eligibility", "leads"];
  const parts = await Promise.all(names.map(n => fetch(`data/${n}.json`).then(r => {
    if (!r.ok) throw new Error(`Could not load data/${n}.json (${r.status})`);
    return r.json();
  })));
  const d = Object.fromEntries(names.map((n, i) => [n, parts[i]]));
  d.cohortById = new Map(d.cohorts.map(c => [c.id, c]));
  d.cancerByCode = new Map(d.cancers.map(c => [c.code, c]));
  d.strata = new Map(d.cancers.flatMap(c => c.strata.map(([id, label]) => [id, { id, label, cancer: c.code }])));
  d.tcgaCounts = d.tcga_counts.projects;
  d.tcgaMeta = d.tcga_counts.meta;
  d.tcgaPanel = d.tcga_counts.meta.panel;
  d.elig = d.tcga_eligibility;
  cache = d;
  return d;
}

// Patient-level TCGA tables are large; load them only when needed.
let tcgaCache = null;
export async function loadTcgaPatients(d) {
  if (tcgaCache) return tcgaCache;
  const [p, f] = await Promise.all(["tcga_patients", "tcga_flags"].map(n => fetch(`data/${n}.json`).then(r => {
    if (!r.ok) throw new Error(`Could not load data/${n}.json (${r.status})`);
    return r.json();
  })));
  const rv = await loadTcgaReviews();
  const pr = await fetch("data/tcga_patient_review.json").then(res => {
    if (!res.ok) throw new Error(`Could not load data/tcga_patient_review.json (${res.status})`);
    return res.json();
  });
  const clinicalBy = new Map(pr.rows.map(row => { const o = Object.fromEntries(pr.columns.map((c, i) => [c, row[i]])); return [o.patient, o]; }));
  const subsetsBy = new Map();
  for (const c of Object.values(d.elig.cohorts)) for (const sub of c.subsets || []) for (const p of sub.patients) {
    if (!subsetsBy.has(p)) subsetsBy.set(p, []);
    subsetsBy.get(p).push(sub.id);
  }
  const flags = f.rows.map(r => Object.fromEntries(f.columns.map((c, i) => [c, r[i]])));
  const flagsBy = new Map();
  for (const x of flags) {
    if (!flagsBy.has(x.patient)) flagsBy.set(x.patient, []);
    flagsBy.get(x.patient).push(x);
  }
  const patients = p.rows.map(r => {
    const x = Object.fromEntries(p.columns.map((c, i) => [c, r[i]]));
    const tr = x.tumour_rna === "retained", tm = x.tumour_met === "retained";
    x.tumour_layers = tr && tm ? "both" : tr ? "rna-only" : tm ? "met-only" : "none";
    x.normal_ref = x.normal_rna_he_met ? "rna-he-met" : x.normal_rna_he ? "rna-he" : "none";
    x.compartments = [x.tumour_layers !== "none" && "primary-tumour", x.normal_ref !== "none" && "solid-normal"].filter(Boolean);
    if (!x.compartments.length) x.compartments = ["none"];
    x.cancer = x.project === "PAAD" ? "PDAC" : x.project;
    x.flags = flagsBy.get(x.patient) || [];
    x.id = x.patient;
    x.histology = rv.histologyBy.get(x.patient) || null;
    x.scope = rv.scopeBy.get(x.patient) || null;
    x.cohort = x.histology ? (x.histology.analysis_cohort || "outside") : "none";
    x.sens = x.cohort === "PDAC" ? (x.histology.focal_squamous_flag ? "excluded" : "included") : "na";
    x.relation = x.histology ? x.histology.gdc_label_relation : "na";
    x.scopeAction = x.scope ? x.scope.summary_action : "none";
    const cl = clinicalBy.get(x.patient) || null;
    x.clinical = cl;
    x.disposition = cl ? cl.main_disposition : "not-reviewed";
    const hasTumour = x.tumour_layers !== "none";
    x.eligible = !!(cl && hasTumour && cl.tumour_eligible);
    x.selected = hasTumour ? (cl && cl.selected_eligible ? "yes" : "no") : "na";
    x.reasons = cl ? [...cl.treatment_exclusion_reasons, ...cl.treatment_hold_reasons, ...cl.diagnosis_reasons] : [];
    x.covariates = cl ? cl.covariates : [];
    x.treatmentContext = treatmentContext(cl);
    if (x.normal_ref !== "none" && !(cl && cl.normal_donor_eligible)) x.normal_ref = "withheld";
    else if (x.normal_ref !== "none" && !cl.normal_catalogue_eligible) x.normal_ref = "inactive";
    x.normalContext = x.normal_ref === "rna-he" || x.normal_ref === "rna-he-met" ? cl.normal_donor_context : "na";
    x.analysisCohort = cl ? (cl.analysis_group || (cl.analysis_role === "excluded" ? "excluded" : "outside")) : "none";
    x.role = cl ? cl.analysis_role : "none";
    x.subsets = subsetsBy.get(x.patient) || ["none"];
    x.histStratum = cl && cl.histology_stratum ? cl.histology_stratum : "na";
    x.panelExclusion = cl && cl.panel_exclusion_reason ? cl.panel_exclusion_reason : "none";
    x.conflict = cl && cl.histology_label_conflict ? "yes" : "no";
    x.siteReported = cl && cl.site_reported ? cl.site_reported : "na";
    x.siteOverride = cl && cl.site_override ? cl.site_override : "none";
    return x;
  });
  tcgaCache = { patients, byId: new Map(patients.map(x => [x.patient, x])), flags, reviews: rv };
  return tcgaCache;
}

let reviewCache = null;
export async function loadTcgaReviews() {
  if (reviewCache) return reviewCache;
  const r = await fetch("data/tcga_reviews.json").then(res => {
    if (!res.ok) throw new Error(`Could not load data/tcga_reviews.json (${res.status})`);
    return res.json();
  });
  const histology = r.histology.map(row => Object.fromEntries(r.histology_columns.map((c, i) => [c, row[i]])));
  const scope = r.scope.map(row => Object.fromEntries(r.scope_columns.map((c, i) => [c, row[i]])));
  reviewCache = {
    meta: r.meta, histology, scope,
    histologyBy: new Map(histology.map(h => [h.patient, h])),
    scopeBy: new Map(scope.map(x => [x.patient, x])),
    cohortBy: new Map(r.meta.cohorts.map(c => [c.id, c])),
  };
  return reviewCache;
}

export function cohortTally(rows) {
  const t = { patients: rows.length, rna: 0, met: 0, both: 0, rnaOnly: 0, metOnly: 0, normal: 0, normalMet: 0 };
  for (const h of rows) {
    const r = h.tumour_rna_retained, m = h.tumour_450k_retained;
    t.rna += r; t.met += m; t.both += r && m; t.rnaOnly += r && !m; t.metOnly += m && !r;
    t.normal += !!h.normal_rna_he; t.normalMet += !!h.normal_rna_he_450k;
  }
  return t;
}

export function cohortMembers(rv, id) {
  if (id === "PDAC-sensitivity") return rv.histology.filter(h => h.analysis_cohort === "PDAC" && !h.focal_squamous_flag);
  return rv.histology.filter(h => h.analysis_cohort === id);
}

export function analysisSection(d, rv, project) {
  const c = d.tcgaCounts[project];
  const defs = rv.meta.cohorts.filter(x => x.project === project);
  if (!defs.length) return "";
  const r = d.tcgaMeta.rule;
  const row = (label, t, cls = "") => `<tr${cls}><td>${label}</td><td class="num">${fmt(t.patients)}</td><td class="num">${fmt(t.rna)}</td><td class="num">${fmt(t.met)}</td><td class="num">${fmt(t.both)}</td><td class="num">${fmt(t.rnaOnly)}</td><td class="num">${fmt(t.metOnly)}</td><td class="num">${fmt(t.normal)}</td><td class="num">${fmt(t.normalMet)}</td></tr>`;
  const proj = { patients: c.post_qc.union, rna: c.post_qc.paired + c.post_qc.rna_only, met: c.post_qc.paired + c.post_qc.met_only, both: c.post_qc.paired, rnaOnly: c.post_qc.rna_only, metOnly: c.post_qc.met_only, normal: c.normal.rna_he, normalMet: c.normal.rna_he_met };
  const regs = rv.histology.filter(h => h.project === project);
  const strata = [...new Set(regs.map(h => h.stratum))].sort((a, b) => Object.keys(LABELS.stratum).indexOf(a) - Object.keys(LABELS.stratum).indexOf(b));
  const stratumRows = strata.map(s => {
    const hs = regs.filter(h => h.stratum === s);
    const qc = hs.filter(h => h.tumour_rna_retained || h.tumour_450k_retained);
    const t = cohortTally(qc);
    const inCohort = hs.filter(h => h.analysis_cohort).length;
    return `<tr><td class="primary" data-label="Stratum"><div>${esc(LABELS.stratum[s] ?? s)}</div></td>
      <td class="num" data-label="Registered"><div>${hs.length}</div></td>
      <td class="num" data-label="Retained tumour assays"><div>${t.patients}</div></td>
      <td class="num" data-label="Both"><div>${t.both}</div></td>
      <td class="num" data-label="Normal RNA + H&E"><div>${t.normal}</div></td>
      <td class="num" data-label="Normal with 450k"><div>${t.normalMet}</div></td>
      <td class="num" data-label="In cohort"><div>${inCohort}</div></td></tr>`;
  }).join("");
  const reviewedOut = regs.filter(h => !h.analysis_cohort && (h.tumour_rna_retained || h.tumour_450k_retained) && (h.publication_review_histology || h.pathology_report_url) );
  const differs = regs.filter(h => ["refined", "differs", "unconfirmed"].includes(h.gdc_label_relation) && (h.tumour_rna_retained || h.tumour_450k_retained));
  const caseList = (hs, extra) => `<ul class="notes">${hs.map(h => `<li><a href="explore.html?view=tcga&open=${esc(h.patient)}" class="mono">${esc(h.patient)}</a>: GDC ${esc(h.gdc_primary_diagnosis)} (${esc(h.gdc_morphology)}) → ${esc(h.reviewed_histology ?? "not reviewed")}${extra ? extra(h) : ""}</li>`).join("")}</ul>`;
  const flagged = regs.filter(h => h.focal_squamous_flag || h.primary_metastatic_separated);
  return `
    <div class="table-wrap"><table class="compact"><thead><tr><th>Unique patients</th><th class="num">RNA-seq and/or 450k</th><th class="num">RNA-seq</th><th class="num">450k</th><th class="num">Both</th><th class="num">RNA only</th><th class="num">450k only</th><th class="num">Normal RNA + H&amp;E</th><th class="num">Normal with 450k</th></tr></thead><tbody>
      ${row(`TCGA-${esc(project)} project, after assay exclusions`, proj)}
      ${(() => { const e = d.elig && d.elig.projects[project]; if (!e) return ""; const a = e.after_patient_screen;
        return row(`TCGA-${esc(project)} project, after the patient screen`, { patients: a.total, rna: a.rna, met: a.met, both: a.paired, rnaOnly: a.rna_only, metOnly: a.met_only, normal: e.normal.rna_he_after, normalMet: e.normal.rna_he_met_after }); })()}
      ${defs.map(x => row(`<strong>${esc(x.label)}</strong>${x.status === "proposed" ? " (proposed)" : ""}`, cohortTally(cohortMembers(rv, x.id)))).join("")}
    </tbody></table></div>
    <ul class="notes" style="margin-top:.6rem">${defs.filter(x => x.exception).map(x => `<li><strong>${esc(x.label)}:</strong> ${esc(x.exception)}</li>`).join("")}
      <li>The general screen (${r.min_total} patients with RNA-seq and/or 450k, ${r.min_paired} with both) is unchanged for all other projects.</li></ul>
    ${defs.map(x => `<p class="small"><strong>${esc(x.label)}.</strong> ${esc(x.definition)}</p>`).join("")}
    <h3>Histology strata of all ${regs.length} registered TCGA-${esc(project)} cases</h3>
    <div class="table-wrap"><table class="stack compact"><thead><tr><th scope="col">Stratum</th><th scope="col" class="num">Registered</th><th scope="col" class="num">Retained tumour assays</th><th scope="col" class="num">Both</th><th scope="col" class="num">Normal RNA + H&amp;E</th><th scope="col" class="num">Normal with 450k</th><th scope="col" class="num">In cohort</th></tr></thead>
      <tbody>${stratumRows}</tbody>
      <caption>Strata follow the source of the diagnosis: ${project === "ESCA" ? "the TCGA oesophageal study's Supplementary Table 1 where available, otherwise the GDC label" : "GDC primary-diagnosis labels; cohort membership comes from the pathology review, not from these labels"}. Normal counts are grouped by the donor's tumour classification; the normal images themselves were not reviewed.</caption>
    </table></div>
    ${differs.length ? `<details class="disclosure"><summary>${differs.length} reviewed diagnoses differ from, refine or do not confirm the GDC label</summary>${caseList(differs, h => ` · ${LABELS.relation[h.gdc_label_relation].toLowerCase()} · ${h.analysis_cohort ? "in cohort" : "outside cohort"}`)}</details>` : ""}
    ${project === "PAAD" && reviewedOut.length ? `<h3>Reviewed cases with retained assays kept outside the cohort (${reviewedOut.length})</h3>${caseList(reviewedOut, h => h.publication_notes ? ` · publication note: ${esc(h.publication_notes)}` : "")}<p class="muted small">Adenosquamous, colloid and “Other” diagnoses are excluded or held. An IPMN note alone is not treated as non-invasive disease; those cases are held because the review does not confirm conventional invasive ductal adenocarcinoma.</p>` : ""}
    ${flagged.length ? `<h3>Flags on included patients</h3><ul class="notes">${flagged.map(h => `<li><span class="mono">${esc(h.patient)}</span>: ${h.focal_squamous_flag ? "pathology report describes ductal adenocarcinoma with a focal non-keratinizing squamous component; retained, and omitted from the sensitivity subset" : esc(h.specimen_note || "primary and metastatic specimens are separated")}.</li>`).join("")}</ul>` : ""}
    <p class="muted small">Histology evidence is a documented diagnosis review from published pathology tables and original GDC pathology reports, not a new expert slide review. Every cohort member also passed the patient treatment and diagnosis screen. The linkage of retained assays to slide images has not been checked.</p>`;
}

function treatmentContext(cl) {
  if (!cl) return ["not-reviewed"];
  const ex = cl.treatment_exclusion_reasons, cov = cl.covariates, out = [];
  if (ex.some(r => r === "neoadjuvant_therapy_annotation" || r === "primary_diagnosis_prior_treatment_yes")) out.push("sampled-cancer");
  if (ex.includes("previous_local_treatment_same_organ")) out.push("same-organ-local");
  if (ex.some(r => r === "systemic_treatment_for_prior_other_malignancy" || r === "unacceptable_prior_other_malignancy_treatment")) out.push("other-systemic");
  if (cl.treatment_hold_reasons.length) out.push("unresolved");
  if (cov.some(c => /radiation/.test(c) && !/childhood/.test(c))) out.push("remote-radiation");
  if (cov.includes("prior_other_malignancy_local_treatment")) out.push("other-local");
  if (cov.some(c => /childhood/.test(c))) out.push("childhood-exposure");
  if (cov.some(c => /^supportive_/.test(c))) out.push("supportive-medication");
  return out.length ? out : ["none-documented"];
}

export function tcgaTally(rows) {
  const t = { patients: rows.length, union: 0, paired: 0, rnaOnly: 0, metOnly: 0, normal: 0, normalMet: 0, both: 0,
    eligible: 0, selected: 0, selPaired: 0, selRnaOnly: 0, selMetOnly: 0, withheldNormal: 0, excluded: 0 };
  for (const r of rows) {
    // Patients of a project excluded from the study are listed for provenance but not counted.
    if (r.role === "excluded") { t.excluded++; continue; }
    const tum = r.tumour_layers !== "none", nor = r.normal_ref === "rna-he" || r.normal_ref === "rna-he-met";
    if (tum) t.union++;
    if (r.tumour_layers === "both") t.paired++;
    if (r.tumour_layers === "rna-only") t.rnaOnly++;
    if (r.tumour_layers === "met-only") t.metOnly++;
    if (r.eligible) t.eligible++;
    if (r.selected === "yes") {
      t.selected++;
      if (r.tumour_layers === "both") t.selPaired++;
      if (r.tumour_layers === "rna-only") t.selRnaOnly++;
      if (r.tumour_layers === "met-only") t.selMetOnly++;
    }
    if (nor) t.normal++;
    if (r.normal_ref === "rna-he-met") t.normalMet++;
    if (r.normal_ref === "withheld") t.withheldNormal++;
    if (r.selected === "yes" && nor) t.both++;
  }
  t.either = t.selected + t.normal - t.both;
  return t;
}

export function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
}

export function chip(kind, value, text) {
  const tone = (TONE[kind] && TONE[kind][value]) || "";
  const label = text ?? (LABELS[kind] && LABELS[kind][value]) ?? value;
  return `<span class="chip ${tone}">${esc(label)}</span>`;
}

export const fmt = n => (n == null ? "—" : Number(n).toLocaleString("en-GB"));

export function patientKey(c) { return `${c.cohort}::${c.patient ?? c.capture}`; }

// Sections, known study-local patients (records without a patient ID are not counted as patients) and studies.
export function tally(captures) {
  const known = captures.filter(c => c.patient);
  const cohorts = new Set(captures.map(c => c.cohort));
  return { captures: captures.length, patients: new Set(known.map(patientKey)).size, unknown: captures.length - known.length, cohorts: cohorts.size };
}

// Checked preview packages counted for a study without individual section records (from its public-route review).
export function countedPreview(d, c, codes = null) {
  if (c.status !== "preview" || capturesOf(d, c.id).length) return 0;
  const sr = c.spatial_review;
  if (codes && !(sr && codes.includes(sr.analysis_cohort))) return 0;
  return (sr && sr.route_review && sr.route_review.sections_with_matching_coordinates) || 0;
}

// Section records of a study at each image level, optionally limited to some cancer codes.
export function levelCounts(d, c, codes = null) {
  const caps = capturesOf(d, c.id).filter(x => !codes || codes.includes(x.cancer));
  const counted = countedPreview(d, c, codes);
  const orig = caps.filter(x => x.image_level === "original"), prev = caps.filter(x => x.image_level === "preview");
  return { original: orig.length, preview: prev.length + counted, listedPreview: prev.length, counted, patients: tally(caps).patients, unknown: tally(caps).unknown };
}

// Plain text for a study's image level with its section counts, e.g. "Original H&E located: 12 sections; 7 more with a preview image".
export function levelText(d, c, codes = null) {
  if (c.status !== "verified" && c.status !== "preview") return "";
  const k = levelCounts(d, c, codes);
  const sec = n => `${fmt(n)} ${n === 1 ? "section" : "sections"}`;
  const parts = c.status === "verified"
    ? [k.original ? `${sec(k.original)} with original H&E` : "", k.preview ? `${sec(k.preview)} with a preview image only` : ""]
    : [k.preview ? `${sec(k.preview)} with a preview image${k.counted ? " (checked packages, not listed one by one)" : ""}` : ""];
  const pts = k.patients ? `${fmt(k.patients)} known ${k.patients === 1 ? "patient" : "patients"}` : "";
  return parts.filter(Boolean).concat(pts ? [pts] : []).join("; ");
}

export function cancerName(d, code) {
  const c = d.cancerByCode.get(code);
  return c ? c.name : code;
}

export function stratumLabel(d, id) {
  return id ? (d.strata.get(id)?.label ?? id) : "No stratum assigned";
}

export function citationText(cit) {
  if (!cit) return "";
  const stop = t => (/[.?!]$/.test(t) ? t : `${t}.`);
  const bits = [];
  if (cit.authors) bits.push(esc(stop(cit.authors)));
  if (cit.title) bits.push(`<em>${esc(stop(cit.title))}</em>`);
  const venue = [cit.journal, cit.year].filter(Boolean).join(" ");
  if (venue) bits.push(esc(stop(venue)));
  let s = bits.join(" ");
  if (cit.doi) s += ` <a href="https://doi.org/${esc(cit.doi)}" rel="noopener">doi:${esc(cit.doi)}</a>`;
  else if (cit.url) s += ` <a href="${esc(cit.url)}" rel="noopener">${esc(hostOf(cit.url))}</a>`;
  return s;
}

export function hostOf(url) {
  try { return new URL(url).host.replace(/^www\./, ""); } catch { return url; }
}

export function setFooter(d) {
  const el = document.getElementById("release");
  if (el) el.textContent = `Release ${d.release.version} · ${formatDate(d.release.date)}`;
}

export function formatDate(iso) {
  if (!iso) return "—";
  const [y, m, day] = iso.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, day)).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
}

export function capturesOf(d, cohortId) { return d.captures.filter(c => c.cohort === cohortId); }

// ---------------------------------------------------------------- detail dialog

function dialogEl() {
  let dlg = document.getElementById("detail");
  if (!dlg) {
    dlg = document.createElement("dialog");
    dlg.id = "detail";
    dlg.className = "detail";
    dlg.setAttribute("aria-labelledby", "detail-title");
    document.body.appendChild(dlg);
    dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
  }
  return dlg;
}

function openDialog(title, sub, body) {
  const dlg = dialogEl();
  dlg.innerHTML = `<div class="detail-head"><div>${sub ? `<div class="muted small">${sub}</div>` : ""}<h2 id="detail-title">${title}</h2></div>
    <button class="close" type="button" aria-label="Close">×</button></div><div class="detail-body">${body}</div>`;
  dlg.querySelector(".close").addEventListener("click", () => dlg.close());
  dlg.querySelectorAll("[data-open-cohort]").forEach(b => b.addEventListener("click", () => showCohort(cache, b.dataset.openCohort)));
  if (!dlg.open) dlg.showModal();
  dlg.querySelector(".detail-body").scrollTop = 0;
}

function kv(rows) {
  const items = rows.filter(([, v]) => v !== undefined && v !== null && v !== "").map(([k, v]) => `<dt>${esc(k)}</dt><dd>${v}</dd>`);
  return items.length ? `<dl class="kv">${items.join("")}</dl>` : "";
}

function linkButton(label, url, note) {
  if (!url) return `<span class="unavailable">${esc(label)}: ${esc(note || "not located")}</span>`;
  return `<a href="${esc(url)}" rel="noopener" target="_blank">${esc(label)} <span aria-hidden="true">↗</span></a>`;
}

const FIELD_NAMES = { patient: "Patient", donor_mapping: "Patient mapping", diagnosis: "Diagnosis", site: "Site", treatment: "Treatment",
  he_mpp: "H&E pixel size", he_mpp_basis: "Pixel-size basis", geometry_check: "Frame check", image_level: "Image level", he_file: "H&E file",
  links: "Data links", tier_reason: "Tier reason", "clinical.subsite": "Subsite", "clinical.grade": "Grade", "clinical.stage": "Stage", "clinical.response": "Response label" };

function subsetText(x) {
  return Object.entries(x).map(([k, v]) => `${k.replace(/_/g, " ")} ${v}`).join(", ");
}

// A frame or geometry check in words: positions inside the image frame, the scale used, and what it does not establish.
export function geometryText(g) {
  const frame = "positions_outside_preview" in g ? "preview" : "original image";
  const out = g.positions_outside_preview ?? g.positions_outside_original;
  const bits = [g.in_tissue_positions ? `${fmt(g.in_tissue_positions)} in-tissue positions` : "", g.finite_positions ? "all coordinates finite" : "",
    out === 0 ? `all inside the ${frame} frame` : out != null ? `${fmt(out)} outside the ${frame} frame` : "",
    g.supplied_scale_matches_original_dimensions ? "the supplied scale matches the original dimensions" : "",
    g.preview_scale ? `preview scale ${g.preview_scale}` : ""].filter(Boolean);
  return `${bits.join("; ")}. Not a registration sign-off.`.replace(/^./, m => m.toUpperCase());
}

export function showCapture(d, id) {
  const c = d.captures.find(x => x.id === id);
  if (!c) return;
  const cohort = d.cohortById.get(c.cohort);
  const raw = (c.links.raw || []);
  const links = [
    linkButton(c.image_level === "preview" ? "Preview image" : "Original H&E", c.links.he),
    linkButton("Expression matrix", c.links.expression),
    linkButton("Coordinates", c.links.coordinates),
    ...raw.slice(0, 3).map((u, i) => linkButton(raw.length > 1 ? `Raw data ${i + 1}` : "Raw data", u)),
  ].join("");
  const clin = c.clinical || {};
  const body = `
    <div class="chips" style="margin-bottom:1rem">${chip("imageLevel", c.image_level)} ${chip("tier", c.tier)} ${chip("treatment", c.treatment, `Treatment: ${c.treatment}`)} ${chip("site", c.site, `Site: ${c.site}`)} ${chip("verification", c.verification)}</div>
    ${kv([
      ["Cohort", `<button class="btn small" type="button" data-open-cohort="${esc(c.cohort)}">${esc(cohort?.label ?? c.cohort)}</button>`],
      ["Cancer", esc(cancerName(d, c.cancer))],
      ["Histology stratum", esc(stratumLabel(d, c.stratum))],
      ["Patient (source ID)", c.patient ? `${esc(c.patient)}${c.donor_mapping ? `<span class="cell-sub">${esc(LABELS.donorMapping[c.donor_mapping])}</span>` : ""}` : esc(c.donor_mapping ? LABELS.donorMapping[c.donor_mapping] : "Not stated")],
      ["Capture (source ID)", `<span class="mono">${esc(c.capture)}</span>`],
      ["Accession", c.accession ? `<span class="mono">${esc(c.accession)}</span>` : ""],
      ["Source sample name", c.source_name && c.source_name !== c.capture ? esc(c.source_name) : ""],
      ["Diagnosis (source)", esc(c.diagnosis)],
      ["Histology (source)", c.histology !== c.diagnosis ? esc(c.histology) : ""],
      ["Site (source wording)", esc(c.site_source)],
      ["Tissue", c.compartment && !["primary-tumour", "metastatic-tumour"].includes(c.compartment) ? esc(LABELS.compartment[c.compartment] ?? c.compartment) : ""],
    ])}
    <h3 class="section-title">Data</h3>
    <div class="links">${links}</div>
    ${kv([
      ["Image level", `${esc(LABELS.imageLevel[c.image_level])}<span class="cell-sub">${esc(LABELS.imageLevelNote[c.image_level])}</span>`],
      ["Shared assay area", c.assay_area_id ? `<span class="mono">${esc(c.assay_area_id)}</span><span class="cell-sub">Several sections share this array area; use only this section's expression subset${c.expression_subset ? ` (${esc(subsetText(c.expression_subset))})` : ""}${c.region_label ? ` (source region ${esc(c.region_label)})` : ""}.</span>` : ""],
      ["Expression subset", !c.assay_area_id && c.expression_subset ? `${esc(subsetText(c.expression_subset))}<span class="cell-sub">These rows of the source object belong to this section.</span>` : ""],
      ["Technique", esc(c.technique)],
      ["Preservation", esc(c.preservation)],
      ["H&E–RNA linkage", esc(LABELS.linkage[c.linkage] ?? c.linkage)],
      ["H&E resolution", c.he_mpp ? `${c.he_mpp} µm/pixel <span class="cell-sub">${esc(c.he_mpp_basis || "")}</span>` : esc(c.he_mpp_basis || "Unknown")],
      ["H&E file", c.he_file ? `<span class="mono">${esc(c.he_file)}</span>` : ""],
      ["Expression data", esc(c.expression_type)],
      ["Frame check", c.geometry_check ? esc(geometryText(c.geometry_check)) : ""],
      ["Out-of-tissue spots", c.out_of_tissue_expression_spots ? `${fmt(c.out_of_tissue_expression_spots)}<span class="cell-sub">Expression spots outside the tissue; filter them explicitly.</span>` : ""],
      ["Registration", esc(c.registration)],
      ["Access", `H&E: ${esc(LABELS.access[c.access.he])} · processed data: ${esc(LABELS.access[c.access.processed])} · raw reads: ${esc(LABELS.access[c.access.raw])}`],
    ])}
    <h3 class="section-title">Curation</h3>
    ${kv([
      ["Capture tier", `${esc(LABELS.tier[c.tier])}${c.tier_reason ? `<span class="cell-sub">${esc(c.tier_reason)}</span>` : ""}`],
      ["Treatment before sampling", `${esc(c.treatment)}${c.treatment_note ? `<span class="cell-sub">${esc(c.treatment_note)}</span>` : ""}`],
      ["Verification", esc(LABELS.verification[c.verification])],
      ["Sampled recurrence", c.sampled_recurrence ? "Yes: a recurrent tumour sector, kept apart from the primary sectors" : ""],
      ["Recurrence (later outcome)", c.recurrence_outcome ? esc(c.recurrence_outcome === "N" ? "No recurrence reported" : c.recurrence_outcome) : ""],
      ["Original image match", c.original_crosswalk_inferred === true ? "Inferred from crossed labels; held at preview level" : ""],
    ])}
    ${c.open_checks && c.open_checks.length ? `<h3 class="section-title">Open checks for this section</h3><ul class="notes">${c.open_checks.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
    ${c.field_sources && Object.keys(c.field_sources).length ? `<h3 class="section-title">Evidence for reviewed fields</h3><ul class="notes">${Object.entries(c.field_sources).map(([f, u]) => `<li>${esc(FIELD_NAMES[f] ?? f)}: <a href="${esc(u)}" rel="noopener" target="_blank">${esc(hostOf(u))}</a></li>`).join("")}</ul>` : ""}
    <h3 class="section-title">Clinical fields reported by the source</h3>
    ${kv([["Age", esc(clin.age)], ["Sex", esc(clin.sex)], ["Stage / TNM", esc(clin.stage)], ["Grade", esc(clin.grade)], ["Subsite", esc(clin.subsite)], ["Markers", esc(clin.markers)],
      ["Response label", clin.response ? `${esc(clin.response)}<span class="cell-sub">As labelled by the source; it does not show when the sample was taken relative to treatment.</span>` : ""]]) || '<p class="muted small">None extracted for this section.</p>'}
    <p class="muted small">Values are copied from the source with their original wording; missing fields were not reported or not extracted. Consult the source tables before analysis.</p>`;
  openDialog(esc(c.capture), esc(`${cancerName(d, c.cancer)} · ${cohort?.label ?? c.cohort}`), body);
}

export function cohortCounts(d, cohort) {
  const caps = capturesOf(d, cohort.id);
  if (!caps.length) return null;
  const core = caps.filter(c => c.tier === "core");
  return { all: tally(caps), core: tally(core), coreUntreated: tally(core.filter(c => c.treatment === "Untreated")),
    original: tally(caps.filter(c => c.image_level === "original")), preview: tally(caps.filter(c => c.image_level === "preview")) };
}

export function showCohort(d, id) {
  const c = d.cohortById.get(id);
  if (!c) return;
  const counts = cohortCounts(d, c);
  const links = (c.access.links || []).map(([label, url]) => linkButton(label, url)).join("");
  const related = (c.related_citations || []).map(x => `<li>${citationText(x)}</li>`).join("");
  const derived = (c.derived_from || []).map(x => `<button class="btn small" type="button" data-open-cohort="${esc(x)}">${esc(d.cohortById.get(x)?.label ?? x)}</button>`).join(" ");
  let countHtml = "";
  if (counts) {
    const both = counts.original.captures && counts.preview.captures;
    countHtml = `<div class="table-wrap"><table><thead><tr><th>Subset</th><th class="num">Known patients</th><th class="num">Sections</th></tr></thead><tbody>
      <tr><td>All catalogued sections</td><td class="num">${counts.all.patients}</td><td class="num">${counts.all.captures}</td></tr>
      ${both ? `<tr><td>… with original H&amp;E</td><td class="num">${counts.original.patients}</td><td class="num">${counts.original.captures}</td></tr>
      <tr><td>… with a preview image only</td><td class="num">${counts.preview.patients}</td><td class="num">${counts.preview.captures}</td></tr>` : ""}
      <tr><td>Core primary</td><td class="num">${counts.core.patients}</td><td class="num">${counts.core.captures}</td></tr>
      <tr><td>Core primary, untreated</td><td class="num">${counts.coreUntreated.patients}</td><td class="num">${counts.coreUntreated.captures}</td></tr>
      </tbody></table></div><p class="muted small">Computed from the section records in this release. Known patients are study-local patient IDs given by the source, counted once per study${counts.all.unknown ? `; ${fmt(counts.all.unknown)} ${counts.all.unknown === 1 ? "section has" : "sections have"} no patient ID and ${counts.all.unknown === 1 ? "is" : "are"} not counted as patients` : ""}. Sections are records of this study, not globally unique physical sections, and they are not eligible-patient counts.</p>`;
  } else if (countedPreview(d, c)) {
    countHtml = `<p class="small"><strong class="num">${fmt(countedPreview(d, c))}</strong> checked section packages with a preview image: their expression barcodes match their tissue coordinates, but they are not yet listed as individual section records, so no patients are counted.</p>`;
  }
  const reported = (c.reported || []).map(([n, unit, basis, scope]) => `<li><strong class="num">${fmt(n)}</strong> ${esc(unit)} <span class="muted">(${esc(basis)}${scope ? `; ${esc(scope)}` : ""})</span></li>`).join("");
  const sr = c.spatial_review;
  const ids = sr ? Object.entries(sr.sample_ids || {}).map(([k, v]) => `${esc(LABELS.sampleIds[k] ?? k)}: <span class="mono">${esc(v.join(", "))}</span>`).join("<br>") : "";
  const reviewHtml = sr ? `<h3 class="section-title">Spatial review</h3>
    ${kv([
      ["Analysis scope", esc(LABELS.spatialScope[sr.analysis_cohort] ?? sr.analysis_cohort)],
      ["Assay class", esc(sr.assay_classes.map(a => LABELS.assayClass[a] ?? a).join("; "))],
      ["Platform (as reported)", esc(sr.platform)],
      ["Role", esc(sr.role)],
      ["Images", esc(sr.image_status)],
      ["Treatment", `${esc(LABELS.treatmentClass[sr.treatment_class])}${sr.treatment_status && sr.treatment_status !== "unknown" ? `<span class="cell-sub">${esc(sr.treatment_status)}</span>` : ""}`],
      ["Sample identifiers", ids],
      ["Specimen", esc([sr.specimen, sr.block && `block ${sr.block}`, sr.slide && `slide ${sr.slide}`, sr.reported_gleason && `Gleason ${sr.reported_gleason}`, sr.reported_stage && `stage ${sr.reported_stage}`].filter(Boolean).join("; "))],
      ["Eligible patients", "Unknown: no patient is promoted into the strict core by this review"],
    ])}${sr.route_review ? `<h3 class="section-title">Public-route review</h3>
    ${kv([
      ["Status", esc(sr.route_review.status)],
      ["Open dependencies", esc(sr.route_review.states.map(x => LABELS.routeState[x] ?? x).join("; "))],
      ["Next step", esc(sr.route_review.next_step)],
      ["Section packages checked", sr.route_review.sections_with_matching_coordinates ? `${fmt(sr.route_review.sections_with_matching_coordinates)}<span class="cell-sub">sections whose expression barcodes match their tissue coordinates exactly; not a patient count or final QC</span>` : "Not part of this check"],
    ])}` : ""}` : "";
  const b = c.backlog_review;
  const backlogHtml = b ? `<h3 class="section-title">Package review${c.followup_review?.outcome ? " (earlier result)" : ""}</h3>
    ${kv([
      ["Result", esc(LABELS.backlogOutcome[b.outcome] ?? b.outcome)],
      ["How far it was checked", esc(b.depth)],
      ["Images", esc(b.image_finding)],
      ["Expression and coordinates", esc(b.molecular_finding)],
      ["Section records listed", b.sections_listed ? `${fmt(b.sections_listed)}<span class="cell-sub">${esc(levelText(d, c))}</span>` : "None"],
      ["Open dependencies", esc(b.states.map(x => LABELS.routeState[x] ?? x).join("; "))],
      ["Next step", esc(b.next_step)],
      ["Eligible patients", "Unknown: no patient is promoted into the strict core by this review"],
    ])}` : "";
  const f = c.followup_review;
  const followupHtml = f ? `<h3 class="section-title">Follow-up review</h3>
    ${kv([
      ["Result", f.outcome ? esc(LABELS.followupOutcome[f.outcome] ?? f.outcome) : "Checked again; no change"],
      ["How far it was checked", esc(f.depth || "")],
      ["Findings", esc(f.findings || "")],
      ["Checks", f.checks && f.checks.length ? `<ul class="notes">${f.checks.map(x => `<li><strong>${esc(x.check)}:</strong> ${esc(x.result)} <span class="muted">(${esc(x.depth)})</span></li>`).join("")}</ul>` : ""],
      ["Open dependencies", f.states ? esc(f.states.map(x => LABELS.routeState[x] ?? x).join("; ")) : ""],
      ["Next step", esc(f.next_step || "")],
    ])}` : "";
  const level = c.status === "verified" || c.status === "preview" ? `<p class="small">${esc(LABELS.imageLevelNote[c.status === "verified" ? "original" : "preview"])}${levelText(d, c) ? ` <strong>${esc(levelText(d, c))}.</strong>` : ""}</p>` : "";
  const body = `
    <div class="chips" style="margin-bottom:1rem">${chip("status", c.status)} ${chip("access", c.access.category)} ${chip("verification", c.verification)}</div>
    ${level}
    ${c.description ? `<p>${esc(c.description)}</p>` : ""}
    <h3 class="section-title">Source</h3>
    <p class="small">${citationText(c.citation)}</p>
    ${related ? `<ul class="notes">${related}</ul>` : ""}
    ${kv([
      ["Cancers", esc(c.cancers.map(x => cancerName(d, x)).join(", "))],
      ["Data layer", esc(LABELS.layer[c.layer])],
      ["Modalities", esc((c.modalities || []).map(m => LABELS.modality[m] ?? m).join(", "))],
      ["Techniques", esc((c.techniques || []).join(", "))],
      ["Preservation", esc((c.preservation || []).join(", "))],
      ["Specimens", esc(LABELS.specimen[c.specimen] ?? c.specimen)],
      ["Tissue compartments", esc((c.compartments || []).map(x => LABELS.compartment[x] ?? x).join(", "))],
      ["Modality linkage", esc(LABELS.linkage[c.linkage] ?? c.linkage)],
      ["Accession", c.accession ? `<span class="mono">${esc(c.accession)}</span>` : ""],
      ["Derived from", derived],
      ["Verification", esc(LABELS.verification[c.verification])],
    ])}
    ${c.tcga_project ? tcgaSection(d, c.tcga_project) : ""}
    ${reviewHtml}
    ${followupHtml}
    ${backlogHtml}
    ${c.gates && c.gates.length ? `<h3 class="section-title">${c.status === "screened" ? "Checks still open" : "Open checks before inclusion"}</h3><ul class="notes">${c.gates.map(g => `<li>${esc(LABELS.gate[g] ?? g)}</li>`).join("")}</ul>` : ""}
    <h3 class="section-title">Access</h3>
    <p class="small">${chip("access", c.access.category)} ${esc(c.access.route || "")}</p>
    <div class="links">${links || '<span class="unavailable">No data link recorded</span>'}</div>
    ${countHtml ? `<h3 class="section-title">Catalogued spatial transcriptomics sections</h3>${countHtml}` : ""}
    ${reported ? `<h3 class="section-title">Counts reported by the source</h3><ul class="notes">${reported}</ul><p class="muted small">Reported counts describe the source as published. They are not deduplicated or checked for eligibility.</p>` : ""}
    ${!countHtml && !reported ? `<p class="muted small">No counts are given for this entry in this release.</p>` : ""}
    ${c.notes && c.notes.length ? `<h3 class="section-title">Notes</h3><ul class="notes">${c.notes.map(n => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}
    <p class="muted small">Listing in the explorer does not mean that access has been granted or requested.</p>`;
  openDialog(esc(c.label), esc(LABELS.layer[c.layer]), body);
}

export function rationale(c) {
  if (c.group === "hausser") return LABELS.hausser[c.hausser];
  if (c.rationale) return c.rationale;
  if (c.group === "tcga-panel") return `Molecular screen; ${LABELS.hausser[c.hausser].replace(/^./, m => m.toLowerCase())}`;
  if (c.group === "pooled") return `Pooled analysis cohort (${(c.includes || []).join(" + ")})`;
  return "Separate published archetype study";
}

// ---------------------------------------------------------------- TCGA molecular screen

export function tcgaPasses(d, project) {
  const c = d.tcgaCounts[project];
  return c && c.post_qc.union >= d.tcgaMeta.rule.min_total && c.post_qc.paired >= d.tcgaMeta.rule.min_paired;
}

// Analysis group of a project at the assay stage (CRC pools COAD and READ).
export function tcgaGroup(d, project) {
  const g = d.tcgaCounts[project] && d.tcgaCounts[project].group;
  return g ? { id: g, ...d.tcga_counts.groups[g] } : null;
}

export function cohortName(d, id) {
  if (!id) return "";
  const c = d.elig.cohorts[id];
  return c && c.label !== id ? `${id}: ${c.label}` : (d.cancerByCode.get(id)?.name ? `${id}: ${d.cancerByCode.get(id).name}` : id);
}

export function tcgaSection(d, project, { heading = true } = {}) {
  const c = d.tcgaCounts[project];
  if (!c) return "";
  const r = d.tcgaMeta.rule;
  const row = (label, x, cls = "") => `<tr${cls}><td>${label}</td><td class="num">${fmt(x.union)}</td><td class="num">${fmt(x.paired)}</td><td class="num">${fmt(x.rna_only)}</td><td class="num">${fmt(x.met_only)}</td></tr>`;
  const al = c.aliquots.tumour, an = c.aliquots.normal;
  const flagged = ["rna", "met"].map(l => `${l === "rna" ? "RNA-seq" : "450k"}: ${al[l].excluded} excluded, ${al[l].unresolved} unresolved of ${al[l].retained + al[l].excluded + al[l].unresolved}`).join(" · ");
  const h = c.historical_matrix;
  const histDiff = h && (h.union !== c.post_qc.union || h.paired !== c.post_qc.paired);
  const e = d.elig && d.elig.projects[project];
  const grp = tcgaGroup(d, project);
  const excluded = !!(e && e.excluded_from_study);
  const cohort = e && e.analysis_cohort ? d.elig.cohorts[e.analysis_cohort] : null;
  const pooled = !!(cohort && cohort.projects.length > 1);
  const lay = x => ({ union: x.total, paired: x.paired, rna_only: x.rna_only, met_only: x.met_only });
  const withheld = e ? e.assay_qc.total - e.after_patient_screen.total : 0;
  const dispText = e ? Object.entries(e.dispositions).filter(([k]) => k !== "pass_annotation_screen")
    .map(([k, v]) => `${v} ${LABELS.dispositionShort[k].toLowerCase()}`).join(", ") : "";
  const n = e && e.normal;
  const chipHtml = excluded ? `<span class="chip">Meets the screen</span> <span class="chip eosin">Excluded from the study panel</span>`
    : tcgaPasses(d, project) ? `<span class="chip ok">Meets the screen</span>`
    : grp && grp.passes_screen && grp.projects.length > 1 ? `<span class="chip">Below the screen on its own</span> <span class="chip ok">Pooled ${esc(grp.id)} meets it</span>`
    : `<span class="chip">Below the screen</span>`;
  const roleChip = cohort && cohort.role !== "discovery" ? ` <span class="chip accent">${esc(LABELS.role[cohort.role])}</span>` : "";
  const outside = n && n.outside_cohort && n.outside_cohort.length ? n.outside_cohort : [];
  return `${heading ? `<h3 class="section-title">TCGA molecular screen</h3>` : ""}
    <p class="small">${chipHtml}${roleChip} Rule: at least ${r.min_total} patients with primary-tumour RNA-seq and/or 450k, and ${r.min_paired} with both, after assay exclusions${grp && grp.projects.length > 1 ? `, applied to the pooled ${esc(grp.id)} cohort (${grp.projects.map(x => `TCGA-${x}`).join(" + ")})` : ""}.</p>
    ${excluded ? `<p class="callout small">TCGA-${esc(project)} is excluded from the study panel: ${esc(LABELS.projectExclusion[e.exclusion_reason] ?? e.exclusion_reason)}. No patient is selected; its counts are kept for provenance and its assay states are unchanged.</p>` : ""}
    <div class="table-wrap"><table class="compact"><thead><tr><th>Primary tumour, unique patients</th><th class="num">RNA and/or 450k</th><th class="num">Both</th><th class="num">RNA only</th><th class="num">450k only</th></tr></thead><tbody>
      ${row("Before assay exclusions", c.pre_qc)}
      ${row("After assay exclusions (quality-covered)", c.post_qc)}
      ${e ? row("After the patient treatment and diagnosis screen", lay(e.after_patient_screen)) : ""}
      ${e && !excluded ? row(pooled ? `<strong>Contribution to the pooled ${esc(e.analysis_cohort)} cohort</strong>` : `<strong>Selected analysis set${e.analysis_cohort !== project ? ` (${esc(e.analysis_cohort)})` : ""}</strong>`, lay(e.selected_analysis)) : ""}
      ${pooled ? row(`<a href="cancers.html?c=${esc(e.analysis_cohort)}">Pooled ${esc(e.analysis_cohort)} cohort, all contributing projects</a>`, lay(cohort.selected_analysis)) : ""}
    </tbody></table></div>
    ${e ? `<p class="small" style="margin-top:.5rem">${withheld ? `The patient screen withholds ${withheld} of ${fmt(e.assay_qc.total)} tumour patients: ${esc(dispText)}.` : `The patient screen withholds no tumour patient in this project.`}
      ${excluded ? "" : pooled ? ` TCGA-${esc(project)} patients count once, inside the pooled ${esc(e.analysis_cohort)} cohort; project counts are provenance, not a separate cohort.` : e.analysis_cohort !== project ? ` The selected set is the histology-defined ${esc(e.analysis_cohort)} cohort${e.after_patient_screen.total > e.selected_analysis.total ? `; ${fmt(e.after_patient_screen.total - e.selected_analysis.total)} patients passing the screen have another histology and stay outside it, with their assays unchanged` : ""}.` : ""} Reasons can overlap; each patient is counted once under its main disposition.</p>` : ""}
    <div class="table-wrap" style="margin-top:.6rem"><table class="compact"><thead><tr><th>Normal reference, unique patients</th><th class="num">Normal RNA + H&amp;E</th><th class="num">Normal with 450k</th></tr></thead><tbody>
      <tr><td>Same-sample normal RNA and H&amp;E, after assay exclusions</td><td class="num">${fmt(c.normal.rna_he)}</td><td class="num">${fmt(c.normal.rna_he_met)}</td></tr>
      ${n ? `<tr><td><strong>… after the patient screen${n.in_active_scope ? "" : " (outside active totals)"}</strong>${n.withheld.length ? `<span class="cell-sub">Withheld: ${esc(n.withheld.join(", "))}</span>` : ""}${outside.length ? `<span class="cell-sub">${outside.length} ${outside.length === 1 ? "donor is" : "donors are"} outside the ${esc(e.analysis_cohort)} cohort: ${esc(outside.map(p => n.outside_cohort_histology ? `${p} (${LABELS.histStratum[n.outside_cohort_histology[p]] ?? n.outside_cohort_histology[p]})` : p).join(", "))}</span>` : ""}</td><td class="num">${fmt(n.rna_he_after)}</td><td class="num">${fmt(n.rna_he_met_after)}</td></tr>
      ${Object.entries(n.context).map(([k, v]) => `<tr><td class="small">Donor context: ${esc(LABELS.normalContext[k])}</td><td class="num">${fmt(v)}</td><td class="num">${fmt(n.context_met[k] || 0)}</td></tr>`).join("")}` : ""}
    </tbody></table></div>
    <p class="muted small" style="margin-top:.5rem">Aliquots, primary tumour: ${esc(flagged)}. Normal: ${an.rna.excluded + an.met.excluded} excluded, ${an.rna.unresolved + an.met.unresolved} unresolved.
      ${h ? ` Historical PanCanAtlas matrices: ${fmt(h.union)} patients with RNA-seq and/or 450k, ${fmt(h.paired)} with both${histDiff ? ", which differs from current GDC files; do not mix the two" : ", matching current GDC files"}.` : ""}
      ${e ? `Treatment and diagnosis annotations were reviewed for every retained patient.` : ""} ${e && e.histology_reviewed ? "Histology was assigned from publication tables and GDC labels, not a new slide review; tumour" : "Histology strata for this project, tumour"} slide linkage and image QC are not yet checked. Normal tissue comes from cancer patients and is not a healthy-donor control; tumour and normal patients overlap and are not additive.${outside.length ? ` Project-level normal counts include donors outside the selected cohort; the cohort's own normal reference is shown with the cohort.` : ""}</p>`;
}

const annValue = (f, v) => v === null || v === undefined ? (f === "site_reported" ? "Not reported" : "No publication record")
  : v === "" ? "Blank in the publication table" : v === true ? "Yes" : v === false ? "No"
  : f === "histology_stratum" || f === "molecular_group" ? (LABELS.histStratum[v] ?? v) : String(v);

// Subsets, reviewed strata, publication–GDC label differences and annotations of one analysis cohort.
export function cohortExtras(d, id) {
  const c = d.elig.cohorts[id];
  if (!c) return "";
  const lay = x => `<td class="num">${fmt(x.total)}</td><td class="num">${fmt(x.paired)}</td><td class="num">${fmt(x.rna_only)}</td><td class="num">${fmt(x.met_only)}</td>`;
  const multi = c.projects.length > 1;
  const subsets = c.subsets ? `<h3>Subsets within the ${esc(id)} cohort</h3>
    <div class="table-wrap"><table class="compact"><thead><tr><th>Subset</th><th class="num">Patients</th><th class="num">Both</th><th class="num">RNA only</th><th class="num">450k only</th></tr></thead><tbody>
    <tr><td><strong>${esc(id)}, all selected patients</strong></td>${lay(c.selected_analysis)}</tr>
    ${c.subsets.map(x => `<tr><td>${esc(x.label)} <a class="small" href="explore.html?view=tcga&subset=${esc(x.id)}">browse</a></td>${lay(x)}</tr>`).join("")}
    </tbody></table></div><p class="muted small" style="margin-top:.4rem">Subsets are sensitivity or benchmark analyses inside the cohort. Their patients are already counted in the cohort and are never added to panel totals.</p>` : "";
  const strata = c.strata ? `<h3>${id === "GLIOMA" ? "Published molecular groups by project" : "Reviewed histology"}</h3>
    <div class="table-wrap"><table class="stack compact"><thead><tr><th scope="col">${id === "GLIOMA" ? "Group" : "Histology"}</th>${multi ? '<th scope="col">Project</th>' : ""}<th scope="col" class="num">Passing the patient screen</th><th scope="col" class="num">Both</th><th scope="col" class="num">RNA only</th><th scope="col" class="num">450k only</th><th scope="col" class="num">In publication table</th><th scope="col" class="num">In cohort</th></tr></thead><tbody>
    ${c.strata.map(x => `<tr><td class="primary" data-label="${id === "GLIOMA" ? "Group" : "Histology"}"><div>${esc(annValue("histology_stratum", x.stratum))}</div></td>${multi ? `<td data-label="Project"><div>TCGA-${esc(x.project)}</div></td>` : ""}<td class="num" data-label="Patients"><div>${fmt(x.total)}</div></td><td class="num" data-label="Both"><div>${fmt(x.paired)}</div></td><td class="num" data-label="RNA only"><div>${fmt(x.rna_only)}</div></td><td class="num" data-label="450k only"><div>${fmt(x.met_only)}</div></td><td class="num" data-label="In publication table"><div>${fmt(x.publication_members)}</div></td><td class="num" data-label="In cohort"><div>${fmt(x.selected)}</div></td></tr>`).join("")}
    </tbody><caption>${id === "GLIOMA" ? "Groups from the TCGA pan-glioma study, kept as annotations. Selected membership is not split by group, and an unassigned group is not the same as an unknown IDH status." : "Publication histology where the case is in the publication table, otherwise the GDC label. Patients outside the cohort keep their valid assays."}</caption></table></div>` : "";
  const conflicts = c.projects.flatMap(p => (d.elig.projects[p].label_conflicts || []).map(x => ({ ...x, project: p })));
  const conflictHtml = conflicts.length ? `<details class="disclosure"><summary>${conflicts.length} ${conflicts.length === 1 ? "case where" : "cases where"} publication and GDC histology differ</summary>
    <ul class="notes">${conflicts.map(x => `<li><a class="mono" href="explore.html?view=tcga&open=${esc(x.patient)}">${esc(x.patient)}</a>: GDC ${esc(x.gdc ?? "no label")} → publication ${esc(x.publication ?? "no record")} · ${x.selected ? "in cohort" : "outside cohort"}</li>`).join("")}</ul></details>` : "";
  const ann = c.annotations ? `<details class="disclosure"><summary>Annotations of the ${fmt(c.selected_analysis.total)} selected patients</summary>
    <div class="ann-grid">${Object.entries(c.annotations).map(([f, vals]) => `<div class="table-wrap"><table class="compact"><thead><tr><th>${esc(LABELS.annotationField[f] ?? f)}</th><th class="num">Patients</th><th class="num">Both</th></tr></thead><tbody>
      ${vals.map(([v, n, b]) => `<tr><td>${esc(annValue(f, v))}</td><td class="num">${fmt(n)}</td><td class="num">${fmt(b)}</td></tr>`).join("")}</tbody></table></div>`).join("")}</div>
    <p class="muted small">Values are shown as recorded. A blank publication field and a patient absent from the publication table are kept apart.</p></details>` : "";
  let normal = "";
  if (!multi) {
    const pn = d.elig.projects[c.projects[0]].normal, cn = c.normal;
    if (pn.outside_cohort && pn.outside_cohort.length) normal = `<h3>Normal reference of the ${esc(id)} cohort</h3>
      <div class="table-wrap"><table class="compact"><thead><tr><th>Normal RNA + H&amp;E, unique patients</th><th class="num">Patients</th><th class="num">… with 450k</th></tr></thead><tbody>
      <tr><td><strong>${esc(id)} donors, after the patient screen</strong></td><td class="num">${fmt(cn.rna_he_after)}</td><td class="num">${fmt(cn.rna_he_met_after)}</td></tr>
      <tr><td class="small">TCGA-${esc(c.projects[0])} project, all donors</td><td class="num">${fmt(pn.rna_he_after)}</td><td class="num">${fmt(pn.rna_he_met_after)}</td></tr>
      </tbody></table></div><p class="muted small" style="margin-top:.4rem">${pn.outside_cohort.length} project-level normal ${pn.outside_cohort.length === 1 ? "package comes" : "packages come"} from ${pn.outside_cohort.length === 1 ? "a donor" : "donors"} outside the ${esc(id)} cohort${pn.outside_cohort_histology ? ` (${esc(pn.outside_cohort.map(p => `${p}: ${LABELS.histStratum[pn.outside_cohort_histology[p]] ?? pn.outside_cohort_histology[p]}`).join("; "))})` : ""}; ${pn.outside_cohort.length === 1 ? "it is" : "they are"} labelled separately and not used as matched ${esc(id)} controls.</p>`;
  }
  return subsets + strata + conflictHtml + ann + normal;
}

// Pooled analysis cohort (CRC from COAD and READ, GLIOMA from LGG and GBM).
export function pooledCohortSection(d, id) {
  const c = d.elig.cohorts[id];
  if (!c) return "";
  const r = d.tcgaMeta.rule;
  const g = d.tcga_counts.groups[id];
  const sum = (stage) => c.projects.reduce((a, p) => { const x = d.elig.projects[p][stage]; ["total", "paired", "rna_only", "met_only", "rna", "met"].forEach(k => a[k] = (a[k] || 0) + x[k]); return a; }, {});
  const row = (label, x) => `<tr><td>${label}</td><td class="num">${fmt(x.total)}</td><td class="num">${fmt(x.rna)}</td><td class="num">${fmt(x.met)}</td><td class="num">${fmt(x.paired)}</td><td class="num">${fmt(x.rna_only)}</td><td class="num">${fmt(x.met_only)}</td></tr>`;
  const head = `<thead><tr><th>Unique patients</th><th class="num">RNA-seq and/or 450k</th><th class="num">RNA-seq</th><th class="num">450k</th><th class="num">Both</th><th class="num">RNA only</th><th class="num">450k only</th></tr></thead>`;
  const n = c.normal;
  const sites = Object.entries(c.reported_sites || {});
  const other = (n.context.non_target_or_uncertain_or_recurrent_donor || 0), unreported = (n.context.normal_only_donor_primary_diagnosis_unreported || 0);
  return `<p class="small">${g && g.passes_screen ? '<span class="chip ok">Pooled cohort meets the screen</span>' : '<span class="chip">Below the screen</span>'}${c.role !== "discovery" ? ` <span class="chip accent">${esc(LABELS.role[c.role])}</span>` : ""}
      Rule: at least ${r.min_total} patients with RNA-seq and/or 450k and ${r.min_paired} with both after assay exclusions, applied to the pooled cohort (${c.projects.map(p => `TCGA-${esc(p)}`).join(" + ")}). Individual projects need not pass on their own.</p>
    <div class="table-wrap"><table class="compact">${head}<tbody>
      ${row("After assay exclusions", sum("assay_qc"))}
      ${row("After the patient treatment and diagnosis screen", sum("after_patient_screen"))}
      ${row(`<strong>Selected ${esc(id)} cohort</strong>`, c.selected_analysis)}
      ${c.projects.map(p => row(`<span class="cell-sub" style="margin:0">… submitted as TCGA-${esc(p)} (provenance)</span>`, c.contributions[p])).join("")}
    </tbody></table></div>
    <p class="small" style="margin-top:.5rem">Each patient is counted once. Contributions by submitted project are provenance counts${id === "CRC" ? ", not adjudicated colon and rectum strata" : ""}.</p>
    ${c.withheld && c.withheld.length ? `<details class="disclosure"><summary>${c.withheld.length} patients with retained tumour assays withheld by the patient screen</summary><ul class="notes">${c.withheld.map(w => `<li><a class="mono" href="explore.html?view=tcga&open=${esc(w.patient)}">${esc(w.patient)}</a> · TCGA-${esc(w.project)} · ${esc(LABELS.disposition[w.disposition])}</li>`).join("")}</ul></details>` : ""}
    ${cohortExtras(d, id)}
    ${c.site_overrides && c.site_overrides.length ? `<h3>Anatomical site corrections</h3>
      <div class="table-wrap"><table class="stack compact"><thead><tr><th scope="col">Patient</th><th scope="col">Submitted</th><th scope="col">Reported site (GDC)</th><th scope="col">Resection site (GDC)</th><th scope="col">Annotation override</th><th scope="col">In cohort</th></tr></thead><tbody>
      ${c.site_overrides.map(o => `<tr><td class="primary" data-label="Patient"><div><a class="mono" href="explore.html?view=tcga&open=${esc(o.patient)}">${esc(o.patient)}</a></div></td><td data-label="Submitted"><div>TCGA-${esc(o.project)}</div></td><td data-label="Reported site"><div>${esc(o.site_reported)}</div></td><td data-label="Resection site"><div>${esc(o.resection_site_reported)}</div></td><td data-label="Override"><div>${esc(LABELS.siteOverride[o.override] ?? o.override)}</div></td><td data-label="In cohort"><div>${o.selected ? `Yes (${esc(LABELS.tumourLayers[o.layers])})` : "No"}</div></td></tr>`).join("")}
      </tbody><caption>Case annotations identify the primary site for these patients. Reported GDC fields are kept as they are, including where they conflict with the annotation or with each other. These are site corrections, not duplicate patients.</caption></table></div>` : ""}
    ${sites.length ? `<details class="disclosure"><summary>Reported tumour site of the ${fmt(c.selected_analysis.total)} selected patients, by submitted project</summary>
      <div class="table-wrap" style="margin-top:.5rem"><table class="compact"><thead><tr><th>Reported site (GDC, not adjudicated)</th>${c.projects.map(p => `<th class="num">TCGA-${esc(p)}</th>`).join("")}</tr></thead><tbody>
      ${sites.map(([sname, v]) => `<tr><td>${esc(sname)}</td>${c.projects.map(p => `<td class="num">${fmt(v[p] || 0)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></details>` : ""}
    <div class="table-wrap" style="margin-top:.8rem"><table class="compact"><thead><tr><th>Normal reference, unique patients</th><th class="num">Normal RNA + H&amp;E</th><th class="num">… with 450k</th></tr></thead><tbody>
      <tr><td><strong>Pooled ${esc(id)}, after the patient screen</strong></td><td class="num">${fmt(n.rna_he_after)}</td><td class="num">${fmt(n.rna_he_met_after)}</td></tr>
      ${c.projects.map(p => `<tr><td class="small">… donors submitted as TCGA-${esc(p)}</td><td class="num">${fmt(d.elig.projects[p].normal.rna_he_after)}</td><td class="num">${fmt(d.elig.projects[p].normal.rna_he_met_after)}</td></tr>`).join("")}
      ${Object.entries(n.context).map(([k, v]) => `<tr><td class="small">Donor context: ${esc(LABELS.normalContext[k])}</td><td class="num">${fmt(v)}</td><td class="num">${fmt(n.context_met[k] || 0)}</td></tr>`).join("")}
    </tbody></table></div>
    <p class="muted small" style="margin-top:.5rem">Normal tissue comes from cancer patients, not healthy donors.${other ? ` ${other} normal donor${other > 1 ? "s carry" : " carries"} a recurrence or uncertain-diagnosis context.` : ""}${unreported ? ` ${unreported} normal package${unreported > 1 ? "s come" : " comes"} from normal-only donors without a reported primary diagnosis.` : ""}${other || unreported ? " Not all packages are verified matched controls." : ""} Treatment-flagged patients are not a treated reference set. Tumour slide linkage and image QC are not yet checked.</p>`;
}

export function showTcgaPatient(d, t, id) {
  const x = t.byId.get(id);
  if (!x) return;
  const st = (v) => chip("tcgaState", v);
  const flags = x.flags.map(f => {
    const why = [f.do_not_use && "Do_not_use", f.awg_pathology && `pathology group${f.pathology_reason ? `: ${f.pathology_reason}` : ""}`].filter(Boolean).join("; ");
    const ann = [["patient", f.patient_annotation], ["sample", f.sample_annotation], ["aliquot", f.aliquot_annotation]].filter(([, v]) => v);
    return `<li><span class="mono">${esc(f.aliquot)}</span> · ${esc(f.compartment === "tumour" ? "primary tumour" : "normal")} ${esc(f.layer === "rna" ? "RNA-seq" : "450k")} · ${chip("tcgaState", f.disposition)}
      <span class="cell-sub">${esc(f.disposition === "unresolved" ? "No exact aliquot and platform match in the quality annotations" : why)}${ann.length ? `. Annotations: ${esc(ann.map(([k, v]) => `${k} level: ${v}`).join("; "))}` : ""}.
      ${f.retained_layers_same_compartment.length ? ` Other retained layer in this compartment: ${esc(f.retained_layers_same_compartment.map(l => l === "rna" ? "RNA-seq" : "450k").join(", "))}.` : ""}</span></li>`;
  }).join("");
  const body = `
    <div class="chips" style="margin-bottom:1rem">${chip("tumourLayers", x.tumour_layers, `Tumour: ${LABELS.tumourLayers[x.tumour_layers]}`)} ${chip("disposition", x.disposition)} ${chip("normalRef", x.normal_ref)}</div>
    ${kv([
      ["Project", `TCGA-${esc(x.project)}`],
      ["Cancer page", `<a href="cancers.html?c=${esc(x.cancer)}">${esc(cancerName(d, x.cancer))}</a>${x.project === "PAAD" ? '<span class="cell-sub">TCGA-PAAD is not a curated conventional PDAC cohort.</span>' : ""}`],
      ["GDC case", `<a href="https://portal.gdc.cancer.gov/cases/${esc(x.case_id)}" rel="noopener" target="_blank">${esc(x.case_id)} ↗</a>`],
      ["Primary tumour RNA-seq", st(x.tumour_rna)],
      ["Primary tumour 450k", st(x.tumour_met)],
      ["Normal RNA-seq", st(x.normal_rna)],
      ["Normal 450k", st(x.normal_met)],
      ["Normal RNA with H&E on the same sample", x.normal_rna_he ? "Yes" : "No"],
      ["… and normal 450k on that sample", x.normal_rna_he_met ? "Yes" : "No"],
    ])}
    ${x.histology ? `<h3 class="section-title">Histology review</h3>${kv([
      ["Histology-defined cohort", esc(LABELS.analysisCohort[x.cohort])],
      ["Reason", esc(LABELS.analysisReason[x.histology.analysis_reason] ?? x.histology.analysis_reason)],
      ["GDC label", `${esc(x.histology.gdc_primary_diagnosis)} (${esc(x.histology.gdc_morphology)}); site: ${esc(x.histology.gdc_site)}`],
      ["Reviewed histology", esc(x.histology.reviewed_histology ?? "Not reviewed")],
      ["Relation to GDC label", esc(LABELS.relation[x.histology.gdc_label_relation])],
      ["Evidence", esc(x.histology.evidence)],
      ["Publication note", esc(x.histology.publication_notes)],
      ["Pathology report", x.histology.pathology_report_url ? `<a href="${esc(x.histology.pathology_report_url)}" rel="noopener" target="_blank">GDC pathology report ↗</a>` : ""],
      ["PDAC sensitivity subset", x.cohort === "PDAC" ? esc(LABELS.sens[x.sens]) : ""],
      ["Specimens", esc(x.histology.specimen_note)],
    ])}` : ""}
    <h3 class="section-title">Clinical eligibility (patient review)</h3>
    ${x.clinical ? kv([
      ["Patient screen", `${chip("disposition", x.disposition)}`],
      ["Primary tumour eligible", x.tumour_layers === "none" ? "No retained tumour assay" : (x.eligible ? "Yes" : "No")],
      ["Selected analysis set", esc(LABELS.selected[x.selected])],
      ["Treatment context", esc(x.treatmentContext.map(c => LABELS.treatmentContext[c]).join("; "))],
      ["Reasons", x.reasons.length ? `<ul class="notes">${x.reasons.map(r => `<li>${esc(LABELS.reason[r] ?? r)}</li>`).join("")}</ul>` : "None"],
      ["Covariates", x.covariates.length ? esc(x.covariates.map(r => LABELS.reason[r] ?? r).join("; ")) : "None"],
      ["Analysis cohort", x.clinical.analysis_group ? `${esc(cohortName(d, x.clinical.analysis_group))}${x.clinical.analysis_group !== x.project ? ` <span class="cell-sub">Submitted as TCGA-${esc(x.project)}</span>` : ""}` : esc(LABELS.analysisGroup[x.analysisCohort])],
      ["Study role", esc(LABELS.role[x.role] ?? x.role)],
      ["Study-scope exclusion", x.panelExclusion !== "none" ? `${esc(LABELS.panelExclusion[x.panelExclusion] ?? x.panelExclusion)}<span class="cell-sub">A selection decision, not an assay failure.</span>` : ""],
      ["Subsets", x.subsets[0] !== "none" ? esc(x.subsets.map(v => LABELS.subset[v] ?? v).join("; ")) : ""],
      ["Reported tumour site (GDC)", x.clinical.site_reported ? `${esc(x.clinical.site_reported)}; resection site: ${esc(x.clinical.resection_site_reported)}` : ""],
      ["Site annotation override", x.clinical.site_override ? esc(LABELS.siteOverride[x.clinical.site_override] ?? x.clinical.site_override) : ""],
      ["Study-primary diagnosis (GDC)", `${esc(x.clinical.primary_diagnosis)} (${esc(x.clinical.morphology)}); prior treatment field: ${esc(x.clinical.prior_treatment_field)}`],
      ["Normal donor", x.normal_ref === "withheld" ? "Normal package withheld by the patient screen" : x.normal_ref === "inactive" ? "Normal package in a project excluded from the study; outside active totals" : esc(LABELS.normalContext[x.normalContext])],
    ]) : '<p class="muted small">Not reviewed: the patient has no retained RNA-seq or 450k layer.</p>'}
    ${x.clinical && x.clinical.histology_stratum ? `<h3 class="section-title">Histology and molecular annotations (panel revision)</h3>${kv([
      ["Reviewed histology or group", esc(LABELS.histStratum[x.clinical.histology_stratum] ?? x.clinical.histology_stratum)],
      ["Histology source", esc(x.clinical.histology_evidence)],
      ["Publication histology", x.clinical.histology_publication_member ? esc(x.clinical.histology_publication === "" ? "Blank in the publication table" : x.clinical.histology_publication) : "Not in the publication table"],
      ["GDC histology", esc(x.clinical.historical_histology_gdc ?? "Not reported")],
      ["Publication and GDC differ", x.clinical.histology_label_conflict ? "Yes; both labels are kept" : ""],
      ["Grade (publication)", x.clinical.grade_publication === null ? "" : esc(x.clinical.grade_publication || "Blank in the publication table")],
      ["Grade (GDC)", esc(x.clinical.historical_grade_gdc ?? "")],
      ["Published molecular group", x.clinical.molecular_group ? esc(LABELS.histStratum[x.clinical.molecular_group] ?? x.clinical.molecular_group) : ""],
      ["IDH status (raw call)", x.clinical.idh_status === null ? "" : esc(x.clinical.idh_status || "Blank in the publication table")],
      ["1p/19q status (raw call)", x.clinical.codeletion_1p19q === null ? "" : esc(x.clinical.codeletion_1p19q || "Blank in the publication table")],
      ["Published subtype", x.clinical.published_subtype === null ? "" : esc(x.clinical.published_subtype || "Blank in the publication table")],
      ["HPV status (publication)", esc(x.clinical.hpv_status_publication ?? "")],
      ["Endometrial-like (publication)", esc(x.clinical.endometrial_like_publication ?? "")],
      ["Adrenal-cortical admixture", x.clinical.adrenal_cortical_admixture === null ? "" : (x.clinical.adrenal_cortical_admixture ? "Yes (annotation, not an exclusion)" : "No")],
      ["Head and neck paraganglioma", x.clinical.head_neck_sensitivity_flag ? "Yes: pathology-confirmed, outside the 176-patient sensitivity subset" : ""],
      ["Integrated WHO diagnosis", x.clinical.who_diagnosis_status === "requires_independent_integrated_diagnosis_and_grade" ? esc(LABELS.whoStatus[x.clinical.who_diagnosis_status]) + '<span class="cell-sub">Historical labels are not treated as integrated diagnoses, and none is inferred from molecular clusters.</span>' : ""],
    ])}<p class="muted small">Annotations come from TCGA publication tables (via TCGAbiolinks) and GDC labels. They are not a new slide review.</p>` : ""}
    <p class="muted small">Clinical decisions are applied on top of the assay states above and do not change them. Exclusions and holds are kept separate, and a hold may be lifted by further evidence. Treatment-flagged patients are not a treated reference set.</p>
    <h3 class="section-title">Other checks</h3>
    ${kv([
      ["Earlier scope review", x.scope ? `${esc(LABELS.scopeAction[x.scope.summary_action] ?? x.scope.summary_action)}<span class="cell-sub">${esc(x.scope.annotations.map(a => `${a.category} (${a.entity_type} ${a.entity}): ${LABELS.scopeAction[a.action] ?? a.action}`).join("; "))}</span>` : "Not in the 172-patient scope review"],
      ["Retained-assay image linkage", "Not yet checked"],
    ])}
    <h3 class="section-title">Excluded or unresolved aliquots</h3>
    ${flags ? `<ul class="notes">${flags}</ul>` : '<p class="muted small">None. All available aliquots for this patient are retained.</p>'}
    <p class="muted small">States are per layer and compartment: an excluded aliquot does not remove other retained assays from the same patient. Where a patient-level annotation was reviewed, its action is shown under other checks; it is not an additional exclusion.</p>`;
  openDialog(esc(x.patient), esc(`TCGA-${x.project}`), body);
}

export function showError(container, err) {
  container.innerHTML = `<div class="empty"><p>The explorer data could not be loaded.</p><p class="small">${esc(err.message)}</p>
  <p class="small">If you opened the file directly from disk, serve the folder over HTTP instead (for example <code>python3 -m http.server</code>).</p></div>`;
}

// ---------------------------------------------------------------- shared route helpers

// Patients with RNA-seq, with methylation (450k) and with both, from a union/paired/single-view count.
export function views(x) {
  if ("rna" in x) return { rna: x.rna, met: x.met, both: x.paired, total: x.total };
  return { rna: x.paired + x.rna_only, met: x.paired + x.met_only, both: x.paired, total: x.union };
}

// How a TCGA project relates to the selected analysis panel, in plain words.
export function panelStatus(d, p) {
  const x = d.tcgaCounts[p], e = d.elig.projects[p];
  if ((d.tcgaMeta.excluded_projects || {})[p]) return LABELS.projectExclusion[p] ?? "No: outside the study";
  if (!x || !x.in_panel || !e) return "No: below the size threshold";
  const id = e.analysis_cohort, c = d.elig.cohorts[id];
  if (c.projects.length > 1) return `Yes: pooled with ${c.projects.filter(q => q !== p).map(q => `TCGA-${q}`).join(" and ")} as ${LABELS.pooledName[id] ?? id} (${id})`;
  if (id !== p) return `Yes: ${LABELS.cohortScope[id] ?? id} (${id})`;
  return "Yes";
}
// "squamous cell carcinoma only (ESCC)" for a cohort that is one histology of its project, else "".
export function cohortScopeText(id) {
  return LABELS.cohortScope[id] ? `${LABELS.cohortScope[id]} (${id})` : "";
}

const viewCells = (v, label = "") => `<td class="num" data-label="Patients with RNA-seq${label}"><div>${fmt(v.rna)}</div></td><td class="num" data-label="Patients with methylation${label}"><div>${fmt(v.met)}</div></td><td class="num" data-label="Patients with both${label}"><div>${fmt(v.both)}</div></td>`;
const viewHead = first => `<thead><tr><th scope="col">${first}</th><th scope="col" class="num">Patients with RNA-seq</th><th scope="col" class="num">Patients with methylation (450k)</th><th scope="col" class="num">Patients with both</th></tr></thead>`;

// Molecular coverage of every solid-tumour TCGA project (broader availability), with full detail on request.
export function screenTable(d) {
  const order = Object.entries(d.tcgaCounts).sort(([a, x], [b, y]) => (y.in_panel - x.in_panel) || (!!y.excluded_from_study - !!x.excluded_from_study) || a.localeCompare(b));
  const rows = order.map(([p, x]) => `<tr><td class="primary" data-label="TCGA project"><div>TCGA-${esc(p)}</div></td>${viewCells(views(x.post_qc))}
      <td data-label="In the selected panel"><div>${esc(panelStatus(d, p))}</div></td></tr>`).join("");
  const det = order.map(([p, x]) => {
    const e = d.elig.projects[p], sel = e && !e.excluded_from_study ? e.selected_analysis : null;
    const cell = (v, label) => `<td class="num" data-label="${label}"><div>${v === null || v === undefined ? "—" : fmt(v)}</div></td>`;
    return `<tr><td class="primary" data-label="TCGA project"><div>TCGA-${esc(p)}</div></td>
      ${cell(x.pre_qc.union, "Before exclusions, any")}${cell(x.pre_qc.paired, "Before exclusions, both")}
      ${cell(x.post_qc.union, "After exclusions, any")}${cell(x.post_qc.paired, "After exclusions, both")}
      ${cell(x.post_qc.rna_only, "RNA-seq only")}${cell(x.post_qc.met_only, "450k only")}
      ${cell(x.normal.rna_he, "Normal RNA + H&E")}${cell(x.normal.rna_he_met, "Normal with 450k")}
      ${cell(e ? e.after_patient_screen.total : null, "After patient screen, any")}${cell(e ? e.after_patient_screen.paired : null, "After patient screen, both")}
      ${cell(sel ? sel.total : null, "Selected, any")}${cell(sel ? sel.paired : null, "Selected, both")}</tr>`;
  }).join("");
  return `<div class="table-wrap"><table class="stack compact">${viewHead("TCGA project").replace("</tr></thead>", '<th scope="col">In the selected panel</th></tr></thead>')}
    <tbody>${rows}</tbody>
    <caption>Broader availability: primary-tumour patients in each project after exact assay-quality exclusions. This is not the selected panel; the last column shows how each project contributes to it, if at all. ESCC, CSCC and PDAC name the histology analysed within TCGA-ESCA, TCGA-CESC and TCGA-PAAD. Patients with both assays are also counted in each single-assay column.</caption>
  </table></div>
  <details class="disclosure"><summary>Detailed counts by project: before and after exclusions, single-assay patients, normal tissue and the patient screen</summary>
    <div class="table-wrap" style="margin-top:.5rem"><table class="stack compact"><thead><tr><th scope="col">TCGA project</th>
      <th scope="col" class="num">Before exclusions: RNA-seq and/or 450k</th><th scope="col" class="num">Before exclusions: both</th>
      <th scope="col" class="num">After exclusions: RNA-seq and/or 450k</th><th scope="col" class="num">After exclusions: both</th>
      <th scope="col" class="num">RNA-seq only</th><th scope="col" class="num">450k only</th>
      <th scope="col" class="num">Normal RNA + H&amp;E</th><th scope="col" class="num">Normal with 450k</th>
      <th scope="col" class="num">After patient screen: any</th><th scope="col" class="num">After patient screen: both</th>
      <th scope="col" class="num">Selected: any</th><th scope="col" class="num">Selected: both</th></tr></thead>
    <tbody>${det}</tbody>
    <caption>Unique patients. Normal columns count same-sample normal RNA and H&amp;E after assay exclusions. Patient-screen and selected columns cover the ${d.elig.meta.projects} panel projects; for pooled cohorts, the selected counts are each project's contribution. The size threshold (${d.tcgaMeta.rule.min_total} patients with RNA-seq, 450k or both, ${d.tcgaMeta.rule.min_paired} with both) applies to analysis cohorts, as explained in the size threshold section.</caption></table></div>
  </details>`;
}

// TCGA overview for a cancer page: the selected panel and broader availability, never mixed in one table.
export function tcgaOverview(d, page) {
  const projects = page.tcga_projects || (page.tcga_project ? [page.tcga_project] : []);
  if (!projects.length) return `<p class="muted">No TCGA project is linked to this page.</p>`;
  let panel;
  const e = page.tcga_project && d.elig.projects[page.tcga_project];
  if (e && e.excluded_from_study) {
    panel = `<p class="callout small">TCGA-${esc(page.tcga_project)} is not in the selected analysis panel. The table below shows the data available for it.</p>`;
  } else {
    let rows;
    if (page.tcga_projects) {
      const c = d.elig.cohorts[page.code];
      rows = [[`<strong>${esc(page.code)}, all contributing projects</strong>`, c.selected_analysis], ...c.projects.map(p => [`… submitted as TCGA-${esc(p)}`, c.contributions[p]])];
    } else {
      const c = d.elig.cohorts[e.analysis_cohort];
      rows = c.projects.length > 1
        ? [[`Contribution of TCGA-${esc(page.tcga_project)}`, e.selected_analysis], [`<a href="cancers.html?c=${esc(e.analysis_cohort)}">Pooled ${esc(e.analysis_cohort)} cohort</a>, all projects`, c.selected_analysis]]
        : [[`<strong>${esc(e.analysis_cohort)}${e.analysis_cohort !== page.tcga_project ? `: ${esc(c.label)}` : ""}</strong>`, e.selected_analysis]];
    }
    panel = `<div class="table-wrap"><table class="stack compact">${viewHead("Selected analysis panel")}
      <tbody>${rows.map(([label, x]) => `<tr><td class="primary" data-label="Selected analysis panel"><div>${label}</div></td>${viewCells(views(x))}</tr>`).join("")}</tbody>
      <caption>Selected analysis panel: primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.${projects.length > 1 || (e && d.elig.cohorts[e.analysis_cohort].projects.length > 1) ? " Each patient counts once in the pooled cohort; project rows show where they were submitted." : ""}</caption></table></div>`;
  }
  const avail = `<div class="table-wrap" style="margin-top:.8rem"><table class="stack compact">${viewHead("Broader availability")}
    <tbody>${projects.map(p => `<tr><td class="primary" data-label="Broader availability"><div>TCGA-${esc(p)} project</div></td>${viewCells(views(d.tcgaCounts[p].post_qc))}</tr>`).join("")}</tbody>
    <caption>Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.</caption></table></div>`;
  return panel + avail;
}

const WORDS = ["No", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"];
const numberWord = n => (n < WORDS.length ? WORDS[n] : fmt(n));

// Matched-spatial resources listed for a cancer page (pooled pages include their constituents).
export function spatialResourcesFor(d, page) {
  const codes = [page.code, ...(page.includes || [])];
  return d.cohorts.filter(x => x.layer === "matched-spatial" && x.cancers.some(k => codes.includes(k)));
}

// One plain sentence on what is catalogued and what is verified.
export function spatialSentence(n, original, preview = 0) {
  if (!n) return "No spatial resources are catalogued for this cancer type yet.";
  const head = `${numberWord(n)} spatial ${n === 1 ? "resource is" : "resources are"} catalogued`;
  if (!original && !preview) return `${head}. Verification of the matched image and molecular data is pending.`;
  const who = k => (k === n ? (n === 1 ? "it" : k === 2 ? "both" : "all of them") : numberWord(k).toLowerCase());
  const bits = [original ? `the original H&E and matched molecular data are located for ${who(original)}` : "",
    preview ? `matched molecular data with a preview image only for ${who(preview)}` : ""].filter(Boolean);
  const rest = n - original - preview;
  return `${head}; ${bits.join(", and ")}.${rest ? ` Verification is pending for the ${rest === 1 ? "other" : "others"}.` : ""}`;
}

// The cancer page that holds an analysis cohort (CSCC on CESC, ESCC on ESCA; pooled cohorts have their own pages).
export function pageForCohort(d, cohort) {
  return d.cancerByCode.get(cohort) || d.cancers.find(c => c.analysis_cohort === cohort && c.tcga_project) || null;
}

// Spatial status of a cancer page over its own codes: located matched packages, candidates and core captures.
export function spatialStatus(d, c) {
  const codes = [c.code, ...(c.includes || [])];
  const spatial = d.cohorts.filter(x => x.layer === "matched-spatial" && x.cancers.some(k => codes.includes(k)));
  const access = new Set(["controlled", "request", "unreleased", "unresolved"]);
  const caps = d.captures.filter(x => codes.includes(x.cancer));
  return {
    located: spatial.filter(x => x.status === "verified").length,
    preview: spatial.filter(x => x.status === "preview").length,
    candidates: spatial.filter(x => x.status === "candidate").length,
    openCandidates: spatial.filter(x => x.status === "candidate" && !access.has(x.access.category)).length,
    accessCandidates: spatial.filter(x => x.status === "candidate" && access.has(x.access.category)).length,
    reviewed: spatial.filter(x => x.spatial_review).length,
    core: tally(caps.filter(x => x.tier === "core")),
    untreated: tally(caps.filter(x => x.tier === "core" && x.treatment === "Untreated")),
    all: tally(caps),
  };
}
