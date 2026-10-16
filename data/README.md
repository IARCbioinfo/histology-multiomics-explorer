# Explorer metadata

All files are UTF-8 JSON. Controlled vocabularies are defined in `scripts/check.py` and labelled for display in `assets/js/common.js`.

## release.json

`version`, `date` (YYYY-MM-DD) and `audit_dates`, the dates on which the underlying sources were checked.

## cancers.json

One object per cancer type.

| Field | Meaning |
| --- | --- |
| `code` | Short code, following TCGA where one exists (`PDAC` is used for pancreatic ductal adenocarcinoma; `CRC` is the pooled colorectal adenocarcinoma page and also marks spatial captures whose colon or rectal origin is not stated; `GLIOMA` is the pooled LGG and GBM classification benchmark) |
| `name` | Display name |
| `group` | `hausser`, `tcga-panel` (added by the molecular screen), `extension`, `additional`, `pooled` (a page combining other cancers, listed in `includes`), `excluded` (kept for provenance, outside the study and the navigation) or `aggregate` |
| `hausser` | Result in Hausser et al. 2019: `significant`, `borderline`, `no-geometry` (screened, no vertices detected) or `not-screened` |
| `tcga_project` | TCGA project code linked to this page, or null; a pooled page lists its projects in `tcga_projects` |
| `analysis_cohort` | TCGA analysis cohort the page's patients belong to, for example `CRC` for COAD and READ, `ESCC` for ESCA, `CSCC` for CESC, `GLIOMA` for LGG and GBM; null for an excluded project |
| `rationale`, `unstated_label`, `evidence_notes` | Optional: a display rationale overriding the group default; the label for captures whose constituent cancer is not stated (pooled pages); page-specific wording of an evidence card's finding, keyed by evidence ID |
| `strata` | `[id, label]` pairs for histology strata used by captures |
| `summary` | Short rationale |
| `gaps` | Known gaps and cautions |

## evidence.json

Published archetype studies used as rationale: `id`, `short`, `cancers`, `citation`, `doi`, `url`, `scale`, `definition`, `finding`, `limits`.

## cohorts.json

One object per underlying study or resource.

