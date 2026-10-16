# Uterine corpus endometrial carcinoma

Code `UCEC`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=UCEC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=UCEC). Data: [data/by-cancer/UCEC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/UCEC.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation. It meets the molecular screen and is analysed as one pooled endometrial carcinoma cohort, with reviewed histology, grade and the published molecular groups kept as annotations and an endometrioid-only sensitivity subset.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| UCEC | 521 | 415 | 413 | 523 |

Normal reference of the cohort after screening: 34 patients with same-sample normal RNA-seq and H&E, 33 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-UCEC project | 528 | 418 | 416 | 530 |

## Spatial studies

2 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| Barkley et al. 2022, UCEC sample (`ucec-barkley-gse203612`) | Visium | Open download | 1 endometrial carcinoma spatial sample (GSM6177623) | Verification pending |
| Cassier et al. 2023, NP137 trial (`ucec-np137-gse225690`); includes treated tissue; metastases only | Visium FFPE | Open download | 2 patients | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Uterine corpus endometrial carcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-UCEC (`tcga-ucec`): in the molecular screen panel; open download. Uterine corpus endometrial carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Analysed as one pooled cohort with publication-first histology, grade and molecular-group annotations. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Histology comes from the TCGA endometrial study where the case is in its table and from the GDC label otherwise: 398 endometrioid, 112 serous, 12 mixed and one other among the 523 selected patients. These are analysis annotations, not independently reviewed current diagnoses.
- Nineteen cases have a publication histology that differs from the GDC label; both are kept.
- The endometrioid-only subset (398 patients, 303 with both assays) is a sensitivity analysis within the cohort, not a separate cohort. No smaller serous cohort is selected.
- Histological type and the published molecular groups (POLE, MSI, copy-number low and high) do not coincide; a molecular serous-like or endometrioid-like profile is not a reason to exclude a case. Uterine carcinosarcoma (TCGA-UCS) is not added.
- Some retained patients have RNA-seq without 450k methylation, and some normal-reference patients have no retained primary-tumour assay.
- Two endometrial spatial resources are listed for review: one primary-tumour Visium sample, and four metastasis biopsy sections from two donors before and during NP137 treatment, for exploratory treated comparison only. None is yet a verified matched package.
