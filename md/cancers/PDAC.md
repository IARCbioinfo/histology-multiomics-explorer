# Pancreatic ductal adenocarcinoma

Code `PDAC`. Molecular screen; not screened by Hausser et al. 2019. Release 0.11.1, 16 October 2026. Web page: [cancers.html?c=PDAC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=PDAC). Data: [data/by-cancer/PDAC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/PDAC.json).

Pancreatic ductal adenocarcinoma was not among the cancer types screened by Hausser et al. TCGA-PAAD meets the molecular screen; analyses use a histology-confirmed ductal adenocarcinoma cohort selected by documented pathology review rather than the whole project.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| PDAC: Confirmed pancreatic ductal adenocarcinoma | 143 | 149 | 143 | 149 |

Normal reference of the cohort after screening: 4 patients with same-sample normal RNA-seq and H&E, 4 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-PAAD project | 151 | 157 | 151 | 157 |

## Spatial studies

3 spatial resources are catalogued; the original H&E and matched molecular data are located for 2, and matched molecular data with a preview image only for 1. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| HTAN WUSTL (Mo et al. 2024) (`htan-wustl`); includes treated tissue; includes metastases | Visium, Visium FFPE | Free account | No count reported | Original H&E located: 20 sections with original H&E; 15 known patients |
| Pei et al. 2025 (`pei-2025`); includes treated tissue; includes metastases | Visium | Open download | No count reported | Original H&E located: 55 sections with original H&E; 13 known patients |
| Schmitt et al. 2026 (`schmitt-2026`) | Visium FFPE | Open download | 14 patients | Matched data with preview image: 14 sections with a preview image; 14 known patients |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 89 sections (75 with original H&E, 14 with a preview image) from 42 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Pancreatic ductal adenocarcinoma | 12 | 16 | 39 | 0 |
| Pancreatobiliary-type adenocarcinoma (harmonisation pending) | 0 | 0 | 18 | 0 |
| No stratum assigned | 0 | 0 | 2 | 14 |

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-PAAD (`tcga-paad`): in the molecular screen panel; open download. Pancreatic adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked beyond the histology review. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Pei et al. primary-site sections come from rapid autopsies of end-stage disease, not early surgical resections.
- HTAN pancreatic sections are labelled pancreatobiliary-type and need pathology harmonisation before pooling with conventional PDAC.
- Original scans for the Schmitt et al. untreated resections have not been located.
- The proposed confirmed PDAC cohort (149 patients) is one patient below the general 150-patient threshold and is shown as an explicit exception.
- Eight TCGA-PAAD patients with retained assays are excluded or held because their reviewed diagnosis is adenosquamous, colloid or “Other”.
- The linkage of retained assays to slide images is not yet checked for the TCGA cohort.
