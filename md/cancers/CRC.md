# Colorectal adenocarcinoma

Code `CRC`. Pooled analysis cohort (COAD + READ). Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=CRC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=CRC). Data: [data/by-cancer/CRC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/CRC.json).

Colon and rectal adenocarcinomas pooled as one colorectal analysis cohort. The TCGA colorectal study characterised both together and found broadly similar genomic alterations outside the hypermutated group; molecular features also vary along the bowel. The submitted project, reported anatomical site, MSI/MMR status and methylation phenotype should be kept as annotations for location-association checks and colon-only sensitivity analyses. The administrative COAD/READ split should not be treated as a biological boundary.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| CRC, all contributing projects | 579 | 373 | 371 | 581 |
| submitted as TCGA-COAD | 425 | 281 | 279 | 427 |
| submitted as TCGA-READ | 154 | 92 | 92 | 154 |

Normal reference of the cohort after screening: 47 patients with same-sample normal RNA-seq and H&E, 19 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-COAD project | 441 | 287 | 285 | 443 |
| TCGA-READ project | 156 | 94 | 94 | 156 |

## Spatial studies

11 spatial resources are catalogued; matched image and molecular data have been located for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| HTAN WUSTL (Mo et al. 2024) (`htan-wustl`); includes treated tissue; includes metastases | Visium, Visium FFPE | Free account | No count reported | Yes, for 17 patients |
| Valdeolivas et al. 2024 (`valdeolivas-2024`) | Visium | Open download | No count reported | Yes, for 6 patients |
| Oliveira et al. 2025 (Visium HD) (`oliveira-2025`) | Visium HD | Open download | No count reported | Yes, for 3 patients |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors (`cand-crc-colonmap-heiser2023`) | Visium FFPE | Free account | No count reported | Verification pending |
| Neve et al. 2026 (`cand-crc-orgares-gse283052`) | Visium | Open download | No count reported | Verification pending |
| Primary colorectal cancer and liver metastasis, Visium CytAssist (`cand-crc-mahidol-gse267401`) | Visium CytAssist | Open download | No count reported | Verification pending |
| Liu et al. 2026 (`cand-crc-liu-maru2026`) | Visium HD | Open download | No count reported | Verification pending |
| Ren et al. 2025 (`cand-crc-spatch-ren2025`) | Visium HD | Open download | No count reported | Verification pending |
| HTAN Vanderbilt colorectal CytAssist captures (`cand-crc-cottam-htan2025`) | Visium CytAssist | Free account | No count reported | Verification pending |
| Schmauch et al. 2025 (`cand-crc-miso-petacc8`) | Visium FFPE | Controlled access | No count reported | Verification pending |
| Srinivasan et al. 2025 (`cand-crc-vri-dartmouth2025`) | Spatial Transcriptomics (legacy arrays), Visium CytAssist | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

Located tissue sections: 45 sections from 26 patients, each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.

| Stated site | Patients, primary tumour | Sections, primary tumour | Other sections |
| --- | --- | --- | --- |
| Colon adenocarcinoma | 4 | 7 | 3 |
| Rectal adenocarcinoma | 2 | 4 | 1 |
| Bowel site not stated | 0 | 0 | 30 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Hausser et al. analysed TCGA-COAD only. Colon adenocarcinoma met their strong significance criterion and was part of the pooled six-cancer analysis. TCGA-READ, with fewer primary tumours, was not among the 15 cancer types screened, and the pooled colorectal cohort has not been tested for archetype geometry.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-COAD (`tcga-coad`): in the molecular screen panel; open download. Colon adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Analysed with TCGA-READ as the pooled colorectal cohort (CRC). Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.
- TCGA-READ (`tcga-read`): in the molecular screen panel; open download. Rectal adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Below the molecular screen on its own and included through the pooled colorectal cohort (CRC) with TCGA-COAD. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- COAD and READ contributions are submitted-project provenance, not adjudicated pure colon and rectum strata; reported GDC site fields can disagree with each other and with case annotations.
- MSI/MMR status and methylation phenotype are not included in this release; they need to be joined from the TCGA colorectal study or PanCanAtlas subtype resources before location analyses.
- Spatial resources listed here include colon, rectal and colorectal specimens whose bowel site is not stated.
- Treatment-flagged patients are not a treated reference set; one normal-reference donor carries a recurrence annotation.
- Patient identity across COAD and READ was checked from identifiers and annotations, not by genotype.
