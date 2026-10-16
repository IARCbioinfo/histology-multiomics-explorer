# Head and neck squamous cell carcinoma

Code `HNSC`. Borderline in Hausser et al. 2019. Release 0.9.3, 16 October 2026. Web page: [cancers.html?c=HNSC](https://iarcbioinfo.github.io/histology-multiomics-explorer/cancers.html?c=HNSC). Data: [data/by-cancer/HNSC.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/by-cancer/HNSC.json).

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

13 spatial resources are catalogued; matched image and molecular data have been located for 1. Verification is pending for the others. These studies usually involve patients other than those in TCGA.

| Study | Assay | Access | Reported by the study | Matched data located |
| --- | --- | --- | --- | --- |
| Simkin et al. 2026 (`simkin-2026`); includes treated tissue | Visium | Open download | No count reported | Yes, for 20 patients |
| Simkin et al. 2026 (`cand-simkin2026-gse268014-hd`) | Visium HD | Open download | No count reported | Verification pending |
| Arora et al. 2023 (`cand-arora2023-gse208253`) | Visium | Open download | No count reported | Verification pending |
| Snail-regulated exosomal microRNA-21 suppresses NLRP3 inflammasome activity to enhance cisplatin resistance (`cand-cheng2022-gse181300`) | Visium | Open download | No count reported | Verification pending |
| Deciphering head and neck cancer microenvironment: Single-cell and spatial transcriptomics reveals HPV-associated differences (`cand-gse281978-hpv2024`) | Visium | Open download | No count reported | Verification pending |
| Spatial Transcriptomic Analysis of Surgical Resection Specimens of Primary Head and Neck Squamous Cell Carcinoma Treated with Afatinib in a Window-of-Opportunity Study (EORTC 90111-24111) (`cand-beyaert2025-gse289908`) | Visium FFPE | Open download | No count reported | Verification pending |
| Weeramange et al. 2026 (`cand-frontiers2026-zenodo18238293`) | Visium FFPE | Open download | No count reported | Verification pending |
| Deep spatial-omics analysis of Head & Neck carcinomas provides alternative therapeutic targets and rationale for treatment failure (`cand-causer2023-uq`) | Visium | Open download | No count reported | Verification pending |
| Head and neck squamous cell carcinoma immune-checkpoint inhibitor spatial study (`cand-gse301720-ici2026`) | Visium | Open download | No count reported | Verification pending |
| TREM2-Expressing Multinucleated Giant Macrophages Are a Biomarker of Good Prognosis in Head and Neck Squamous Cell Carcinoma (`cand-gessain2024-e-mtab-14409`) | Visium FFPE | Controlled access | No count reported | Verification pending |
| Cancer-associated fibroblast subsets in head and neck squamous cell carcinoma (`cand-li2024-hra005551-hra005576`) | Spatial RNA (protocol unverified) | Controlled access | No count reported | Verification pending |
| Hypopharyngeal cancer chemoradiotherapy resistance, spatial transcriptomics (`cand-hypopharynx2025-ccrt`) | Visium CytAssist | Author request | No count reported | Verification pending |
| Integrative spatiotemporal analysis of squamous tumorigenesis (`cand-oraltumorigenesis2025-preprint`) | Visium HD | Unresolved | No count reported | Verification pending |

Study-reported numbers keep each study's own unit and are not added together. Located means the image and molecular files were found; it does not imply completed image registration or tissue QC.

Located tissue sections: 20 sections from 20 patients, each with an original H&E image, measured spatial RNA and coordinates. Primary tumour counts sections from primary tumours within the stratum; other sections are metastatic, under review, held for quality control or outside the stratum.

| Histology stratum | Patients, primary tumour | Sections, primary tumour | Other sections |
| --- | --- | --- | --- |
| HPV-negative keratinizing SCC | 12 | 12 | 0 |
| HPV-positive nonkeratinizing SCC | 8 | 8 | 0 |

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
