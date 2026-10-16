# Breast invasive carcinoma

Code `BRCA`. Significant geometry in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=BRCA](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=BRCA). Data: [data/by-cancer/BRCA.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/BRCA.json).

Breast cancer is one of six TCGA cancer types in which Hausser et al. found significant within-type polyhedral structure in tumour expression, and one of the six pooled in their shared-task analysis. Ductal/NST and lobular carcinomas are kept as separate strata here.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| BRCA | 1,060 | 764 | 762 | 1,062 |

Normal reference of the cohort after screening: 98 patients with same-sample normal RNA-seq and H&E, 73 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-BRCA project | 1,082 | 778 | 775 | 1,085 |

## Spatial studies

8 spatial resources are catalogued; matched image and molecular data have been located for 2. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| HTAN WUSTL (Mo et al. 2024) (`htan-wustl`); includes treated tissue; includes metastases | Visium, Visium FFPE | Free account | No count reported | Yes, for 15 patients |
| Janesick et al. 2023 (`janesick-2023`) | Visium CytAssist | Open download | No count reported | Yes, for 1 patient |
| Wu et al. 2021 (`cand-wu-2021`) | Visium | Open download | No count reported | Verification pending |
| Spatial transcriptomic analysis of a diverse patient cohort reveals a conserved architecture in triple-negative breast cancer (`cand-bassiouni-gse210616`) | Visium | Open download | No count reported | Verification pending |
| 10x Genomics human breast Visium demonstration datasets (`cand-official-10x-breast-demos`) | Visium HD, Visium CytAssist | Open download | No count reported | Verification pending |
| Wang et al. 2024 (`cand-wang-venet-2024-legacy-st`) | Spatial Transcriptomics (legacy arrays) | Open download | No count reported | Verification pending |
| Spatial atlas of tertiary lymphoid structures and high endothelial venules in breast cancer (`cand-bcarc-tls-hev-2026`) | Visium HD | Not released | No count reported | Verification pending |
| TNBC spatial transcriptomics resource (AACR 2026 abstract 1442) (`cand-dartmouth-aacr2026-1442`) | Visium | Not released | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

Located tissue sections: 41 sections from 16 patients, each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections |
| --- | --- | --- | --- |
| Invasive ductal carcinoma / NST | 13 | 38 | 0 |
| Invasive lobular carcinoma | 3 | 3 | 0 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Breast invasive carcinoma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-BRCA (`tcga-brca`): in the molecular screen panel; open download. Breast invasive carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Five ductal/NST patients were sampled after neoadjuvant therapy and one has unknown timing; use the treatment filter for an untreated design.
- One further HTAN ductal donor could be added if its specimen is confirmed as the initial primary rather than recurrent-site tissue.
- Several larger breast spatial cohorts release only downsampled images or are not yet released.
