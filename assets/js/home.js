import { loadData, fmt, esc, LABELS, setFooter, showError, spatialResourcesFor, cohortScopeText } from "./common.js";

const LAYER_TEXT = {
  "matched-spatial": ["H&E images, original scans or previews, with measured spatial RNA and coordinates from the same tissue", "Locating molecular programmes and cell states in tissue; relating them to morphology"],
  "wsi-bulk": ["Whole-slide images, bulk RNA-seq and 450k methylation from the same patients, with normal tissue from some", "Tumour-level molecular variation, classification and morphology–molecular modelling; normal-tissue reference"],
  "bulk-rna": ["Published bulk RNA without matched slides", "Molecular references, signatures and classifiers"],
  "single-cell": ["Single-cell or single-nucleus RNA", "Cell-state interpretation, composition and deconvolution references"],
  "image-only": ["Histology images without matched RNA", "Morphology replication; marker-based comparisons"],
};

try {
  const d = await loadData();
  setFooter(d);
  const ep = d.elig.panel, m = d.elig.meta;
  const spatial = d.cohorts.filter(c => c.layer === "matched-spatial");
  const located = spatial.filter(c => c.status === "verified").length, preview = spatial.filter(c => c.status === "preview").length;
  const pages = d.cancers.filter(c => c.group !== "aggregate" && c.group !== "excluded").length;
  const row = (value, label, href) => `<div><dt>${value}</dt><dd><a href="${href}">${label}</a></dd></div>`;
  document.getElementById("glance").innerHTML = [
    row(fmt(ep.selected_analysis.total), "TCGA patients in the selected analysis panel", "tcga.html#panel"),
    row(fmt(ep.selected_analysis.paired), "of them with both RNA-seq and DNA methylation", "tcga.html#panel"),
    row(fmt(ep.normal.rna_he_after), "TCGA patients with normal tissue profiled by RNA-seq and imaged", "tcga.html#panel"),
    row(fmt(spatial.length), "spatial omics resources catalogued", "spatial.html"),
    row(fmt(located), "of them with the original H&E and matched molecular data located", "spatial.html#by-cancer"),
    row(fmt(preview), "more with matched molecular data and a preview image only", "spatial.html#levels"),
    row(fmt(pages), "cancer types, each with its own page", "cancers.html"),
  ].join("");
  document.getElementById("route-tcga").textContent = `${m.analysis_cohorts} analysis cohorts · ${fmt(ep.selected_analysis.total)} patients`;
  document.getElementById("route-spatial").textContent = `${fmt(spatial.length)} spatial resources · ${fmt(located)} with original H&E · ${fmt(preview)} with a preview image`;

  const layers = Object.keys(LABELS.layer).filter(l => d.cohorts.some(c => c.layer === l));
  document.getElementById("layers").innerHTML = layers.map(l => {
    const n = d.cohorts.filter(c => c.layer === l).length;
    const [what, use] = LAYER_TEXT[l];
    return `<tr><td class="primary" data-label="Layer"><div><a href="explore.html?view=cohorts&layer=${l}">${esc(LABELS.layer[l])}</a></div></td>
      <td data-label="Contains"><div>${esc(what)}</div></td><td data-label="Use"><div>${esc(use)}</div></td><td class="num" data-label="Entries"><div>${n}</div></td></tr>`;
  }).join("");

  const grid = document.getElementById("cancer-grid");
  grid.innerHTML = d.cancers.filter(c => c.group !== "aggregate" && c.group !== "excluded").map(c => {
    const proj = c.tcga_project;
    const e = proj && d.elig.projects[proj];
    const pool = c.tcga_projects ? d.elig.cohorts[c.code] : e && d.elig.cohorts[e.analysis_cohort].projects.length > 1 ? d.elig.cohorts[e.analysis_cohort] : null;
    const tcgaText = c.tcga_projects ? `TCGA: ${fmt(pool.selected_analysis.total)} patients in the selected panel (${c.tcga_projects.join(" + ")}${pool.role !== "discovery" ? ", benchmark" : ""})`
      : pool ? `TCGA: ${fmt(e.selected_analysis.total)} patients in the selected panel, within pooled ${e.analysis_cohort}`
      : e ? `TCGA: ${fmt(e.selected_analysis.total)} patients in the selected panel${cohortScopeText(e.analysis_cohort) ? `, ${cohortScopeText(e.analysis_cohort)}` : ""}` : "No TCGA cohort";
    const list = spatialResourcesFor(d, c), nLoc = list.filter(x => x.status === "verified").length, nPrev = list.filter(x => x.status === "preview").length;
    const spatialText = !list.length ? "Spatial: none catalogued yet"
      : `Spatial: ${fmt(list.length)} ${list.length === 1 ? "resource" : "resources"}, ${nLoc || nPrev ? [nLoc ? `${fmt(nLoc)} with original H&E` : "", nPrev ? `${fmt(nPrev)} with a preview image` : ""].filter(Boolean).join(", ") : "verification pending"}`;
    return `<a class="card" href="cancers.html?c=${c.code}">
      <span class="code">${c.code}</span><h3>${esc(c.name)}</h3>
      <span class="meta">${esc(tcgaText)}<br>${esc(spatialText)}</span></a>`;
  }).join("");
} catch (err) {
  showError(document.getElementById("cancer-grid"), err);
}
