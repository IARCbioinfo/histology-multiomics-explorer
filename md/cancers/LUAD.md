# Lung adenocarcinoma

Code `LUAD`. Borderline in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=LUAD](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=LUAD). Data: [data/by-cancer/LUAD.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/LUAD.json).

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

11 spatial resources are catalogued; matched image and molecular data have been located for 1. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| Steiner et al. 2026 (`steiner-2026`) | Visium FFPE | Open download | No count reported | Yes, for 13 patients |
| Takano et al. 2024 (`cand-takano-suzuki-2024`) | Visium FFPE | Open download | No count reported | Verification pending |
| De Zuani et al. 2024 (`cand-dezuani-cvejic-2024`); includes normal or adjacent tissue | Visium | Open download | 40 sections in the complete study, all histologies (all cancer sites) | Verification pending |
| Zhao et al. 2025 (`cand-zhao-htapp-2025`) | Visium | Open download | No count reported | Verification pending |
| Peng et al. 2026 (`cand-peng-kadara-2025`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Luo et al. 2024 (`cand-chen-liu-2024`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Visium HD CytAssist Gene Expression Human Lung Cancer post-Xenium experiment (`cand-10x-post-xenium-hd`) | Visium HD | Open download | No count reported | Verification pending |
| METI lung adenocarcinoma sample LUAD-14C (`cand-meti-luad14c`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Defining the cellular and molecular identities of histologic subtypes in lung adenocarcinoma (`cand-knuch-2026`) | Visium | Unresolved | No count reported | Verification pending |
| Deng et al. 2025 (`cand-deng-micropapillary-2025`) | Visium CytAssist | Author request | No count reported | Verification pending |
| Wang et al. 2023 (`cand-lu-cell-discovery-2023`) | Visium | Controlled access | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

Located tissue sections: 15 sections from 13 patients, each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections |
| --- | --- | --- | --- |
| Invasive non-mucinous adenocarcinoma | 13 | 15 | 0 |

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
