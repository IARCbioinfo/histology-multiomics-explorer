# Glioblastoma (historical TCGA diagnosis)

Code `GBM`. Glioma benchmark extension; pooled in GLIOMA. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=GBM](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=GBM). Data: [data/by-cancer/GBM.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/GBM.json).

TCGA-GBM is used only within the pooled glioma classification benchmark, with TCGA-LGG. Its diagnoses are historical histological categories that predate the integrated molecular classification of CNS tumours; they are kept as labels to be compared with an independently curated integrated diagnosis, not treated as one.

## TCGA reference

Selected analysis panel (classification benchmark). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| Contribution of TCGA-GBM | 141 | 130 | 46 | 225 |
| Pooled GLIOMA cohort, all projects | 643 | 632 | 548 | 727 |

Normal reference of the cohort after screening: 5 patients with same-sample normal RNA-seq and H&E, 1 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-GBM project | 154 | 139 | 51 | 242 |

## Spatial studies

3 spatial resources are catalogued; the original H&E and matched molecular data are located for 1, and matched molecular data with a preview image only for 1. Verification is pending for the other. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Greenwald et al. 2024 (`cand-greenwald2024`) | Visium | Open download | 13 IDH-wildtype glioblastoma sections | Original H&E located |
| Ritter et al. 2025 (`cand-ritternepsta2025`) | Visium FFPE | Open download | No count reported | Matched data with preview image: 44 sections with a preview image |
| Sonpatki et al. 2026 (`cand-snu2026`) | Visium FFPE, Visium, Xenium | Open download | 13 patients with glioblastoma | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 44 sections (0 with original H&E, 44 with a preview image) from 0 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| No stratum assigned | 0 | 0 | 0 | 44 |

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-GBM (`tcga-gbm`): in the molecular screen panel; open download. Glioblastoma, as historically diagnosed in TCGA. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from a few donors. Below the molecular screen on its own and included only through the pooled glioma classification benchmark (GLIOMA) with TCGA-LGG. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; integrated WHO diagnosis and grade have not been adjudicated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Below the screen on its own (242 patients, 51 with both assays after assay QC). After the patient screen 225 remain, but only 46 have both RNA-seq and 450k, so GBM adds few paired cases to the benchmark.
- Among the 225, the pan-glioma study assigns 202 to IDH-wildtype and 11 to IDH-mutant non-codeleted groups; 12 have no complete group, although some of them have an IDH call.
- Historical GBM is not a verified integrated WHO diagnosis, and IDH-wildtype status alone does not make a tumour glioblastoma.
- One patient submitted under GBM is annotated as lower-grade glioma and keeps both labels. One received dexamethasone and phenytoin before procurement; this is recorded as supportive medication, not antineoplastic pretreatment.
- The five normal RNA + H&E packages come from normal-only donors without a reported primary diagnosis. They are not verified matched glioblastoma controls.
- Two glioma spatial resources include glioblastoma: 13 IDH-wildtype GBM sections from five donor labels (Greenwald et al.) and an anatomical-niche atlas of 32 genotyped glioma sections. Original H&E for part of the first is available through a separate archive, but aliases, coverage and registration are unresolved; neither is a verified matched package.
