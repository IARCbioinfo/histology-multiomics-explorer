#!/usr/bin/env python3
"""Import the reviewed spatial-resource records into data/cohorts.json.

Usage: python3 scripts/import_spatial_review.py <review-dir>

Reads from <review-dir>:
  spatial_expansion_public_manifest.json  curated resource records (the specification)
and, for validation only (nothing from them is written):
  spatial_expansion_sample_files.json     public GEO sample-metadata rows
  EMTAB13530_unique_samples.json          deduplicated E-MTAB-13530 SDRF rows
  image_header_checks.json                representative GEO image dimensions
  greenwald_HE_zip_manifest.json          directory of the Zenodo 12624860 H&E archive
  existing_catalogue_overlap.json         records that enrich existing catalogue entries

Every reported count is copied from the manifest and labelled with its unit and basis; a count the
manifest leaves null stays absent (unknown), never zero. Records are candidates: no capture rows are
created and nothing enters the strict core. Entries that already existed in the catalogue keep their
ID, label, citation and hand-curated fields and are enriched; entries created by this importer are
rewritten on each run. The script stops if the manifest, its supporting evidence or the catalogue
disagree with the expectations below.
"""
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
REVIEW_DATE = "2026-10-15"
GROUPS = {"CSCC", "ESCC", "KIRC", "KIRP", "LUSC", "PCPG", "PRAD", "STAD", "UCEC", "GLIOMA"}
# Selected histology mapped to the catalogue's cancer pages (CSCC and ESCC live on the CESC and ESCA pages).
PAGE_OF = {"CSCC": ["CESC"], "ESCC": ["ESCA"], "KIRC": ["KIRC"], "KIRP": ["KIRP"], "LUSC": ["LUSC"], "PCPG": ["PCPG"],
           "PRAD": ["PRAD"], "STAD": ["STAD"], "UCEC": ["UCEC"]}
EXISTING = {"lusc-emtab13530": "cand-dezuani-cvejic-2024", "glioma-greenwald-gse237183": "cand-greenwald2024",
            "glioma-2026-niche-atlas": "cand-snu2026"}
ACCESS = {"open", "account", "controlled", "request", "unreleased", "unresolved"}


def cite(authors, title, journal, year, doi):
    return {"authors": authors, "title": title, "journal": journal, "year": year, "doi": doi,
            "url": f"https://doi.org/{doi}" if doi else None}


def vendor(title, url):
    return {"authors": "10x Genomics", "title": title, "journal": "10x Genomics datasets", "year": None, "doi": None, "url": url}


def archive(title, where, url):
    return {"authors": None, "title": title, "journal": where, "year": None, "doi": None, "url": url}


