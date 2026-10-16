# Thyroid carcinoma

Code `THCA`. Significant geometry in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=THCA](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=THCA). Data: [data/by-cancer/THCA.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/THCA.json).

Thyroid carcinoma met the strong significance criterion in Hausser et al. and contributed to the pooled analysis. Papillary carcinoma variants and background thyroiditis are recorded where sources report them.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| THCA | 493 | 495 | 493 | 495 |

Normal reference of the cohort after screening: 58 patients with same-sample normal RNA-seq and H&E, 50 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-THCA project | 500 | 502 | 500 | 502 |

## Spatial studies

9 spatial resources are catalogued; matched image and molecular data have been located for 1. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| Zhang et al. 2024 (thyroid) (`zhang-2024-thca`) | Visium | Open download | No count reported | Yes, for 2 patients |
| Liao et al. 2025 (`cand-liao-2025-gse250521`) | Visium | Open download | No count reported | Verification pending |
| Spatial and single-nuclei transcriptomics reveals idiosyncratic and generic patterns in papillary and anaplastic thyroid cancers (`cand-tourneur-2026-legacyst`) | Spatial Transcriptomics (legacy arrays) | Open download | No count reported | Verification pending |
| An integrated single-cell and spatial transcriptomic atlas of thyroid cancer progression identifies prognostic fibroblast subpopulations (`cand-loberg-2026-jci191990`) | Visium FFPE | Author request | No count reported | Verification pending |
| Spatial transcriptomics reveals prognosis-associated cellular heterogeneity in the papillary thyroid carcinoma microenvironment (`cand-yan-2024-hra003537`) | Visium | Controlled access | No count reported | Verification pending |
| Single-cell RNA-sequencing and spatial transcriptomic analysis reveal a distinct population of APOE-negative cells yielding pathological lymph node metastasis in papillary thyroid cancer (`cand-zhang-2025-prjca021247`) | Visium | Unresolved | No count reported | Verification pending |
| Interactions between LAMP3+ dendritic cells and T-cell subpopulations promote immune evasion in papillary thyroid carcinoma (`cand-wang-2024-hra005594`) | Visium FFPE | Author request | No count reported | Verification pending |
| Tumor microenvironment remodeling across thyroid cancer differentiation states revealed by spatial transcriptomics (`cand-seok-2025-cii`) | Visium CytAssist | Author request | No count reported | Verification pending |
| Integrated spatial metabolomics and transcriptomics reveal the molecular landscape of papillary thyroid cancer and its lymph node metastasis (`cand-li-2025-s12967-07566`) | Visium | Author request | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

Located tissue sections: 2 sections from 2 patients, each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections |
| --- | --- | --- | --- |
| Papillary thyroid carcinoma, variant not specified | 2 | 2 | 0 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Thyroid carcinoma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-THCA (`tcga-thca`): in the molecular screen panel; open download. Thyroid carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Both patients with primary-tumour sections located have background Hashimoto thyroiditis and no reported treatment history; no case of classical-variant papillary carcinoma alone is verified.
- Further thyroid spatial cohorts lack released original-resolution scans or require requests.
