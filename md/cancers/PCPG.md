# Pheochromocytoma and paraganglioma

Code `PCPG`. Molecular screen; not screened by Hausser et al. 2019. Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=PCPG](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=PCPG). Data: [data/by-cancer/PCPG.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/PCPG.json).

Pheochromocytoma and paraganglioma were not among the cancer types screened by Hausser et al. The project meets the molecular screen, with RNA-seq and 450k methylation for every selected patient, and is analysed as one pooled cohort with tumour location, published molecular subtype and adrenal-cortical admixture kept as annotations.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| PCPG | 178 | 178 | 178 | 178 |

Normal reference of the cohort after screening: 3 patients with same-sample normal RNA-seq and H&E, 3 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-PCPG project | 178 | 178 | 178 | 178 |

## Spatial studies

2 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Ling et al., SSRN manuscript (`pcpg-ling-ssrn`) | Spatial transcriptomics (platform unverified) | Unresolved | No count reported | Verification pending |
| Zhu et al. 2026, preprint (`pcpg-developmental-preprint`) | Spatial transcriptomics (human assay details unverified) | Not released | 2 human PPGL specimens | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-PCPG (`tcga-pcpg`): in the molecular screen panel; open download. Pheochromocytoma and paraganglioma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Analysed as one pooled cohort with location, publication-first histology, molecular subtype and adrenal-cortical admixture annotations. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Publication-first histology gives 146 pheochromocytomas and 32 paragangliomas; five patients absent from the TCGA PCPG table use the GDC label. Two cases labelled pheochromocytoma in GDC are extra-adrenal paragangliomas in the publication table.
- Two paragangliomas of the head and neck are confirmed by their pathology reports and retained; whether they are sympathetic or parasympathetic is not established. A sensitivity subset without them has 176 patients, all with both assays.
- Historical benign and malignant morphology codes do not determine eligibility.
- Cases with adrenal-cortical admixture are annotated, not removed as adrenocortical carcinoma; tissue composition and identity need their own checks.
- Only three patients contribute normal-reference tissue.
- PCPG remains a spatial access gap: two manuscript or preprint leads are listed, but no reusable measured spatial-RNA package with original H&E was verified.
