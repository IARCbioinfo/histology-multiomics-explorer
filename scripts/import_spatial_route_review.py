#!/usr/bin/env python3
"""Apply the 15 October 2026 public-route review to the 26 reviewed spatial resources.

Usage: python3 scripts/import_spatial_route_review.py <followup-dir>

Run after scripts/import_spatial_review.py, which rewrites the entries it created. Reads from <followup-dir>:
  spatial_public_route_followup.json   the 26-resource route ledger (verification only; nothing is copied verbatim)
  checksums.json                       the ledger's recorded SHA-256

The corrections below are curated public-source text. They supersede the earlier package follow-up and extended
audit statements, which the ledger accumulates. Every record gets a route review: a plain status, the open
dependencies (vocabulary `route_state` in scripts/vocab.py), the next step and, where checked, the number of sections
whose expression barcodes match the in-tissue coordinates exactly. Nothing is promoted: records stay gated candidates,
no section rows are created and eligible patients stay unknown (null). Related leads that add no resources or patients
are written to data/leads.json. The script is idempotent and stops if the ledger or the catalogue disagree with it.
"""
import hashlib
import json
import sys
from pathlib import Path

from vocab import ENUMS

DATA = Path(__file__).resolve().parent.parent / "data"
DATE = "2026-10-15"
CATALOGUE_ID = {"lusc-emtab13530": "cand-dezuani-cvejic-2024", "glioma-greenwald-gse237183": "cand-greenwald2024",
                "glioma-2026-niche-atlas": "cand-snu2026"}
# Ledger next-dependency codes and the route states they imply.
IMPLIES = {"vendor_registration_and_terms": {"vendor-terms"}, "controlled_access_and_image_crosswalk": {"dac-approval"},
           "public_file_retrieval_then_local_QC": {"download-failure", "local-qc"}}
VENDOR_ROUTE = "Vendor dataset page; downloading requires registration and acceptance of the vendor's terms (CC BY 4.0 data). No registration was made."
VENDOR = dict(access="account", route=VENDOR_ROUTE, states=["vendor-terms", "local-qc"],
              status="Vendor page requires registration and terms before download",
              next="Complete the vendor registration if wanted (not done), then check the files, H&E and donor history.",
              notes_add=["Vendor download requires registration and acceptance of terms; no form was submitted"])