# Explicit decisions per manifest record. "reported" lists manifest count keys with the unit and basis to show and,
# optionally, the cancer page the count belongs to; every non-null manifest count must appear exactly once.
D = {
    "cscc-10x-ffpe": dict(
        label="10x Genomics cervical SCC, Visium FFPE", citation=None, assays=["whole-transcriptome"], techniques=["Visium FFPE"],
        preservation=["FFPE"], compartments=["primary-tumour"], treatment="unknown", linkage="listed-together",
        gates=["he-unverified", "identity", "treatment-review"], access="open", accession="10x Genomics dataset; block C00084155.1a",
        reported=[("sections", "section (vendor specimen)", "vendor dataset page")],
        description="Vendor Visium FFPE demonstration of one invasive cervical squamous cell carcinoma specimen, reported as T1bN0M0, stage IB (block C00084155.1a). The source describes a 20x H&E of the assayed section; the original image file and its registration were not checked here."),
    "cscc-hpv-gse208654": dict(
        label="Guo et al. 2023, HPV progression series",
        citation=cite("Guo C, et al.", "Spatiotemporally deciphering the mysterious mechanism of persistent HPV-induced malignant transition and immune remodelling from HPV-infected normal cervix, precancer to cervical cancer: Integrating single-cell RNA-sequencing and spatial transcriptome", "Clinical and Translational Medicine", 2023, "10.1002/ctm2.1219"),
        assays=["unverified"], techniques=["Spatial transcriptomics array (platform to confirm)"], preservation=[],
        compartments=["primary-tumour", "normal", "precursor"], treatment="reported-untreated", linkage="unverified",
        gates=["he-unverified", "calibration", "identity"], access="open", accession="GSE208654 (SCC section GSM6360691)",
        reported=[("scc_sections", "squamous cell carcinoma section (GSM6360691)", "GEO series", "CESC"),
                  ("adenocarcinoma_sections", "adenocarcinoma section (GSM6360692), outside CSCC", "GEO series"),
                  ("nonmalignant_sections", "HPV-positive normal and HSIL sections", "GEO series"),
                  ("study_sections", "sections in the complete series", "GEO series")],
        description="Four spatial sections along cervical HPV progression: one squamous cell carcinoma (GSM6360691), one adenocarcinoma (GSM6360692), one HPV-positive normal cervix and one HSIL. Only the carcinoma section of squamous histology belongs to the CSCC scope; the others are kept separate. JPG images are deposited, but the coordinate package and original image resolution are incomplete or unverified, and the exact array platform is still to be confirmed."),
    "cscc-ou-stereo": dict(
        label="Ou et al. 2022",
        citation=cite("Ou Z, et al.", "Single-Nucleus RNA Sequencing and Spatial Transcriptomics Reveal the Immunological Microenvironment of Cervical Squamous Cell Carcinoma", "Advanced Science", 2022, "10.1002/advs.202203040"),
        assays=["whole-transcriptome"], techniques=["Stereo-seq"], preservation=["Fresh frozen"],
        compartments=["tumour-unspecified", "normal"], treatment="unknown", linkage="serial-section",
        gates=["serial-section", "release-unresolved", "he-not-located", "treatment-review"], access="unresolved", accession="CNSA CNP0002543",
        reported=[("tumour_patients_reported", "tumour patients", "publication"), ("tumour_sections", "tumour slides", "publication"),
                  ("normal_patients_reported", "normal-tissue patients", "publication"), ("normal_sections", "normal-tissue slides", "publication")],
        description="Stereo-seq study of cervical squamous cell carcinoma reporting 14 tumour patients on 15 slides and two normal-tissue patients on three slides, alongside single-nucleus RNA-seq. H&E comes from serial cryosections, not from the assayed section. The data are listed under CNSA CNP0002543; processed data and image access were not verified."),
    "escc-hra000776-omix009524": dict(
        label="HRA000776 / OMIX009524, multistage ESCC", citation=archive("Multistage ESCC spatial profiling with linked image deposit", "NGDC GSA-Human", "https://ngdc.cncb.ac.cn/gsa-human/browse/HRA000776"),
        assays=["whole-transcriptome"], techniques=["Visium (library details to verify)"], preservation=[],
        compartments=["tumour-unspecified"], treatment="unknown", linkage="unverified",
        gates=["controlled", "he-unverified", "identity"], access="controlled", accession="HRA000776; OMIX009524",
        reported=[("named_image_packages", "named tumour image packages", "OMIX009524 release")],
        description="Controlled multistage ESCC spatial profiling (HRA000776) with a linked image deposit (OMIX009524) that provides Space Ranger hires images for five named tumours (LZE7T, LZE8T, LZE21T, LZE22T and LZE24T). These are processed images, not verified original-resolution scans. No access has been requested or approved."),
    "escc-hra007162": dict(
        label="HRA007162, ESCC single-cell and spatial", citation=archive("Single-cell and spatial multi-omics of human ESCC", "NGDC GSA-Human", "https://ngdc.cncb.ac.cn/gsa-human/browse/HRA007162"),
        assays=["whole-transcriptome"], techniques=["Visium"], preservation=[], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["controlled", "package-unverified", "he-not-located", "identity"], access="controlled", accession="HRA007162",
        reported=[("cancer_tissues_reported", "cancer tissues", "archive description")],
        description="Controlled single-cell and spatial multi-omics study of ESCC with Visium data reported for five cancer tissues. A matched processed and image release was not located, and possible overlap with HRA000776 must be resolved before any aggregation. The archive page timed out during review; only its metadata search result was available."),
    "escc-precancer-geomx": dict(
        label="Liu et al. 2023, GeoMx precancer",
        citation=cite("Liu X, et al.", "Spatial transcriptomics analysis of esophageal squamous precancerous lesions and their progression to esophageal cancer", "Nature Communications", 2023, "10.1038/s41467-023-40343-5"),
        assays=["roi"], techniques=["GeoMx WTA (ROI)"], preservation=[], compartments=["precursor", "tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["platform", "package-unverified", "identity"], access="unresolved", accession=None, reported=[],
        description="GeoMx whole-transcriptome ROI profiling of oesophageal squamous precancerous lesions and cancer. ROI data are a supplementary resource, kept apart from spot- or bin-based transcriptomics. Patient counts, ROI matrices and image registration were not verified."),
    "kirc-meylan-gse175540": dict(
        label="Meylan et al. 2022",
        citation=cite("Meylan M, et al.", "Tertiary lymphoid structures generate and propagate anti-tumor antibody-producing plasma cells in renal cell cancer", "Immunity", 2022, "10.1016/j.immuni.2022.02.001"),
        assays=["whole-transcriptome"], techniques=["Visium FFPE", "Visium"], preservation=["FFPE", "Fresh frozen"], compartments=["tumour-unspecified"],
        treatment="unknown", linkage="listed-together", gates=["he-unverified", "identity", "treatment-review"], access="open", accession="GSE175540",
        reported=[("spatial_samples", "spatial samples", "GEO series"), ("ffpe_samples", "FFPE samples", "GEO series"), ("frozen_samples", "fresh-frozen samples", "GEO series")],
        description="Visium data from 24 renal cell carcinoma samples (12 FFPE, 12 fresh frozen) in a study of tertiary lymphoid structures; processed data are public and raw reads are withheld. The deposited images of the checked sample are 2,000 × 1,958-pixel previews, and no original scan was found. The 24 samples are not a verified count of independent untreated patients."),
    "kirc-egad00001008781": dict(
        label="EGAD00001008781, ccRCC Visium", citation=archive("Understanding multicellular dynamics of ccRCC", "European Genome-phenome Archive", "https://ega-archive.org/datasets/EGAD00001008781"),
        assays=["whole-transcriptome"], techniques=["Visium"], preservation=[], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["controlled", "he-not-located", "identity"], access="controlled", accession="EGAD00001008781 (EGAS00001006045)",
        reported=[("sections_reported", "sections", "EGA dataset description")],
        description="Controlled EGA Visium dataset reporting 16 ccRCC sections, covering tumour core and the tumour–normal interface. No access has been requested; the donor crosswalk and image package are not established."),
    "kirc-treated-gse294006": dict(
        label="GSE294006, treated advanced ccRCC", citation=archive("Treatment-induced hypoxia and resistance in advanced ccRCC", "NCBI GEO", "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294006"),
        assays=["whole-transcriptome"], techniques=["Visium FFPE"], preservation=["FFPE"], compartments=["primary-tumour"], treatment="treated",
        linkage="listed-together", gates=["treated", "he-unverified"], access="open", accession="GSE294006",
        reported=[("spatial_samples", "primary-tumour samples after systemic treatment", "GEO series"), ("donor_labels", "donor labels", "GEO series")],
        description="Three primary ccRCC tumours resected after systemic treatment, two of them sarcomatoid, profiled with Visium FFPE. The study concerns advanced disease, but all three samples are primary tumours. Kept outside the untreated reference as an exploratory treated comparison; original-resolution images are still to be checked."),
    "kirc-10x-xenium-protein": dict(
        label="10x Genomics ccRCC, Xenium RNA and protein", citation=vendor("FFPE human renal ccRCC, Xenium gene and protein", "https://www.10xgenomics.com/datasets/xenium-protein-ffpe-human-renal-ccrcc"),
        assays=["rna-protein"], techniques=["Xenium"], preservation=["FFPE"], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["platform", "he-unverified", "treatment-review"], access="open", accession="10x Genomics dataset",
        reported=[("samples", "sample (vendor specimen)", "vendor dataset page")], modalities=["spatial-rna", "spatial-protein"],
        description="Vendor FFPE ccRCC dataset with targeted Xenium RNA (377-gene base panel plus custom genes) and a 27-plex protein panel. Targeted RNA and protein measurements are kept separate from whole-transcriptome resources; H&E availability and alignment were not checked."),
    "kirp-10x-xenium-preview": dict(
        label="10x Genomics kidney preview, Xenium (papillary RCC)", citation=vendor("Human kidney preview data, Xenium multi-tissue and cancer panel", "https://www.10xgenomics.com/datasets/human-kidney-preview-data-xenium-human-multi-tissue-and-cancer-panel-1-standard"),
        assays=["targeted-rna"], techniques=["Xenium"], preservation=[], compartments=["tumour-unspecified", "normal"], treatment="unknown",
        linkage="listed-together", gates=["platform", "he-unverified", "treatment-review"], access="open", accession="10x Genomics dataset",
        reported=[("tumour_samples", "papillary RCC sample", "vendor dataset page"), ("non_diseased_samples", "non-diseased kidney sample", "vendor dataset page"),
                  ("study_donors", "donors in the dataset", "vendor dataset page")],
        description="Vendor Xenium preview with one papillary RCC block and one non-diseased kidney block from two donors, measured with a preliminary 377-gene targeted panel. Post-assay H&E and alignment are described by the source but were not checked here. It is one tumour specimen, not two tumour donors, and no whole-transcriptome papillary RCC package was verified in this review."),
    "kirp-macrophage-abstract": dict(
        label="Soupir et al. 2024, abstract",
        citation=cite("Soupir A, et al.", "Spatial Clustering of Immunosuppressive Macrophages in Papillary Renal Cell Carcinoma", "The Oncologist", 2024, "10.1093/oncolo/oyae181.034"),
        assays=["targeted-rna", "protein-imaging"], techniques=["Multiplex immunofluorescence", "Targeted spatial RNA (960 transcripts)"], preservation=[],
        compartments=["tumour-unspecified"], treatment="unknown", linkage="unverified", gates=["release-unresolved", "platform"], access="unresolved", accession=None,
        reported=[("prcc_mif_patients", "papillary RCC patients, multiplex IF (not a spatial RNA count)", "conference abstract"),
                  ("ccrcc_mif_patients", "clear-cell RCC patients, multiplex IF", "conference abstract")], modalities=["spatial-rna", "spatial-protein"],
        description="Conference abstract on immunosuppressive macrophages in papillary RCC using multiplex immunofluorescence and a 960-transcript targeted spatial RNA assay. Its 16 papillary RCC patients (and 70 clear-cell RCC patients) are the multiplex-IF cohorts, not a spatial RNA sample count. No deposited package was found."),
    "lusc-10x-cytassist": dict(
        label="10x Genomics lung SCC, Visium CytAssist FFPE", citation=vendor("Human lung cancer FFPE, squamous cell carcinoma (Visium CytAssist)", "https://www.10xgenomics.com/datasets/human-lung-cancer-ffpe-2-standard"),
        assays=["whole-transcriptome"], techniques=["Visium CytAssist"], preservation=["FFPE"], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="listed-together", gates=["he-unverified", "identity", "treatment-review"], access="open", accession="10x Genomics dataset; slide V42A20-354 D1",
        reported=[("samples", "sample (vendor specimen)", "vendor dataset page")],
        description="Vendor Visium CytAssist FFPE demonstration of one lung squamous cell carcinoma specimen (slide V42A20-354, area D1). The source describes a 20x Olympus VS200 microscope H&E, distinct from the CytAssist instrument image; its listed size of 35,637 × 29,395 pixels and the transform were not checked here."),
    "lusc-emtab13530": dict(
        cancers_add=["LUSC"], assays=["whole-transcriptome"], techniques=[], preservation=[], compartments=["solid-normal", "normal"],
        treatment="unknown", gates=["identity", "treatment-review"], access=None,
        reported=[("lusc_donors", "LUSC donors (Patients 11 and 19)", "SDRF, deduplicated", "LUSC"),
                  ("lusc_tumour_sections", "LUSC tumour sections", "SDRF, deduplicated", "LUSC"),
                  ("lusc_adjacent_sections", "LUSC adjacent-normal sections", "SDRF, deduplicated", "LUSC"),
                  ("study_sections", "sections in the complete study, all histologies", "SDRF, deduplicated"),
                  ("study_tumour_sections", "tumour sections in the complete study", "SDRF, deduplicated")],
        description="Visium fresh-frozen atlas of non-small cell lung cancer with 40 sections in all, 20 of them tumour sections, across adenocarcinoma, squamous, unspecified NSCLC and healthy donors. The LUSC subset is Patients 11 and 19: six tumour sections and four adjacent-normal sections. Several staging values in the deposited metadata are inconsistent and should be taken from the publication's clinical table."),
    "pcpg-ling-ssrn": dict(
        label="Ling et al., SSRN manuscript", citation=archive("Ling et al. integrated single-cell and spatial PCC profiling", "SSRN", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5035122"),
        assays=["unverified"], techniques=["Spatial transcriptomics (platform unverified)"], preservation=[], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["release-unresolved", "package-unverified"], access="unresolved", accession=None, reported=[],
        description="Author manuscript on SSRN describing integrated single-cell and spatial profiling of pheochromocytoma. The spatial platform, sample count and data release were not verified, and an SSRN 'review complete' label does not establish peer review or release."),
    "pcpg-developmental-preprint": dict(
        label="Zhu et al. 2026, preprint",
        citation=cite("Zhu J, et al.", "Spatially organized developmental cell states link paraganglioma and neuroblastoma through chromaffin-neuroblast plasticity", "bioRxiv (preprint)", 2026, "10.64898/2026.04.07.715303"),
        assays=["unverified"], techniques=["Spatial transcriptomics (human assay details unverified)"], preservation=[], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="unverified", gates=["release-unresolved", "package-unverified"], access="unresolved", accession=None, reported=[],
        notes_extra=["An earlier version of the preprint was titled 'Sympathoadrenal lineage plasticity following KIF1Bβ-NF1 loss'."],
        description="Preprint on spatially organised developmental cell states linking paraganglioma and neuroblastoma. Human PCC/PGL samples must be separated from neuroblastoma, composite tumours and mouse models. The full text and data accession were not available, so no sample count or platform is assigned."),
    "prad-10x-acinar": dict(
        label="10x Genomics prostate acinar carcinoma, Visium FFPE", citation=vendor("Human prostate cancer, acinar cell carcinoma (FFPE)", "https://www.10xgenomics.com/datasets/human-prostate-cancer-acinar-cell-carcinoma-ffpe-1-standard"),
        assays=["whole-transcriptome"], techniques=["Visium FFPE"], preservation=["FFPE"], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="listed-together", gates=["he-unverified", "identity", "treatment-review"], access="open", accession="10x Genomics dataset; block 1D1061-Tp11",
        reported=[("samples", "sample (vendor specimen)", "vendor dataset page")],
        description="Vendor Visium FFPE demonstration of one prostate acinar adenocarcinoma specimen (block 1D1061-Tp11), with Gleason score 7 and stage IV as reported by the vendor. A 20x Metafer H&E is source-described; the full image and registration were not checked, and prior hormonal or systemic therapy is unknown."),
    "prad-10x-invasive": dict(
        label="10x Genomics prostate invasive adenocarcinoma, Visium FFPE", citation=vendor("Human prostate cancer, adenocarcinoma with invasive carcinoma (FFPE)", "https://www.10xgenomics.com/datasets/human-prostate-cancer-adenocarcinoma-with-invasive-carcinoma-ffpe-1-standard-1-3-0"),
        assays=["whole-transcriptome"], techniques=["Visium FFPE"], preservation=["FFPE"], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="listed-together", gates=["he-unverified", "identity", "treatment-review"], access="open", accession="10x Genomics dataset; block 1E500_Tp12",
        reported=[("samples", "sample (vendor specimen)", "vendor dataset page")],
        description="Vendor Visium FFPE demonstration of one prostate adenocarcinoma with invasive carcinoma (block 1E500_Tp12), with Gleason score 7 and stage III as reported by the vendor. The two vendor prostate pages are not assumed to come from distinct patients. A 20x Metafer H&E is source-described; the full image, registration and treatment history were not checked."),
    "prad-hirz-slideseq": dict(
        label="Hirz et al. 2023",
        citation=cite("Hirz T, et al.", "Dissecting the immune suppressive human prostate tumor microenvironment via integrated single-cell and spatial transcriptomic analyses", "Nature Communications", 2023, "10.1038/s41467-023-36325-2"),
        assays=["whole-transcriptome"], techniques=["Slide-seqV2"], preservation=[], compartments=["primary-tumour", "normal"], treatment="reported-untreated",
        linkage="serial-section", gates=["serial-section", "he-unverified", "identity"], access="open", accession="Zenodo 7526696",
        reported=[("tumour_donors", "prostate cancer donors", "publication"), ("non_prostate_cancer_controls", "control donors without prostate cancer", "publication"),
                  ("spatial_donors", "spatial donors in all", "publication"), ("spatial_arrays", "Slide-seqV2 arrays", "publication")],
        description="Slide-seqV2 profiling within a study of the prostate tumour microenvironment: 12 arrays from four donors, two with prostate cancer from a treatment-naive prostatectomy cohort and two controls without prostate cancer. H&E comes from consecutive sections, not the assayed ones. The study's 19 cancer patients are single-cell RNA-seq donors, not spatial patients. Spatial data are in a Zenodo archive; GEO GSE181294 holds mainly single-cell data."),
    "prad-erickson-clonal": dict(
        label="Erickson et al. 2022",
        citation=cite("Erickson A, et al.", "Spatially resolved clonal copy number alterations in benign and malignant tissue", "Nature", 2022, "10.1038/s41586-022-05023-2"),
        assays=["whole-transcriptome"], techniques=["Spatial Transcriptomics (legacy arrays)"], preservation=[], compartments=["tumour-unspecified", "normal"],
        treatment="unknown", linkage="unverified", gates=["platform", "package-unverified", "identity"], access="open", accession="Mendeley Data svw96g68dv (version 5)", reported=[],
        description="Legacy Spatial Transcriptomics study mapping clonal copy-number alterations across benign and malignant prostate tissue. A Mendeley release with processed data and images is listed, but its files were not audited. Benign fields and multiple regions from one patient must not be counted as separate patients."),
    "stad-gse251950": dict(
        label="Lee et al. 2024",
        citation=cite("Lee SH, et al.", "Spatial dissection of tumour microenvironments in gastric cancers reveals the immunosuppressive crosstalk between CCL2+ fibroblasts and STAT3-activated macrophages", "Gut", 2024, "10.1136/gutjnl-2024-332901"),
        assays=["whole-transcriptome"], techniques=["Visium"], preservation=[], compartments=["primary-tumour", "metastatic-tumour"], treatment="unknown",
        linkage="listed-together", gates=["he-unverified", "identity", "treatment-review"], access="open", accession="GSE251950",
        reported=[("donor_labels", "donor labels", "GEO series"), ("primary_sections", "primary-tumour sections", "GEO series"),
                  ("metastatic_sections", "metastasis section (GC6-PM, same donor as GC6)", "GEO series"), ("spatial_samples", "spatial samples in all", "GEO series")],
        description="Visium sections from nine gastric cancer donor labels: nine primary tumours and one metastasis (GC6-PM, from the same donor as GC6), kept separate. Space Ranger archives include H&E previews; the original scans were not verified."),
    "stad-gse270678": dict(
        label="Gao et al. 2026",
        citation=cite("Gao S, et al.", "A spatially resolved atlas of gastric cancer characterises a lymphocyte-aggregated region", "Nature Communications", 2026, "10.1038/s41467-026-68612-z"),
        assays=["whole-transcriptome"], techniques=["Visium"], preservation=[], compartments=["primary-tumour"], treatment="reported-untreated",
        linkage="listed-together", gates=["count-reconciliation", "he-unverified", "identity"], access="open", accession="GSE270678; HRA007814 (raw, controlled)",
        reported=[("spatial_samples", "deposited sections", "GEO series"), ("donor_labels_in_deposit", "donor labels in the deposit", "GEO series"),
                  ("main_study_tumour_samples_reported", "main tumour samples in the series summary", "GEO series summary"),
                  ("main_sections_reported", "main sections", "study description"), ("additional_replicates_reported", "additional replicate sections", "study description")],
        description="Visium atlas of lymphocyte-aggregated regions in gastric cancer: 72 sections from 20 donor labels in the deposit, whereas the series summary describes 19 main tumour samples (33 main sections and 39 additional replicates). The discrepancy is unresolved. The paper reports treatment-naive surgical donors; histology (intestinal, diffuse, indeterminate) and core, edge and in-between regions are annotated. The representative deposited H&E is a 1,943 × 2,000-pixel preview."),
    "ucec-barkley-gse203612": dict(
        label="Barkley et al. 2022, UCEC sample",
        citation=cite("Barkley D, et al.", "Cancer cell states recur across tumor types and form specific interactions with the tumor microenvironment", "Nature Genetics", 2022, "10.1038/s41588-022-01141-9"),
        assays=["whole-transcriptome"], techniques=["Visium"], preservation=[], compartments=["tumour-unspecified"], treatment="unknown",
        linkage="listed-together", gates=["he-unverified", "treatment-review", "pathology-review"], access="open", accession="GSE203612 (UCEC spatial sample GSM6177623)",
        reported=[("ucec_spatial_samples", "endometrial carcinoma spatial sample (GSM6177623)", "GEO series")],
        description="One endometrial carcinoma Visium sample (GSM6177623, NYU_UCEC3_Vis) from a pan-cancer cell-state atlas; single-cell samples and other cancers in the series are not part of this entry. Its deposited images are 1,899 × 2,000-pixel previews, and the original scan, histological subtype and treatment history are unknown."),
    "ucec-np137-gse225690": dict(
        label="Cassier et al. 2023, NP137 trial",
        citation=cite("Cassier PA, et al.", "Netrin-1 blockade inhibits tumour growth and EMT features in endometrial cancer", "Nature", 2023, "10.1038/s41586-023-06367-z"),
        assays=["whole-transcriptome"], techniques=["Visium FFPE"], preservation=["FFPE"], compartments=["metastatic-tumour"], treatment="baseline-and-on-treatment",
        linkage="unverified", gates=["treated", "count-reconciliation", "he-unverified"], access="open", accession="GSE225690",
        reported=[("deposited_captures", "metastasis biopsy sections profiled", "GEO series"), ("deposited_donor_labels", "donor labels (01-034 and 01-039)", "GEO series"),
                  ("timepoints_per_donor", "timepoints per donor (baseline and after one month)", "GEO series"),
                  ("series_summary_patients", "patient in the series summary", "GEO series summary")],
        description="Visium FFPE profiles of endometrial cancer metastasis biopsies from the NP137 netrin-1 blockade trial: four biopsy sections from two donor labels (01-034 and 01-039), each at baseline and after one month of treatment, although the series summary describes one patient. Baseline does not establish the absence of earlier anticancer treatment. An exploratory treated, metastatic comparison, not an untreated primary reference."),
    "glioma-greenwald-gse237183": dict(
        cancers_add=["GBM"], assays=["whole-transcriptome"], techniques=[], preservation=[], compartments=[], treatment="unknown",
        gates=["he-unverified", "identity", "treatment-review"], gates_remove=["he-not-located"], access=None,
        reported=[("idh_wt_gbm_sections", "IDH-wildtype glioblastoma sections", "GEO series", "GBM"), ("idh_wt_donor_labels", "IDH-wildtype donor labels", "GEO series", "GBM"),
                  ("idh_mutant_sections", "IDH-mutant glioma sections", "GEO series", "LGG"), ("idh_mutant_donor_labels", "IDH-mutant donor labels", "GEO series", "LGG"),
                  ("study_sections", "sections in the study", "GEO series")],
        description="Visium study of glioma organisation with 19 sections: 13 IDH-wildtype glioblastoma sections from five donor labels and six IDH-mutant sections (astrocytoma and oligodendroglioma) from six donor labels. Repeated regions of one donor (ZH881) are one donor label, not separate patients. Besides the GEO previews (about 2,000 pixels), Zenodo record 12624860 holds an H&E archive with 12 OME-TIFF entries; two checked headers are 20,780 × 17,696 and 10,414 × 10,839 pixels. Sample aliases (ZH811 in the archive versus ZH881 in the expression data), section coverage and transforms are unresolved."),
    "glioma-2026-niche-atlas": dict(
        cancers_add=["GBM"], assays=["whole-transcriptome", "targeted-rna"], techniques=["Visium", "Xenium"], preservation=["Fresh frozen"], compartments=[],
        treatment="unknown", gates=["identity", "treatment-review"], access=None, accession_add="Zenodo 17622242",
        reported=[("visium_sections_reported", "Visium sections of genotyped glioma (not GBM donors)", "publication"),
                  ("ffpe_sections_reported", "FFPE Visium sections", "publication"), ("frozen_sections_reported", "fresh-frozen Visium sections", "publication"),
                  ("xenium_patients_reported", "Xenium patients", "publication")],
        description="Glioblastoma anatomical-niche atlas reporting 32 Visium sections of genotyped glioma (27 FFPE, five fresh frozen) and Xenium data from four patients, released in Zenodo 17572905 (Visium) and 17622242 (Xenium) with a UCSC Cell Browser view. The 32 sections are not 32 GBM donors, and reused external datasets must be deduplicated. Zenodo 16505469 is not relabelled as the Ravi 2022 study until its provenance is resolved."),
}
LINK_LABELS = [("source_url", "Data record"), ("publication_url", "Publication"), ("image_source_url", "Image release"), ("spatial_archive", "Spatial archive"),
               ("archive", "Data archive"), ("image_archive", "H&E archive"), ("visium_archive", "Visium release"), ("xenium_archive", "Xenium release"),
               ("browser", "Cell browser")]
SAMPLE_FIELDS = ["sample_ids", "exclude_sample_ids", "normal_or_precursor_ids", "tumour_sample_ids", "adjacent_sample_ids", "metastatic_sample_ids"]
KEEP = ["specimen", "block", "slide", "panel", "reported_stage", "reported_gleason", "reused_in", "title_alias", "source_review_limit"]


def stop(msg):
    sys.exit(f"import stopped: {msg}")


def union(a, b):
    return list(dict.fromkeys([*(a or []), *(b or [])]))


def validate_evidence(src, recs):
    rows = json.load(open(src / "spatial_expansion_sample_files.json", encoding="utf-8"))
    per = {}
    for r in rows:
        per.setdefault(r["study"], set()).add(r["sample"])
    expect = {"GSE270678": recs["stad-gse270678"]["reported_counts"]["spatial_samples"], "GSE175540": recs["kirc-meylan-gse175540"]["reported_counts"]["spatial_samples"],
              "GSE237183": recs["glioma-greenwald-gse237183"]["reported_counts"]["study_sections"], "GSE251950": recs["stad-gse251950"]["reported_counts"]["spatial_samples"],
              "GSE225690": recs["ucec-np137-gse225690"]["reported_counts"]["deposited_captures"], "GSE294006": recs["kirc-treated-gse294006"]["reported_counts"]["spatial_samples"],
              "GSE203612": recs["ucec-barkley-gse203612"]["reported_counts"]["ucec_spatial_samples"]}
    if len(rows) != 133 or {k: len(v) for k, v in per.items()} != expect:
        stop(f"supporting GEO rows differ from the manifest units: {({k: len(v) for k, v in per.items()})}")
    for rid, series in (("ucec-np137-gse225690", "GSE225690"), ("kirc-treated-gse294006", "GSE294006"), ("ucec-barkley-gse203612", "GSE203612")):
        if set(recs[rid]["sample_ids"]) != per[series]:
            stop(f"{rid}: sample IDs differ from the GEO rows")
    if not set(recs["stad-gse251950"]["metastatic_sample_ids"]) <= per["GSE251950"]:
        stop("GSE251950: metastatic sample not among the GEO rows")
    sdrf = json.load(open(src / "EMTAB13530_unique_samples.json", encoding="utf-8"))
    lusc = [s for s in sdrf if s["Characteristics[disease]"] == "lung squamous cell carcinoma"]
    r = recs["lusc-emtab13530"]
    tum = sorted(s["Source Name"] for s in lusc if s["Characteristics[sampling site]"] == "tumor")
    adj = sorted(s["Source Name"] for s in lusc if s["Characteristics[sampling site]"] == "normal tissue adjacent to tumor")
    rc = r["reported_counts"]
    if (len(sdrf), sum(s["Characteristics[sampling site]"] == "tumor" for s in sdrf)) != (rc["study_sections"], rc["study_tumour_sections"]) \
            or sorted({s["Characteristics[individual]"] for s in lusc}) != ["Patient 11", "Patient 19"] \
            or tum != sorted(r["tumour_sample_ids"]) or adj != sorted(r["adjacent_sample_ids"]) \
            or (len({s["Characteristics[individual]"] for s in lusc}), len(tum), len(adj)) != (rc["lusc_donors"], rc["lusc_tumour_sections"], rc["lusc_adjacent_sections"]):
        stop("E-MTAB-13530: LUSC selection differs from the deduplicated SDRF")
    zipdir = json.load(open(src / "greenwald_HE_zip_manifest.json", encoding="utf-8"))
    if sum(x["name"].endswith("_HE.ome.tif") for x in zipdir) != 12:
        stop("Zenodo 12624860: expected 12 H&E OME-TIFF entries")
    dims = {(x["gsm"], tuple(x["dimensions"])) for x in json.load(open(src / "image_header_checks.json", encoding="utf-8")) if x.get("dimensions")}
    for gsm, wh in (("GSM6177623", (1899, 2000)), ("GSM5924030", (2000, 1958)), ("GSM7596587", (1799, 2000)), ("GSM8349861", (1943, 2000))):
        if (gsm, wh) not in dims:
            stop(f"image header check for {gsm} does not show {wh}")
    overlap = {x["resource_id"]: x["possible_existing_cohort_ids"] for x in json.load(open(src / "existing_catalogue_overlap.json", encoding="utf-8"))}
    if {k: v[0] for k, v in overlap.items() if v} != EXISTING or set(overlap) != set(recs):
        stop("existing-catalogue overlap differs from the three expected enrichments")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    m = json.load(open(src / "spatial_expansion_public_manifest.json", encoding="utf-8"))
    pol = m["policy"]
    if m["schema_version"] != 1 or not (pol["existing_tcga_panel_unchanged"] and pol["existing_spatial_captures_unchanged"]
                                        and pol["no_strict_core_promotion"] and pol["no_cross_study_donor_sum"]):
        stop("unexpected manifest version or policy")
    recs = {r["id"]: r for r in m["records"]}
    if len(recs) != 26 or len(m["records"]) != 26 or set(recs) != set(D) or {r["analysis_cohort"] for r in recs.values()} != GROUPS or set(m["scope"]) != GROUPS:
        stop("manifest records or tumour groups differ from the reviewed set")
    for r in recs.values():
        if r["strict_core_promoted"] or r["strict_core_eligible_patients"] is not None or r["review_date"] != REVIEW_DATE:
            stop(f"{r['id']}: strict-core promotion or eligible count present")
        if r.get("existing_catalogue_id", EXISTING.get(r["id"])) != EXISTING.get(r["id"]):
            stop(f"{r['id']}: existing catalogue ID differs")
        used = [k for k, *_ in D[r["id"]]["reported"]]
        nonnull = [k for k, v in r["reported_counts"].items() if v is not None]
        if sorted(used) != sorted(nonnull) or len(set(used)) != len(used):
            stop(f"{r['id']}: reported units {used} do not cover the manifest counts {nonnull} exactly once")
    validate_evidence(src, recs)

    cohorts = json.load(open(DATA / "cohorts.json", encoding="utf-8"))
    by_id = {c["id"]: c for c in cohorts}
    cancers = {c["code"] for c in json.load(open(DATA / "cancers.json", encoding="utf-8"))}

    def review_block(r, d):
        out = {"id": r["id"], "date": REVIEW_DATE, "analysis_cohort": r["analysis_cohort"], "assay_classes": d["assays"],
               "platform": r["platform"], "role": r.get("role", "candidate resource"), "image_status": r["image_status"],
               "treatment_status": r["treatment_status"], "treatment_class": d["treatment"], "eligible_patients": None,
               "strict_core_promoted": False, "sample_ids": {k: r[k] for k in SAMPLE_FIELDS if r.get(k)}}
        out.update({k: r[k] for k in KEEP if r.get(k) is not None})
        return out

    def reported(r, d):
        return [[r["reported_counts"][k], unit, basis] + ([scope[0]] if scope else []) for k, unit, basis, *scope in d["reported"]]

    def source_label(url):
        for host, label in (("ncbi.nlm.nih.gov/geo", "GEO series"), ("biostudies", "ArrayExpress"), ("ega-archive", "EGA dataset"),
                            ("ngdc.cncb.ac.cn/gsa", "GSA-Human"), ("10xgenomics.com", "Vendor dataset"), ("ssrn.com", "SSRN manuscript"),
                            ("doi.org", "Publication"), ("pmc.ncbi", "Publication")):
            if host in url:
                return label
        return "Data record"

    def links(r):
        def label_of(k, default):
            if k == "source_url":
                return source_label(r[k])
            return "Full text (PMC)" if k == "publication_url" and "pmc.ncbi" in r[k] else default
        return [[label_of(k, label), r[k]] for k, label in LINK_LABELS if r.get(k)]

    built = []
    for r in m["records"]:
        d = D[r["id"]]
        notes = r["open_checks"] + d.get("notes_extra", []) + ([f"Also redistributed through {', '.join(r['reused_in'])}; not a separate cohort."] if r.get("reused_in") else []) \
            + ([f"Review limit: {r['source_review_limit']}."] if r.get("source_review_limit") else [])
        if r["id"] in EXISTING:
            c = by_id.get(EXISTING[r["id"]])
            if not c:
                stop(f"existing record {EXISTING[r['id']]} not found")
            c["cancers"] = union(c["cancers"], d["cancers_add"])
            c["techniques"] = union(c.get("techniques"), d["techniques"])
            c["preservation"] = union(c.get("preservation"), d["preservation"])
            c["compartments"] = union(c.get("compartments"), d["compartments"])
            c["gates"] = union([g for g in c.get("gates", []) if g not in d.get("gates_remove", [])], d["gates"])
            if d.get("accession_add") and d["accession_add"] not in (c.get("accession") or ""):
                c["accession"] = f"{c['accession']}; {d['accession_add']}" if c.get("accession") else d["accession_add"]
            have = {u for _, u in c["access"].get("links", [])}
            doi = ((c.get("citation") or {}).get("doi") or "").lower()
            c["access"]["links"] = c["access"].get("links", []) + [[lbl, u] for lbl, u in links(r)
                                                                    if u not in have and not (doi and doi in u.lower())]
            if not c["access"].get("route"):
                c["access"]["route"] = r["access"]
            if not c.get("description"):
                c["description"] = d["description"]
            c["reported"] = reported(r, d)
            c["notes"] = union(c.get("notes"), notes)
            c["verification"], c["verified_on"] = "metadata-checked", REVIEW_DATE
            c["spatial_review"] = review_block(r, d)
            continue
        cid = r["id"]
        if cid in by_id and "spatial_review" not in by_id[cid]:
            stop(f"{cid}: an unrelated catalogue entry already uses this ID")
        cit = d["citation"]
        entry = {
            "id": cid, "label": d["label"], "title": cit["title"] if cit else r["title"],
            "citation": cit, "cancers": PAGE_OF[r["analysis_cohort"]], "layer": "matched-spatial", "status": "candidate",
            "modalities": d.get("modalities", ["spatial-rna"]), "techniques": d["techniques"], "preservation": d["preservation"],
            "specimen": "clinical-tumour", "linkage": d["linkage"], "gates": d["gates"], "accession": d["accession"],
            "access": {"category": d["access"], "route": r["access"], "links": links(r)},
            "verification": "metadata-checked", "verified_on": REVIEW_DATE, "description": d["description"],
            "compartments": d["compartments"], "reported": reported(r, d), "notes": notes, "spatial_review": review_block(r, d),
        }
        if d["access"] not in ACCESS or any(x not in cancers for x in entry["cancers"]):
            stop(f"{cid}: invalid access category or cancer code")
        built.append(entry)

    # Deduplicate by accession and DOI against every other catalogue entry.
    def keys(c):
        text = " ".join([c.get("accession") or ""] + [u for _, u in c["access"].get("links", [])])
        out = {k.upper() for k in re.findall(r"\b(GSE\d+|E-MTAB-\d+|EGA[DS]\d+|HRA\d+|OMIX\d+|CNP\d+|PRJNA\d+)\b", text)}
        out |= {f"ZENODO:{z}" for z in re.findall(r"zenodo(?:\.org/records/|\s+)(\d+)", text, re.I)}
        out |= {f"10X:{v}" for v in re.findall(r"10xgenomics\.com/datasets/([\w-]+)", text)}
        if (c.get("citation") or {}).get("doi"):
            out.add(c["citation"]["doi"].lower())
        return out
    others = [c for c in cohorts if "spatial_review" not in c and c["id"] not in EXISTING.values()]
    seen = {}
    for c in others:
        for k in keys(c):
            seen.setdefault(k, c["id"])
    for c in built + [by_id[x] for x in EXISTING.values()]:
        for k in keys(c):
            if k in seen and seen[k] != c["id"]:
                stop(f"{c['id']}: {k} already catalogued as {seen[k]}")
            seen[k] = c["id"]

    # Replace earlier imports in place; append new entries after the last spatial resource.
    kept = [c for c in cohorts if not ("spatial_review" in c and c["id"] not in EXISTING.values())]
    last = max(i for i, c in enumerate(kept) if c["layer"] == "matched-spatial")
    out = kept[:last + 1] + built + kept[last + 1:]
    with open(DATA / "cohorts.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"spatial review: {len(built)} new and {len(EXISTING)} enriched entries ({len(recs)} records, "
          f"{len({r['analysis_cohort'] for r in recs.values()})} tumour groups); cohorts.json now {len(out)} entries")


if __name__ == "__main__":
    main()
