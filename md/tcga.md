# TCGA reference

Release 0.11.0, 16 October 2026. Web page: [tcga.html](https://iarcbioinfo.github.io/histology-multiomics-explorer/tcga.html). Data: [tcga_eligibility.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_eligibility.json), [tcga_counts.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_counts.json), [tcga_patient_review.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_patient_review.json), [tcga_patients.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_patients.json).

The Cancer Genome Atlas (TCGA) holds tumour and normal tissue from thousands of patients across many cancer types, with slide images and molecular measurements released through the NCI Genomic Data Commons. TCGA is reported in two ways here. Data availability is what each project provides after assay-quality exclusions. The selected analysis panel is a selection for studies of tumour heterogeneity, which adds a patient treatment and diagnosis screen, histology-defined and pooled cohorts, and a minimum cohort size.

## Size threshold

A cohort enters the panel only if it has enough patients for the planned RNA-seq and methylation analyses: at least 150 patients with a primary-tumour RNA-seq or 450k methylation profile, and at least 100 of them with both. Patients are counted once, after assay-quality exclusions and before the treatment and diagnosis screen.

- It applies to the analysis cohort, not to the TCGA project. Colorectal cancer (CRC: 599 patients, 379 with both) and diffuse glioma (GLIOMA: 756 and 565) are pooled cohorts; TCGA-READ (156 and 94) and TCGA-GBM (242 and 51) would not pass on their own.
- Where a project mixes distinct diseases, the cohort is the histology analysed: oesophageal squamous cell carcinoma (ESCC) from TCGA-ESCA, which also contains adenocarcinoma; cervical squamous cell carcinoma (CSCC) from TCGA-CESC, which also contains adenocarcinoma; and pancreatic ductal adenocarcinoma (PDAC) from TCGA-PAAD, which also contains a few adenosquamous, colloid and other carcinomas.
- Two cohorts are explicit exceptions: ESCC has 90 patients, below both limits, and PDAC has 149, one patient below the total limit.
- Sarcoma is not in the panel. TCGA-SARC passes as a project (225 patients, 223 with both), but it combines several distinct sarcoma types, each below the threshold: the largest, soft-tissue leiomyosarcoma, has 53 patients, and all leiomyosarcomas together 87.

## Selected analysis panel

18 analysis cohorts from 20 TCGA projects: 17 discovery cohorts and 1 glioma classification benchmark. 7,826 patients, 6,561 with both RNA-seq and 450k methylation.

| Cancer cohort | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients | Normal RNA-seq + H&E | Normal with 450k |
| --- | --- | --- | --- | --- | --- | --- |
| Bladder urothelial carcinoma (BLCA; TCGA-BLCA) | 382 | 388 | 382 | 388 | 19 | 17 |
| Breast invasive carcinoma (BRCA; TCGA-BRCA) | 1,060 | 764 | 762 | 1,062 | 98 | 73 |
| Colorectal adenocarcinoma (CRC; TCGA-COAD + TCGA-READ) | 579 | 373 | 371 | 581 | 47 | 19 |
| Cervical squamous cell carcinoma (CSCC; TCGA-CESC) | 248 | 249 | 248 | 249 | 2 | 2 |
| Confirmed oesophageal squamous cell carcinoma (ESCC; TCGA-ESCA) | 90 | 90 | 90 | 90 | 2 | 2 |
| Diffuse glioma classification benchmark (GLIOMA; TCGA-LGG + TCGA-GBM) | 643 | 632 | 548 | 727 | 5 | 1 |
| Head and neck squamous cell carcinoma (HNSC; TCGA-HNSC) | 506 | 514 | 506 | 514 | 39 | 20 |
| Kidney renal clear cell carcinoma (KIRC; TCGA-KIRC) | 493 | 306 | 305 | 494 | 71 | 23 |
| Kidney renal papillary cell carcinoma (KIRP; TCGA-KIRP) | 274 | 262 | 261 | 275 | 32 | 23 |
| Liver hepatocellular carcinoma (LIHC; TCGA-LIHC) | 351 | 357 | 351 | 357 | 50 | 41 |
| Lung adenocarcinoma (LUAD; TCGA-LUAD) | 453 | 407 | 403 | 457 | 56 | 19 |
| Lung squamous cell carcinoma (LUSC; TCGA-LUSC) | 471 | 358 | 358 | 471 | 45 | 8 |
| Pheochromocytoma and paraganglioma (PCPG; TCGA-PCPG) | 178 | 178 | 178 | 178 | 3 | 3 |
| Pancreatic ductal adenocarcinoma (PDAC; TCGA-PAAD) | 143 | 149 | 143 | 149 | 4 | 4 |
| Prostate adenocarcinoma (PRAD; TCGA-PRAD) | 401 | 402 | 401 | 402 | 48 | 32 |
| Stomach adenocarcinoma (STAD; TCGA-STAD) | 385 | 377 | 348 | 414 | 34 | 0 |
| Thyroid carcinoma (THCA; TCGA-THCA) | 493 | 495 | 493 | 495 | 58 | 50 |
| Uterine corpus endometrial carcinoma (UCEC; TCGA-UCEC) | 521 | 415 | 413 | 523 | 34 | 33 |
| All 18 cohorts (20 TCGA projects) | 7,671 | 6,716 | 6,561 | 7,826 | 656 | 377 |

Each patient belongs to one cohort, so the rows add up to the total. Patients with both assays also appear in the RNA-seq and methylation columns. Normal columns count the cohort's own donors with same-sample normal RNA-seq and H&E after screening.

## Patient screen

Of 8,139 primary-tumour patients after assay QC in the panel projects, the treatment and diagnosis screen withholds 169: 67 treatment exclusions, 40 treatment holds and 62 diagnosis, identity, recurrence or specimen cases. Reasons can overlap; each patient is counted once under its main disposition. Not all withheld patients were treated, and they do not form a treated reference set. Histology selection then keeps 7,826 of the 7,970 patients who pass the screen. 
## Coverage by project

Broader availability: primary-tumour patients in each project after exact assay-quality exclusions, not the selected panel. The last column shows how each project contributes to the panel, if at all.

| TCGA project | Patients with RNA-seq | Patients with methylation (450k) | Patients with both | Total patients | Normal RNA-seq + H&E | In the selected panel |
| --- | --- | --- | --- | --- | --- | --- |
| TCGA-BLCA | 395 | 401 | 395 | 401 | 19 | Yes |
| TCGA-BRCA | 1,082 | 778 | 775 | 1,085 | 98 | Yes |
| TCGA-CESC | 300 | 302 | 300 | 302 | 3 | Yes: squamous cell carcinoma only (CSCC) |
| TCGA-COAD | 441 | 287 | 285 | 443 | 37 | Yes: pooled with TCGA-READ as colorectal cancer (CRC) |
| TCGA-ESCA | 173 | 174 | 173 | 174 | 10 | Yes: squamous cell carcinoma only (ESCC) |
| TCGA-GBM | 154 | 139 | 51 | 242 | 5 | Yes: pooled with TCGA-LGG as diffuse glioma (GLIOMA) |
| TCGA-HNSC | 514 | 522 | 514 | 522 | 43 | Yes |
| TCGA-KIRC | 515 | 312 | 311 | 516 | 71 | Yes |
| TCGA-KIRP | 279 | 267 | 266 | 280 | 32 | Yes |
| TCGA-LGG | 514 | 514 | 514 | 514 | 0 | Yes: pooled with TCGA-GBM as diffuse glioma (GLIOMA) |
| TCGA-LIHC | 362 | 368 | 362 | 368 | 50 | Yes |
| TCGA-LUAD | 457 | 410 | 406 | 461 | 57 | Yes |
| TCGA-LUSC | 486 | 363 | 363 | 486 | 47 | Yes |
| TCGA-PAAD | 151 | 157 | 151 | 157 | 4 | Yes: ductal adenocarcinoma only (PDAC) |
| TCGA-PCPG | 178 | 178 | 178 | 178 | 3 | Yes |
| TCGA-PRAD | 405 | 406 | 405 | 406 | 48 | Yes |
| TCGA-READ | 156 | 94 | 94 | 156 | 10 | Yes: pooled with TCGA-COAD as colorectal cancer (CRC) |
| TCGA-STAD | 387 | 378 | 349 | 416 | 34 | Yes |
| TCGA-THCA | 500 | 502 | 500 | 502 | 58 | Yes |
| TCGA-UCEC | 528 | 418 | 416 | 530 | 34 | Yes |
| TCGA-ACC | 78 | 79 | 78 | 79 | 0 | No: below the size threshold |
| TCGA-CHOL | 34 | 35 | 34 | 35 | 9 | No: below the size threshold |
| TCGA-DLBC | 48 | 48 | 48 | 48 | 0 | No: below the size threshold |
| TCGA-KICH | 65 | 65 | 65 | 65 | 24 | No: below the size threshold |
| TCGA-MESO | 83 | 83 | 83 | 83 | 0 | No: below the size threshold |
| TCGA-OV | 268 | 10 | 9 | 269 | 0 | No: below the size threshold |
| TCGA-SARC | 223 | 225 | 223 | 225 | 2 | No: it combines several sarcoma types, each below the size threshold |
| TCGA-SKCM | 103 | 104 | 103 | 104 | 1 | No: below the size threshold |
| TCGA-TGCT | 149 | 149 | 149 | 149 | 0 | No: below the size threshold |
| TCGA-THYM | 120 | 124 | 120 | 124 | 2 | No: below the size threshold |
| TCGA-UCS | 57 | 57 | 57 | 57 | 0 | No: below the size threshold |
| TCGA-UVM | 80 | 80 | 80 | 80 | 0 | No: below the size threshold |

Patient-level data: [tcga_patients.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_patients.json) gives the assay states of every patient; [tcga_patient_review.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/tcga_patient_review.json) gives the screen decisions as reason codes, the analysis cohort and published annotations. Field definitions are in [data/README.md](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/README.md).
