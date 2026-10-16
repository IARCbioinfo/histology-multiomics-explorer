# Liver hepatocellular carcinoma

Code `LIHC`. Significant geometry in Hausser et al. 2019. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=LIHC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=LIHC). Data: [data/by-cancer/LIHC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/LIHC.json).

Hepatocellular carcinoma met the strong significance criterion in Hausser et al. and contributed to the pooled analysis. Combined hepatocellular–cholangiocarcinoma and post-treatment cohorts are kept separate.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| LIHC | 351 | 357 | 351 | 357 |

Normal reference of the cohort after screening: 50 patients with same-sample normal RNA-seq and H&E, 41 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-LIHC project | 362 | 368 | 362 | 368 |

## Spatial studies

17 spatial resources are catalogued; the original H&E and matched molecular data are located for 1, and matched molecular data with a preview image only for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Giraud et al. 2024 (`gse245908-lihc`) | Visium | Open download | No count reported | Original H&E located: 2 sections with original H&E; 2 known patients |
| Spatial transcriptomics analysis of neoadjuvant cabozantinib and nivolumab in advanced hepatocellular carcinoma identifies independent mechanisms of resistance and recurrence (`cand-gse238264`); includes treated tissue | Visium | Open download | No count reported | Matched data with preview image: 7 sections with a preview image; 7 known patients |
| Multiomics and multi-region spatial transcriptome analysis reveal cellular networks and pathways associated with hepatocellular carcinoma recurrence (`cand-gse281759`) | Visium | Open download | No count reported | Matched data with preview image: 17 sections with a preview image; 3 known patients |
| Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in hepatocellular carcinoma (`cand-wu2025-zenodo`); includes treated tissue | Visium FFPE | Open download | No count reported | Matched data with preview image: 22 sections with a preview image |
| Ren et al. 2025 (`cand-spatch-hcc`) | Visium HD | Open download | No count reported | Verification pending |
| Wu et al. 2021 (`cand-wu2021-hcc`) | Visium | Open download | No count reported | Verification pending |
| Deep versus standard spatial transcriptomic sequencing (`cand-gse283406`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Lau et al. 2022 (`cand-prjna858545-hcc`) | Visium | Open download | No count reported | Verification pending |
| Jia et al. 2025 (`cand-times-hra006579`) | Visium FFPE | Unresolved | No count reported | Verification pending |
| Jing et al. 2024 (`cand-he2024-new4plc`) | Visium | Controlled access | No count reported | Verification pending |
| Fan et al. 2024 (`cand-fan2024-hra006757`) | Visium FFPE | Controlled access | No count reported | Verification pending |
| Murai et al. 2022 (`cand-jgad000422-hcc`) | Visium | Controlled access | No count reported | Verification pending |
| 10x Visium Spatial Transcriptomics of 61 Human HCC Samples (`cand-egad50000002122`) | Visium | Controlled access | No count reported | Verification pending |
| Targeting Treg–fibroblast interaction to enhance immunotherapy in SLD-related HCC (`cand-egad50000001506`) | Visium CytAssist | Controlled access | No count reported | Verification pending |
| Spatial Transcriptomics Reveals Distinct Architectures but Shared Vulnerabilities in Primary and Metastatic Liver Tumors (`cand-adapa2025-hd`) | Visium HD | Unresolved | No count reported | Verification pending |
| Spatial maps of hepatocellular carcinoma transcriptomes reveal spatial expression patterns in tumor immune microenvironment (`cand-xin2022-hcc`) | Visium | Unresolved | No count reported | Verification pending |
| Spatial Transcriptomics and snRNA-seq Expose CAF Niches Orchestrating Dual Stromal-Immune Barriers in Hepatocellular Carcinoma (`cand-li2025-caf`) | Visium | Author request | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 48 sections (2 with original H&E, 46 with a preview image) from 12 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Hepatocellular carcinoma NOS | 2 | 2 | 0 | 0 |
| No stratum assigned | 0 | 0 | 0 | 46 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Liver hepatocellular carcinoma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-LIHC (`tcga-lihc`): in the molecular screen panel; open download. Liver hepatocellular carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Only two patients have primary-tumour sections located, and their image calibration estimates disagree.
- Several larger cohorts are controlled, post-treatment or lack original scans.
