# Kidney renal papillary cell carcinoma

Code `KIRP`. Molecular screen; not screened by Hausser et al. 2019. Release 0.11.1, 16 October 2026. Web page: [cancers.html?c=KIRP](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=KIRP). Data: [data/by-cancer/KIRP.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/KIRP.json).

Papillary renal cell carcinoma is a separate TCGA project from clear cell carcinoma. It was not among the cancer types screened by Hausser et al. and is included because it meets the molecular screen.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| KIRP | 274 | 262 | 261 | 275 |

Normal reference of the cohort after screening: 32 patients with same-sample normal RNA-seq and H&E, 23 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-KIRP project | 279 | 267 | 266 | 280 |

## Spatial studies

2 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| 10x Genomics kidney preview, Xenium (papillary RCC) (`kirp-10x-xenium-preview`); includes normal or adjacent tissue | Xenium | Free account | 1 papillary RCC sample | Verification pending |
| Soupir et al., papillary RCC CosMx study (`kirp-macrophage-abstract`) | Multiplex immunofluorescence, Targeted spatial RNA (960 transcripts) | Open download | 11 mixed-RCC patients prepared for spatial RNA | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

## Selection history: published archetype evidence

No archetype analysis specific to this cancer type is catalogued.

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-KIRP (`tcga-kirp`): in the molecular screen panel; open download. Kidney renal papillary cell carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Not interchangeable with KIRC; analyse separately.
- Papillary RCC has only a targeted spatial resource: one vendor Xenium specimen (377-gene panel) beside a non-diseased kidney block. No whole-transcriptome papillary RCC package was verified, and the 16 patients of a related abstract are a multiplex-IF cohort, not a spatial RNA count.
