import { loadData, LABELS, esc, chip, fmt, tally, setFooter, showCohort, showError, rationale, tcgaSection, loadTcgaReviews, analysisSection, pooledCohortSection, cohortExtras, tcgaOverview, spatialResourcesFor, spatialSentence, cohortScopeText, levelCounts } from "./common.js";

const root = document.getElementById("content");

const plural = (n, one, many) => `${fmt(n)} ${n === 1 ? one : many}`;
const ACCESS_DEPENDENT = new Set(["controlled", "request", "unreleased", "unresolved"]);
const codesOf = c => [c.code, ...(c.includes || [])];
const resourcesUrl = codes => `explore.html?view=cohorts&layer=matched-spatial&cancer=${codes.join(",")}`;
const located = list => list.filter(x => x.status === "verified").length;
const previewOnly = list => list.filter(x => x.status === "preview").length;
const LEVEL_CAPTION = "Original H&E located means the original scan, measured expression and coordinates were found. Matched data with preview image means the expression and coordinates match a preview image released with them, and the original scan was not located. Neither implies completed registration, calibration or tissue QC.";

// A count reported by the source: one scoped to this page, or the study total when the study spans several of the
// page's cancers (pooled pages); never one scoped to another cancer.
function reportedFor(c, codes) {
  const spans = c.cancers.filter(k => codes.includes(k)).length > 1;
  const r = (!spans && (c.reported || []).find(x => x[3] && codes.includes(x[3]))) || (c.reported || []).find(x => !x[3]);
  return r ? `${fmt(r[0])} ${r[1]}${!r[3] && c.cancers.some(k => !codes.includes(k)) ? " (all cancer sites)" : ""}` : "";
}

// Non-spatial resources, briefly; their details open in the resource dialog.
function cohortItem(d, c, codes) {
  const rep = reportedFor(c, codes);
  return `<div class="cohort-row">
    <button class="linkish" type="button" data-cohort="${esc(c.id)}">${esc(c.label)}</button>
    <div class="chips">${chip("status", c.status)}${chip("access", c.access.category)}</div>
    ${c.description ? `<div class="desc">${esc(c.description)}</div>` : ""}
    <div class="desc muted small">${esc([(c.techniques || []).join(", "), rep && `reported by the source: ${rep}`].filter(Boolean).join(" · "))}</div>
  </div>`;
}

// Tissue and linkage notes that change how a spatial resource can be used.
function notesFor(d, c, codes) {
  const out = [], comps = c.compartments || [];
  const caps = d.captures.filter(x => x.cohort === c.id && codes.includes(x.cancer));
  const tc = c.spatial_review && c.spatial_review.treatment_class;
  if (tc === "treated" || tc === "baseline-and-on-treatment" || caps.some(x => x.treatment === "Post-treatment")) out.push("includes treated tissue");
  if (comps.length && comps.every(x => x === "metastatic-tumour")) out.push("metastases only");
  else if (comps.includes("metastatic-tumour") || caps.some(x => x.site === "Metastasis")) out.push("includes metastases");
  if (comps.some(x => ["solid-normal", "normal", "peritumoral"].includes(x))) out.push("includes normal or adjacent tissue");
  if (comps.includes("precursor")) out.push("includes precursor lesions");
  if (c.linkage === "serial-section") out.push("H&E from serial sections");
  return out;
}

