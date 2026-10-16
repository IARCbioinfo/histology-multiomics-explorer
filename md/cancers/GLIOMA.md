# Diffuse glioma classification benchmark

Code `GLIOMA`. Pooled analysis cohort (LGG + GBM). Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=GLIOMA](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=GLIOMA). Data: [data/by-cancer/GLIOMA.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/GLIOMA.json).

TCGA-LGG and TCGA-GBM pooled as one classification benchmark rather than a discovery cohort. It asks whether a molecular target, frozen before comparison, recovers the historical diagnosis-plus-grade labels or an independently curated integrated (WHO CNS5) diagnosis and grade better, using held-out comparisons and sensitivity analyses within each entity. Recovering known diagnostic groups would not by itself show that the target adds biological information.

## TCGA reference

Selected analysis panel (classification benchmark). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| GLIOMA, all contributing projects | 643 | 632 | 548 | 727 |
| submitted as TCGA-LGG | 502 | 502 | 502 | 502 |
| submitted as TCGA-GBM | 141 | 130 | 46 | 225 |

Normal reference of the cohort after screening: 5 patients with same-sample normal RNA-seq and H&E, 1 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-LGG project | 514 | 514 | 514 | 514 |
| TCGA-GBM project | 154 | 139 | 51 | 242 |

## Spatial studies

10 spatial resources are catalogued; the original H&E and matched molecular data are located for 1, and matched molecular data with a preview image only for 4. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Greenwald et al. 2024 (`cand-greenwald2024`) | Visium | Open download | 19 sections in the study | Original H&E located: 12 sections with original H&E; 7 sections with a preview image only |
| Webb et al. 2025 (`cand-webb2025`) | Visium | Open download | No count reported | Matched data with preview image: 17 sections with a preview image |
| Ritter et al. 2025 (`cand-ritternepsta2025`) | Visium FFPE | Open download | No count reported | Matched data with preview image: 46 sections with a preview image |
| Spatially resolved gene expression and tumour-microenvironment interactions across malignant transformation in IDH-mutant glioma (`cand-longitudinal2026`) | Visium CytAssist | Open download | No count reported | Matched data with preview image: 3 sections with a preview image |
| He et al. 2024 (`cand-he2024`) | Visium | Open download | No count reported | Matched data with preview image: 4 sections with a preview image |
| Hoefflin et al. 2026 (`cand-hoefflin2026`) | Visium | Open download | No count reported | Verification pending |
| Sonpatki et al. 2026 (`cand-snu2026`) | Visium FFPE, Visium, Xenium | Open download | 17 patients in all, including one normal-brain control | Verification pending |
| Tang et al. 2025 (`cand-tang2025`) | Visium HD | Unresolved | No count reported | Verification pending |
| Kuchroo et al. 2022 (`cand-kuchroosparc2022`) | Visium | Unresolved | No count reported | Verification pending |
| Gaspard-Boulinc et al. 2025 (`cand-gaspardboulin2025`) | Visium | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 89 sections (12 with original H&E, 77 with a preview image) from 0 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. Checked preview packages that are not listed one by one are not included.

| Stated site | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Lower-grade glioma | 0 | 0 | 0 | 25 |
| Glioblastoma (historical TCGA diagnosis) | 0 | 0 | 0 | 44 |
| Glioma, project not stated | 0 | 0 | 12 | 8 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Hausser et al. analysed TCGA-LGG, which met their strong significance criterion and was part of the pooled six-cancer analysis. TCGA-GBM was not among the 15 cancer types screened. The pooled glioma set is used here as a classification benchmark, not as evidence of archetype geometry.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-LGG (`tcga-lgg`): in the molecular screen panel; open download. Lower-grade glioma. Slide images, RNA-seq and Illumina 450k methylation from the same patients. Analysed with TCGA-GBM as the pooled glioma classification benchmark (GLIOMA), not as a discovery cohort. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; integrated WHO diagnosis and grade have not been adjudicated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.
- TCGA-GBM (`tcga-gbm`): in the molecular screen panel; open download. Glioblastoma, as historically diagnosed in TCGA. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from a few donors. Below the molecular screen on its own and included only through the pooled glioma classification benchmark (GLIOMA) with TCGA-LGG. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; integrated WHO diagnosis and grade have not been adjudicated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Integrated WHO diagnosis and grade have not been independently adjudicated. They are not inferred from RNA or methylation clusters, IDH-wildtype status is not equated with glioblastoma, and historical GBM is not treated as an integrated entity.
- Project, platform and missing views are confounded: LGG contributes 502 paired patients and GBM 46, and most GBM patients have only one assay. Run the paired-only sensitivity (548 patients) and check project and assay effects before interpreting classification recovery.
- Published molecular groups are annotations: 254 IDH-mutant non-codeleted, 163 IDH-mutant codeleted and 295 IDH-wildtype among the 727 selected patients. The 15 without a complete published group are not the same as 15 with unknown IDH status; raw IDH and 1p/19q calls are kept separately.
- The LGG-only subset (502 patients, all paired) is part of the benchmark and is not counted again in panel totals. Selected membership is not split by IDH or 1p/19q.
- The five normal packages are GBM-origin, normal-only donors without a reported primary diagnosis, not verified matched controls; LGG has none.
- Supportive dexamethasone and anticonvulsant use is a covariate, distinct from antineoplastic pretreatment; its effect on immune programmes remains relevant.
- Spatial candidates: Greenwald et al. (19 sections; 13 IDH-wildtype from five donor labels and six IDH-mutant from six) and the niche atlas (32 genotyped glioma sections, Xenium from four patients). Section counts are not patient counts, and no spatial package is verified yet.
- Tumour slide linkage and image QC are not yet checked.
