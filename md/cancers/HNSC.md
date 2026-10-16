# Head and neck squamous cell carcinoma

Code `HNSC`. Borderline in Hausser et al. 2019. Release 0.11.1, 16 October 2026. Web page: [cancers.html?c=HNSC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=HNSC). Data: [data/by-cancer/HNSC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/HNSC.json).

Hausser et al. described head and neck cancer as borderline under their significance criterion. HPV status, keratinization and subsite are kept as separate strata because they correspond to different tumour biology.

## TCGA reference

Selected analysis panel (discovery cohort). Primary-tumour patients after assay-quality exclusions, the patient treatment and diagnosis screen and, where stated, histology selection.

| Selected analysis panel | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| HNSC | 506 | 514 | 506 | 514 |

Normal reference of the cohort after screening: 39 patients with same-sample normal RNA-seq and H&E, 20 of them also with normal 450k. Normal tissue comes from patients with cancer, not healthy donors.

Broader availability, not the selected panel: all primary-tumour patients in the project after assay-quality exclusions, before the patient screen and histology selection.

| Broader availability | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients |
| --- | --- | --- | --- | --- |
| TCGA-HNSC project | 514 | 522 | 514 | 522 |

## Spatial studies

13 spatial resources are catalogued; the original H&E and matched molecular data are located for 3, and matched molecular data with a preview image only for 3. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Image level |
| --- | --- | --- | --- | --- |
| Simkin et al. 2026 (`simkin-2026`); includes treated tissue | Visium | Open download | No count reported | Original H&E located: 20 sections with original H&E; 20 known patients |
| Deciphering head and neck cancer microenvironment: Single-cell and spatial transcriptomics reveals HPV-associated differences (`cand-gse281978-hpv2024`); includes metastases | Visium | Open download | No count reported | Original H&E located: 6 sections with original H&E |
| Weeramange et al. 2026 (`cand-frontiers2026-zenodo18238293`) | Visium FFPE | Open download | No count reported | Original H&E located: 11 sections with original H&E; 10 known patients |
| Arora et al. 2023 (`cand-arora2023-gse208253`) | Visium | Open download | 12 spatial samples | Matched data with preview image: 12 sections with a preview image |
| Snail-regulated exosomal microRNA-21 suppresses NLRP3 inflammasome activity to enhance cisplatin resistance (`cand-cheng2022-gse181300`) | Visium | Open download | No count reported | Matched data with preview image: 8 sections with a preview image; 2 known patients |
| Head and neck squamous cell carcinoma immune-checkpoint inhibitor spatial study (`cand-gse301720-ici2026`) | Visium | Open download | No count reported | Matched data with preview image: 8 sections with a preview image |
| Simkin et al. 2026 (`cand-simkin2026-gse268014-hd`) | Visium HD | Open download | No count reported | Verification pending |
| Spatial Transcriptomic Analysis of Surgical Resection Specimens of Primary Head and Neck Squamous Cell Carcinoma Treated with Afatinib in a Window-of-Opportunity Study (EORTC 90111-24111) (`cand-beyaert2025-gse289908`) | Visium FFPE | Open download | No count reported | Verification pending |
| TREM2-Expressing Multinucleated Giant Macrophages Are a Biomarker of Good Prognosis in Head and Neck Squamous Cell Carcinoma (`cand-gessain2024-e-mtab-14409`) | Visium FFPE | Open download | No count reported | Verification pending |
| Deep spatial-omics analysis of Head & Neck carcinomas provides alternative therapeutic targets and rationale for treatment failure (`cand-causer2023-uq`) | Visium | Open download | No count reported | Verification pending |
| Cancer-associated fibroblast subsets in head and neck squamous cell carcinoma (`cand-li2024-hra005551-hra005576`) | Spatial RNA (protocol unverified) | Controlled access | No count reported | Verification pending |
| Hypopharyngeal cancer chemoradiotherapy resistance, spatial transcriptomics (`cand-hypopharynx2025-ccrt`) | Visium CytAssist | Author request | No count reported | Verification pending |
| Integrative spatiotemporal analysis of squamous tumorigenesis (`cand-oraltumorigenesis2025-preprint`) | Visium HD | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located; such sections support molecular maps, not whole-slide or tile models, morphology or distances. Neither level implies completed registration, calibration or tissue QC. Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count.

Located tissue section records: 65 sections (37 with original H&E, 28 with a preview image) from 32 known patients, each with measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum, all with original H&E; other sections are metastatic, under review, held for quality control or outside the stratum. 

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections, original H&E | Other sections, preview image |
| --- | --- | --- | --- | --- |
| HPV-negative keratinizing SCC | 12 | 12 | 0 | 0 |
| HPV-positive nonkeratinizing SCC | 8 | 8 | 0 | 0 |
| No stratum assigned | 0 | 0 | 17 | 28 |

## Selection history: published archetype evidence

### Hausser et al. 2019

- Scale: Bulk tumour RNA (TCGA; METABRIC for breast)
- Definition: Archetypes are vertices of a polytope fitted to tumour expression (Pareto task inference); each vertex is interpreted as a profile specialised for a task.
- Finding: Head and neck squamous cell carcinoma was described as borderline under the authors' significance criterion and was not part of the pooled analysis.
- Limits: Task labels are interpretations of enrichment near each vertex. The five-task result depends on the six selected cancers and on centring within cancer type; it does not establish five tasks in every cancer or in morphology. A negative geometry test in one RNA representation does not show that archetypes are absent. Cancer types outside the screen, including ESCA, PAAD and READ, were not tested.
- Citation: Hausser J, Szekely P, Bar N, Zimmer A, Sheftel H, Caldas C, Alon U. Tumor diversity and the trade-off between universal cancer tasks. Nature Communications 10, 5423 (2019). [doi:10.1038/s41467-019-13195-1](https://www.nature.com/articles/s41467-019-13195-1)

## Other resources

### Whole-slide images with bulk RNA and methylation

- TCGA-HNSC (`tcga-hnsc`): in the molecular screen panel; open download. Head and neck squamous cell carcinoma. Slide images, RNA-seq and Illumina 450k methylation from the same patients, with solid normal tissue from some patients. Counts are shown after PanCanAtlas assay exclusions, after a patient-level treatment and diagnosis screen, and for the selected analysis set. Tumour slide linkage and image QC have not yet been checked; histology strata have not yet been curated. Diagnostic and tissue slides, RNA-seq, Illumina 450k methylation.

## Gaps and cautions

- No patient with primary-tumour sections located is documented as untreated: prior treatment recorded as NA is catalogued as unknown.
- HPV status, keratinization and subsite are kept as separate strata.