// One table of spatial resources for this page: study, assay, access, what the study reports and what is located.
function spatialTable(d, page, list) {
  if (!list.length) return "";
  const codes = codesOf(page);
  const rank = c => (c.status === "verified" ? 0 : c.status === "preview" ? 1 : ACCESS_DEPENDENT.has(c.access.category) ? 3 : 2);
  const rows = [...list].sort((a, b) => rank(a) - rank(b)).map(c => {
    const notes = notesFor(d, c, codes);
    const k = levelCounts(d, c, codes);
    const sec = n => plural(n, "section", "sections");
    const counts = [c.status === "verified" && k.original ? `${sec(k.original)} with original H&E` : "",
      k.preview ? `${sec(k.preview)} with a preview image${c.status === "verified" ? " only" : ""}${k.counted ? ", not listed one by one" : ""}` : "",
      k.patients ? plural(k.patients, "known patient", "known patients") : ""].filter(Boolean).join("; ");
    const rep = reportedFor(c, codes);
    return `<tr>
      <td class="primary" data-label="Study"><div><button class="linkish" type="button" data-cohort="${esc(c.id)}">${esc(c.label)}</button>${notes.length ? `<span class="cell-sub">${esc(notes.join("; "))}</span>` : ""}</div></td>
      <td data-label="Assay"><div>${esc((c.techniques || []).join(", ") || "Not specified")}</div></td>
      <td data-label="Access"><div>${chip("access", c.access.category)}</div></td>
      <td data-label="Reported by the study"><div>${rep ? esc(rep) : '<span class="muted">No count reported</span>'}</div></td>
      <td data-label="Image level"><div>${c.status === "verified" || c.status === "preview" ? `${chip("status", c.status)}${counts ? `<span class="cell-sub">${esc(counts)}</span>` : ""}` : '<span class="muted">Verification pending</span>'}</div></td>
    </tr>`;
  }).join("");
  return `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Study</th><th scope="col">Assay</th><th scope="col">Access</th><th scope="col">Reported by the study</th><th scope="col">Image level</th></tr></thead>
    <tbody>${rows}</tbody>
    <caption>Study-reported numbers keep each study's own unit and are not added together. ${LEVEL_CAPTION} Sections are records of each study, and known patients are study-local IDs given by the source; neither is an eligible-patient count. Select a study for its open checks, section linkage and treatment details.</caption>
  </table></div>`;
}

// Located data by histology stratum (or, on pooled pages, by stated site), in plain units.
function locatedBreakdown(d, page, caps) {
  if (!caps.length) return "";
  const groups = page.includes
    ? [...page.includes, page.code].map(k => ({ label: k === page.code ? (page.unstated_label || "Not stated") : d.cancerByCode.get(k).name, sel: x => x.cancer === k, q: `cancer=${k}` }))
    : [...page.strata.map(([id, label]) => ({ label, sel: x => x.stratum === id, q: `cancer=${page.code}&stratum=${id}` })),
       { label: "No stratum assigned", sel: x => !x.stratum, q: `cancer=${page.code}&stratum=none` }];
  const rows = groups.map(g => {
    const inG = caps.filter(g.sel);
    if (!inG.length && g.label === "No stratum assigned") return "";
    const primary = inG.filter(x => x.tier === "core"), other = inG.filter(x => x.tier !== "core");
    return `<tr><td class="primary" data-label="${page.includes ? "Stated site" : "Histology stratum"}"><div>${esc(g.label)}</div></td>
      <td class="num" data-label="Patients, primary tumour"><div>${fmt(tally(primary).patients)}</div></td>
      <td class="num" data-label="Sections, primary tumour"><div>${fmt(primary.length)}</div></td>
      <td class="num" data-label="Other sections, original H&amp;E"><div>${fmt(other.filter(x => x.image_level === "original").length)}</div></td>
      <td class="num" data-label="Other sections, preview image"><div>${fmt(other.filter(x => x.image_level === "preview").length)}</div></td>
      <td data-label="Explore"><div>${inG.length ? `<a href="explore.html?${g.q}">View ${inG.length}</a>` : '<span class="muted">—</span>'}</div></td></tr>`;
  }).join("");
  return `<details class="disclosure"><summary>Located data by ${page.includes ? "stated site" : "histology stratum"}</summary>
    <div class="table-wrap" style="margin-top:.5rem"><table class="stack compact">
    <thead><tr><th scope="col">${page.includes ? "Stated site" : "Histology stratum"}</th><th scope="col" class="num">Patients, primary tumour</th><th scope="col" class="num">Sections, primary tumour</th><th scope="col" class="num">Other sections, original H&amp;E</th><th scope="col" class="num">Other sections, preview image</th><th scope="col">Explore</th></tr></thead>
    <tbody>${rows}</tbody>
    <caption>Section records listed in this release. Primary tumour counts sections from primary tumours within the stratum, all with original H&amp;E located; other sections are metastatic, under review, held for quality control or outside the stratum, and are split by image level. Patients are known study-local IDs; sections without one are not counted as patients. Treatment before sampling is recorded per section in the data explorer.</caption>
  </table></div></details>`;
}

