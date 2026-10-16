# Lung squamous cell carcinoma

Code `LUSC`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=LUSC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=LUSC). Data: [data/by-cancer/LUSC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/LUSC.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation. It meets the molecular screen; about a quarter of retained patients have RNA-seq without 450k methylation.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| LUSC | 471 | 358 | 358 | 471 |

Normal reference of the cohort after screening: 45 patients with same-sample normal RNA-seq and H&E, 8 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-LUSC project | 486 | 363 | 363 | 486 |

## Spatial studies

2 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| De Zuani et al. 2024 (`cand-dezuani-cvejic-2024`); includes normal or adjacent tissue | Visium | Open download | 2 LUSC donors (Patients 11 and 19) | Verification pending |
| 10x Genomics lung SCC, Visium CytAssist FFPE (`lusc-10x-cytassist`) | Visium CytAssist | Free account | 1 sample (vendor specimen) | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Lung squamous cell carcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-LUSC (`tcga-lusc`): in the molecular screen panel; open download. Lung squamous cell carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Few normal-reference patients have retained normal 450k.
- Two LUSC spatial resources are listed for review: a vendor Visium CytAssist FFPE specimen and the LUSC subset of an NSCLC atlas (two donors, six tumour and four adjacent-normal sections). None is yet a verified matched package.