| Field | Meaning |
| --- | --- |
| `id`, `label` | Stable identifier and display label |
| `citation` | `authors`, `title`, `journal`, `year`, `doi`, `url`; fields may be null where not curated |
| `related_citations` | Further publications describing the same cohort |
| `cancers` | Cancer codes |
| `layer` | `matched-spatial`, `wsi-bulk`, `bulk-rna`, `single-cell`, `image-only` |
| `status` | `verified` (original H&E located: the original scan, expression and coordinates were found, for at least the stated subset of sections), `preview` (matched data with preview image: expression and coordinates match a preview released with them, and the original scan was not located), `screened` (TCGA project in the molecular screen panel; READ and GBM are included through pooled cohorts), `excluded` (TCGA project kept for provenance but excluded from the study), `candidate`, `reference`, `listed` |
| `tcga_project`, `analysis_cohort` | For TCGA entries, the project code used in the `tcga_*` files and the analysis cohort it contributes to |
| `compartments` | Tissue compartments: `primary-tumour`, `metastatic-tumour`, `tumour-unspecified`, `solid-normal` (tumour-adjacent), `peritumoral`, `normal` (not tumour-adjacent or adjacency not stated) and `precursor` |
| `modalities`, `techniques`, `preservation` | What was measured and how |
| `specimen` | `clinical-tumour`, `cell-line` or `mouse` |
| `linkage` | Level of H&E–RNA linkage (see Methods) |
| `gates` | Open checks: for candidates, what prevents inclusion; for screened TCGA projects, the curation still to do |
| `accession` | Repository accessions as recorded |
| `access` | `category`, `route` (text) and `links` (`[label, url]` pairs) |
| `reported` | `[value, unit, basis]` or `[value, unit, basis, cancer]` counts in the source's own units (sections, slides, samples, donor labels, patients); a fourth element limits the count to one of the entry's cancers. Not deduplicated, not patient counts unless stated, never added across studies; an unknown count is absent rather than zero |
| `spatial_review` | For the 26 spatial resources reviewed on 15 October 2026: review `id` and `date`, `analysis_cohort` (selected histology, for example `CSCC` shown on the CESC page), `assay_classes` (`whole-transcriptome`, `targeted-rna`, `rna-protein`, `roi`, `protein-imaging`, `unverified`), reported `platform`, `role`, `image_status`, `treatment_status` with `treatment_class` (`unknown`, `reported-untreated`, `treated`, `baseline-and-on-treatment`), `eligible_patients` (always null: unknown), `strict_core_promoted` (false), `sample_ids` by role (selected, excluded, normal or precursor, tumour, adjacent, metastatic) and specimen details where given. Written by `scripts/import_spatial_review.py`; three earlier entries keep their IDs and are enriched |
| `spatial_review.route_review` | Public-route review of 15 October 2026, written by `scripts/import_spatial_route_review.py`: `date`, a plain `status`, `states` (open dependencies: `public-download`, `download-failure` for a technical download failure, `vendor-terms`, `account-registration` for a free account, `dac-approval`, `author-release` for a release or metadata the authors still have to provide, `local-qc`), `next_step` and `sections_with_matching_coordinates` (sections whose expression barcodes match the in-tissue coordinates exactly; null when not checked). Not a patient count or final QC |
| `backlog_review` | Package review of the 77 candidates not checked file by file before, written by `scripts/import_spatial_backlog_review.py`: `date`, `outcome` (`original-ready`, `preview-ready`, `bounded-public-work`, `access-dependent`, `release-unresolved`, `author-release`, `release-gap`, `code-only-lead`, `technical-gap`, `coordinate-gap`, `registration-gap`, `linkage-gap`, `account-route`, `unspecified-vendor-lead`, `vendor-boundary`), `depth` of the check, `states` (open dependencies, as in `route_review`), `image_finding`, `molecular_finding`, `next_step`, `sections_listed` (section records it added, or null) and `study_local_donors` (donor labels the source establishes for the reviewed selection, or null; for a resource with original and preview sections, the original-image sections). Eligible patients are not given |
| `followup_review` | Follow-up review, written by `scripts/import_spatial_followup_review.py`: `date`; where the result changed, `outcome` (`original-ready`, `preview-ready`, `preview-ready-partial`, `preview-clinical-correction`, `preview-additional-route`, `bounded-public-work`, `bounded-public-work-reuse-known`, `image-linkage-gap`, `image-alias-review`, `public-processed-decoding-gap`, `spatial-release-unresolved`, `public-portal-link-resolved`, `coordinate-gap`, `barcode-grid-gap`), `depth`, `findings`, `states` (latest open dependencies) and `next_step`; and `checks`, the checks made without change, each with `check`, `depth` and `result` |
| `derived_from` | Cohort IDs this resource reuses |
| `verification`, `verified_on` | Verification label and date |
| `description`, `notes` | Curated text |

## leads.json

Related leads that add no resources or patients: releases whose patients cannot yet be assigned to a cancer type, precursor studies and reuse records. Fields: `id`, `label`, `url`, `doi`, `tissues`, `description`, `not_counted` (why it is outside the totals), `next`, `sections_checked`, optional `links` and `checked_on`. Written by `scripts/import_spatial_route_review.py`.

## captures.json

One object per study–section record: an assayed section or capture area of one study with its own measured expression, coordinates and H&E image, either the original scan (`image_level` `original`) or only a preview released with the data (`preview`). Records are not globally unique physical sections: several specimens can share one array area, and reused data can repeat a physical section.

