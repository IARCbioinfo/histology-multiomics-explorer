# Stomach adenocarcinoma

Code `STAD`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=STAD](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=STAD). Data: [data/by-cancer/STAD.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/STAD.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation. It meets the molecular screen.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| STAD | 385 | 377 | 348 | 414 |

Normal reference of the cohort after screening: 34 patients with same-sample normal RNA-seq and H&E, 0 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-STAD project | 387 | 378 | 349 | 416 |

## Spatial studies

2 spatial resources are catalogued; matched molecular data with a preview image only for both. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Lee et al. 2024 (`stad-gse251950`); includes metastases | Visium | Open download | 9 donor labels | Matched data with preview image: 10 sections with a preview image; 9 known patients |
| Gao et al. 2026 (`stad-gse270678`) | Visium | Open download | 19 patients with main sections | Matched data with preview image: 72 sections with a preview image; 20 known patients |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 82 sections (0 with original H&E, 82 with a preview image) from 29 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| No stratum assigned | 0 | 0 | 0 | 82 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Stomach adenocarcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-STAD (`tcga-stad`): in the molecular screen panel; open download. Stomach adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Gastro-oesophageal junction tumours need site review against ESCA.
- No normal-reference patient has retained normal 450k.
- Two gastric Visium resources are listed for review: nine donor labels including one metastasis section, and a 72-section deposit with 20 donor labels whose series summary reports 19 main tumour samples, a discrepancy not yet reconciled. None is yet a verified matched package.
