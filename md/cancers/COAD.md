# Colon adenocarcinoma

Code `COAD`. Significant geometry in Hausser et al. 2019. Release 0.11.1, 16 October 2026. Web page: [cancers.html?c=COAD](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=COAD). Data: [data/by-cancer/COAD.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/COAD.json).

Colon adenocarcinoma met the strong significance criterion in Hausser et al. and contributed to the pooled six-cancer analysis. Mucinous carcinomas and metastatic deposits are listed but kept outside the conventional primary stratum.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection. Each patient counts once in the pooled cohort; project rows show where patients were submitted.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| Contribution of TCGA-COAD | 425 | 281 | 279 | 427 |
| Pooled CRC cohort, all projects | 579 | 373 | 371 | 581 |

Normal reference of the cohort after screening: 47 patients with same-sample normal RNA-seq and H&E, 19 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-COAD project | 441 | 287 | 285 | 443 |

## Spatial studies

11 spatial resources are catalogued; the original H&E and matched molecular data are located for 3, and matched molecular data with a preview image only for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| HTAN WUSTL (Mo et al. 2024) (`htan-wustl`); includes metastases | Visium, Visium FFPE | Free account | No count reported | Original H&E located: 1 section with original H&E; 1 known patient |
| Valdeolivas et al. 2024 (`valdeolivas-2024`) | Visium | Open download | No count reported | Original H&E located: 8 sections with original H&E; 4 known patients |
| Oliveira et al. 2025 (Visium HD) (`oliveira-2025`) | Visium HD | Open download | No count reported | Original H&E located: 1 section with original H&E; 1 known patient |
| Neve et al. 2026 (`cand-crc-orgares-gse283052`) | Visium | Open download | No count reported | Matched data with preview image |
| Primary colorectal cancer and liver metastasis, Visium CytAssist (`cand-crc-mahidol-gse267401`) | Visium CytAssist | Open download | No count reported | Matched data with preview image |
| Liu et al. 2026 (`cand-crc-liu-maru2026`) | Visium HD | Open download | No count reported | Matched data with preview image |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors (`cand-crc-colonmap-heiser2023`) | Visium FFPE | Free account | No count reported | Verification pending |
| Ren et al. 2025 (`cand-crc-spatch-ren2025`) | Visium HD | Open download | No count reported | Verification pending |
| HTAN Vanderbilt colorectal CytAssist captures (`cand-crc-cottam-htan2025`) | Visium CytAssist | Free account | No count reported | Verification pending |
| Schmauch et al. 2025 (`cand-crc-miso-petacc8`) | Visium FFPE | Controlled access | No count reported | Verification pending |
| Srinivasan et al. 2025 (`cand-crc-vri-dartmouth2025`) | Spatial Transcriptomics (legacy arrays), Visium CytAssist | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 10 sections (10 with original H&E, 0 with a preview image) from 6 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| Conventional colon adenocarcinoma | 4 | 7 | 0 | 0 |
| No stratum assigned | 0 | 0 | 3 | 0 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Colon adenocarcinoma was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. After removing cancer-type means, 3,180 tumours from the six significant types fitted five archetypes, interpreted as cell division, biomass and energy, lipogenesis, immune interaction and invasion/tissue remodelling.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-COAD (`tcga-coad`): in the molecular screen panel; open download. Colon adenocarcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Analysed with TCGA-READ as the pooled colorectal cohort (CRC). Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- TCGA-COAD is analysed with TCGA-READ as the pooled colorectal cohort (CRC); its counts here are provenance, and two COAD-submitted rectal primaries previously excluded for site alone are now included in CRC.
- Valdeolivas et al. sections must be located on the original whole-slide scans before patch-level alignment.
- The Colon Molecular Atlas Project (HTAN Vanderbilt) is the largest candidate expansion and needs histology review.
- Most HTAN colorectal sections are from metastatic deposits and are kept separate from the primary stratum.