| Field | Meaning |
| --- | --- |
| `id` | `<cohort>:<capture>` |
| `cohort`, `cancer`, `stratum` | Cross-references; `stratum` is null when no stratum applies |
| `patient`, `capture`, `accession`, `source_name` | Source identifiers; `patient` is null when the source does not establish the donor |
| `image_level` | `original` (original H&E scan located) or `preview` (preview image only; not for whole-slide or tile models, morphology, distances or registration sign-off) |
| `donor_mapping` | Reviewed records: `source-established`, `source-patient-column`, `source-sample-title` or `unresolved` (no patient ID) |
| `assay_area_id`, `region_label`, `expression_subset` | For sections that share an array area: the area, the source region and the slide and tissue labels of this section's expression subset |
| `compartment` | Tissue compartment where it is not the primary or metastatic tumour (for example `precursor` or `normal`) |
| `open_checks` | Checks still open for this section |
| `out_of_tissue_expression_spots`, `recurrence_outcome`, `original_crosswalk_inferred` | Expression spots outside the tissue to filter; a recurrence recorded as a later outcome; whether the original-image match was inferred (then held at preview level) |
| `review_batch` | The review that added the record (`backlog-2026-10-16` or `followup-2026-10-16`), where it was not curated by hand |
| `geometry_check` | Frame check: finite coordinates and positions inside the original or preview frame after the supplied scale, with the scale used; not a registration sign-off |
| `sampled_recurrence` | True for a sampled recurrent tumour sector |
| `field_sources` | Evidence URL of each field changed by the follow-up review, keyed by field (`clinical.<field>` for clinical fields) |
| `tier` | `core`, `metastatic`, `review`, `outside-stratum`, `held`; `tier_reason` gives the source-backed reason |
| `site`, `site_source` | `Primary`, `Metastasis` or `Unknown`, with the source wording |
| `treatment`, `treatment_note` | `Untreated`, `Post-treatment` or `Unknown` before sampling, with the evidence |
| `diagnosis`, `histology` | Source wording |
| `technique`, `preservation` | Assay and tissue preparation |
| `linkage`, `registration` | H&E–RNA linkage level and alignment status |
| `expression_type` | The expression data and how they were checked against the coordinates |
| `he_mpp`, `he_mpp_basis` | Image resolution in µm/pixel where established, and how it was obtained; a value read from an image header is an observation, not an independent calibration |
| `he_file` | Original image filename where recorded |
| `links` | `he`, `expression`, `coordinates` and `raw` (list) URLs |
| `access` | Access category for `he`, `processed` and `raw` data |
| `verification`, `verified_on` | Verification label and date |
| `clinical` | `age`, `sex`, `stage`, `grade`, `subsite`, `markers` and `response` (a response label, which does not show when the sample was taken) as reported by the source |

Known patients are unique `(cohort, patient)` pairs with a patient ID; records without one are not counted as patients, and no count here is an eligible-patient count.

## TCGA molecular screen

Generated by `scripts/build_tcga.py` from public GDC file metadata and the PanCanAtlas merged sample-quality annotations; see the script for queries and rules. Do not edit by hand; rerun the script with a new date instead.

`tcga_counts.json`: `meta` (date, rule, representation, panel, groups, excluded_projects), `projects`, keyed by TCGA project code, and `groups`, keyed by analysis group, with unique-patient counts:

| Field | Meaning |
| --- | --- |
| `pre_qc`, `post_qc` | Primary-tumour `union` (RNA-seq and/or 450k), `paired` (both), `rna_only`, `met_only`, before and after exclusions |
| `normal` | `rna_he`: retained normal RNA-seq with an H&E image of the same sample; `rna_he_met`: also retained normal 450k on that sample; `also_in_tumour_union`, `normal_only` |
| `patients_either_compartment` | Distinct patients in the post-QC tumour set or the normal reference |
| `aliquots` | Retained, excluded and unresolved aliquot counts by compartment and layer |
| `historical_matrix` | The same counts for the PanCanAtlas final harmonized matrices (header membership), or null |
| `passes_screen`, `in_panel`, `group`, `excluded_from_study` | Result of the 150 / 100 rule for the project alone, membership of the listed panel, the screen group, and whether the project is excluded from the study by decision |

