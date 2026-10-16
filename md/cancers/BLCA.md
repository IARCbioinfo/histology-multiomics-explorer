# Bladder urothelial carcinoma

Code `BLCA`. Significant geometry in Hausser et al. 2019. Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=BLCA](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=BLCA). Data: [data/by-cancer/BLCA.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/BLCA.json).

Bladder urothelial carcinoma met the strong significance criterion in Hausser et al. and contributed to the pooled analysis. Variant morphology is not always reported and may need pathology review.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| BLCA | 382 | 388 | 382 | 388 |

Normal reference of the cohort after screening: 19 patients with same-sample normal RNA-seq and H&E, 17 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-BLCA project | 395 | 401 | 395 | 401 |

## Spatial studies

10 spatial resources are catalogued; the original H&E and matched molecular data are located for 2, and matched molecular data with a preview image only for 2. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Gouin et al. 2021 (`gouin-2021`) | Visium | Open download | No count reported | Original H&E located: 4 sections with original H&E; 4 known patients |
| Batf3+ DCs and the 4–1BB/4–1BBL axis are required at the effector phase in the tumor microenvironment for PD-1/PD-L1 blockade efficacy (`cand-ziblat2024`) | Visium HD, Visium CytAssist | Open download | No count reported | Original H&E located: 2 sections with original H&E; 10 sections with a preview image only; 8 known patients |
| Yu et al. 2026 (`cand-yu2026atlas`) | Visium CytAssist | Open download | No count reported | Matched data with preview image: 22 sections with a preview image |
| Unveiling Immune Metabolic Mechanisms in Bladder Cancer: Spatial Profiling Identifies ZFP36 as a Therapeutic Target (`cand-zheng2025`) | Visium | Open download | No count reported | Matched data with preview image: 6 sections with a preview image |
| Jiang et al. 2024 (`cand-jiang2024meti`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Yoshihara et al. 2026 (`cand-yoshihara2026erbt`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Pribus et al. 2026 (`cand-pribus2026`) | Visium | Open download | No count reported | Verification pending |
| Grande et al. 2025 (`cand-dutreneo`) | Visium FFPE | Open download | No count reported | Verification pending |
| Integrated single-cell and spatial transcriptomic profiling reveals higher intratumour heterogeneity and epithelial–fibroblast interactions in recurrent bladder cancer (`cand-xuzhou2023`) | Visium | Unresolved | No count reported | Verification pending |
| Single-nucleus and Spatially Resolved Intratumor Subtype Heterogeneity in Bladder Cancer (`cand-lindskrog2023`) | Visium | Controlled access | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 44 sections (6 with original H&E, 38 with a preview image) from 12 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. Checked preview packages that are not listed one by one are not included.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| High-grade muscle-invasive urothelial carcinoma | 4 | 4 | 0 | 0 |
| No stratum assigned | 0 | 0 | 2 | 38 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Bladder urothelial carcinoma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-BLCA (`tcga-blca`): in the molecular screen panel; open download. Bladder urothelial carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Variant morphology of the four primary tumours with located data has not been reviewed.
- A larger untreated muscle-invasive cohort (GSE319536) releases only downsampled H&E.
