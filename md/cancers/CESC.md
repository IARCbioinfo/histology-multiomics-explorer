# Cervical squamous cell carcinoma and endocervical adenocarcinoma

Code `CESC`. Molecular screen; no geometry detected in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=CESC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=CESC). Data: [data/by-cancer/CESC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/CESC.json).

Hausser et al. screened this cancer type and detected no significant archetype geometry in their RNA representation; that result does not rule out archetypes under another representation. It is included because it meets the RNA and 450k methylation screen. Analyses use cervical squamous cell carcinoma (CSCC), selected by histology from the TCGA cervical study with the GDC label as an explicit fallback; adenocarcinomas and adenosquamous carcinomas are outside the selected cohort.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| CSCC: Cervical squamous cell carcinoma | 248 | 249 | 248 | 249 |

Normal reference of the cohort after screening: 2 patients with same-sample normal RNA-seq and H&E, 2 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-CESC project | 300 | 302 | 300 | 302 |

## Spatial studies

3 spatial resources are catalogued. Verification of the matched image and molecular data is pending. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| 10x Genomics cervical SCC, Visium FFPE (`cscc-10x-ffpe`) | Visium FFPE | Free account | 1 section (vendor specimen) | Verification pending |
| Guo et al. 2023, HPV progression series (`cscc-hpv-gse208654`); includes normal or adjacent tissue; includes precursor lesions | Spatial transcriptomics array (platform to confirm) | Open download | 1 squamous cell carcinoma section (GSM6360691) | Verification pending |
| Ou et al. 2022 (`cscc-ou-stereo`); includes normal or adjacent tissue; H&E from serial sections | Stereo-seq | Unresolved | 14 tumour patients | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Cervical squamous cell carcinoma and endocervical adenocarcinoma was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-CESC (`tcga-cesc`): in the molecular screen panel; open download. Cervical squamous cell carcinoma and endocervical adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. The selected cohort is cervical squamous cell carcinoma (CSCC), using histology from the TCGA cervical study with the GDC label as fallback. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- CSCC histology comes from the TCGA cervical study's merged diagnosis where the case is in that table and from the GDC morphology label otherwise. Three cases differ between the two sources and are listed with both labels.
- 46 adenocarcinomas and six adenosquamous carcinomas are outside the selected cohort. Their assays remain valid; they are not marked as failed or relabelled.
- HPV status and the endometrial-like group from the publication are annotations, not exclusion criteria; keratin-high and keratin-low programmes are variation within the cohort.
- A duplicate patient is counted once: the second biopsy record is excluded from independent counts.
- The CSCC normal reference is two squamous-donor packages; a third TCGA-CESC normal package comes from an adenocarcinoma donor and is not a matched CSCC control.
- Histology comes from publication tables and GDC labels, not a new slide review; tumour slide linkage and image QC are not yet checked.
- Three cervical spatial resources are listed for review: one vendor Visium FFPE squamous carcinoma specimen, one public SCC section from an HPV progression series (its adenocarcinoma, normal and HSIL sections are kept separate) and a Stereo-seq study with serial-section H&E. None is yet a verified matched package.
