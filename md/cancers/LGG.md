# Lower-grade glioma

Code `LGG`. Significant geometry in Hausser et al. 2019. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=LGG](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=LGG). Data: [data/by-cancer/LGG.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/LGG.json).

Lower-grade glioma met the strong significance criterion in Hausser et al. and contributed to the pooled analysis. The TCGA LGG cohort predates current molecular glioma classification, so astrocytoma and oligodendroglioma are separated here using IDH and 1p/19q status where available. In the TCGA analyses, LGG is part of the pooled glioma classification benchmark with TCGA-GBM rather than a discovery cohort; the LGG-only set is a subset of that benchmark.

## TCGA reference

Selected analysis panel (classification benchmark). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| Contribution of TCGA-LGG | 502 | 502 | 502 | 502 |
| Pooled GLIOMA cohort, all projects | 643 | 632 | 548 | 727 |

Normal reference of the cohort after screening: 5 patients with same-sample normal RNA-seq and H&E, 1 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-LGG project | 514 | 514 | 514 | 514 |

## Spatial studies

10 spatial resources are catalogued; the original H&E and matched molecular data are located for 1, and matched molecular data with a preview image only for 4. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Greenwald et al. 2024 (`cand-greenwald2024`) | Visium | Open download | 6 IDH-mutant glioma sections | Original H&E located |
| Webb et al. 2025 (`cand-webb2025`) | Visium | Open download | No count reported | Matched data with preview image: 17 sections with a preview image; 1 known patient |
| Ritter et al. 2025 (`cand-ritternepsta2025`) | Visium FFPE | Open download | No count reported | Matched data with preview image: 1 section with a preview image |
| Spatially resolved gene expression and tumour-microenvironment interactions across malignant transformation in IDH-mutant glioma (`cand-longitudinal2026`) | Visium CytAssist | Open download | No count reported | Matched data with preview image: 3 sections with a preview image |
| He et al. 2024 (`cand-he2024`) | Visium | Open download | No count reported | Matched data with preview image: 4 sections with a preview image |
| Hoefflin et al. 2026 (`cand-hoefflin2026`) | Visium | Open download | No count reported | Verification pending |
| Sonpatki et al. 2026 (`cand-snu2026`) | Visium FFPE, Visium, Xenium | Open download | 3 patients with IDH-mutant astrocytoma | Verification pending |
| Tang et al. 2025 (`cand-tang2025`) | Visium HD | Unresolved | No count reported | Verification pending |
| Kuchroo et al. 2022 (`cand-kuchroosparc2022`) | Visium | Unresolved | No count reported | Verification pending |
| Gaspard-Boulinc et al. 2025 (`cand-gaspardboulin2025`) | Visium | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 25 sections (0 with original H&E, 25 with a preview image) from 1 known patient, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| IDH-mutant astrocytoma, grade 2/3 | 0 | 0 | 0 | 0 |
| IDH-mutant, 1p/19q-codeleted oligodendroglioma, grade 2/3 | 0 | 0 | 0 | 0 |
| No stratum assigned | 0 | 0 | 0 | 25 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Lower-grade glioma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-LGG (`tcga-lgg`): in the molecular screen panel; open download. Lower-grade glioma. Slide images, RNA-seq and Illumina 450k methylation from the same patients. Analysed with TCGA-GBM as the pooled glioma classification benchmark (GLIOMA), not as a discovery cohort. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; integrated WHO diagnosis and grade have not been adjudicated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- TCGA-LGG contributes 502 patients, all with both assays, to the glioma classification benchmark (GLIOMA); the LGG-only subset is not counted as a separate cohort.
- Historical histology and grade predate the integrated WHO classification of CNS tumours (2021). Published IDH and 1p/19q groups are annotations; an integrated diagnosis and grade have not been adjudicated.
- No package with verified original-resolution H&E has been confirmed yet.
- The Hoefflin et al. archive names candidate astrocytoma and oligodendroglioma donors; scan resolution and grade assignments still need checking.