# Curated corrections per review record. Keys: label, citation, description, access, route, links_add, reported,
# gates, notes_add, notes_remove, sr (spatial_review fields to set), sr_remove, techniques_add, linkage,
# status, states, next, packages (sections with exact barcode-coordinate agreement).
R = {
    "glioma-greenwald-gse237183": dict(
        description="Visium study of glioma organisation with 19 sections: 13 IDH-wildtype glioblastoma sections from five donor labels and six IDH-mutant sections (astrocytoma and oligodendroglioma) from six donor labels. Repeated regions of one donor (ZH881) are one donor label, not separate patients. All 15 original images in the author-linked Visium image archive were retrieved; 14 have geometrically supported counterparts among the GEO sections, and five GEO sections have no original in that archive. The two ZH881 bulk originals match the opposite GEO labels (ZH881_1A_bulk.tif matches GSM7596598 and ZH881_1B_bulk.tif matches GSM7596597); this is an inferred correspondence awaiting author confirmation, and the source labels are kept. In the public clinical Table S1, ZH1041_T1 is CODEX-only, the ZH1019 rows carry the patient ID ZH1007 although age, MGMT status and location differ, BWH23 is reported as IDH-mutant oligodendroglioma grade 4 and BWH28 as astrocytoma grade 2/3; treatment and recurrence are not reported. The Zenodo 12624860 H&E archive accompanies the CODEX data and is a separate serial-section resource, not the Visium image route.",
        links_add=[["Author repository (Visium image archive link)", "https://github.com/tiroshlab/Spatial_Glioma"],
                   ["Clinical Table S1", "https://www.cell.com/cms/10.1016/j.cell.2024.03.029/attachment/89b1c464-df78-4b1d-b0c4-22ff214799c7/mmc1.pdf"]],
        reported_add=[[14, "GEO sections with a matched original image", "image correspondence check"],
                      [5, "GEO sections without an original image in the author archive", "image correspondence check"]],
        gates=["identity", "treatment-review", "pathology-review", "he-not-located", "calibration", "image-qc"],
        notes_add=["ZH881 bulk labels are crossed by inference: keep the source filenames and GEO labels until the authors confirm",
                   "The ZH1019 rows carry the conflicting patient ID ZH1007; keep five provisional IDH-wildtype donor labels",
                   "BWH23 (reported oligodendroglioma grade 4) and BWH28 (astrocytoma grade 2/3) need diagnosis and grade review",
                   "Treatment and recurrence are not reported",
                   "Keep CODEX-associated H&E separate from the Visium images"],
        sr=dict(image_status="All 15 originals in the author-linked Visium archive retrieved (about 3,800 × 4,200 to 17,000 × 17,000 pixels); 14 match GEO sections geometrically, with the ZH881 bulk labels crossed by inference; five GEO sections have no original. TIFF DPI tags are not scanner calibration.",
                treatment_status="not reported in clinical Table S1; recurrence unknown"),
        status="14 of 19 sections matched to original images; labels and clinical issues flagged",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study team for the five missing originals, confirmation of the crossed ZH881 labels, the ZH1019 patient ID, BWH23 and BWH28 diagnosis and grade, scanner calibration and treatment and recurrence; then image and pathology QC.",
        packages=19),
    "glioma-2026-niche-atlas": dict(
        description="Glioma anatomical-niche atlas with 32 Visium sections from 17 patients: 13 with glioblastoma (28 sections), three with IDH-mutant astrocytoma (two grade 3 and one grade 4; three sections) and one normal-brain control from a central-neurocytoma patient. Twenty-seven sections are FFPE and five fresh frozen. Four glioblastoma patients (SNU18, SNU21, SNU25 and SNU33) also have Xenium data and are not additional patients. Section SNU25B is assigned to SNU25 provisionally, following the publication and spot metadata, although the author slide table lists SNU26. The eight public Visium archive packages contain Space Ranger outputs and previews without a separately listed original scan, so they do not establish image coverage of all 32 sections. All five Xenium archives are inventoried, including SNU21's nested analysis archive; their morphology TIFFs are fluorescence images, not H&E. The data statement labels Zenodo 16505469 as Ravi 2022, but that record belongs to the Ravikumar/Al-Holou study (see related leads); which reused dataset the atlas analysed is unresolved. Released in Zenodo 17572905 (Visium) and 17622242 (Xenium), with a UCSC Cell Browser view.",
        links_add=[["Author repository", "https://github.com/nameetas/TSKGA"]],
        reported=[[17, "patients in all, including one normal-brain control", "publication and spot metadata"],
                  [13, "patients with glioblastoma", "publication and spot metadata", "GBM"],
                  [28, "glioblastoma sections", "publication and spot metadata", "GBM"],
                  [3, "patients with IDH-mutant astrocytoma", "publication and spot metadata", "LGG"],
                  [3, "IDH-mutant astrocytoma sections", "publication and spot metadata", "LGG"],
                  [1, "normal-brain control patient (central neurocytoma), one section", "publication and spot metadata"],
                  [32, "Visium sections in all", "publication"],
                  [27, "FFPE Visium sections", "publication"], [5, "fresh-frozen Visium sections", "publication"],
                  [4, "Xenium patients, all also profiled with Visium", "publication"]],
        gates=["package-unverified", "identity", "treatment-review", "he-not-located"],
        notes_remove=["32 is a mixed genotyped-glioma section count, not 32 confirmed GBM donors",
                      "Match original images, matrices and transforms to every capture",
                      "Do not label Zenodo16505469 as Ravi2022 without resolving creator/provenance discrepancy"],
        notes_add=["Xenium patients overlap the Visium patients; do not add them",
                   "SNU25B is provisionally SNU25; the author slide table says SNU26",
                   "The eight Visium archives hold outputs and previews only; they are not image coverage of all 32 sections",
                   "Xenium morphology TIFFs are fluorescence images, not H&E",
                   "Zenodo 16505469 is the Ravikumar/Al-Holou release, not Ravi 2022; the atlas's actual reused input is unresolved",
                   "Match original images, matrices and transforms to every section",
                   "Treatment and recurrence are not reported"],
        sr=dict(image_status="Eight public Visium archive packages inventoried: Space Ranger outputs and previews, no separately listed original scan; five Xenium archives inventoried, with fluorescence morphology TIFFs only; complete section–patient–image linkage unresolved",
                treatment_status="not reported in the clinical table; primary or recurrent status needs a per-patient crosswalk"),
        status="Patient and diagnosis denominator resolved; image coverage and linkage unresolved",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study team for the per-section count, image and patient crosswalk, original H&E beyond previews and fluorescence images, treatment and recurrence, and which reused dataset was analysed.",
        packages=1),
    "lusc-emtab13530": dict(
        description="Visium fresh-frozen atlas of non-small cell lung cancer with 40 sections in all, 20 of them tumour sections, across adenocarcinoma, squamous, unspecified NSCLC and healthy donors. The LUSC subset is Patients 11 and 19: six tumour sections and four adjacent-normal sections. The publication's Supplementary Data 1 gives Patient 11 as T2b N0 M0 and Patient 19 as T3 N0 M0; prior treatment is not reported. All ten LUSC sections have expression barcodes that match their tissue coordinates exactly, but their image archives contain only outputs of about 2,000 pixels; original scans were not found.",
        notes_add=["Staging from Supplementary Data 1: Patient 11 T2b N0 M0, Patient 19 T3 N0 M0", "Prior treatment is not reported"],
        notes_remove=["Check original scans and overlay"],
        sr=dict(image_status="All ten LUSC section packages checked: exact barcode-coordinate agreement; image archives contain 2,000-pixel outputs only; original scans not found",
                treatment_status="not reported; staging resolved from Supplementary Data 1"),
        status="Ten LUSC section packages checked; preview images only",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study team for original scans and the prior treatment of Patients 11 and 19.",
        packages=10),
    "cscc-10x-ffpe": VENDOR,
    "cscc-hpv-gse208654": dict(
        description="Four spatial sections along cervical HPV progression: one squamous cell carcinoma (GSM6360691), one adenocarcinoma (GSM6360692), one HPV-positive normal cervix and one HSIL. Only the carcinoma section of squamous histology belongs to the CSCC scope; the others are kept separate. For GSM6360691 the deposited H&E (10,322 × 9,666 pixels) and expression for 1,757 spots were retrieved, and processing and image evidence support Visium, but no released spot coordinates or scale factors were found, so it is not yet a complete spatial package.",
        gates=["coordinates", "calibration", "identity"],
        sr=dict(platform="Visium, supported by processing and image evidence", assay_classes=["whole-transcriptome"],
                image_status="GSM6360691 H&E 10,322 × 9,666 pixels and 1,757 expression spots retrieved; coordinates and scale factors not released"),
        status="H&E and expression retrieved; spot coordinates missing",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the submitter for the tissue-position table and scale factors of GSM6360691, the image calibration and the clinical provenance."),
    "cscc-ou-stereo": dict(
        description="Stereo-seq study of cervical squamous cell carcinoma reporting 14 tumour patients on 15 slides and two normal-tissue patients on three slides, alongside single-nucleus RNA-seq. H&E comes from serial cryosections, not from the assayed section. The data are listed under CNSA CNP0002543, but the project listing did not resolve and the CNSA accession search returned no result; this does not establish controlled access.",
        route="CNSA CNP0002543 listed in the paper; the public listing did not resolve",
        status="Serial-section study; public data route unresolved",
        states=["download-failure", "author-release"],
        next="Ask the authors or CNSA support for a working route to CNP0002543, processed matrices and coordinates, and original serial H&E with patient and section mapping."),
    "escc-hra000776-omix009524": dict(
        description="Controlled multistage ESCC spatial profiling (HRA000776) with a linked image deposit (OMIX009524) that provides Space Ranger hires images for five named tumours (LZE7T, LZE8T, LZE21T, LZE22T and LZE24T). These are processed images, not verified original-resolution scans. The parent HRA000776 cohort is described as treatment-naive, but the spatial subset's link to it is not established, and the parent cohort's patient count must not be transferred. A live refresh of the access page timed out; the controlled-access policy recorded earlier is kept. No access has been requested or approved.",
        sr=dict(treatment_status="parent cohort described as treatment-naive; spatial subset linkage not established"),
        status="Controlled data; image and assay crosswalk unresolved",
        states=["dac-approval", "author-release", "local-qc"],
        next="Apply through the repository's data access committee only if the data are needed, and ask for the five-tumour image and assay crosswalk and original scans."),
    "escc-hra007162": dict(
        description="Single-cell and spatial multi-omics study of ESCC with Visium data reported for five cancer tissues. NGDC lists the raw reads as open access: the public directory has 13 run folders, and experiment HRX1389699 uses Visium. The earlier controlled-access label was wrong. A processed spatial matrix, original H&E and coordinates were not found, and open raw reads alone do not supply them. Possible overlap with HRA000776 must be resolved before any aggregation.",
        access="open", route="Open raw reads at GSA-Human; processed spatial matrix, original H&E and coordinates not released",
        gates=["package-unverified", "he-not-located", "identity"],
        notes_remove=["Review limit: Archive metadata search result available; direct page retrieval timed out."],
        notes_add=["Open raw reads: do not inherit the controlled status of HRA000776 or HRA003627"],
        sr_remove=["source_review_limit"],
        sr=dict(image_status="Original H&E, processed matrix and coordinates not released"),
        status="Open raw reads; processed and image package unresolved",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study authors for the processed five-case spatial package, original H&E, coordinates and a de-identified donor and run crosswalk."),
    "escc-precancer-geomx": dict(
        description="GeoMx whole-transcriptome ROI profiling of oesophageal squamous precancerous lesions and cancer in 19 patients: six with low-grade and six with high-grade intraepithelial neoplasia, and seven with invasive ESCC; normal regions come from the low-grade donors. Forty-two ROIs were profiled, with H&E from serial sections. The public source-data workbook gives selected genes for the 42 ROIs, not the complete whole-transcriptome matrix, and the author repository holds analysis scripts only; raw reads (HRA003627) are controlled. ROI data are a supplementary resource, kept apart from spot- or bin-based transcriptomics.",
        access="request", route="Public source-data workbook (selected genes, 42 ROIs); complete ROI matrices on request; raw reads HRA003627 controlled",
        links_add=[["Source-data workbook", "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-40343-5/MediaObjects/41467_2023_40343_MOESM4_ESM.xlsx"],
                   ["Author repository", "https://github.com/hrcnlab/escc_pipline"]],
        reported=[[7, "patients with invasive ESCC", "publication", "ESCA"], [19, "patients in the study", "publication"],
                  [12, "patients with intraepithelial neoplasia (six low-grade, six high-grade)", "publication"], [42, "ROIs", "publication"]],
        linkage="serial-section", gates=["platform", "package-unverified", "serial-section", "identity"],
        notes_remove=["Verify patient counts, access, ROI matrices and image registration"],
        notes_add=["Seven invasive ESCC patients within a 19-patient study; normal regions share the low-grade donors",
                   "The public workbook is a selected gene set, not the complete whole-transcriptome matrix"],
        sr=dict(image_status="Serial-section H&E; ROI geometries and image crosswalk not released"),
        status="Selected genes public; complete ROI matrix not released",
        states=["author-release", "local-qc"],
        next="Ask the corresponding authors for the complete normalised and raw ROI matrices, QC annotations, ROI geometries and the serial H&E crosswalk."),
    "kirc-meylan-gse175540": dict(
        description="Visium data from 24 primary ccRCC tumours (12 FFPE, 12 fresh frozen) in a study of tertiary lymphoid structures; the primary paper documents treatment-naive primary ccRCC. Processed data are public and raw reads are withheld. All 24 deposited section packages have expression barcodes that match their tissue coordinates exactly, but the images are previews of at most 2,000 pixels; a check of all 426 links of the STOmicsDB mirror found 48 preview PNGs and no original scan. The public clinical Table S1 could not be downloaded (a technical failure), so the donor, section and grade join is unresolved.",
        links_add=[["STOmicsDB mirror", "https://db.cngb.org/stomics/datasets/STDS0000223/data"]],
        gates=["he-not-located", "identity"],
        notes_remove=["Review treatment and TLS enrichment"],
        notes_add=["Review TLS enrichment",
                   "Study-level treatment-naive status is documented in the primary paper",
                   "Clinical Table S1 is publicly linked but its download failed: a technical gap, not author-only data"],
        sr=dict(image_status="All 24 section packages checked: exact barcode-coordinate agreement; previews of at most 2,000 pixels; no TIFF, SVS or NDPI among 426 mirror links",
                treatment_status="treatment-naive primary ccRCC documented in the primary paper", treatment_class="reported-untreated"),
        status="24 section packages checked; preview images only",
        states=["public-download", "download-failure", "author-release", "local-qc"],
        next="Retry the public clinical table, then ask the submitter for the original H&E of the 24 sections and the donor, section and grade crosswalk.",
        packages=24),
    "kirc-egad00001008781": dict(
        label="Li et al. 2022, ccRCC Visium (EGAD00001008781)",
        citation={"authors": "Li R, et al.", "title": "Mapping single-cell transcriptomes in the intra-tumoral and associated territories of kidney cancer",
                  "journal": "Cancer Cell", "year": 2022, "doi": "10.1016/j.ccell.2022.11.001", "url": "https://doi.org/10.1016/j.ccell.2022.11.001"},
        description="Visium study of clear-cell RCC: 16 sections from eight ccRCC patients (38,836 spots), covering tumour core and the tumour–normal interface. Processed spatial data are public through Mendeley Data (g67bkbnhhg.1) and Sanger's public FTP directory; metadata inspection of both spatial H5AD files confirms the eight patients and 16 sections. Both files copy the image metadata of all 16 sections, so together they hold 16 sections, not 32. Their images are previews (2,000 and 600 pixels). The paper documents treatment-naive surgery. Controlled raw reads (EGAD00001008781) are needed only for raw-data reuse; original H&E and calibration need an author release. Numerical matrix QC has not been done.",
        access="open",
        route="Public processed H5AD files: Mendeley Data g67bkbnhhg.1 and the Sanger public FTP directory ftp.sanger.ac.uk/pub/teams/332/mapping_single_cell_RCC (anonymous FTP works; the Mendeley file link returned an error). Controlled raw CRAMs at EGA are optional for processed reuse.",
        links_add=[["Publication", "https://doi.org/10.1016/j.ccell.2022.11.001"],
                   ["Mendeley Data", "https://data.mendeley.com/datasets/g67bkbnhhg/1"],
                   ["Project page", "https://www.sanger.ac.uk/project/microenvironment-of-kidney-cancer/"]],
        reported=[[8, "patients with ccRCC", "public H5AD metadata"], [16, "sections", "public H5AD metadata"], [38836, "spots", "public H5AD metadata"]],
        gates=["he-not-located", "calibration", "image-qc"],
        notes_remove=["Obtain specimen/donor crosswalk and image package"],
        notes_add=["The two public H5AD files copy all 16 sections' image metadata: count 16 sections, not 32",
                   "EGA approval is needed only for controlled raw reads",
                   "Original H&E and calibration need an author release"],
        sr=dict(image_status="Public H5AD images are 2,000- and 600-pixel previews; original scans not among the public files",
                treatment_status="treatment-naive surgery documented in the primary paper", treatment_class="reported-untreated"),
        status="Public processed data located; eight patients and 16 sections confirmed",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study team for original H&E and calibration; apply to EGA only if raw reads are needed."),
    "kirc-treated-gse294006": dict(
        sr=dict(image_status="All three expression and coordinate sets agree; supplied images at most 2,000 pixels; originals not found"),
        status="Three section packages checked; preview images only",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the submitter for original H&E, calibration and matching metadata for the three sections.",
        packages=3),
    "kirc-10x-xenium-protein": VENDOR,
    "kirp-10x-xenium-preview": VENDOR,
    "kirp-macrophage-abstract": dict(
        label="Soupir et al., papillary RCC CosMx study",
        description="Study of immunosuppressive macrophages in papillary RCC. The 2025 full paper describes a CosMx 960-target RNA assay on tissue from 11 mixed-RCC patients, with four papillary and 24 clear-cell cores across three orthogonal sections; its 16 papillary and 70 clear-cell RCC patients are multiplex-IF cohorts, not spatial RNA counts. A public Seurat object (Harvard Dataverse OUWYBU, CC BY 4.0; also on Zenodo 12730227) holds 199,112 cells and three slide identifiers but no patient, histology or treatment crosswalk, and the broader deposit spans several treatment groups. Both repositories direct clinical enquiries to Brandon Manley, and the public code refers to an unreleased clinical table.",
        access="open", route="Public Seurat object (Harvard Dataverse, CC BY 4.0; Zenodo copy); clinical and H&E mapping from the study team",
        links_add=[["Full paper (2025)", "https://doi.org/10.1177/24684562251358595"], ["Harvard Dataverse", "https://doi.org/10.7910/DVN/OUWYBU"],
                   ["Zenodo copy", "https://zenodo.org/records/12730227"], ["Public code", "https://github.com/FridleyLab/ccRCC_CosMx_SMI_2023"]],
        reported=[[11, "mixed-RCC patients prepared for spatial RNA", "full paper"], [4, "papillary RCC tissue cores", "full paper"],
                  [24, "clear-cell RCC tissue cores", "full paper"], [3, "orthogonal sections", "full paper"],
                  [16, "papillary RCC patients, multiplex IF (not a spatial RNA count)", "conference abstract"],
                  [70, "clear-cell RCC patients, multiplex IF", "conference abstract"]],
        gates=["platform", "identity", "he-not-located", "treatment-review"],
        notes_remove=["Locate full study and deposited counts/coordinates/images"],
        notes_add=["Four papillary cores and 11 mixed-RCC patients do not give a papillary patient count",
                   "Do not apply the paper subset's surgical eligibility to the whole public release",
                   "Clinical crosswalk needed from Brandon Manley, as both repositories state; never request internal record numbers"],
        sr=dict(platform="CosMx 960-target RNA; multiplex IF in separate cohorts", role="candidate resource",
                image_status="Slide identifiers released; H&E mapping and registration not released"),
        status="Public molecular object; clinical and H&E crosswalk needed from the study team",
        states=["public-download", "author-release", "local-qc"],
        next="Ask Brandon Manley, as both repositories direct, for a de-identified slide-to-patient, histology and treatment crosswalk, the paper's subset membership and H&E registration."),
    "lusc-10x-cytassist": VENDOR,
    "pcpg-ling-ssrn": dict(
        route="Author manuscript on SSRN; full-text retrieval blocked by a security check; no data release found",
        status="Manuscript lead; data release unresolved",
        states=["author-release"],
        next="Ask the authors for the final publication, platform, patient and section counts, accession and expression and H&E package."),
    "pcpg-developmental-preprint": dict(
        description="Preprint on spatially organised developmental cell states linking paraganglioma and neuroblastoma. Its full text describes two human PPGL specimens (PPGL #1 and malignant PPGL #263) profiled with Visium HD; mouse in-situ sequencing, neuroblastoma and composite tumours are separate analyses. An adjacent H&E inset is shown for PPGL #1, but original same-section images are not established. The data statement promises public accessions but supplies none, and describes de-identified human data as controlled under ethics approval and data agreements.",
        access="unreleased", route="No actionable accession; release promised at publication; human data described as controlled",
        reported=[[2, "human PPGL specimens", "preprint full text"]],
        sr=dict(platform="Visium HD (two human PPGL specimens)", assay_classes=["whole-transcriptome"],
                image_status="Adjacent H&E inset shown for PPGL #1; original images not released"),
        notes_remove=["Retrieve primary full text and accession before assigning a sample count or platform"],
        notes_add=["Count only the two human PPGL specimens; exclude mouse, neuroblastoma and composite tumours"],
        status="Human Visium HD assay resolved; accession not supplied",
        states=["author-release"],
        next="Ask the lead contact for the accession and the human PPGL processed data, coordinates, original H&E, section relation and donor and treatment metadata."),
    "prad-10x-acinar": VENDOR,
    "prad-10x-invasive": VENDOR,
    "prad-hirz-slideseq": dict(
        description="Slide-seqV2 profiling within a study of the prostate tumour microenvironment: 12 arrays from four donors, two with prostate cancer from a treatment-naive prostatectomy cohort and two controls without prostate cancer. H&E comes from consecutive sections, not the assayed ones. The study's 19 cancer patients are single-cell RNA-seq donors, not spatial patients. The public Zenodo archive has count matrices and annotations for the 12 arrays, but all 12 bead-location tables are defective (missing bead barcodes and x and y values) and the archive contains no H&E; archived code refers to local coordinate files that were not released. The data are not spatially usable until corrected coordinates are released.",
        gates=["coordinates", "serial-section", "he-not-located", "identity"],
        notes_add=["All 12 released bead-location tables are defective; do not treat the package as spatially usable"],
        sr=dict(image_status="No H&E in the public archive; consecutive-section H&E not released"),
        status="Bead coordinates defective in all 12 released tables",
        states=["author-release"],
        next="Ask the study authors for corrected bead locations or the per-array input files, the barcode crosswalk and original serial H&E."),
    "prad-erickson-clonal": dict(
        description="Legacy Spatial Transcriptomics and Visium study mapping clonal copy-number alterations across benign and malignant prostate tissue. The public Mendeley release lists original-image folders for two patients (Patient 1, with legacy-array and Visium folders, and Patient 2), with large JPEG files and a checksum, but the actual file downloads failed (an HTTP error and a browser timeout): a technical gap, not a permission requirement. Benign fields and multiple regions from one patient must not be counted as separate patients. Controlled raw sequencing at EGA is not needed for processed reuse.",
        route="Public Mendeley release (versions 1 and 5); file downloads failed technically; raw sequencing controlled at EGA",
        links_add=[["Data archive, version 1", "https://data.mendeley.com/datasets/svw96g68dv/1"]],
        techniques_add=["Visium"],
        reported=[[2, "patients with public image folders", "Mendeley release"]],
        notes_remove=["Verify archive manifest, donor counts and tumour regions"],
        notes_add=["Public image folders verified for two patients; actual files still to retrieve"],
        sr=dict(image_status="Original-image folders and large JPEGs listed publicly; downloads failed"),
        status="Public image folders verified; file download failed",
        states=["download-failure", "local-qc"],
        next="Retry the public file downloads, then check images, coordinates and the clinical mapping."),
    "stad-gse251950": dict(
        sr=dict(image_status="All ten section packages checked: exact barcode-coordinate agreement; images 2,000-pixel outputs only; original scans not found"),
        status="Ten section packages checked; preview images only",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the submitter for original scans and the clinical, histology and treatment linkage for the nine donor labels and the GC6 peritoneal metastasis.",
        packages=10),
    "stad-gse270678": dict(
        description="Visium atlas of lymphocyte-aggregated regions in gastric cancer: 33 main sections from 19 patients and 39 repeat sections; donor D30 appears only among the repeats, which gives 20 donor labels in the deposit. All 72 deposited section packages have expression barcodes that match their tissue coordinates exactly; the images are 2,000-pixel previews. The paper reports treatment-naive surgical donors; histology (intestinal, diffuse, indeterminate) and core, edge and in-between regions are annotated. An additional Mendeley release holds one 6.12 GB spatial RDS file, whose download failed (a technical gap). Raw reads (HRA007814) are controlled and are not needed for processed reuse.",
        links_add=[["Additional Mendeley release", "https://data.mendeley.com/datasets/559mchb37p/1"]],
        reported=[[19, "patients with main sections", "Supplementary Data 1"], [33, "main sections", "Supplementary Data 1"],
                  [39, "repeat sections", "Supplementary Data 1"], [20, "donor labels in the deposit, D30 in repeats only", "GEO series"],
                  [72, "deposited sections", "GEO series"]],
        gates=["he-not-located", "image-qc"],
        notes_remove=["Reconcile 19 main tumour samples versus 20 deposited donor labels"],
        notes_add=["Repeat sections add sections, not patients; D30 appears only among the repeats"],
        sr=dict(image_status="All 72 section packages checked: exact barcode-coordinate agreement; 2,000-pixel previews; original scans not found"),
        status="72 section packages checked; patient and section count resolved",
        states=["public-download", "download-failure", "author-release", "local-qc"],
        next="Retry the Mendeley download; ask the submitter for original scans and calibration if they are not in the public RDS.",
        packages=72),
    "ucec-barkley-gse203612": dict(
        description="One endometrial carcinoma Visium sample (GSM6177623, NYU_UCEC3_Vis) from a pan-cancer cell-state atlas; single-cell samples and other cancers in the series are not part of this entry. Its section package was checked (expression barcodes match the tissue coordinates), but the deposited image is a 1,899 × 2,000-pixel preview. The author-linked Dropbox and NYU SharePoint data folders are deleted or disabled, and the archived code on Zenodo (6611786) contains scripts only, without the original scan or clinical table. Histological subtype and treatment history are unknown.",
        notes_add=["Author-linked data folders are disabled; the archived code contains no original scan or clinical table"],
        sr=dict(image_status="GSM6177623 section package checked; image is a 1,899 × 2,000-pixel preview; author data links disabled"),
        status="Section package checked; author data links disabled",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the study team to restore the public data links and for the original image, histological subtype and treatment of NYU_UCEC3.",
        packages=1),
    "ucec-np137-gse225690": dict(
        description="Visium FFPE profiles of endometrial cancer metastasis biopsies from the NP137 netrin-1 blockade trial: four sections from two patients, each at baseline and after one month of NP137. The trial supplement identifies 01-034 as endometrioid adenocarcinoma (initial grade 2) and 01-039 as papillary serous adenocarcinoma (initial grade 3), and every trial participant had received at least two earlier lines of systemic therapy (two to six, median three), so both patients were previously treated even at baseline. All four section packages have expression barcodes that match their tissue coordinates exactly (539 to 2,141 spots); the images are previews of at most 2,000 pixels. An exploratory treated, metastatic comparison of two histologies, not a homogeneous endometrioid reference.",
        reported=[[2, "patients", "trial publication"], [4, "metastasis biopsy sections profiled", "GEO series"],
                  [2, "timepoints per patient (baseline and after one month)", "GEO series"]],
        gates=["treated", "he-not-located"],
        notes_remove=["Deposit contains 01-034 and 01-039; summary says one patient: reconcile before validated patient count"],
        notes_add=["Two histologies: 01-034 endometrioid (initial grade 2) and 01-039 papillary serous (initial grade 3); do not pool as one endometrioid reference",
                   "Both patients had at least two earlier systemic lines; baseline means before NP137"],
        sr=dict(image_status="All four section packages checked: exact barcode-coordinate agreement; previews of at most 2,000 pixels",
                treatment_status="every trial participant had two to six earlier systemic lines; sampled at baseline and after one month of NP137"),
        status="Two previously treated patients and four sections confirmed",
        states=["public-download", "author-release", "local-qc"],
        next="Ask the trial team for original H&E and calibration, and for exact earlier regimens only if a response analysis needs them.",
        packages=4),
}

LEADS = [
    {"id": "lead-tls-kidney-lung", "label": "Kidney and lung TLS Visium release (Zenodo 14620362)",
     "url": "https://zenodo.org/records/14620362", "doi": "10.5281/zenodo.14620362", "tissues": "kidney and lung",
     "description": "Visium FFPE release of three kidney and five lung specimens with expert tertiary lymphoid structure, immune, tumour and normal annotations. The full archive was retrieved and checksum-verified: all eight expression packages have exact barcode-coordinate agreement, and all eight original TIFF images (about 10,000 × 10,000 pixels) are readable. A relation between the preprocessed and full-resolution coordinates was fitted, which is an inference rather than a supplied calibration.",
     "not_counted": "Histological subtype, donor independence and treatment are not established, so its specimens are not assigned to KIRC, KIRP, LUAD or LUSC.",
     "next": "Ask the study authors for histological subtypes, donor independence and treatment mapping.", "sections_checked": 8},
    {"id": "lead-cin3-precursor", "label": "CIN3 spatial study (precursor lesions)",
     "url": "https://doi.org/10.1002/path.70002", "doi": "10.1002/path.70002", "tissues": "cervical precursor lesions (CIN3)",
     "description": "Spatial transcriptomics of cervical intraepithelial neoplasia grade 3: eight biopsies were selected and seven samples analysed. The University of Queensland repository lists eight large H&E TIFFs; coordinates, expression and the patient and section matching are not verified.",
     "not_counted": "Precursor biology: not invasive cervical squamous cell carcinoma, so it adds no CSCC patients.",
     "next": "Verify the coordinates, expression and patient and section matching.", "sections_checked": None,
     "links": [["Repository", "https://espace.library.uq.edu.au/view/UQ:1bd2e07"], ["Code", "https://github.com/BiomedicalMachineLearning/CIN3"]]},
    {"id": "lead-ravikumar-glioma", "label": "Ravikumar/Al-Holou glioma release (Zenodo 16505469)",
     "url": "https://zenodo.org/records/16505469", "doi": None, "tissues": "glioma",
     "description": "Public spatial H5AD linked by a Ravikumar/Al-Holou preprint (bioRxiv 10.1101/2025.10.17.683110). Its metadata show 14 section labels with images of at most 2,000 pixels; the preprint reports seven patients and 14 new sections, eight primary and six recurrent. Its four filename prefixes are not four patients, and its pooled 44-section analysis reuses Freiburg and Broad sections, which are not new patients. The newer glioma atlas labels this record as Ravi 2022, but it belongs to this study.",
     "not_counted": "A linked reuse record: donor mapping and original scans are unresolved, and it is not a new eligible cohort.",
     "next": "Ask the authors for the seven-patient section crosswalk, treatment, IDH and diagnosis, and original H&E with calibration.", "sections_checked": None,
     "links": [["Preprint", "https://www.biorxiv.org/content/10.1101/2025.10.17.683110v2.full"]]},
]


def stop(msg):
    sys.exit(f"import_spatial_route_review: {msg}")


def main():
    if len(sys.argv) != 2:
        stop("usage: import_spatial_route_review.py <followup-dir>")
    src = Path(sys.argv[1])
    raw = (src / "spatial_public_route_followup.json").read_bytes()
    recorded = {x["file"]: x["sha256"] for x in json.loads((src / "checksums.json").read_text(encoding="utf-8"))}
    if hashlib.sha256(raw).hexdigest() != recorded.get("spatial_public_route_followup.json"):
        stop("the ledger does not match its recorded checksum")
    ledger = json.loads(raw)
    recs = {r["review_record_id"]: r for r in ledger["records"]}
    elig = json.loads((DATA / "tcga_eligibility.json").read_text(encoding="utf-8"))["panel"]["selected_analysis"]
    s = ledger["followup_summary"]
    if ledger["review_date"] != DATE or ledger["new_globally_eligible_patients"] is not None or ledger["tcga_counts_changed"]:
        stop("the ledger must be the 15 October review with no eligible patients and no TCGA change")
    if (s["unchanged_TCGA_union"], s["unchanged_TCGA_paired"]) != (elig["total"], elig["paired"]):
        stop("the ledger's TCGA totals differ from tcga_eligibility.json")
    if set(recs) != set(R) or len(ledger["records"]) != 26:
        stop(f"ledger records differ from the 26 curated corrections: {sorted(set(recs) ^ set(R))}")
    if sum(d.get("packages") or 0 for d in R.values()) != ledger["molecular_packages_checked"]:
        stop("section packages checked do not add up to the ledger's total")
    if ledger["additional_tls_section_packages_checked"] != LEADS[0]["sections_checked"]:
        stop("TLS section packages differ from the ledger")

    cohorts = json.loads((DATA / "cohorts.json").read_text(encoding="utf-8"))
    by_review = {c["spatial_review"]["id"]: c for c in cohorts if c.get("spatial_review")}
    if set(by_review) != set(R):
        stop("cohorts.json does not hold the 26 reviewed records; run import_spatial_review.py first")
    for rid, d in R.items():
        r, c = recs[rid], by_review[rid]
        if c["id"] != CATALOGUE_ID.get(rid, rid):
            stop(f"{rid}: catalogue ID {c['id']} changed")
        if r["eligible_patients"] is not None or r.get("author_contact_sent"):
            stop(f"{rid}: the ledger must leave eligible patients unknown and record no author contact")
        states = set(d["states"])
        if any(x not in ENUMS["route_state"] for x in states) or not IMPLIES.get(r["next_dependency"], set()) <= states:
            stop(f"{rid}: route states {sorted(states)} do not match the ledger's next dependency {r['next_dependency']}")
        if r.get("formal_approval_required_for_public_processed_data") is True and "dac-approval" not in states:
            stop(f"{rid}: the ledger requires approval for processed data")
        if r.get("formal_approval_required_for_public_processed_data") is False and "dac-approval" in states:
            stop(f"{rid}: the ledger says processed data need no approval")

        for k in ("label", "citation", "description", "linkage"):
            if k in d:
                c[k] = d[k]
        if "access" in d:
            c["access"]["category"] = d["access"]
        if "route" in d:
            c["access"]["route"] = d["route"]
        have = {u for _, u in c["access"].get("links", [])}
        c["access"]["links"] = c["access"].get("links", []) + [l for l in d.get("links_add", []) if l[1] not in have]
        if "techniques_add" in d:
            c["techniques"] = c.get("techniques", []) + [t for t in d["techniques_add"] if t not in c.get("techniques", [])]
        if "reported" in d:
            c["reported"] = d["reported"]
        have = {tuple(x[:2]) for x in c.get("reported") or []}
        c["reported"] = (c.get("reported") or []) + [x for x in d.get("reported_add", []) if tuple(x[:2]) not in have]
        if "gates" in d:
            c["gates"] = d["gates"]
        notes = [n for n in c.get("notes") or [] if n not in d.get("notes_remove", [])]
        c["notes"] = notes + [n for n in d.get("notes_add", []) if n not in notes]
        sr = c["spatial_review"]
        for k in d.get("sr_remove", []):
            sr.pop(k, None)
        sr.update(d.get("sr", {}))
        sr["route_review"] = {"date": DATE, "status": d["status"], "states": d["states"], "next_step": d["next"],
                              "sections_with_matching_coordinates": d.get("packages")}
        c["verified_on"] = DATE

    (DATA / "cohorts.json").write_text(json.dumps(cohorts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    leads = [{**lead, "checked_on": DATE} for lead in LEADS]
    (DATA / "leads.json").write_text(json.dumps(leads, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for d in R.values():
        for x in d["states"]:
            counts[x] = counts.get(x, 0) + 1
    print(f"route review: 26 records updated, {sum(d.get('packages') or 0 for d in R.values())} section packages, "
          f"{len(leads)} related leads; states {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
