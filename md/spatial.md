# Spatial studies

Release 0.10.0, 16 October 2026. Web page: [spatial.html](https://iarcbioinfo.github.io/histology-multiomics-explorer/spatial.html). Data: [cohorts.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/cohorts.json) (resources with layer `matched-spatial`) and [captures.json](https://iarcbioinfo.github.io/histology-multiomics-explorer/data/captures.json) (located tissue sections).

Published spatial omics studies show where molecular programmes and cell states sit within a tumour and how they relate to its morphology. They usually come from patients other than those in TCGA, so they add tissue context to the reference but no measurements for TCGA patients.

113 catalogued spatial resources: 15 with original H&E located, 28 with matched data and a preview image, and 70 not yet verified; 20 cancer types represented. 255 tissue section records have the original H&E, and 483 have a preview image (359 listed one by one, 124 counted for their resource), from 193 known study-local patients; 283 listed sections have no patient ID. No eligible-patient total is established.

## By cancer type

| Cancer type | Code | Catalogued resources | Original H&E located | Matched data with preview image |
| --- | --- | --- | --- | --- |
| [Breast invasive carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/BRCA.md) | BRCA | 8 | 2 | 2 |
| [Colon adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/COAD.md) | COAD | 11 | 3 | 3 |
| [Rectal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/READ.md) | READ | 11 | 3 | 3 |
| [Colorectal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/CRC.md) | CRC | 11 | 3 | 3 |
| [Thyroid carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/THCA.md) | THCA | 9 | 2 | 1 |
| [Bladder urothelial carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/BLCA.md) | BLCA | 10 | 2 | 2 |
| [Lower-grade glioma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LGG.md) | LGG | 10 | 1 | 4 |
| [Glioblastoma (historical TCGA diagnosis)](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/GBM.md) | GBM | 3 | 1 | 1 |
| [Diffuse glioma classification benchmark](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/GLIOMA.md) | GLIOMA | 10 | 1 | 4 |
| [Liver hepatocellular carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LIHC.md) | LIHC | 17 | 1 | 2 |
| [Lung adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LUAD.md) | LUAD | 11 | 2 | 3 |
| [Head and neck squamous cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/HNSC.md) | HNSC | 13 | 2 | 4 |
| [Cervical squamous cell carcinoma and endocervical adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/CESC.md) | CESC | 3 | 0 | 0 |
| [Oesophageal carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/ESCA.md) | ESCA | 3 | 0 | 0 |
| [Kidney renal clear cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/KIRC.md) | KIRC | 4 | 0 | 2 |
| [Kidney renal papillary cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/KIRP.md) | KIRP | 2 | 0 | 0 |
| [Lung squamous cell carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/LUSC.md) | LUSC | 2 | 0 | 1 |
| [Pheochromocytoma and paraganglioma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PCPG.md) | PCPG | 2 | 0 | 0 |
| [Prostate adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PRAD.md) | PRAD | 4 | 0 | 0 |
| [Stomach adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/STAD.md) | STAD | 2 | 0 | 2 |
| [Uterine corpus endometrial carcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/UCEC.md) | UCEC | 2 | 0 | 2 |
| [Pancreatic ductal adenocarcinoma](https://iarcbioinfo.github.io/histology-multiomics-explorer/md/cancers/PDAC.md) | PDAC | 3 | 2 | 1 |

Catalogued resources are all listed spatial studies and vendor examples, including those not yet verified and those that need an access request. A resource with matched data counts once, at its best image level; registration, calibration and tissue QC may still be pending at either level. The pooled colorectal and glioma rows reuse the resources of their constituent cancers, and some studies cover several cancers, so the rows should not be summed.

## Image levels

| Level | Image located | Supports | Does not support |
| --- | --- | --- | --- |
| Original H&E located | The original H&E scan of the assayed tissue, with measured expression and coordinates | Molecular spatial maps; whole-slide and tile models, morphology and distance measurements once registration and scanner calibration are checked | Any use that assumes registration, calibration or tissue QC are complete |
| Matched data with preview image | A reduced preview released with the data (for example a Space Ranger image); the original scan was not located | Molecular spatial visualisation and analyses of expression in tissue coordinates | Whole-slide or tile modelling, cell morphology, physical-distance comparisons or registration sign-off |

A resource counts once, at its best level; when only some of its sections have an original scan, that subset is stated and the other sections are listed at the preview level. Section records are per study and are not globally unique physical sections: several specimens can share one array area (`assay_area_id`), and reused or mirrored data are linked to their original study rather than counted again. Image level is separate from registration, scanner calibration, clinical eligibility and assay QC.

| Image level | Resources | Section records | Known patients | Sections without a patient ID |
| --- | --- | --- | --- | --- |
| Original H&E located | 15 | 255 | 134 | 12 |
| Matched data with preview image | 28 | 483 (359 listed, 124 counted for their resource) | 59 | 271 |

## Package review

77 candidates that had not been checked file by file were reviewed against their public records and packages. Sections were listed only where the source supports them; the others stay candidates with their dependencies, and no eligible-patient count is given.

| Result | Resources | Now shown as |
| --- | --- | --- |
| Original H&E and matched data checked | 4 | Original H&E located |
| Matched data checked; preview image only | 21 | Matched data with preview image |
| Public files listed; inspection not finished | 11 | Candidate, not yet verified |
| Access needs approval or permission | 11 | Candidate, not yet verified |
| Data release not identified | 8 | Candidate, not yet verified |
| Release by the authors needed | 6 | Candidate, not yet verified |
| Public record without downloadable files | 1 | Candidate, not yet verified |
| Code only; no data package identified | 1 | Candidate, not yet verified |
| Public download failed (technical) | 5 | Candidate, not yet verified |
| Coordinates or image scale missing | 3 | Candidate, not yet verified |
| Original image or its transform missing | 1 | Candidate, not yet verified |
| Image and expression files not yet joined | 1 | Candidate, not yet verified |
| Free account needed | 2 | Candidate, not yet verified |
| Vendor catalogue without a specific dataset | 1 | Candidate, not yet verified |
| Vendor registration and terms | 1 | Candidate, not yet verified |

| Resource | ID | Result | Next step |
| --- | --- | --- | --- |
| Schmitt et al. 2026 | `schmitt-2026` | Matched data checked; preview image only | Original scans; clinical and image QC. |
| Wu et al. 2021 | `cand-wu-2021` | Matched data checked; preview image only | Original scans and the provenance of the image PDF; filter the out-of-tissue spots in three sections explicitly. |
| Spatial transcriptomic analysis of a diverse patient cohort reveals a conserved architecture in triple-negative breast cancer | `cand-bassiouni-gse210616` | Matched data checked; preview image only | Treatment, original scans and registration QC. |
| Spatial atlas of tertiary lymphoid structures and high endothelial venules in breast cancer | `cand-bcarc-tls-hev-2026` | Public record without downloadable files | Await an actionable public file release; do not count record views as released data. |
| 10x Genomics human breast Visium demonstration datasets | `cand-official-10x-breast-demos` | Vendor catalogue without a specific dataset | Pin exact dataset, specimen, assay and version; respect vendor registration/terms; deduplicate other breast entries. |
| Wang et al. 2024 | `cand-wang-venet-2024-legacy-st` | Public files listed; inspection not finished | Use 8135721, inspect code/data README and array-to-patient/image join; old 13867935/36 is code. |
| TNBC spatial transcriptomics resource (AACR 2026 abstract 1442) | `cand-dartmouth-aacr2026-1442` | Data release not identified | Find final publication and released accession, then inspect patient/section/image files; 25 is a reported denominator, not available matched patients. |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors | `cand-crc-colonmap-heiser2023` | Free account needed | Pin Vanderbilt/COLON MAP section/file IDs, donor and histology crosswalk; separate from WUSTL and cottam reuse. |
| Neve et al. 2026 | `cand-crc-orgares-gse283052` | Matched data checked; preview image only | Map donor IDs and primary or metastatic site before counting patients; keep the shared barcode-vector provenance. |
| Primary colorectal cancer and liver metastasis, Visium CytAssist | `cand-crc-mahidol-gse267401` | Matched data checked; preview image only | Original scans and treatment; the primary and metastatic sections of patients 21 and 17 stay separate sites. |
| Schmauch et al. 2025 | `cand-crc-miso-petacc8` | Access needs approval or permission | FFCD controls measured PETACC8-Visium use; separate measured packages from model-predicted outputs, and verify any public processed alternative before a permission decision. |
| Srinivasan et al. 2025 | `cand-crc-vri-dartmouth2025` | Data release not identified | Locate released measured development-cohort files; do not count virtual RNA as measured spatial RNA. |
| Liu et al. 2026 | `cand-crc-liu-maru2026` | Matched data checked; preview image only | Donor count and treatment; all 37 tissues are colorectal metastases. |
| Ren et al. 2025 | `cand-crc-spatch-ren2025` | Public files listed; inspection not finished | Match each COAD platform to its measured RNA/coordinates; do not count CODEX/DAPI as H&E or colon specimens as READ. |
| HTAN Vanderbilt colorectal CytAssist captures | `cand-crc-cottam-htan2025` | Free account needed | Pin exact study/HTAN donor-capture manifest and deduplicate Heiser/COLON MAP/WUSTL; preserve primary/metastatic labels. |
| Liao et al. 2025 | `cand-liao-2025-gse250521` | Matched data checked; preview image only | Original scans; four anaplastic thyroid carcinoma sections and nine single-cell samples stay outside this selection. |
| An integrated single-cell and spatial transcriptomic atlas of thyroid cancer progression identifies prognostic fibroblast subpopulations | `cand-loberg-2026-jci191990` | Access needs approval or permission | Lead-contact/institutional permission required for individual data; aggregate results on request do not replace spatial package. |
| Spatial transcriptomics reveals prognosis-associated cellular heterogeneity in the papillary thyroid carcinoma microenvironment | `cand-yan-2024-hra003537` | Access needs approval or permission | Locate processed public supplement/image package independently of controlled raw reads. |
| Single-cell RNA-sequencing and spatial transcriptomic analysis reveal a distinct population of APOE-negative cells yielding pathological lymph node metastasis in papillary thyroid cancer | `cand-zhang-2025-prjca021247` | Data release not identified | Resolve project-to-spatial accession and processed original-image/coordinate release. |
| Interactions between LAMP3+ dendritic cells and T-cell subpopulations promote immune evasion in papillary thyroid carcinoma | `cand-wang-2024-hra005594` | Release by the authors needed | Author/repository release of processed matrix, coordinates and original image. |
| Tumor microenvironment remodeling across thyroid cancer differentiation states revealed by spatial transcriptomics | `cand-seok-2025-cii` | Release by the authors needed | Locate a released processed-data accession or obtain author release later. |
| Integrated spatial metabolomics and transcriptomics reveal the molecular landscape of papillary thyroid cancer and its lymph node metastasis | `cand-li-2025-s12967-07566` | Release by the authors needed | Processed spatial-RNA and matched-image release needed. |
| Spatial and single-nuclei transcriptomics reveals idiosyncratic and generic patterns in papillary and anaplastic thyroid cancers | `cand-tourneur-2026-legacyst` | Original H&E and matched data checked | Overlay and calibration QC for the legacy arrays; section treatment and site unknown; 12 anaplastic sections excluded. |
| Yu et al. 2026 | `cand-yu2026atlas` | Matched data checked; preview image only | Clinical adjudication against the reported 22-patient denominator; one preview has an out-of-frame spot flagged. |
| Batf3+ DCs and the 4–1BB/4–1BBL axis are required at the effector phase in the tumor microenvironment for PD-1/PD-L1 blockade efficacy | `cand-ziblat2024` | Original H&E and matched data checked | Original-image overlay and calibration QC; the ten smaller-image regions share eight array areas and need multi-specimen review. |
| Jiang et al. 2024 | `cand-jiang2024meti` | Original image or its transform missing | Recover original/transform or establish source-backed scaling; TIFF extension is not original-scan proof. |
| Yoshihara et al. 2026 | `cand-yoshihara2026erbt` | Public download failed (technical) | Retry authoritative DDBJ/GEA release listing and specimen identifiers; technical failure is not access denial. |
| Pribus et al. 2026 | `cand-pribus2026` | Public files listed; inspection not finished | Inspect metadata and combined measured-count object, original H&E and reuse crosswalk; raw GHGA is a separate permission route. |
| Integrated single-cell and spatial transcriptomic profiling reveals higher intratumour heterogeneity and epithelial–fibroblast interactions in recurrent bladder cancer | `cand-xuzhou2023` | Public download failed (technical) | Inspect supporting tables and recover public NODE listing before inferring author-only access. |
| Unveiling Immune Metabolic Mechanisms in Bladder Cancer: Spatial Profiling Identifies ZFP36 as a Therapeutic Target | `cand-zheng2025` | Matched data checked; preview image only | Donor, site and treatment from the source; original image QC. |
| Single-nucleus and Spatially Resolved Intratumor Subtype Heterogeneity in Bladder Cancer | `cand-lindskrog2023` | Access needs approval or permission | Locate any public processed/original-image alternative; approval needed only for actually controlled files. |
| Grande et al. 2025 | `cand-dutreneo` | Public files listed; inspection not finished | Inspect the targeted expression and centroids and their relation to the H&E; do not infer 20 independent patients. |
| Hoefflin et al. 2026 | `cand-hoefflin2026` | Public files listed; inspection not finished | Inspect IDH-mutant image/matrix packages and clinical alias map; reused Ravi GBM is not independent new patients. |
| Webb et al. 2025 | `cand-webb2025` | Matched data checked; preview image only | Donor independence and two image-frame checks; recurrent, oligodendroglioma and astrocytoma labels are kept. |
| Ritter et al. 2025 | `cand-ritternepsta2025` | Matched data checked; preview image only | Donor independence; 15 gliosarcoma sections are kept as glioblastoma variants, unrelated to TCGA-SARC; other CNS tumour types excluded. |
| Tang et al. 2025 | `cand-tang2025` | Public download failed (technical) | Resolve study-specific processed-data/source image links; software page is not package evidence. |
| Spatially resolved gene expression and tumour-microenvironment interactions across malignant transformation in IDH-mutant glioma | `cand-longitudinal2026` | Matched data checked; preview image only | Same-patient timeline and the crosswalk of a fourth sample. |
| He et al. 2024 | `cand-he2024` | Matched data checked; preview image only | Original scans and the donor, histology, grade and reuse crosswalk. |
| Kuchroo et al. 2022 | `cand-kuchroosparc2022` | Code only; no data package identified | Identify released measured specimens behind method demonstration and deduplicate reused studies. |
| Gaspard-Boulinc et al. 2025 | `cand-gaspardboulin2025` | Data release not identified | Find final publication and actionable accession before counts. |
| Ren et al. 2025 | `cand-spatch-hcc` | Public files listed; inspection not finished | Join HCC assays to measured expression/coordinates; preserve multi-assay overlap and serial/same-section relation. |
| Spatial transcriptomics analysis of neoadjuvant cabozantinib and nivolumab in advanced hepatocellular carcinoma identifies independent mechanisms of resistance and recurrence | `cand-gse238264` | Matched data checked; preview image only | Original scans; all seven donors were treated with cabozantinib and nivolumab. |
| Multiomics and multi-region spatial transcriptome analysis reveal cellular networks and pathways associated with hepatocellular carcinoma recurrence | `cand-gse281759` | Matched data checked; preview image only | Donor total (the B0013 and B013 aliases conflict); regions, recurrent versus primary labels and one normal section are kept. |
| Jia et al. 2025 | `cand-times-hra006579` | Data release not identified | Resolve processed release and original-image coordinates separately from HRA raw access. |
| Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in hepatocellular carcinoma | `cand-wu2025-zenodo` | Image and expression files not yet joined | Join RNA sections to 22 preview image libraries and independent position tables; do not substitute 36 CODEX-region H&E images for 22 Visium sections. |
| Wu et al. 2021 | `cand-wu2021-hcc` | Public download failed (technical) | Recover intact HCC-only release; keep mixed/cholangiocarcinoma out and preserve sample/donor repeats. |
| Jing et al. 2024 | `cand-he2024-new4plc` | Access needs approval or permission | Public processed/original-image route or formal access decision; preserve four primary-liver histologies. |
| Fan et al. 2024 | `cand-fan2024-hra006757` | Access needs approval or permission | Resolve processed matrix/image/coordinates separately from raw permission. |
| Murai et al. 2022 | `cand-jgad000422-hcc` | Access needs approval or permission | Obtain approved access or public processed alternative. |
| 10x Visium Spatial Transcriptomics of 61 Human HCC Samples | `cand-egad50000002122` | Access needs approval or permission | Approved access or public processed alternative, with specimen/image crosswalk. |
| Targeting Treg–fibroblast interaction to enhance immunotherapy in SLD-related HCC | `cand-egad50000001506` | Access needs approval or permission | Approved access or public processed alternative; original-image promise must be checked separately. |
| Spatial Transcriptomics Reveals Distinct Architectures but Shared Vulnerabilities in Primary and Metastatic Liver Tumors | `cand-adapa2025-hd` | Data release not identified | Resolve original data accession and metastatic histology; do not pool liver metastasis as HCC. |
| Deep versus standard spatial transcriptomic sequencing | `cand-gse283406` | Coordinates or image scale missing | Recover two physical-section coordinate/scale crosswalk; do not count platform resequencing as four independent sections/patients. |
| Lau et al. 2022 | `cand-prjna858545-hcc` | Public files listed; inspection not finished | Join images to actual BioProject spatial samples and processed counts/positions; raw SRA alone insufficient. |
| Spatial maps of hepatocellular carcinoma transcriptomes reveal spatial expression patterns in tumor immune microenvironment | `cand-xin2022-hcc` | Data release not identified | Find an actionable processed/image accession or later author release. |
| Spatial Transcriptomics and snRNA-seq Expose CAF Niches Orchestrating Dual Stromal-Immune Barriers in Hepatocellular Carcinoma | `cand-li2025-caf` | Release by the authors needed | Processed RNA, coordinates, images and clinical/region map require release. |
| Takano et al. 2024 | `cand-takano-suzuki-2024` | Original H&E and matched data checked | Only LUAD3B is checked; the rest of the study and image calibration remain (the 72 DPI tag is not a micron scale). |
| Zhao et al. 2025 | `cand-zhao-htapp-2025` | Public files listed; inspection not finished | Extract spatial_list and join the exact 20 sections and 8 reported donor labels to the image members; a directory listing alone does not verify the study. |
| Peng et al. 2026 | `cand-peng-kadara-2025` | Matched data checked; preview image only | Only the 30 invasive or minimally invasive sections are tumour; 25 precursor lesions and one normal stay separate; repeated sections of a patient stay linked. |
| Luo et al. 2024 | `cand-chen-liu-2024` | Matched data checked; preview image only | Original pathology scans and the image transform; the donor relation of the solid and lepidic sections is unknown. |
| Defining the cellular and molecular identities of histologic subtypes in lung adenocarcinoma | `cand-knuch-2026` | Public files listed; inspection not finished | Inspect the actual spatial subset; do not equate 18 scRNA donors with one source-described Visium specimen. |
| Deng et al. 2025 | `cand-deng-micropapillary-2025` | Release by the authors needed | Locate release or later ask for processed/original-image package; histology stratum explicit. |
| Wang et al. 2023 | `cand-lu-cell-discovery-2023` | Access needs approval or permission | Locate public processed original-image alternative or formal access route. |
| Visium HD CytAssist Gene Expression Human Lung Cancer post-Xenium experiment | `cand-10x-post-xenium-hd` | Vendor registration and terms | Treat vendor form/terms as distinct dependency; do not count post-Xenium assay as independent donor. |
| METI lung adenocarcinoma sample LUAD-14C | `cand-meti-luad14c` | Coordinates or image scale missing | Inspect the metadata CSV for coordinates and an original-image or scale route; the released image is not an original scan. |
| Simkin et al. 2026 | `cand-simkin2026-gse268014-hd` | Public files listed; inspection not finished | Audit only GSM9701483/84 HD components; link to existing two patients, add zero new patients; resolve study-versus-assay resource counting. |
| Arora et al. 2023 | `cand-arora2023-gse208253` | Matched data checked; preview image only | Patient IDs, treatment and original scans. |
| Snail-regulated exosomal microRNA-21 suppresses NLRP3 inflammasome activity to enhance cisplatin resistance | `cand-cheng2022-gse181300` | Matched data checked; preview image only | Original scans and treatment; repeated invasive-front and inner sections of two patients. |
| Deciphering head and neck cancer microenvironment: Single-cell and spatial transcriptomics reveals HPV-associated differences | `cand-gse281978-hpv2024` | Matched data checked; preview image only | Donor and site join before counting the three paired donors; the PT and LNMT labels conflict with the primary-tissue metadata. |
| Spatial Transcriptomic Analysis of Surgical Resection Specimens of Primary Head and Neck Squamous Cell Carcinoma Treated with Afatinib in a Window-of-Opportunity Study (EORTC 90111-24111) | `cand-beyaert2025-gse289908` | Coordinates or image scale missing | Recover validated barcode-to-grid/JSON map and original-image relation; no direct expression-coordinate verification yet. |
| TREM2-Expressing Multinucleated Giant Macrophages Are a Biomarker of Good Prognosis in Head and Neck Squamous Cell Carcinoma | `cand-gessain2024-e-mtab-14409` | Public files listed; inspection not finished | Decode the counts, positions and preview inside the .cloupe files; transfer of the original whole-slide images needs a separate agreement. |
| Weeramange et al. 2026 | `cand-frontiers2026-zenodo18238293` | Original H&E and matched data checked | Treatment and timing; 11 tissue blocks from ten donors share four array areas, and the recurrence field is a later outcome. |
| Deep spatial-omics analysis of Head & Neck carcinomas provides alternative therapeutic targets and rationale for treatment failure | `cand-causer2023-uq` | Public download failed (technical) | Retrieve exact UQ processed spatial package and assayed-section H&E; separate PhenoCycler and controlled raw reads. |
| Cancer-associated fibroblast subsets in head and neck squamous cell carcinoma | `cand-li2024-hra005551-hra005576` | Access needs approval or permission | Processed public alternative or formal approval. |
| Hypopharyngeal cancer chemoradiotherapy resistance, spatial transcriptomics | `cand-hypopharynx2025-ccrt` | Release by the authors needed | Author/institution release needed for processed RNA/image/clinical map. |
| Head and neck squamous cell carcinoma immune-checkpoint inhibitor spatial study | `cand-gse301720-ici2026` | Matched data checked; preview image only | Clinical timing and source site; response labels do not show that samples were taken after immunotherapy. |
| Integrative spatiotemporal analysis of squamous tumorigenesis | `cand-oraltumorigenesis2025-preprint` | Data release not identified | Identify human invasive subset and accession; exclude mouse/precursor counts from invasive HNSC denominator. |

## Open dependencies

The 103 reviewed resources (26 in the public-route review, 77 in the package review) were followed to a retrieved result, a registration or controlled-access boundary, a missing release or a reproducible download failure. The open dependencies below are kept apart: a download failure is a technical gap, not a permission requirement. In the public-route review, 144 section packages have expression barcodes that match their tissue coordinates exactly; this is not a patient count or final QC.

| Open dependency | Resources |
| --- | --- |
| Public download works | 49 |
| Public files listed, download failed (technical) | 9 |
| Vendor registration and terms | 8 |
| Free account registration | 2 |
| Data access committee approval | 11 |
| Author release or metadata needed | 61 |
| Local scientific QC remaining | 63 |

| Resource | ID | Route status | Next step |
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
| Batf3+ DCs and the 4–1BB/4–1BBL axis are required at the effector phase in the tumor microenvironment for PD-1/PD-L1 blockade efficacy | `cand-ziblat2024` | BLCA | Original H&E located | Open download | Visium HD, Visium CytAssist |
| Giraud et al. 2024 | `gse245908-lihc` | LIHC | Original H&E located | Open download | Visium |
| Gouin et al. 2021 | `gouin-2021` | BLCA | Original H&E located | Open download | Visium |
| Greenwald et al. 2024 | `cand-greenwald2024` | LGG, GBM | Original H&E located | Open download | Visium |
| HTAN WUSTL (Mo et al. 2024) | `htan-wustl` | BRCA, COAD, READ, PDAC | Original H&E located | Free account | Visium, Visium FFPE |
| Janesick et al. 2023 | `janesick-2023` | BRCA | Original H&E located | Open download | Visium CytAssist |
| Oliveira et al. 2025 (Visium HD) | `oliveira-2025` | COAD, READ | Original H&E located | Open download | Visium HD |
| Pei et al. 2025 | `pei-2025` | PDAC | Original H&E located | Open download | Visium |
| Simkin et al. 2026 | `simkin-2026` | HNSC | Original H&E located | Open download | Visium |
| Spatial and single-nuclei transcriptomics reveals idiosyncratic and generic patterns in papillary and anaplastic thyroid cancers | `cand-tourneur-2026-legacyst` | THCA | Original H&E located | Open download | Spatial Transcriptomics (legacy arrays) |
| Steiner et al. 2026 | `steiner-2026` | LUAD | Original H&E located | Open download | Visium FFPE |
| Takano et al. 2024 | `cand-takano-suzuki-2024` | LUAD | Original H&E located | Open download | Visium FFPE |
| Valdeolivas et al. 2024 | `valdeolivas-2024` | COAD, READ | Original H&E located | Open download | Visium |
| Weeramange et al. 2026 | `cand-frontiers2026-zenodo18238293` | HNSC | Original H&E located | Open download | Visium FFPE |
| Zhang et al. 2024 (thyroid) | `zhang-2024-thca` | THCA | Original H&E located | Open download | Visium |
| Arora et al. 2023 | `cand-arora2023-gse208253` | HNSC | Matched data with preview image | Open download | Visium |
| Barkley et al. 2022, UCEC sample | `ucec-barkley-gse203612` | UCEC | Matched data with preview image | Open download | Visium |
| Cassier et al. 2023, NP137 trial | `ucec-np137-gse225690` | UCEC | Matched data with preview image | Open download | Visium FFPE |
| De Zuani et al. 2024 | `cand-dezuani-cvejic-2024` | LUAD, LUSC | Matched data with preview image | Open download | Visium |
| Deciphering head and neck cancer microenvironment: Single-cell and spatial transcriptomics reveals HPV-associated differences | `cand-gse281978-hpv2024` | HNSC | Matched data with preview image | Open download | Visium |
| Gao et al. 2026 | `stad-gse270678` | STAD | Matched data with preview image | Open download | Visium |
| GSE294006, treated advanced ccRCC | `kirc-treated-gse294006` | KIRC | Matched data with preview image | Open download | Visium FFPE |
| He et al. 2024 | `cand-he2024` | LGG | Matched data with preview image | Open download | Visium |
| Head and neck squamous cell carcinoma immune-checkpoint inhibitor spatial study | `cand-gse301720-ici2026` | HNSC | Matched data with preview image | Open download | Visium |
| Lee et al. 2024 | `stad-gse251950` | STAD | Matched data with preview image | Open download | Visium |
| Liao et al. 2025 | `cand-liao-2025-gse250521` | THCA | Matched data with preview image | Open download | Visium |
| Liu et al. 2026 | `cand-crc-liu-maru2026` | COAD, READ | Matched data with preview image | Open download | Visium HD |
| Luo et al. 2024 | `cand-chen-liu-2024` | LUAD | Matched data with preview image | Open download | Visium CytAssist |
| Meylan et al. 2022 | `kirc-meylan-gse175540` | KIRC | Matched data with preview image | Open download | Visium FFPE, Visium |
| Multiomics and multi-region spatial transcriptome analysis reveal cellular networks and pathways associated with hepatocellular carcinoma recurrence | `cand-gse281759` | LIHC | Matched data with preview image | Open download | Visium |
| Neve et al. 2026 | `cand-crc-orgares-gse283052` | COAD, READ | Matched data with preview image | Open download | Visium |
| Peng et al. 2026 | `cand-peng-kadara-2025` | LUAD | Matched data with preview image | Open download | Visium CytAssist |
| Primary colorectal cancer and liver metastasis, Visium CytAssist | `cand-crc-mahidol-gse267401` | COAD, READ | Matched data with preview image | Open download | Visium CytAssist |
| Ritter et al. 2025 | `cand-ritternepsta2025` | LGG, GBM | Matched data with preview image | Open download | Visium FFPE |
| Schmitt et al. 2026 | `schmitt-2026` | PDAC | Matched data with preview image | Open download | Visium FFPE |
| Snail-regulated exosomal microRNA-21 suppresses NLRP3 inflammasome activity to enhance cisplatin resistance | `cand-cheng2022-gse181300` | HNSC | Matched data with preview image | Open download | Visium |
| Spatial transcriptomic analysis of a diverse patient cohort reveals a conserved architecture in triple-negative breast cancer | `cand-bassiouni-gse210616` | BRCA | Matched data with preview image | Open download | Visium |
| Spatial transcriptomics analysis of neoadjuvant cabozantinib and nivolumab in advanced hepatocellular carcinoma identifies independent mechanisms of resistance and recurrence | `cand-gse238264` | LIHC | Matched data with preview image | Open download | Visium |
| Spatially resolved gene expression and tumour-microenvironment interactions across malignant transformation in IDH-mutant glioma | `cand-longitudinal2026` | LGG | Matched data with preview image | Open download | Visium CytAssist |
| Unveiling Immune Metabolic Mechanisms in Bladder Cancer: Spatial Profiling Identifies ZFP36 as a Therapeutic Target | `cand-zheng2025` | BLCA | Matched data with preview image | Open download | Visium |
| Webb et al. 2025 | `cand-webb2025` | LGG | Matched data with preview image | Open download | Visium |
| Wu et al. 2021 | `cand-wu-2021` | BRCA | Matched data with preview image | Open download | Visium |
| Yu et al. 2026 | `cand-yu2026atlas` | BLCA | Matched data with preview image | Open download | Visium CytAssist |
| 10x Genomics ccRCC, Xenium RNA and protein | `kirc-10x-xenium-protein` | KIRC | Candidate, not yet verified | Free account | Xenium |
| 10x Genomics cervical SCC, Visium FFPE | `cscc-10x-ffpe` | CESC | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Genomics human breast Visium demonstration datasets | `cand-official-10x-breast-demos` | BRCA | Candidate, not yet verified | Open download | Visium HD, Visium CytAssist |
| 10x Genomics kidney preview, Xenium (papillary RCC) | `kirp-10x-xenium-preview` | KIRP | Candidate, not yet verified | Free account | Xenium |
| 10x Genomics lung SCC, Visium CytAssist FFPE | `lusc-10x-cytassist` | LUSC | Candidate, not yet verified | Free account | Visium CytAssist |
| 10x Genomics prostate acinar carcinoma, Visium FFPE | `prad-10x-acinar` | PRAD | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Genomics prostate invasive adenocarcinoma, Visium FFPE | `prad-10x-invasive` | PRAD | Candidate, not yet verified | Free account | Visium FFPE |
| 10x Visium Spatial Transcriptomics of 61 Human HCC Samples | `cand-egad50000002122` | LIHC | Candidate, not yet verified | Controlled access | Visium |
| An integrated single-cell and spatial transcriptomic atlas of thyroid cancer progression identifies prognostic fibroblast subpopulations | `cand-loberg-2026-jci191990` | THCA | Candidate, not yet verified | Author request | Visium FFPE |
| Cancer-associated fibroblast subsets in head and neck squamous cell carcinoma | `cand-li2024-hra005551-hra005576` | HNSC | Candidate, not yet verified | Controlled access | Spatial RNA (protocol unverified) |
| Deep spatial-omics analysis of Head & Neck carcinomas provides alternative therapeutic targets and rationale for treatment failure | `cand-causer2023-uq` | HNSC | Candidate, not yet verified | Open download | Visium |
| Deep versus standard spatial transcriptomic sequencing | `cand-gse283406` | LIHC | Candidate, not yet verified | Open download | Visium CytAssist |
| Defining the cellular and molecular identities of histologic subtypes in lung adenocarcinoma | `cand-knuch-2026` | LUAD | Candidate, not yet verified | Unresolved | Visium |
| Deng et al. 2025 | `cand-deng-micropapillary-2025` | LUAD | Candidate, not yet verified | Author request | Visium CytAssist |
| Erickson et al. 2022 | `prad-erickson-clonal` | PRAD | Candidate, not yet verified | Open download | Spatial Transcriptomics (legacy arrays), Visium |
| Fan et al. 2024 | `cand-fan2024-hra006757` | LIHC | Candidate, not yet verified | Controlled access | Visium FFPE |
| Gaspard-Boulinc et al. 2025 | `cand-gaspardboulin2025` | LGG | Candidate, not yet verified | Unresolved | Visium |
| Grande et al. 2025 | `cand-dutreneo` | BLCA | Candidate, not yet verified | Open download | Visium FFPE |
| Guo et al. 2023, HPV progression series | `cscc-hpv-gse208654` | CESC | Candidate, not yet verified | Open download | Spatial transcriptomics array (platform to confirm) |
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
| Li et al. 2022, ccRCC Visium (EGAD00001008781) | `kirc-egad00001008781` | KIRC | Candidate, not yet verified | Open download | Visium |
| Ling et al., SSRN manuscript | `pcpg-ling-ssrn` | PCPG | Candidate, not yet verified | Unresolved | Spatial transcriptomics (platform unverified) |
| Liu et al. 2023, GeoMx precancer | `escc-precancer-geomx` | ESCA | Candidate, not yet verified | Author request | GeoMx WTA (ROI) |
| METI lung adenocarcinoma sample LUAD-14C | `cand-meti-luad14c` | LUAD | Candidate, not yet verified | Open download | Visium CytAssist |
| Molecular cartography uncovers evolutionary and microenvironmental dynamics in sporadic colorectal tumors | `cand-crc-colonmap-heiser2023` | COAD, READ | Candidate, not yet verified | Free account | Visium FFPE |
| Murai et al. 2022 | `cand-jgad000422-hcc` | LIHC | Candidate, not yet verified | Controlled access | Visium |
| Ou et al. 2022 | `cscc-ou-stereo` | CESC | Candidate, not yet verified | Unresolved | Stereo-seq |
| Pribus et al. 2026 | `cand-pribus2026` | BLCA | Candidate, not yet verified | Open download | Visium |
| Ren et al. 2025 | `cand-crc-spatch-ren2025` | COAD, READ | Candidate, not yet verified | Open download | Visium HD |
| Ren et al. 2025 | `cand-spatch-hcc` | LIHC | Candidate, not yet verified | Open download | Visium HD |
| Schmauch et al. 2025 | `cand-crc-miso-petacc8` | COAD, READ | Candidate, not yet verified | Controlled access | Visium FFPE |
| Simkin et al. 2026 | `cand-simkin2026-gse268014-hd` | HNSC | Candidate, not yet verified | Open download | Visium HD |
| Single-cell RNA-sequencing and spatial transcriptomic analysis reveal a distinct population of APOE-negative cells yielding pathological lymph node metastasis in papillary thyroid cancer | `cand-zhang-2025-prjca021247` | THCA | Candidate, not yet verified | Unresolved | Visium |
| Single-nucleus and Spatially Resolved Intratumor Subtype Heterogeneity in Bladder Cancer | `cand-lindskrog2023` | BLCA | Candidate, not yet verified | Controlled access | Visium |
| Sonpatki et al. 2026 | `cand-snu2026` | LGG, GBM | Candidate, not yet verified | Open download | Visium FFPE, Visium, Xenium |
| Soupir et al., papillary RCC CosMx study | `kirp-macrophage-abstract` | KIRP | Candidate, not yet verified | Open download | Multiplex immunofluorescence, Targeted spatial RNA (960 transcripts) |
| Spatial atlas of tertiary lymphoid structures and high endothelial venules in breast cancer | `cand-bcarc-tls-hev-2026` | BRCA | Candidate, not yet verified | Not released | Visium HD |
| Spatial maps of hepatocellular carcinoma transcriptomes reveal spatial expression patterns in tumor immune microenvironment | `cand-xin2022-hcc` | LIHC | Candidate, not yet verified | Unresolved | Visium |
| Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in hepatocellular carcinoma | `cand-wu2025-zenodo` | LIHC | Candidate, not yet verified | Open download | Visium FFPE |
| Spatial Transcriptomic Analysis of Surgical Resection Specimens of Primary Head and Neck Squamous Cell Carcinoma Treated with Afatinib in a Window-of-Opportunity Study (EORTC 90111-24111) | `cand-beyaert2025-gse289908` | HNSC | Candidate, not yet verified | Open download | Visium FFPE |
| Spatial Transcriptomics and snRNA-seq Expose CAF Niches Orchestrating Dual Stromal-Immune Barriers in Hepatocellular Carcinoma | `cand-li2025-caf` | LIHC | Candidate, not yet verified | Author request | Visium |
| Spatial Transcriptomics Reveals Distinct Architectures but Shared Vulnerabilities in Primary and Metastatic Liver Tumors | `cand-adapa2025-hd` | LIHC | Candidate, not yet verified | Unresolved | Visium HD |
| Spatial transcriptomics reveals prognosis-associated cellular heterogeneity in the papillary thyroid carcinoma microenvironment | `cand-yan-2024-hra003537` | THCA | Candidate, not yet verified | Controlled access | Visium |
| Srinivasan et al. 2025 | `cand-crc-vri-dartmouth2025` | COAD, READ | Candidate, not yet verified | Unresolved | Spatial Transcriptomics (legacy arrays), Visium CytAssist |
| Tang et al. 2025 | `cand-tang2025` | LGG | Candidate, not yet verified | Unresolved | Visium HD |
| Targeting Treg–fibroblast interaction to enhance immunotherapy in SLD-related HCC | `cand-egad50000001506` | LIHC | Candidate, not yet verified | Controlled access | Visium CytAssist |
| TNBC spatial transcriptomics resource (AACR 2026 abstract 1442) | `cand-dartmouth-aacr2026-1442` | BRCA | Candidate, not yet verified | Not released | Visium |
| TREM2-Expressing Multinucleated Giant Macrophages Are a Biomarker of Good Prognosis in Head and Neck Squamous Cell Carcinoma | `cand-gessain2024-e-mtab-14409` | HNSC | Candidate, not yet verified | Open download | Visium FFPE |
| Tumor microenvironment remodeling across thyroid cancer differentiation states revealed by spatial transcriptomics | `cand-seok-2025-cii` | THCA | Candidate, not yet verified | Author request | Visium CytAssist |
| Visium HD CytAssist Gene Expression Human Lung Cancer post-Xenium experiment | `cand-10x-post-xenium-hd` | LUAD | Candidate, not yet verified | Open download | Visium HD |
| Wang et al. 2023 | `cand-lu-cell-discovery-2023` | LUAD | Candidate, not yet verified | Controlled access | Visium |
| Wang et al. 2024 | `cand-wang-venet-2024-legacy-st` | BRCA | Candidate, not yet verified | Open download | Spatial Transcriptomics (legacy arrays) |
| Wu et al. 2021 | `cand-wu2021-hcc` | LIHC | Candidate, not yet verified | Open download | Visium |
| Yoshihara et al. 2026 | `cand-yoshihara2026erbt` | BLCA | Candidate, not yet verified | Open download | Visium CytAssist |
| Zhao et al. 2025 | `cand-zhao-htapp-2025` | LUAD | Candidate, not yet verified | Open download | Visium |
| Zhu et al. 2026, preprint | `pcpg-developmental-preprint` | PCPG | Candidate, not yet verified | Not released | Spatial transcriptomics (human assay details unverified) |