function renderCancer(d, code) {
  const c = d.cancerByCode.get(code);
  if (!c || c.group === "aggregate") return renderIndex(d, "That cancer type is not in the explorer.");
  const excluded = c.group === "excluded";
  document.title = `${c.name} · Tumour Histology and Multi-omics Explorer`;
  // A pooled page (CRC, GLIOMA) gathers the resources of its constituent cancers.
  const codes = codesOf(c);
  const caps = d.captures.filter(x => codes.includes(x.cancer));
  const evidence = d.evidence.filter(e => e.cancers.includes(code));
  const cohorts = d.cohorts.filter(x => x.cancers.some(k => codes.includes(k)));
  const spatial = spatialResourcesFor(d, c);
  const others = cohorts.filter(x => x.layer !== "matched-spatial");
  const pooledIn = c.analysis_cohort && c.analysis_cohort !== code && d.cancerByCode.get(c.analysis_cohort)?.group === "pooled" ? d.cancerByCode.get(c.analysis_cohort) : null;
  const why = rationale(c);
  const cohortRole = c.analysis_cohort && d.elig.cohorts[c.analysis_cohort] && d.elig.cohorts[c.analysis_cohort].role !== "discovery" ? d.elig.cohorts[c.analysis_cohort].role : null;
  const singleCohort = c.tcga_project && c.analysis_cohort && d.elig.cohorts[c.analysis_cohort] && d.elig.cohorts[c.analysis_cohort].projects.length === 1
    && !["ESCA", "PAAD"].includes(c.tcga_project) && (d.elig.cohorts[c.analysis_cohort].strata || d.elig.cohorts[c.analysis_cohort].subsets) ? d.elig.cohorts[c.analysis_cohort] : null;

  const evidenceHtml = evidence.length ? `<div class="evidence">${evidence.map(e => {
    let finding = e.finding;
    if (c.evidence_notes && c.evidence_notes[e.id]) finding = c.evidence_notes[e.id];
    else if (e.id === "hausser-2019") {
      finding = c.hausser === "significant"
        ? `${c.name} was one of six cancer types with significant within-type structure under the authors' strong criterion, and was included in the pooled six-cancer analysis. ${e.finding.split(". ").slice(2).join(". ")}`
        : c.hausser === "borderline"
          ? `${c.name} was described as borderline under the authors' significance criterion and was not part of the pooled analysis.`
          : `${c.name} was among the 15 cancer types screened, but no significant archetype geometry was detected in the RNA representation tested. This does not show that archetypes are absent under another representation, for example one combining RNA and methylation.`;
    }
    return `<article class="card">
      <h3>${esc(e.short)}</h3>
      <dl><dt>Scale</dt><dd>${esc(e.scale)}</dd><dt>Definition</dt><dd>${esc(e.definition)}</dd><dt>Finding</dt><dd>${esc(finding)}</dd><dt>Limits</dt><dd>${esc(e.limits)}</dd></dl>
      <p class="small muted" style="margin:.4rem 0 0">${esc(e.citation)} <a href="${esc(e.url)}" rel="noopener">doi:${esc(e.doi)}</a></p>
    </article>`;
  }).join("")}</div>`
    : `<p class="muted">No archetype analysis specific to this cancer type is catalogued. ${pooledIn ? `See <a href="cancers.html?c=${esc(pooledIn.code)}">${esc(pooledIn.name.toLowerCase())}</a> for the closest published evidence.` : ""}</p>`;

  const layers = Object.keys(LABELS.layer).filter(l => l !== "matched-spatial").map(l => {
    const inL = others.filter(x => x.layer === l);
    if (!inL.length) return "";
    return `<h3>${esc(LABELS.layer[l])}</h3><div class="cohort-list">${inL.map(x => cohortItem(d, x, codes)).join("")}</div>`;
  }).join("");

  // What is available, with links: TCGA, spatial studies and other resources.
  const e = c.tcga_project && d.elig.projects[c.tcga_project];
  const tcgaLine = c.tcga_projects ? `${plural(d.elig.cohorts[code].selected_analysis.total, "patient", "patients")} in the selected analysis panel`
    : !e ? "No TCGA project linked"
    : e.excluded_from_study ? "Excluded from the selected analysis panel"
    : d.elig.cohorts[e.analysis_cohort].projects.length > 1 ? `${plural(e.selected_analysis.total, "patient", "patients")} in the selected panel, within pooled ${e.analysis_cohort}`
    : `${plural(e.selected_analysis.total, "patient", "patients")} in the selected analysis panel${cohortScopeText(e.analysis_cohort) ? `: ${cohortScopeText(e.analysis_cohort)}` : ""}`;
  const browse = c.tcga_projects ? `explore.html?view=tcga&group=${code}` : c.tcga_project ? `explore.html?view=tcga&project=${c.tcga_project}` : null;
  const nLoc = located(spatial), nPrev = previewOnly(spatial);
  const available = `<section class="route-grid" aria-label="Data available">
    <div class="card"><h3>TCGA</h3><span class="figure-line">${esc(tcgaLine)}</span>
      <span class="small"><a href="#tcga">TCGA details</a>${browse ? ` · <a href="${browse}">Browse patients</a>` : ""}</span></div>
    <div class="card"><h3>Spatial studies</h3><span class="figure-line">${spatial.length ? `${plural(spatial.length, "resource", "resources")} catalogued` : "None catalogued yet"}</span>
      ${spatial.length ? `<span class="small muted">${nLoc || nPrev ? [nLoc ? `${fmt(nLoc)} with original H&amp;E located` : "", nPrev ? `${fmt(nPrev)} with matched data and a preview image` : ""].filter(Boolean).join("; ") : "Verification pending"}</span>` : ""}
      <span class="small">${spatial.length ? `<a href="#spatial">View resources</a>` : `<a href="spatial.html">All spatial studies</a>`}${caps.length ? ` · <a href="explore.html?cancer=${codes.join(",")}">Explore located data</a>` : ""}</span></div>
    <div class="card"><h3>Other resources</h3><span class="figure-line">${others.length ? `${plural(others.length, "resource", "resources")}` : "None catalogued"}</span>
      ${others.length ? `<span class="small muted">${esc([...new Set(others.map(x => LABELS.layer[x.layer]))].join("; "))}</span>` : ""}
      ${others.length ? `<span class="small"><a href="#resources">View resources</a></span>` : ""}</div>
  </section>`;

  const tcgaDetails = c.tcga_project ? `<details class="disclosure"><summary>Detailed TCGA counts: exclusions, single-assay patients, the patient screen and normal tissue</summary>${tcgaSection(d, c.tcga_project, { heading: false })}</details>`
    : c.tcga_projects ? `<details class="disclosure"><summary>Detailed counts for the pooled cohort: patient screen, subsets, annotations and normal tissue</summary>${pooledCohortSection(d, code)}</details>` : "";
  const histology = ["ESCA", "PAAD"].includes(c.tcga_project) ? `<details class="disclosure"><summary>Histology-defined analysis cohort: review, strata and flagged cases</summary><div id="analysis"><p class="muted">Loading histology review…</p></div></details>`
    : singleCohort ? `<details class="disclosure"><summary>Analysis cohort ${esc(c.analysis_cohort !== c.tcga_project ? `${c.analysis_cohort}: ${singleCohort.label}` : c.name)}: subsets, histology and annotations</summary>${cohortExtras(d, c.analysis_cohort)}</details>` : "";

  root.innerHTML = `
    <nav class="small muted" aria-label="Breadcrumb"><a href="cancers.html">Cancer types</a> › ${esc(code)}</nav>
    <div class="page-head">
      <div class="code">${esc(code)}</div>
      <h1>${esc(c.name)}</h1>
      <div class="chips" style="margin-bottom:1rem"><span class="chip ${excluded ? "eosin" : "accent"}">${esc(why)}</span>
        ${cohortRole ? `<span class="chip accent">${esc(LABELS.role[cohortRole])}</span>` : ""}</div>
      <p class="prose">${esc(c.summary)}</p>
      ${excluded ? `<p class="callout">This cancer type is not in the selected analysis panel, and no patient is selected from it. Its TCGA data are listed below for provenance and can still be used for other questions.</p>` : ""}
    </div>
    ${available}
    <nav class="page-nav" aria-label="On this page"><span class="page-nav-label">On this page</span><a href="#tcga">TCGA reference</a><a href="#spatial">Spatial studies</a><a href="#evidence">Selection history</a><a href="#resources">Other resources</a><a href="#gaps">Gaps and cautions</a></nav>

    <h2 id="tcga">TCGA reference</h2>
    ${tcgaOverview(d, c)}
    <p class="note">${browse ? `<a href="${browse}">Browse and export patients</a>` : ""}${pooledIn ? ` · <a href="cancers.html?c=${esc(pooledIn.code)}">Pooled ${esc(pooledIn.code)} cohort</a>` : ""}${(c.tcga_projects || (c.tcga_project ? [c.tcga_project] : [])).map(p => ` · <button class="linkish small" type="button" data-cohort="tcga-${p.toLowerCase()}">TCGA-${esc(p)} details and links</button>`).join("")} · <a href="methods.html#panel">Panel versus availability</a></p>
    ${tcgaDetails}
    ${histology}

    <h2 id="spatial">Spatial studies</h2>
    <p>${esc(spatialSentence(spatial.length, nLoc, nPrev))}${spatial.length ? ` These studies usually involve patients other than those in TCGA.` : ""}</p>
    ${spatialTable(d, c, spatial)}
    ${locatedBreakdown(d, c, caps)}
    <p class="note">${spatial.length ? `<a href="${resourcesUrl(codes)}">List these resources in the data explorer</a>` : `<a href="spatial.html">All spatial studies</a>`}${caps.length ? ` · <a href="explore.html?cancer=${codes.join(",")}">Explore located data, with histology, site and treatment filters</a>` : ""}</p>

    <h2 id="evidence">Selection history: published archetype evidence</h2>
    <p class="muted small">Archetype analysis is one use of these data, and the published evidence below is part of how the current panel was chosen. <a href="applications.html#archetypes">About archetype analysis</a>.</p>
    ${evidenceHtml}

    <h2 id="resources">Other resources</h2>
    ${layers || '<p class="muted">No other resources are catalogued yet.</p>'}

    <h2 id="gaps">Gaps and cautions</h2>
    <ul class="notes prose">${(c.gaps || []).map(g => `<li>${esc(g)}</li>`).join("")}</ul>
  `;
  root.querySelectorAll("[data-cohort]").forEach(b => b.addEventListener("click", () => showCohort(d, b.dataset.cohort)));
  const an = document.getElementById("analysis");
  if (an) loadTcgaReviews().then(rv => { an.innerHTML = analysisSection(d, rv, c.tcga_project); }).catch(err => showError(an, err));
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
}

function renderIndex(d, message) {
  document.title = "Cancer types · Tumour Histology and Multi-omics Explorer";
  const list = d.cancers.filter(c => c.group !== "aggregate" && c.group !== "excluded");
  const excludedList = d.cancers.filter(c => c.group === "excluded");
  const rows = list.map(c => {
    const codes = codesOf(c);
    const spatial = spatialResourcesFor(d, c), nLoc = located(spatial), nPrev = previewOnly(spatial);
    const e = c.tcga_project && d.elig.projects[c.tcga_project];
    const pooled = c.tcga_projects ? d.elig.cohorts[c.code] : null;
    const tcga = pooled ? `${fmt(pooled.selected_analysis.total)}<span class="cell-sub">pooled ${c.tcga_projects.map(p => `TCGA-${p}`).join(" + ")}${pooled.role !== "discovery" ? `; ${esc(LABELS.role[pooled.role].toLowerCase())}` : ""}</span>`
      : e ? `${fmt(e.selected_analysis.total)}${e.analysis_cohort !== c.tcga_project ? `<span class="cell-sub">${d.elig.cohorts[e.analysis_cohort].projects.length > 1 ? `contribution to ${esc(e.analysis_cohort)}` : esc(cohortScopeText(e.analysis_cohort))}</span>` : ""}`
      : '<span class="muted">No TCGA cohort</span>';
    return `<tr>
      <td class="primary" data-label="Cancer type"><div><a href="cancers.html?c=${c.code}">${esc(c.name)}</a> <span class="mono muted small">${c.code}</span></div></td>
      <td class="num" data-label="TCGA patients, selected panel"><div>${tcga}</div></td>
      <td class="num" data-label="Spatial resources"><div>${spatial.length ? `<a href="${resourcesUrl(codes)}">${fmt(spatial.length)}</a>` : '<span class="muted">None catalogued</span>'}</div></td>
      <td class="num" data-label="Original H&amp;E located"><div>${!spatial.length ? '<span class="muted">—</span>' : fmt(nLoc)}</div></td>
      <td class="num" data-label="Matched data with preview image"><div>${!spatial.length ? '<span class="muted">—</span>' : fmt(nPrev)}</div></td>
    </tr>`;
  }).join("");
  root.innerHTML = `
    ${message ? `<p class="callout">${message}</p>` : ""}
    <div class="page-head"><h1>Cancer types</h1>
    <p class="prose muted">Each page brings together the TCGA data and the spatial studies for one cancer type, with its selection history, other resources and open checks. The list follows the current analysis panel. Eight cancer types come from Hausser et al. (2019), and the other ten are included because their TCGA projects meet the RNA and 450k methylation screen. Colorectal cancer and diffuse glioma also have pooled pages; the glioma cohort is a classification benchmark.</p></div>
    <div class="table-wrap"><table class="stack">
      <thead><tr><th scope="col">Cancer type</th><th scope="col" class="num">TCGA patients, selected panel</th><th scope="col" class="num">Spatial resources</th><th scope="col" class="num">Original H&amp;E located</th><th scope="col" class="num">Matched data with preview image</th></tr></thead>
      <tbody>${rows}</tbody>
      <caption>TCGA counts are patients in the selected analysis panel with RNA-seq, methylation or both. The COAD, READ, LGG and GBM rows show their contributions to the pooled colorectal and glioma rows. Spatial counts are resources, not patients: each resource counts once, at its best image level, and the rest are not yet verified. Pooled pages reuse the resources of their constituent cancers, so the columns should not be summed. Neither level means that registration, calibration or tissue QC is complete.</caption>
    </table></div>`;
}

try {
  const d = await loadData();
  setFooter(d);
  const code = new URLSearchParams(location.search).get("c");
  code ? renderCancer(d, code.toUpperCase()) : renderIndex(d);
} catch (err) {
  showError(root, err);
}
