# Lung adenocarcinoma

Code `LUAD`. Borderline in Hausser et al. 2019. Release 0.11.0, 16 October 2026. Web page: [cancers.html?c=LUAD](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=LUAD). Data: [data/by-cancer/LUAD.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/LUAD.json).

Hausser et al. described lung as borderline under their significance criterion, so it was not part of the pooled analysis. Predominant growth patterns are recorded for each tissue section where the source provides them.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| LUAD | 453 | 407 | 403 | 457 |

Normal reference of the cohort after screening: 56 patients with same-sample normal RNA-seq and H&E, 19 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-LUAD project | 457 | 410 | 406 | 461 |

## Spatial studies

11 spatial resources are catalogued; the original H&E and matched molecular data are located for 2, and matched molecular data with a preview image only for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Steiner et al. 2026 (`steiner-2026`) | Visium FFPE | Open download | No count reported | Original H&E located: 15 sections with original H&E; 13 known patients |
| Takano et al. 2024 (`cand-takano-suzuki-2024`) | Visium FFPE | Open download | No count reported | Original H&E located: 1 section with original H&E; 1 known patient |
| De Zuani et al. 2024 (`cand-dezuani-cvejic-2024`); includes normal or adjacent tissue | Visium | Open download | 40 sections in the complete study, all histologies (all cancer sites) | Matched data with preview image |
| Peng et al. 2026 (`cand-peng-kadara-2025`) | Visium CytAssist | Open download | No count reported | Matched data with preview image: 56 sections with a preview image; 25 known patients |
| Luo et al. 2024 (`cand-chen-liu-2024`) | Visium CytAssist | Open download | No count reported | Matched data with preview image: 2 sections with a preview image |
| Zhao et al. 2025 (`cand-zhao-htapp-2025`) | Visium | Open download | No count reported | Verification pending |
| Visium HD CytAssist Gene Expression Human Lung Cancer post-Xenium experiment (`cand-10x-post-xenium-hd`) | Visium HD | Open download | No count reported | Verification pending |
| METI lung adenocarcinoma sample LUAD-14C (`cand-meti-luad14c`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Defining the cellular and molecular identities of histologic subtypes in lung adenocarcinoma (`cand-knuch-2026`) | Visium | Unresolved | No count reported | Verification pending |
| Deng et al. 2025 (`cand-deng-micropapillary-2025`) | Visium CytAssist | Author request | No count reported | Verification pending |
| Wang et al. 2023 (`cand-lu-cell-discovery-2023`) | Visium | Controlled access | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 74 sections (16 with original H&E, 58 with a preview image) from 39 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Invasive non-mucinous adenocarcinoma | 13 | 15 | 0 | 0 |
| No stratum assigned | 0 | 0 | 1 | 58 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Lung adenocarcinoma was described as borderline under the authors' significance criterion and was not part of the pooled analysis.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-LUAD (`tcga-luad`): in the molecular screen panel; open download. Lung adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- All patients with primary-tumour sections located are untreated stage I resections from one study.
- Other candidate cohorts need image calibration, QC or donor crosswalks.
- TCGA-LUAD pathology-group exclusions include unclassified non-small cell carcinoma and cases favouring large cell neuroendocrine carcinoma. EPIC v2 methylation for 53 patients is a different platform and is not counted.
