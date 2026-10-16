# Spatial studies

Release 0.9.3, 16 October 2026. Web page: [spatial.html](https://iarcbioinfo.github.io/histology-multiomics-explorer/spatial.html). Data: [cohorts.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/cohorts.json) (resources with layer `matched-spatial`) and [captures.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/captures.json) (located tissue sections).

Published spatial omics studies show where molecular programmes and cell states sit within a tumour and how they relate to its morphology. They usually come from patients other than those in TCGA, so they add tissue context to the reference but no measurements for TCGA patients.

113 catalogued spatial resources, 10 with matched data located, 20 cancer types represented. 204 tissue sections with an original H&E image, measured spatial RNA and coordinates are located.

## By cancer type

| Cancer type | Code | Catalogued resources | With matched data located |
| --- | --- | --- | --- |
| [Breast invasive carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/BRCA.md) | BRCA | 8 | 2 |
| [Colon adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/COAD.md) | COAD | 11 | 3 |
| [Rectal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/READ.md) | READ | 11 | 3 |
| [Colorectal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/CRC.md) | CRC | 11 | 3 |
| [Thyroid carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/THCA.md) | THCA | 9 | 1 |
| [Bladder urothelial carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/BLCA.md) | BLCA | 10 | 1 |
| [Lower-grade glioma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LGG.md) | LGG | 10 | Verification pending |
| [Glioblastoma (historical TCGA diagnosis)](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/GBM.md) | GBM | 2 | Verification pending |
| [Diffuse glioma classification benchmark](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/GLIOMA.md) | GLIOMA | 10 | Verification pending |
| [Liver hepatocellular carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LIHC.md) | LIHC | 17 | 1 |
| [Lung adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LUAD.md) | LUAD | 11 | 1 |
| [Head and neck squamous cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/HNSC.md) | HNSC | 13 | 1 |
| [Cervical squamous cell carcinoma and endocervical adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/CESC.md) | CESC | 3 | Verification pending |
| [Oesophageal carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/ESCA.md) | ESCA | 3 | Verification pending |
| [Kidney renal clear cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/KIRC.md) | KIRC | 4 | Verification pending |
| [Kidney renal papillary cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/KIRP.md) | KIRP | 2 | Verification pending |
| [Lung squamous cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LUSC.md) | LUSC | 2 | Verification pending |
| [Pheochromocytoma and paraganglioma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PCPG.md) | PCPG | 2 | Verification pending |
| [Prostate adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PRAD.md) | PRAD | 4 | Verification pending |
| [Stomach adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/STAD.md) | STAD | 2 | Verification pending |
| [Uterine corpus endometrial carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/UCEC.md) | UCEC | 2 | Verification pending |
| [Pancreatic ductal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PDAC.md) | PDAC | 3 | 2 |

Catalogued resources are all listed spatial studies and vendor examples, including those not yet verified and those that need an access request. A resource counts as having matched data located once its image and molecular files have been found; image registration and tissue QC may still be pending. The pooled colorectal and glioma rows reuse the resources of their constituent cancers, and some studies cover several cancers, so the rows should not be summed.

## Public-route review

The 26 reviewed resources were followed to a retrieved result, a registration or controlled-access boundary, a missing release or a reproducible download failure. The open dependencies below are kept apart: a download failure is a technical gap, not a permission requirement. 144 section packages have expression barcodes that match their tissue coordinates exactly; this is not a patient count or final QC, and no eligible-patient total is established.

| Open dependency | Resources |
| --- | --- |
| Public download works | 13 |
| Public files listed, download failed (technical) | 4 |
| Vendor registration and terms | 6 |
| Data access committee approval | 1 |
| Author release or metadata needed | 19 |
| Local scientific QC remaining | 22 |

| Resource | ID | Status | Next step |
| --- | --- | --- | --- |
| Greenwald et al. 2024 | `cand-greenwald2024` | 14 of 19 sections matched to original images; labels and clinical issues flagged | Ask the study team for the five missing originals, confirmation of the crossed ZH881 labels, the ZH1019 patient ID, BWH23 and BWH28 diagnosis and grade, scanner calibration and treatment and recurrence; then image and pathology QC. |
| Sonpatki et al. 2026 | `cand-snu2026` | Patient and diagnosis denominator resolved; image coverage and linkage unresolved | Ask the study team for the per-section count, image and patient crosswalk, original H&E beyond previews and fluorescence images, treatment and recurrence, and which reused dataset was analysed. |
| De Zuani et al. 2024 | `cand-dezuani-cvejic-2024` | Ten LUSC section packages checked; preview images only | Ask the study team for original scans and the prior treatment of Patients 11 and 19. |
| 10x Genomics cervical SCC, Visium FFPE | `cscc-10x-ffpe` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| Guo et al. 2023, HPV progression series | `cscc-hpv-gse208654` | H&E and expression retrieved; spot coordinates missing | Ask the submitter for the tissue-position table and scale factors of GSM6360691, the image calibration and the clinical provenance. |
| Ou et al. 2022 | `cscc-ou-stereo` | Serial-section study; public data route unresolved | Ask the authors or CNSA support for a working route to CNP0002543, processed matrices and coordinates, and original serial H&E with patient and section mapping. |
| HRA000776 / OMIX009524, multistage ESCC | `escc-hra000776-omix009524` | Controlled data; image and assay crosswalk unresolved | Apply through the repository's data access committee only if the data are needed, and ask for the five-tumour image and assay crosswalk and original scans. |
| HRA007162, ESCC single-cell and spatial | `escc-hra007162` | Open raw reads; processed and image package unresolved | Ask the study authors for the processed five-case spatial package, original H&E, coordinates and a de-identified donor and run crosswalk. |
| Liu et al. 2023, GeoMx precancer | `escc-precancer-geomx` | Selected genes public; complete ROI matrix not released | Ask the corresponding authors for the complete normalised and raw ROI matrices, QC annotations, ROI geometries and the serial H&E crosswalk. |
| Meylan et al. 2022 | `kirc-meylan-gse175540` | 24 section packages checked; preview images only | Retry the public clinical table, then ask the submitter for the original H&E of the 24 sections and the donor, section and grade crosswalk. |
| Li et al. 2022, ccRCC Visium (EGAD00001008781) | `kirc-egad00001008781` | Public processed data located; eight patients and 16 sections confirmed | Ask the study team for original H&E and calibration; apply to EGA only if raw reads are needed. |
| GSE294006, treated advanced ccRCC | `kirc-treated-gse294006` | Three section packages checked; preview images only | Ask the submitter for original H&E, calibration and matching metadata for the three sections. |
| 10x Genomics ccRCC, Xenium RNA and protein | `kirc-10x-xenium-protein` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| 10x Genomics kidney preview, Xenium (papillary RCC) | `kirp-10x-xenium-preview` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| Soupir et al., papillary RCC CosMx study | `kirp-macrophage-abstract` | Public molecular object; clinical and H&E crosswalk needed from the study team | Ask Brandon Manley, as both repositories direct, for a de-identified slide-to-patient, histology and treatment crosswalk, the paper's subset membership and H&E registration. |
| 10x Genomics lung SCC, Visium CytAssist FFPE | `lusc-10x-cytassist` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| Ling et al., SSRN manuscript | `pcpg-ling-ssrn` | Manuscript lead; data release unresolved | Ask the authors for the final publication, platform, patient and section counts, accession and expression and H&E package. |
| Zhu et al. 2026, preprint | `pcpg-developmental-preprint` | Human Visium HD assay resolved; accession not supplied | Ask the lead contact for the accession and the human PPGL processed data, coordinates, original H&E, section relation and donor and treatment metadata. |
| 10x Genomics prostate acinar carcinoma, Visium FFPE | `prad-10x-acinar` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| 10x Genomics prostate invasive adenocarcinoma, Visium FFPE | `prad-10x-invasive` | Vendor page requires registration and terms before download | Complete the vendor registration if wanted (not done), then check the files, H&E and donor history. |
| Hirz et al. 2023 | `prad-hirz-slideseq` | Bead coordinates defective in all 12 released tables | Ask the study authors for corrected bead locations or the per-array input files, the barcode crosswalk and original serial H&E. |
| Erickson et al. 2022 | `prad-erickson-clonal` | Public image folders verified; file download failed | Retry the public file downloads, then check images, coordinates and the clinical mapping. |
| Lee et al. 2024 | `stad-gse251950` | Ten section packages checked; preview images only | Ask the submitter for original scans and the clinical, histology and treatment linkage for the nine donor labels and the GC6 peritoneal metastasis. |
| Gao et al. 2026 | `stad-gse270678` | 72 section packages checked; patient and section count resolved | Retry the Mendeley download; ask the submitter for original scans and calibration if they are not in the public RDS. |
| Barkley et al. 2022, UCEC sample | `ucec-barkley-gse203612` | Section package checked; author data links disabled | Ask the study team to restore the public data links and for the original image, histological subtype and treatment of NYU_UCEC3. |
| Cassier et al. 2023, NP137 trial | `ucec-np137-gse225690` | Two previously treated patients and four sections confirmed | Ask the trial team for original H&E and calibration, and for exact earlier regimens only if a response analysis needs them. |

## Related leads, not counted

These releases add no resources or patients to the totals above.

- [Kidney and lung TLS Visium release (Zenodo 14620362)](https://zenodo.org/records/14620362): Visium FFPE release of three kidney and five lung specimens with expert tertiary lymphoid structure, immune, tumour and normal annotations. The full archive was retrieved and checksum-verified: all eight expression packages have exact barcode-coordinate agreement, and all eight original TIFF images (about 10,000 × 10,000 pixels) are readable. A relation between the preprocessed and full-resolution coordinates was fitted, which is an inference rather than a supplied calibration. Histological subtype, donor independence and treatment are not established, so its specimens are not assigned to KIRC, KIRP, LUAD or LUSC. Next: Ask the study authors for histological subtypes, donor independence and treatment mapping.
- [CIN3 spatial study (precursor lesions)](https://doi.org/10.1002/path.70002): Spatial transcriptomics of cervical intraepithelial neoplasia grade 3: eight biopsies were selected and seven samples analysed. The University of Queensland repository lists eight large H&E TIFFs; coordinates, expression and the patient and section matching are not verified. Precursor biology: not invasive cervical squamous cell carcinoma, so it adds no CSCC patients. Next: Verify the coordinates, expression and patient and section matching.
- [Ravikumar/Al-Holou glioma release (Zenodo 16505469)](https://zenodo.org/records/16505469): Public spatial H5AD linked by a Ravikumar/Al-Holou preprint (bioRxiv 10.1101/2025.10.17.683110). Its metadata show 14 section labels with images of at most 2,000 pixels; the preprint reports seven patients and 14 new sections, eight primary and six recurrent. Its four filename prefixes are not four patients, and its pooled 44-section analysis reuses Freiburg and Broad sections, which are not new patients. The newer glioma atlas labels this record as Ravi 2022, but it belongs to this study. A linked reuse record: donor mapping and original scans are unresolved, and it is not a new eligible cohort. Next: Ask the authors for the seven-patient section crosswalk, treatment, IDH and diagnosis, and original H&E with calibration.

## All spatial resources

| Resource | ID | Cancer codes | Status | Access | Assay |
| --- | --- | --- | --- | --- | --- |
| Giraud et al. 2024 | `gse245908-lihc` | LIHC | Matched packages located | Open download | Visium |
| Gouin et al. 2021 | `gouin-2021` | BLCA | Matched packages located | Open download | Visium |
| HTAN WUSTL (Mo et al. 2024) | `htan-wustl` | BRCA, COAD, READ, PDAC | Matched packages located | Free account | Visium, Visium FFPE |
| Janesick et al. 2023 | `janesick-2023` | BRCA | Matched packages located | Open download | Visium CytAssist |
| Oliveira et al. 2025 (Visium HD) | `oliveira-2025` | COAD, READ | Matched packages located | Open download | Visium HD |
| Pei et al. 2025 | `pei-2025` | PDAC | Matched packages located | Open download | Visium |
| Simkin et al. 2026 | `simkin-2026` | HNSC | Matched packages located | Open download | Visium |
| Steiner et al. 2026 | `steiner-2026` | LUAD | Matched packages located | Open download | Visium FFPE |
| Valdeolivas et al. 2024 | `valdeolivas-2024` | COAD, READ | Matched packages located | Open download | Visium |
| Zhang et al. 2024 (thyroid) | `zhang-2024-thca` | THCA | Matched packages located | Open download | Visium |
| 10x Genomics ccRCC, Xenium RNA and protein | `kirc-10x-xenium-protein` | KIRC | Candidate, not yet verified | Free account | Xenium |
| 10x Genomics cervical SCC, Visium FFPE | `cscc-10x-ffpe` | CESC | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Genomics human breast Visium demonstration datasets | `cand-official-10x-breast-demos` | BRCA | Candidate, not yet verified | Open download | Visium HD, Visium CytAssist |
| 10x Genomics kidney preview, Xenium (papillary RCC) | `kirp-10x-xenium-preview` | KIRP | Candidate, not yet verified | Free account | Xenium |
| 10x Genomics lung SCC, Visium CytAssist FFPE | `lusc-10x-cytassist` | LUSC | Candidate, not yet verified | Free account | Visium CytAssist |
| 10x Genomics prostate acinar carcinoma, Visium FFPE | `prad-10x-acinar` | PRAD | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Genomics prostate invasive adenocarcinoma, Visium FFPE | `prad-10x-invasive` | PRAD | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Visium Spatial Transcriptomics of 61 Human HCC Samples | `cand-egad50000002122` | LIHC | Candidate, not yet verified | Controlled access | Visium |
| An integrated single-cell and spatial transcriptomic atlas of thyroid cancer progression identifies prognostic fibroblast subpopulations | `cand-loberg-2026-jci191990` | THCA | Candidate, not yet verified | Author request | Visium FFPE |
| Arora et al. 2023 | `cand-arora2023-gse208253` | HNSC | Candidate, not yet verified | Open download | Visium |
| Barkley et al. 2022, UCEC sample | `ucec-barkley-gse203612` | UCEC | Candidate, not yet verified | Open download | Visium |
| Batf3+ DCs and the 4–1BB/4–1BBL axis are required at the effector phase in the tumor microenvironment for PD-1/PD-L1 blockade efficacy | `cand-ziblat2024` | BLCA | Candidate, not yet verified | Open download | Visium HD, Visium CytAssist |
| Cancer-associated fibroblast subsets in head and neck squamous cell carcinoma | `cand-li2024-hra005551-hra005576` | HNSC | Candidate, not yet verified | Controlled access | Spatial RNA (protocol unverified) |
| Cassier et al. 2023, NP137 trial | `ucec-np137-gse225690` | UCEC | Candidate, not yet verified | Open download | Visium FFPE |
| De Zuani et al. 2024 | `cand-dezuani-cvejic-2024` | LUAD, LUSC | Candidate, not yet verified | Open download | Visium |
| Deciphering head and neck cancer microenvironment: Single-cell and spatial transcriptomics reveals HPV-associated differences | `cand-gse281978-hpv2024` | HNSC | Candidate, not yet verified | Open download | Visium |
| Deep spatial-omics analysis of Head & Neck carcinomas provides alternative therapeutic targets and rationale for treatment failure | `cand-causer2023-uq` | HNSC | Candidate, not yet verified | Open download | Visium |
| Deep versus standard spatial transcriptomic sequencing | `cand-gse283406` | LIHC | Candidate, not yet verified | Open download | Visium CytAssist |
| Defining the cellular and molecular identities of histologic subtypes in lung adenocarcinoma | `cand-knuch-2026` | LUAD | Candidate, not yet verified | Unresolved | Visium |
| Deng et al. 2025 | `cand-deng-micropapillary-2025` | LUAD | Candidate, not yet verified | Author request | Visium CytAssist |
| Erickson et al. 2022 | `prad-erickson-clonal` | PRAD | Candidate, not yet verified | Open download | Spatial Transcriptomics (legacy arrays), Visium |
| Fan et al. 2024 | `cand-fan2024-hra006757` | LIHC | Candidate, not yet verified | Controlled access | Visium FFPE |
| Gao et al. 2026 | `stad-gse270678` | STAD | Candidate, not yet verified | Open download | Visium |
| Gaspard-Boulinc et al. 2025 | `cand-gaspardboulin2025` | LGG | Candidate, not yet verified | Unresolved | Visium |
| Grande et al. 2025 | `cand-dutreneo` | BLCA | Candidate, not yet verified | Author request | Visium FFPE |
| Greenwald et al. 2024 | `cand-greenwald2024` | LGG, GBM | Candidate, not yet verified | Open download | Visium |
| GSE294006, treated advanced ccRCC | `kirc-treated-gse294006` | KIRC | Candidate, not yet verified | Open download | Visium FFPE |
| Guo et al. 2023, HPV progression series | `cscc-hpv-gse208654` | CESC | Candidate, not yet verified | Open download | Spatial transcriptomics array (platform to confirm) |
| He et al. 2024 | `cand-he2024` | LGG | Candidate, not yet verified | Open download | Visium |
| Head and neck squamous cell carcinoma immune-checkpoint inhibitor spatial study | `cand-gse301720-ici2026` | HNSC | Candidate, not yet verified | Open download | Visium |
| Hirz et al. 2023 | `prad-hirz-slideseq` | PRAD | Candidate, not yet verified | Open download | Slide-seqV2 |
| Hoefflin et al. 2026 | `cand-hoefflin2026` | LGG | Candidate, not yet verified | Open download | Visium |
| HRA000776 / OMIX009524, multistage ESCC | `escc-hra000776-omix009524` | ESCA | Candidate, not yet verified | Controlled access | Visium (library details to verify) |
| HRA007162, ESCC single-cell and spatial | `escc-hra007162` | ESCA | Candidate, not yet verified | Open download | Visium |
| HTAN Vanderbilt colorectal CytAssist captures | `cand-crc-cottam-htan2025` | COAD, READ | Candidate, not yet verified | Free account | Visium CytAssist |
| Hypopharyngeal cancer chemoradiotherapy resistance, spatial transcriptomics | `cand-hypopharynx2025-ccrt` | HNSC | Candidate, not yet verified | Author request | Visium CytAssist |
| Integrated single-cell and spatial transcriptomic profiling reveals higher intratumour heterogeneity and epithelial–fibroblast interactions in recurrent bladder cancer | `cand-xuzhou2023` | BLCA | Candidate, not yet verified | Unresolved | Visium |
| Integrated spatial metabolomics and transcriptomics reveal the molecular landscape of papillary thyroid cancer and its lymph node metastasis | `cand-li-2025-s12967-07566` | THCA | Candidate, not yet verified | Author request | Visium |
| Integrative spatiotemporal analysis of squamous tumorigenesis | `cand-oraltumorigenesis2025-preprint` | HNSC | Candidate, not yet verified | Unresolved | Visium HD |
| Interactions between LAMP3+ dendritic cells and T-cell subpopulations promote immune evasion in papillary thyroid carcinoma | `cand-wang-2024-hra005594` | THCA | Candidate, not yet verified | Author request | Visium FFPE |
| Jia et al. 2025 | `cand-times-hra006579` | LIHC | Candidate, not yet verified | Unresolved | Visium FFPE |
| Jiang et al. 2024 | `cand-jiang2024meti` | BLCA | Candidate, not yet verified | Open download | Visium CytAssist |
| Jing et al. 2024 | `cand-he2024-new4plc` | LIHC | Candidate, not yet verified | Controlled access | Visium |
| Kuchroo et al. 2022 | `cand-kuchroosparc2022` | LGG | Candidate, not yet verified | Unresolved | Visium |
| Lau et al. 2022 | `cand-prjna858545-hcc` | LIHC | Candidate, not yet verified | Open download | Visium |
| Lee et al. 2024 | `stad-gse251950` | STAD | Candidate, not yet verified | Open download | Visium |
| Li et al. 2022, ccRCC Visium (EGAD00001008781) | `kirc-egad00001008781` | KIRC | Candidate, not yet verified | Open download | Visium |
| Liao et al. 2025 | `cand-liao-2025-gse250521` | THCA | Candidate, not yet verified | Open download | Visium |
| Ling et al., SSRN manuscript | `pcpg-ling-ssrn` | PCPG | Candidate, not yet verified | Unresolved | Spatial transcriptomics (platform unverified) |
| Liu et al. 2023, GeoMx precancer | `escc-precancer-geomx` | ESCA | Candidate, not yet verified | Author request | GeoMx WTA (ROI) |
| Liu et al. 2026 | `cand-crc-liu-maru2026` | COAD, READ | Candidate, not yet verified | Open download | Visium HD |
| Luo et al. 2024 | `cand-chen-liu-2024` | LUAD | Candidate, not yet verified | Open download | Visium CytAssist |
| METI lung adenocarcinoma sample LUAD-14C | `cand-meti-luad14c` | LUAD | Candidate, not yet verified | Open download | Visium CytAssist |
| Meylan et al. 2022 | `kirc-meylan-gse175540` | KIRC | Candidate, not yet verified | Open download | Visium FFPE, Visium |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors | `cand-crc-colonmap-heiser2023` | COAD, READ | Candidate, not yet verified | Free account | Visium FFPE |
| Multiomics and multi-region spatial transcriptome analysis reveal cellular networks and pathways associated with hepatocellular carcinoma recurrence | `cand-gse281759` | LIHC | Candidate, not yet verified | Open download | Visium |
| Murai et al. 2022 | `cand-jgad000422-hcc` | LIHC | Candidate, not yet verified | Controlled access | Visium |
| Neve et al. 2026 | `cand-crc-orgares-gse283052` | COAD, READ | Candidate, not yet verified | Open download | Visium |
| Ou et al. 2022 | `cscc-ou-stereo` | CESC | Candidate, not yet verified | Unresolved | Stereo-seq |
| Peng et al. 2026 | `cand-peng-kadara-2025` | LUAD | Candidate, not yet verified | Open download | Visium CytAssist |
| Pribus et al. 2026 | `cand-pribus2026` | BLCA | Candidate, not yet verified | Open download | Visium |
| Primary colorectal cancer and liver metastasis, Visium CytAssist | `cand-crc-mahidol-gse267401` | COAD, READ | Candidate, not yet verified | Open download | Visium CytAssist |
| Ren et al. 2025 | `cand-crc-spatch-ren2025` | COAD, READ | Candidate, not yet verified | Open download | Visium HD |
| Ren et al. 2025 | `cand-spatch-hcc` | LIHC | Candidate, not yet verified | Open download | Visium HD |
| Ritter et al. 2025 | `cand-ritternepsta2025` | LGG | Candidate, not yet verified | Open download | Visium FFPE |
| Schmauch et al. 2025 | `cand-crc-miso-petacc8` | COAD, READ | Candidate, not yet verified | Controlled access | Visium FFPE |
| Schmitt et al. 2026 | `schmitt-2026` | PDAC | Candidate, not yet verified | Open download | Visium FFPE |
| Simkin et al. 2026 | `cand-simkin2026-gse268014-hd` | HNSC | Candidate, not yet verified | Open download | Visium HD |
| Single-cell RNA-sequencing and spatial transcriptomic analysis reveal a distinct population of APOE-negative cells yielding pathological lymph node metastasis in papillary thyroid cancer | `cand-zhang-2025-prjca021247` | THCA | Candidate, not yet verified | Unresolved | Visium |
| Single-nucleus and Spatially Resolved Intratumor Subtype Heterogeneity in Bladder Cancer | `cand-lindskrog2023` | BLCA | Candidate, not yet verified | Controlled access | Visium |
| Snail-regulated exosomal microRNA-21 suppresses NLRP3 inflammasome activity to enhance cisplatin resistance | `cand-cheng2022-gse181300` | HNSC | Candidate, not yet verified | Open download | Visium |
| Sonpatki et al. 2026 | `cand-snu2026` | LGG, GBM | Candidate, not yet verified | Open download | Visium FFPE, Visium, Xenium |
| Soupir et al., papillary RCC CosMx study | `kirp-macrophage-abstract` | KIRP | Candidate, not yet verified | Open download | Multiplex immunofluorescence, Targeted spatial RNA (960 transcripts) |
| Spatial and single-nuclei transcriptomics reveals idiosyncratic and generic patterns in papillary and anaplastic thyroid cancers | `cand-tourneur-2026-legacyst` | THCA | Candidate, not yet verified | Open download | Spatial Transcriptomics (legacy arrays) |
| Spatial atlas of tertiary lymphoid structures and high endothelial venules in breast cancer | `cand-bcarc-tls-hev-2026` | BRCA | Candidate, not yet verified | Not released | Visium HD |
| Spatial maps of hepatocellular carcinoma transcriptomes reveal spatial expression patterns in tumor immune microenvironment | `cand-xin2022-hcc` | LIHC | Candidate, not yet verified | Unresolved | Visium |
| Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in hepatocellular carcinoma | `cand-wu2025-zenodo` | LIHC | Candidate, not yet verified | Open download | Visium FFPE |
| Spatial transcriptomic analysis of a diverse patient cohort reveals a conserved architecture in triple-negative breast cancer | `cand-bassiouni-gse210616` | BRCA | Candidate, not yet verified | Open download | Visium |
| Spatial Transcriptomic Analysis of Surgical Resection Specimens of Primary Head and Neck Squamous Cell Carcinoma Treated with Afatinib in a Window-of-Opportunity Study (EORTC 90111-24111) | `cand-beyaert2025-gse289908` | HNSC | Candidate, not yet verified | Open download | Visium FFPE |
| Spatial transcriptomics analysis of neoadjuvant cabozantinib and nivolumab in advanced hepatocellular carcinoma identifies independent mechanisms of resistance and recurrence | `cand-gse238264` | LIHC | Candidate, not yet verified | Open download | Visium |
| Spatial Transcriptomics and snRNA-seq Expose CAF Niches Orchestrating Dual Stromal-Immune Barriers in Hepatocellular Carcinoma | `cand-li2025-caf` | LIHC | Candidate, not yet verified | Author request | Visium |
| Spatial Transcriptomics Reveals Distinct Architectures but Shared Vulnerabilities in Primary and Metastatic Liver Tumors | `cand-adapa2025-hd` | LIHC | Candidate, not yet verified | Unresolved | Visium HD |
| Spatial transcriptomics reveals prognosis-associated cellular heterogeneity in the papillary thyroid carcinoma microenvironment | `cand-yan-2024-hra003537` | THCA | Candidate, not yet verified | Controlled access | Visium |
| Spatially resolved gene expression and tumour-microenvironment interactions across malignant transformation in IDH-mutant glioma | `cand-longitudinal2026` | LGG | Candidate, not yet verified | Open download | Visium CytAssist |
| Srinivasan et al. 2025 | `cand-crc-vri-dartmouth2025` | COAD, READ | Candidate, not yet verified | Unresolved | Spatial Transcriptomics (legacy arrays), Visium CytAssist |
| Takano et al. 2024 | `cand-takano-suzuki-2024` | LUAD | Candidate, not yet verified | Open download | Visium FFPE |
| Tang et al. 2025 | `cand-tang2025` | LGG | Candidate, not yet verified | Unresolved | Visium HD |
| Targeting Treg–fibroblast interaction to enhance immunotherapy in SLD-related HCC | `cand-egad50000001506` | LIHC | Candidate, not yet verified | Controlled access | Visium CytAssist |
| TNBC spatial transcriptomics resource (AACR 2026 abstract 1442) | `cand-dartmouth-aacr2026-1442` | BRCA | Candidate, not yet verified | Not released | Visium |
| TREM2-Expressing Multinucleated Giant Macrophages Are a Biomarker of Good Prognosis in Head and Neck Squamous Cell Carcinoma | `cand-gessain2024-e-mtab-14409` | HNSC | Candidate, not yet verified | Controlled access | Visium FFPE |
| Tumor microenvironment remodeling across thyroid cancer differentiation states revealed by spatial transcriptomics | `cand-seok-2025-cii` | THCA | Candidate, not yet verified | Author request | Visium CytAssist |
| Unveiling Immune Metabolic Mechanisms in Bladder Cancer: Spatial Profiling Identifies ZFP36 as a Therapeutic Target | `cand-zheng2025` | BLCA | Candidate, not yet verified | Open download | Visium |
| Visium HD CytAssist Gene Expression Human Lung Cancer post-Xenium experiment | `cand-10x-post-xenium-hd` | LUAD | Candidate, not yet verified | Open download | Visium HD |
| Wang et al. 2023 | `cand-lu-cell-discovery-2023` | LUAD | Candidate, not yet verified | Controlled access | Visium |
| Wang et al. 2024 | `cand-wang-venet-2024-legacy-st` | BRCA | Candidate, not yet verified | Open download | Spatial Transcriptomics (legacy arrays) |
| Webb et al. 2025 | `cand-webb2025` | LGG | Candidate, not yet verified | Open download | Visium |
| Weeramange et al. 2026 | `cand-frontiers2026-zenodo18238293` | HNSC | Candidate, not yet verified | Open download | Visium FFPE |
| Wu et al. 2021 | `cand-wu-2021` | BRCA | Candidate, not yet verified | Open download | Visium |
| Wu et al. 2021 | `cand-wu2021-hcc` | LIHC | Candidate, not yet verified | Open download | Visium |
| Yoshihara et al. 2026 | `cand-yoshihara2026erbt` | BLCA | Candidate, not yet verified | Open download | Visium CytAssist |
| Yu et al. 2026 | `cand-yu2026atlas` | BLCA | Candidate, not yet verified | Open download | Visium CytAssist |
| Zhao et al. 2025 | `cand-zhao-htapp-2025` | LUAD | Candidate, not yet verified | Open download | Visium |
| Zhu et al. 2026, preprint | `pcpg-developmental-preprint` | PCPG | Candidate, not yet verified | Not released | Spatial transcriptomics (human assay details unverified) |
