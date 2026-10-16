# Rectal adenocarcinoma

Code `READ`. Colorectal extension; pooled in CRC. Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=READ](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=READ). Data: [data/by-cancer/READ.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/READ.json).

Rectal adenocarcinoma was not part of the Hausser et al. geometry analysis. It is kept as a separate rectal stratum for spatial data, and TCGA-READ is analysed together with TCGA-COAD as the pooled colorectal cohort (CRC).

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| Contribution of TCGA-READ | 154 | 92 | 92 | 154 |
| Pooled CRC cohort, all projects | 579 | 373 | 371 | 581 |

Normal reference of the cohort after screening: 47 patients with same-sample normal RNA-seq and H&E, 19 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-READ project | 156 | 94 | 94 | 156 |

## Spatial studies

11 spatial resources are catalogued; the original H&E and matched molecular data are located for 3, and matched molecular data with a preview image only for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| HTAN WUSTL (Mo et al. 2024) (`htan-wustl`); includes metastases | Visium, Visium FFPE | Free account | No count reported | Original H&E located |
| Valdeolivas et al. 2024 (`valdeolivas-2024`) | Visium | Open download | No count reported | Original H&E located: 4 sections with original H&E; 2 known patients |
| Oliveira et al. 2025 (Visium HD) (`oliveira-2025`) | Visium HD | Open download | No count reported | Original H&E located: 1 section with original H&E; 1 known patient |
| Neve et al. 2026 (`cand-crc-orgares-gse283052`) | Visium | Open download | No count reported | Matched data with preview image |
| Primary colorectal cancer and liver metastasis, Visium CytAssist (`cand-crc-mahidol-gse267401`) | Visium CytAssist | Open download | No count reported | Matched data with preview image |
| Liu et al. 2026 (`cand-crc-liu-maru2026`) | Visium HD | Open download | No count reported | Matched data with preview image |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors (`cand-crc-colonmap-heiser2023`) | Visium FFPE | Free account | No count reported | Verification pending |
| Ren et al. 2025 (`cand-crc-spatch-ren2025`) | Visium HD | Open download | No count reported | Verification pending |
| HTAN Vanderbilt colorectal CytAssist captures (`cand-crc-cottam-htan2025`) | Visium CytAssist | Free account | No count reported | Verification pending |
| Schmauch et al. 2025 (`cand-crc-miso-petacc8`) | Visium FFPE | Controlled access | No count reported | Verification pending |
| Srinivasan et al. 2025 (`cand-crc-vri-dartmouth2025`) | Spatial Transcriptomics (legacy arrays), Visium CytAssist | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 5 sections (5 with original H&E, 0 with a preview image) from 3 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. Checked preview packages that are not listed one by one are not included.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Conventional rectal adenocarcinoma | 2 | 4 | 1 | 0 |

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-READ (`tcga-read`): in the molecular screen panel; open download. Rectal adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Below the molecular screen on its own and included through the pooled colorectal cohort (CRC) with TCGA-COAD. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- TCGA-READ does not meet the screen on its own (156 patients, 94 with both assays after assay QC); it contributes to the pooled CRC cohort, which does. The earlier standalone exclusion is superseded.
- Only two patients have primary-tumour sections with matched data located; the same registration step as for colon applies.
- One Visium HD rectal section is under review because its primary status is not stated.