`groups` gives the same counts per screen group with its `projects` and `passes_screen`; the rule is applied to the group, so TCGA-READ (CRC) and TCGA-GBM (GLIOMA) are in the panel although each is below the rule on its own. TCGA-SARC passes the rule as a project but combines several sarcoma types, each below it; it is outside the panel (`excluded_projects` gives the reason), and only its project-level counts are kept.

`panel_totals` sums the 20 panel projects (18 screen groups); TCGA patients belong to one project, so project totals add.

`tcga_patients.json`: `columns` and `rows`, one row per patient in the 20 panel projects. States for `tumour_rna`, `tumour_met`, `normal_rna`, `normal_met` are `retained`, `excluded`, `unresolved` (no exact annotation match) or `absent`; `normal_rna_he` and `normal_rna_he_met` follow the definitions above.

`tcga_flags.json`: every excluded or unresolved aliquot in the 20 panel projects, with both flags, the pathology-group reason, patient/sample/aliquot annotations and the layers still retained for that patient in the same compartment.

`tcga_resources.json`: curated links to current GDC data, PanCanAtlas files, histology-review sources and reference publications.

## TCGA histology and scope review

`tcga_reviews.json` is imported by `scripts/import_tcga_review.py` from the structured review exports; report text and free-text annotation notes are not included.

- `meta.cohorts`: definitions of the confirmed ESCC cohort, the proposed confirmed PDAC cohort and its sensitivity subset, with any exception to the general screen.
- `histology_columns` / `histology`: one row per registered TCGA-ESCA and TCGA-PAAD case (370). Fields include the histology `stratum`, the `evidence` source and level, the GDC primary diagnosis, morphology, diagnosis ID and site, published histology fields (ESCA supplement histology and site category; PAAD publication-table membership, reviewed histology and notes), the GDC pathology-report link where used, `reviewed_histology`, `gdc_label_relation` (`concordant`, `refined`, `differs`, `unconfirmed`, `not-reviewed`), retained tumour layers, normal-reference flags, `analysis_cohort` (exact membership), `analysis_reason`, `focal_squamous_flag`, `primary_metastatic_separated` and `specimen_note`.
- `scope_columns` / `scope`: one row per patient in the scope review of annotated, excluded aliquots, with the summary action, the number of reviewed aliquots and each annotation's category, level, scope, action and GDC annotation ID.

Cohort membership is an explicit patient list. Treatment eligibility and retained-assay image linkage are not part of these files.

## TCGA patient review: treatment and diagnosis screen, histology panel revision and analysis cohorts

Imported by `scripts/import_patient_review.py` (followed by `scripts/remove_excluded_projects.py`, which removes TCGA-SARC from the patient-level files), which recomputes every count, membership list, stratum and normal-reference figure from `tcga_patients.json` plus the overlay and stops if any differs from the review's own figures. The overlay never changes assay states.

`tcga_patient_review.json`: `columns` and `rows`, one row per patient with any retained RNA-seq or 450k layer in the 20 panel projects (8,187). Fields: `case_id` (GDC); `analysis_group` (`CRC` for COAD and READ, `GLIOMA` for LGG and GBM, `ESCC`, `PDAC` or `CSCC` for histology-cohort members, null for ESCA, PAAD and CESC cases outside them, otherwise the project); `analysis_role` (`discovery`, `classification-benchmark` or `excluded`); `panel_exclusion_reason` (study-scope exclusions: cervical adenocarcinoma or adenosquamous outside CSCC; not assay failures); `has_retained_tumour`; the GDC study-primary `primary_diagnosis`, `morphology` and `prior_treatment_field`; reason-code lists `treatment_exclusion_reasons`, `treatment_hold_reasons`, `diagnosis_reasons` and `covariates`; `patient_screen_pass`; `tumour_eligible`; `selected_cohort` and `selected_eligible` (applying the ESCC and PDAC histology cohorts); `normal_donor_eligible`; `normal_in_active_scope` and `normal_catalogue_eligible`; `normal_donor_context` (`target_project_donor`, `organ_specific_control`, `non_target_or_uncertain_or_recurrent_donor`, `normal_only_donor_primary_diagnosis_unreported`); `main_disposition`, assigned in the order diagnosis/identity/episode, treatment exclusion, treatment hold; for CRC and PCPG patients, `site_reported` and `resection_site_reported` as given by GDC, with `site_override` (`rectum` or `colon_unspecified`, CRC only) where a case annotation identifies the primary site; reported site fields are not adjudicated and can conflict. For the projects in the histology panel revision (CESC, UCEC, PCPG, LGG and GBM): `histology_stratum` (reviewed histology, or the published molecular group for glioma), `histology_evidence`, `histology_publication` and `histology_publication_member`, `historical_histology_gdc`, `histology_label_conflict`, `historical_grade_gdc` and `published_subtype`. Further structured publication annotations where available: `grade_publication`, `molecular_group`, raw `idh_status` and `codeletion_1p19q`, `hpv_status_publication`, `endometrial_like_publication`, `adrenal_cortical_admixture` (boolean from the published 0/1 flag), `head_neck_sensitivity_flag`, `benchmark_subsets` and `who_diagnosis_status` (glioma patients need an independent integrated diagnosis and grade; none is adjudicated). An empty string means the publication table has the patient but a blank field; null means no publication record. Reason lists overlap; the main disposition counts each patient once. No clinical notes or reports are included.

