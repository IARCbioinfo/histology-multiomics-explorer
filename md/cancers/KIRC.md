# Kidney renal clear cell carcinoma

Code `KIRC`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=KIRC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=KIRC). Data: [data/by-cancer/KIRC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/KIRC.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation. It meets the molecular screen; a large share of retained patients have RNA-seq without 450k methylation.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| KIRC | 493 | 306 | 305 | 494 |

Normal reference of the cohort after screening: 71 patients with same-sample normal RNA-seq and H&E, 23 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-KIRC project | 515 | 312 | 311 | 516 |

## Spatial studies

4 spatial resources are catalogued; matched molecular data with a preview image only for 2. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Meylan et al. 2022 (`kirc-meylan-gse175540`) | Visium FFPE, Visium | Open download | 24 spatial samples | Matched data with preview image: 24 sections with a preview image, not listed one by one |
| GSE294006, treated advanced ccRCC (`kirc-treated-gse294006`); includes treated tissue | Visium FFPE | Open download | 3 primary-tumour samples after systemic treatment | Matched data with preview image: 3 sections with a preview image, not listed one by one |
| Li et al. 2022, ccRCC Visium (EGAD00001008781) (`kirc-egad00001008781`) | Visium | Open download | 8 patients with ccRCC | Verification pending |
| 10x Genomics ccRCC, Xenium RNA and protein (`kirc-10x-xenium-protein`) | Xenium | Free account | 1 sample (vendor specimen) | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Kidney renal clear cell carcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-KIRC (`tcga-kirc`): in the molecular screen panel; open download. Kidney renal clear cell carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Analyse separately from papillary renal cell carcinoma (KIRP).
- Four clear-cell RCC spatial resources are listed for review: 24 public Visium samples (not a verified count of independent untreated patients), 16 controlled sections, three treated primary tumours for exploratory comparison and one targeted Xenium RNA-and-protein specimen. None is yet a verified matched package.
