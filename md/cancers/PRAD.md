# Prostate adenocarcinoma

Code `PRAD`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.10.0, 16 October 2026. Web page: [cancers.html?c=PRAD](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=PRAD). Data: [data/by-cancer/PRAD.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/PRAD.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation. It meets the molecular screen after a substantial number of pathology-group exclusions.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| PRAD | 401 | 402 | 401 | 402 |

Normal reference of the cohort after screening: 48 patients with same-sample normal RNA-seq and H&E, 32 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-PRAD project | 405 | 406 | 405 | 406 |

## Spatial studies

4 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| 10x Genomics prostate acinar carcinoma, Visium FFPE (`prad-10x-acinar`) | Visium FFPE | Free account | 1 sample (vendor specimen) | Verification pending |
| 10x Genomics prostate invasive adenocarcinoma, Visium FFPE (`prad-10x-invasive`) | Visium FFPE | Free account | 1 sample (vendor specimen) | Verification pending |
| Hirz et al. 2023 (`prad-hirz-slideseq`); includes normal or adjacent tissue; H&E from serial sections | Slide-seqV2 | Open download | 2 prostate cancer donors | Verification pending |
| Erickson et al. 2022 (`prad-erickson-clonal`); includes normal or adjacent tissue | Spatial Transcriptomics (legacy arrays), Visium | Open download | 2 patients with public image folders | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Prostate adenocarcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-PRAD (`tcga-prad`): in the molecular screen panel; open download. Prostate adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- Many tumour aliquots carry pathology-group exclusions for RNA degradation, so the retained count is well below raw availability.
- Four prostate spatial resources are listed for review: two vendor Visium FFPE specimens (not assumed to come from distinct patients), a Slide-seqV2 study with two cancer donors and consecutive-section H&E, and a legacy Spatial Transcriptomics clonal-mapping release. None is yet a verified matched package.