`tcga_eligibility.json`: per audited project, the `analysis_cohort`, `role`, `histology_reviewed`, unique-patient counts at three stages (`assay_qc`, `after_patient_screen`, `selected_analysis`, each with `total`, `rna`, `met`, `paired`, `rna_only`, `met_only`), the main dispositions of withheld tumour patients, publication/GDC `label_conflicts`, and the normal reference after screening (`rna_he_after`, `rna_he_met_after`, `in_active_scope`, withheld patients, donor context and the donors `outside_cohort`, with their histology for revised projects). `cohorts` gives each of the 18 analysis cohorts its `role`, contributing `projects`, selected counts, `contributions` by submitted project and the cohort's own normal reference; where applicable `subsets` (sensitivity and benchmark subsets with their exact patient lists, never added to totals), `strata` (reviewed histology or glioma groups among patients passing the patient screen, by project), `annotations` (value counts of structured annotations among selected patients), and for CRC `reported_sites`, `site_overrides` and `withheld`. `panel` gives the stages for the 20 active projects, the `discovery` and `benchmark` totals, dispositions, overlapping `reason_dimensions` and the active normal reference.

Treatment-flagged patients are not a treated reference set. Supportive steroid or anticonvulsant medication is a covariate, distinct from antineoplastic pretreatment.

## Generated files

Written by `scripts/build_agent_files.py` from the files above; do not edit by hand. `scripts/check.py` fails if they are out of date.

`by-cancer/<CODE>.json`: one file per cancer page (22). Fields: `release`; `code`; `page` and `markdown`, the matching web page and text version; `notes`, the points to read before using the counts; `cancer`, the record from `cancers.json`; `tcga`, with `panel_date`, `availability_date`, the page's `analysis_cohort` (the record from `tcga_eligibility.json` with its `id`, or null) and, per linked TCGA project, `selected_panel` (from `tcga_eligibility.json`) and `availability` (from `tcga_counts.json`); `spatial_resources` and `other_resources`, records from `cohorts.json` for the page's cancer codes (pooled pages include their constituents); `located_sections`, the selection fields of the page's records in `captures.json` (the full record has the same `id`); and `evidence`, the page's records from `evidence.json`.

`glossary.json`: `release`; `concepts`, the terms used for counts and curation with their definitions; and `vocabularies`, every display label of the site keyed by vocabulary and code (parsed from `assets/js/common.js`).

`index.json`: `name`, `release`, `agent_guide` (`llms.txt`), `field_reference`, `notes` and `files`, one entry per data file with `path`, `description`, `records`, `bytes`, `sha256` and `schema`.

`../schemas/<file>.schema.json`: JSON Schema (2020-12) for each data file, the per-cancer files and the index. Types and fields are inferred from the data; controlled vocabularies come from `scripts/vocab.py`, so a value outside them fails the check.
