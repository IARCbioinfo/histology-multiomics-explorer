# Oesophageal carcinoma

Code `ESCA`. Molecular screen; not screened by Hausser et al. 2019. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=ESCA](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=ESCA). Data: [data/by-cancer/ESCA.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/ESCA.json).

Oesophageal carcinoma combines two distinct diseases, squamous cell carcinoma and adenocarcinoma. It was not among the cancer types screened by Hausser et al. The project meets the molecular screen; analyses use a histology-defined squamous cell carcinoma cohort rather than the pooled project.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| ESCC: Confirmed oesophageal squamous cell carcinoma | 90 | 90 | 90 | 90 |

Normal reference of the cohort after screening: 2 patients with same-sample normal RNA-seq and H&E, 2 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-ESCA project | 173 | 174 | 173 | 174 |

## Spatial studies

3 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| HRA007162, ESCC single-cell and spatial (`escc-hra007162`) | Visium | Open download | 5 cancer tissues | Verification pending |
| HRA000776 / OMIX009524, multistage ESCC (`escc-hra000776-omix009524`) | Visium (library details to verify) | Controlled access | 5 named tumour image packages | Verification pending |
| Liu et al. 2023, GeoMx precancer (`escc-precancer-geomx`); includes precursor lesions; H&E from serial sections | GeoMx WTA (ROI) | Author request | 7 patients with invasive ESCC | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-ESCA (`tcga-esca`): in the molecular screen panel; open download. Oesophageal carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked beyond the histology review. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- The confirmed ESCC cohort (90 patients) is an approved exception to the general screen thresholds.
- Adenocarcinomas are split by site in the publication table into definite and probable oesophageal, junctional of indeterminate origin and gastric; they are not pooled with ESCC and are not reassigned to STAD.
- Two squamous carcinomas with retained assays carry only a GDC label and stay outside the ESCC cohort as provisional.
- The linkage of retained assays to slide images is not yet checked.
- Three ESCC spatial resources are listed for review: two controlled datasets (no access requested) and a GeoMx ROI study of precancer and cancer. The linked image deposit holds processed hires images for five tumours, not verified original scans. None is yet a verified matched package.
