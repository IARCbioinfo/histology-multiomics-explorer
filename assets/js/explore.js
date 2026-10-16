import {
  loadData, LABELS, esc, chip, fmt, tally, cancerName, stratumLabel, setFooter,
  showCapture, showCohort, cohortCounts, showError, loadTcgaPatients, tcgaTally, showTcgaPatient, tcgaPasses, cohortName, countedPreview, geometryText,
} from "./common.js";

const PAGE = 60;

const CAPTURE_FACETS = [
  { key: "level", label: "Image level", get: c => [c.image_level] },
  { key: "cancer", label: "Cancer", get: c => [c.cancer] },
  { key: "stratum", label: "Histology stratum", get: c => [c.stratum ?? "none"] },
  { key: "site", label: "Primary or metastatic", get: c => [c.site] },
  { key: "treatment", label: "Treatment before sampling", get: c => [c.treatment] },
  { key: "tier", label: "Curation tier", get: c => [c.tier] },
  { key: "technique", label: "Technique", get: c => [c.technique] },
  { key: "preservation", label: "Preservation", get: c => [c.preservation ?? "Unknown"] },
  { key: "access", label: "H&E access", get: c => [c.access.he] },
  { key: "verification", label: "Verification", get: c => [c.verification] },
  { key: "pid", label: "Patient ID", get: c => [c.patient ? "known" : "unknown"] },
  { key: "area", label: "Array area", get: c => [c.assay_area_id ? "shared" : "own"] },
  { key: "cohort", label: "Cohort", get: c => [c.cohort] },
];

const COHORT_FACETS = [
  { key: "cancer", label: "Cancer", get: c => c.cancers },
  { key: "layer", label: "Data layer", get: c => [c.layer] },
  { key: "modality", label: "Modality", get: c => c.modalities || [] },
  { key: "status", label: "Resource status and image level", get: c => [c.status] },
  { key: "technique", label: "Technique", get: c => (c.techniques && c.techniques.length ? c.techniques : ["Not specified"]) },
  { key: "access", label: "Access", get: c => [c.access.category] },
  { key: "compartment", label: "Tissue compartment", get: c => c.compartments || [] },
  { key: "assay", label: "Spatial assay class", get: c => (c.spatial_review ? c.spatial_review.assay_classes : [c.layer === "matched-spatial" ? "not-classified" : "na"]) },
  { key: "linkage", label: "H&E linkage", get: c => [c.linkage] },
  { key: "treat", label: "Treatment (spatial review)", get: c => [c.spatial_review ? c.spatial_review.treatment_class : "na"] },
  { key: "sreview", label: "Spatial review", get: c => [c.spatial_review ? c.spatial_review.analysis_cohort : "none"] },
  { key: "outcome", label: "Package review result", get: c => [c.backlog_review ? c.backlog_review.outcome : "na"] },
  { key: "followup", label: "Follow-up review result", get: c => [c.followup_review ? (c.followup_review.outcome ?? "checked") : "na"] },
  { key: "route", label: "Open dependency (spatial reviews)", get: c => c.followup_review?.states || c.backlog_review?.states || c.spatial_review?.route_review?.states || ["na"] },
  { key: "specimen", label: "Specimens", get: c => [c.specimen] },
  { key: "verification", label: "Verification", get: c => [c.verification] },
];

const TCGA_FACETS = [
  { key: "group", label: "Analysis cohort", get: r => [r.analysisCohort] },
  { key: "role", label: "Study role", get: r => [r.role] },
  { key: "subset", label: "Sensitivity and benchmark subsets", get: r => r.subsets },
  { key: "project", label: "Submitted TCGA project", get: r => [r.project] },
  { key: "disp", label: "Patient screen", get: r => [r.disposition] },
  { key: "selected", label: "Selected analysis set", get: r => [r.selected] },
  { key: "reason", label: "Withholding reasons (can overlap)", get: r => (r.reasons.length ? r.reasons : ["none"]) },
  { key: "tctx", label: "Treatment context", get: r => r.treatmentContext },
  { key: "covariate", label: "Recorded covariates", get: r => (r.covariates.length ? r.covariates : ["none"]) },
  { key: "tcomp", label: "Retained compartment (assay QC)", get: r => r.compartments },
  { key: "tumourLayers", label: "Primary tumour assays retained", get: r => [r.tumour_layers] },
  { key: "trna", label: "Primary tumour RNA-seq", get: r => [r.tumour_rna] },
  { key: "tmet", label: "Primary tumour 450k", get: r => [r.tumour_met] },
  { key: "normalRef", label: "Normal reference", get: r => [r.normal_ref] },
  { key: "nctx", label: "Normal donor context", get: r => [r.normalContext] },
  { key: "flagged", label: "Excluded or unresolved aliquots", get: r => [r.flags.length ? "yes" : "no"] },
  { key: "gsite", label: "Reported tumour site (GDC, CRC only)", get: r => [r.siteReported] },
  { key: "sover", label: "Site annotation override", get: r => [r.siteOverride] },
  { key: "hist", label: "Reviewed histology or glioma group (panel revision)", get: r => [r.histStratum] },
  { key: "conflict", label: "Publication and GDC histology differ", get: r => [r.conflict] },
  { key: "pexcl", label: "Study-scope exclusion", get: r => [r.panelExclusion] },
  { key: "acohort", label: "ESCA/PAAD histology review cohort", get: r => [r.cohort] },
  { key: "sens", label: "PDAC sensitivity subset", get: r => [r.sens] },
  { key: "relation", label: "Reviewed histology vs GDC label", get: r => [r.relation] },
  { key: "scopeAction", label: "Earlier 172-patient scope review", get: r => [r.scopeAction] },
];

const VOCAB = {
  tcomp: LABELS.tcgaCompartment, trna: LABELS.tcgaState, tmet: LABELS.tcgaState,
  tumourLayers: LABELS.tumourLayers, normalRef: LABELS.normalRef, compartment: LABELS.compartment,
  flagged: { yes: "At least one", no: "None" },
  acohort: LABELS.analysisCohort, sens: LABELS.sens, relation: LABELS.relation, scopeAction: LABELS.scopeAction,
  disp: LABELS.disposition, selected: LABELS.selected, reason: { ...LABELS.reason, none: "None" }, covariate: { ...LABELS.reason, none: "None" },
  tctx: LABELS.treatmentContext, nctx: LABELS.normalContext, sover: LABELS.siteOverride,
  role: LABELS.role, subset: LABELS.subset, pexcl: LABELS.panelExclusion, conflict: { yes: "Yes", no: "No" },
  assay: LABELS.assayClass, treat: LABELS.treatmentClass, linkage: LABELS.linkageShort, route: { ...LABELS.routeState, na: "Not reviewed" },
  level: LABELS.imageLevel, pid: { known: "Given by the source", unknown: "Not given or not mapped" },
  area: { own: "One section per array area", shared: "Array area shared with other sections" },
  outcome: { ...LABELS.backlogOutcome, na: "Not in the package review" },
  followup: { ...LABELS.followupOutcome, checked: "Checked again; no change", na: "Not in the follow-up review" },
  sreview: { ...Object.fromEntries(Object.keys(LABELS.spatialScope).map(k => [k, `Reviewed for ${k}`])), none: "Not in the spatial review" },
};

let D, T = null;
const state = { view: "captures", q: "", strict: false, sel: {}, shown: PAGE };

function facetsFor() { return state.view === "captures" ? CAPTURE_FACETS : state.view === "tcga" ? TCGA_FACETS : COHORT_FACETS; }
function rows() { return state.view === "captures" ? D.captures : state.view === "tcga" ? (T ? T.patients : []) : D.cohorts; }

function optionLabel(key, v) {
  switch (key) {
    case "cancer": return cancerName(D, v);
    case "stratum": return v === "none" ? "No stratum assigned" : stratumLabel(D, v);
    case "cohort": return D.cohortById.get(v)?.label ?? v;
    case "access": return LABELS.access[v] ?? v;
    case "modality": return LABELS.modality[v] ?? v;
    case "specimen": return LABELS.specimen[v] ?? v;
    case "project": return `TCGA-${v}`;
    case "group": return LABELS.analysisGroup[v] ?? cohortName(D, v);
    case "gsite": return LABELS.siteReported[v] ?? v;
    case "hist": return LABELS.histStratum[v] ?? v;
    default: return (VOCAB[key] && VOCAB[key][v]) ?? (LABELS[key] && LABELS[key][v]) ?? v;
  }
}

function optionOrder(key, values) {
  if (key === "cancer") {
    const order = D.cancers.map(c => c.code);
    return values.sort((a, b) => order.indexOf(a) - order.indexOf(b));
  }
  if (key === "stratum") {
    const order = [...D.strata.keys(), "none"];
    return values.sort((a, b) => order.indexOf(a) - order.indexOf(b));
  }
  if (key === "project") return values.sort();
  if (key === "group") return values.sort((a, b) => (a in LABELS.analysisGroup) - (b in LABELS.analysisGroup) || a.localeCompare(b));
  if (key === "gsite") return values.sort((a, b) => (a === "na") - (b === "na") || a.localeCompare(b));
  if (key === "hist") {
    const order = Object.keys(LABELS.histStratum);
    return values.sort((a, b) => (order.indexOf(a) + 1 || 90) - (order.indexOf(b) + 1 || 90) || a.localeCompare(b));
  }
  const vocab = VOCAB[key] || LABELS[key] || (key === "access" ? LABELS.access : null);
  if (vocab) {
    const order = Object.keys(vocab);
    return values.sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
  }
  return values.sort((a, b) => optionLabel(key, a).localeCompare(optionLabel(key, b)));
}

function searchText(r) {
  if (state.view === "tcga") return [r.patient, r.project, `tcga-${r.project}`, r.case_id, cancerName(D, r.cancer), r.analysisCohort,
    r.siteReported === "na" ? "" : r.siteReported, r.histStratum === "na" ? "" : r.histStratum, r.role,
    ...r.flags.map(f => `${f.aliquot} ${f.pathology_reason ?? ""}`)].join(" ").toLowerCase();
  if (state.view === "captures") {
    const co = D.cohortById.get(r.cohort);
    return [r.capture, r.patient, r.accession, r.source_name, co?.label, r.diagnosis, r.histology,
      stratumLabel(D, r.stratum), cancerName(D, r.cancer), r.cancer, r.technique].join(" ").toLowerCase();
  }
  return [r.label, r.title, r.citation?.authors, r.citation?.title, r.citation?.journal, r.citation?.doi, r.accession,
    r.description, ...(r.cancers || []), ...(r.cancers || []).map(x => cancerName(D, x)), ...(r.techniques || [])].join(" ").toLowerCase();
}

function matches(r, except) {
  if (state.q) {
    const terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    const text = searchText(r);
    if (!terms.every(t => text.includes(t))) return false;
  }
  if (state.view === "captures" && state.strict && !(r.tier === "core" && r.treatment === "Untreated")) return false;
  for (const f of facetsFor()) {
    if (f.key === except) continue;
    const chosen = state.sel[f.key];
    if (chosen && chosen.length && !f.get(r).some(v => chosen.includes(v))) return false;
  }
  return true;
}

function filtered() { return rows().filter(r => matches(r)); }

// ---------------------------------------------------------------- URL state

function readUrl() {
  const p = new URLSearchParams(location.search);
  state.view = ["cohorts", "tcga"].includes(p.get("view")) ? p.get("view") : "captures";
  state.q = p.get("q") || "";
  state.strict = p.get("strict") === "1";
  state.sel = {};
  for (const f of [...CAPTURE_FACETS, ...COHORT_FACETS, ...TCGA_FACETS]) {
    const v = p.get(f.key);
    if (v) state.sel[f.key] = v.split(",").filter(Boolean);
  }
}

function writeUrl() {
  const p = new URLSearchParams();
  if (state.view !== "captures") p.set("view", state.view);
  if (state.q) p.set("q", state.q);
  if (state.strict && state.view === "captures") p.set("strict", "1");
  for (const f of facetsFor()) {
    const v = state.sel[f.key];
    if (v && v.length) p.set(f.key, v.join(","));
  }
  const qs = p.toString();
  history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
}

// ---------------------------------------------------------------- facets

function renderFacets() {
  const wrap = document.getElementById("facets");
  const html = facetsFor().map(f => {
    const counts = new Map();
    for (const r of rows()) {
      if (!matches(r, f.key)) continue;
      for (const v of new Set(f.get(r))) counts.set(v, (counts.get(v) || 0) + 1);
    }
    const all = new Set(rows().flatMap(f.get));
    const chosen = state.sel[f.key] || [];
    const values = optionOrder(f.key, [...all]);
    if (values.length < 2 && !chosen.length) return "";
    const opts = values.map(v => {
      const n = counts.get(v) || 0;
      const checked = chosen.includes(v);
      return `<label style="${!n && !checked ? "opacity:.5" : ""}"><input type="checkbox" data-facet="${f.key}" value="${esc(v)}" ${checked ? "checked" : ""}>
        <span>${esc(optionLabel(f.key, v))}</span><span class="n">${n}</span></label>`;
    }).join("");
    return `<fieldset class="fgroup"><legend>${esc(f.label)}</legend>${opts}</fieldset>`;
  }).join("");
  wrap.innerHTML = html;
  wrap.querySelectorAll("input[data-facet]").forEach(inp => inp.addEventListener("change", () => {
    const k = inp.dataset.facet;
    const set = new Set(state.sel[k] || []);
    inp.checked ? set.add(inp.value) : set.delete(inp.value);
    state.sel[k] = [...set];
    state.shown = PAGE;
    update();
  }));
}

// ---------------------------------------------------------------- tables

function captureRow(c) {
  const co = D.cohortById.get(c.cohort);
  return `<tr class="clickable" tabindex="0" data-id="${esc(c.id)}">
    <td class="primary" data-label="Section"><div><span class="mono">${esc(c.capture)}</span><span class="cell-sub">Patient ${esc(c.patient ?? "not mapped")} · ${esc(co?.label ?? c.cohort)}</span></div></td>
    <td data-label="Cancer"><div>${esc(c.cancer)}<span class="cell-sub">${esc(stratumLabel(D, c.stratum))}</span></div></td>
    <td data-label="Site / treatment"><div>${esc(c.site)}<span class="cell-sub">${chip("treatment", c.treatment)}</span></div></td>
    <td data-label="Technique"><div>${esc(c.technique)}<span class="cell-sub">${esc(c.preservation ?? "")}</span></div></td>
    <td data-label="Image level / tier"><div>${chip("imageLevel", c.image_level)}<span class="cell-sub">${chip("tier", c.tier)} ${chip("access", c.access.he)}</span></div></td>
  </tr>`;
}

function cohortCountCell(c) {
  if (c.tcga_project && D.tcgaCounts[c.tcga_project]) {
    const x = D.tcgaCounts[c.tcga_project], e = D.elig.projects[c.tcga_project];
    if (e && e.excluded_from_study) return `<span class="muted">Excluded from the study</span><span class="cell-sub">${fmt(x.post_qc.union)} / ${fmt(x.post_qc.paired)} after assay QC, kept for provenance; no patient selected</span>`;
    const pool = e && D.elig.cohorts[e.analysis_cohort].projects.length > 1 ? D.elig.cohorts[e.analysis_cohort] : null;
    if (pool) return `<span class="num">${fmt(e.selected_analysis.total)} / ${fmt(e.selected_analysis.paired)}</span><span class="cell-sub">contribution to the pooled ${esc(e.analysis_cohort)} ${pool.role === "discovery" ? "cohort" : esc(LABELS.role[pool.role].toLowerCase())} (${fmt(pool.selected_analysis.total)} / ${fmt(pool.selected_analysis.paired)}), total / both; ${fmt(x.post_qc.union)} after assay QC; normal reference ${fmt(e.normal.rna_he_after)}</span>`;
    if (e) return `<span class="num">${fmt(e.selected_analysis.total)} / ${fmt(e.selected_analysis.paired)}</span><span class="cell-sub">selected tumour patients${e.analysis_cohort !== c.tcga_project ? ` (${esc(e.analysis_cohort)})` : ""}, total / both; ${fmt(x.post_qc.union)} after assay QC; normal reference ${fmt(e.normal.rna_he_after)}</span>`;
    return `<span class="num">${fmt(x.post_qc.union)} / ${fmt(x.post_qc.paired)}</span><span class="cell-sub">tumour patients, RNA and/or 450k / both, after exclusions; normal reference ${fmt(x.normal.rna_he)}</span>`;
  }
  const k = cohortCounts(D, c);
  if (k) return `<span class="num">${fmt(k.all.captures)}</span> tissue section records<span class="cell-sub">${[k.original.captures ? `${fmt(k.original.captures)} with original H&E` : "", k.preview.captures ? `${fmt(k.preview.captures)} with a preview image` : ""].filter(Boolean).join(", ")}; ${fmt(k.all.patients)} known ${k.all.patients === 1 ? "patient" : "patients"}${k.all.unknown ? `, ${fmt(k.all.unknown)} sections without a patient ID` : ""}; ${fmt(k.core.patients)} with primary-tumour sections in a defined histology stratum</span>`;
  if (countedPreview(D, c)) return `<span class="num">${fmt(countedPreview(D, c))}</span> checked section packages<span class="cell-sub">preview image; not listed one by one, so no patients are counted; eligible patients unknown</span>`;
  if (c.reported && c.reported.length) {
    const [n, unit, , scope] = c.reported[0];
    return `<span class="num">${fmt(n)}</span> ${esc(unit)}<span class="cell-sub">reported by source${scope ? `, ${esc(scope)} only` : c.cancers.length > 1 ? ", all cancer sites" : ""}${c.reported.length > 1 ? `; ${c.reported.length - 1} more ${c.reported.length === 2 ? "unit" : "units"}` : ""}${c.spatial_review ? "; eligible patients unknown" : ""}</span>`;
  }
  if (c.spatial_review) return `<span class="muted">No reliable count verified</span><span class="cell-sub">eligible patients unknown</span>`;
  return `<span class="muted">Not counted</span>`;
}

function cohortRow(c) {
  const cit = c.citation || {};
  const sub = [cit.journal, cit.year].filter(Boolean).join(" ");
  return `<tr class="clickable" tabindex="0" data-id="${esc(c.id)}">
    <td class="primary" data-label="Resource"><div>${esc(c.label)}${c.status === "candidate" && cit.title && cit.title !== c.label
      ? `<span class="cell-sub">${esc(cit.title.length > 110 ? cit.title.slice(0, 108) + "…" : cit.title)}</span>`
      : (sub ? `<span class="cell-sub">${esc(sub)}</span>` : "")}</div></td>
    <td data-label="Cancers"><div>${esc(c.cancers.join(", "))}</div></td>
    <td data-label="Layer"><div>${esc(LABELS.layer[c.layer])}<span class="cell-sub">${esc((c.techniques || []).join(", "))}</span></div></td>
    <td data-label="Status / access"><div>${chip("status", c.status)}<span class="cell-sub">${chip("access", c.access.category)}</span></div></td>
    <td data-label="Counts"><div>${cohortCountCell(c)}</div></td>
  </tr>`;
}

function tcgaRow(r) {
  return `<tr class="clickable" tabindex="0" data-id="${esc(r.patient)}">
    <td class="primary" data-label="Patient"><div><span class="mono">${esc(r.patient)}</span><span class="cell-sub">TCGA-${esc(r.project)}${r.analysisCohort !== r.project && !(r.analysisCohort in LABELS.analysisGroup) ? ` · ${esc(r.analysisCohort)} ${r.role === "classification-benchmark" ? "benchmark" : "cohort"}${r.sens === "excluded" ? " (flagged)" : ""}` : ""}${r.role === "excluded" ? " · excluded from the study" : ""}${r.panelExclusion !== "none" && r.role !== "excluded" ? " · outside the squamous cohort" : ""}${r.siteOverride !== "none" ? " · site corrected" : ""}${r.scope ? " · scope reviewed" : ""}</span></div></td>
    <td data-label="Primary tumour"><div>${chip("tumourLayers", r.tumour_layers)}<span class="cell-sub">RNA-seq: ${esc(LABELS.tcgaState[r.tumour_rna])} · 450k: ${esc(LABELS.tcgaState[r.tumour_met])}</span></div></td>
    <td data-label="Patient screen"><div>${chip("disposition", r.disposition, LABELS.dispositionShort[r.disposition])}${r.reasons.length ? `<span class="cell-sub">${esc(LABELS.reason[r.reasons[0]] ?? r.reasons[0])}${r.reasons.length > 1 ? ` (+${r.reasons.length - 1})` : ""}</span>` : ""}</div></td>
    <td data-label="Normal reference"><div>${chip("normalRef", r.normal_ref)}</div></td>
    <td data-label="Flagged aliquots"><div>${r.flags.length ? `${r.flags.length}<span class="cell-sub">${esc([...new Set(r.flags.map(f => f.disposition))].join(", "))}</span>` : '<span class="muted">None</span>'}</div></td>
  </tr>`;
}

function renderTable(list) {
  const t = document.getElementById("table");
  if (!list.length) {
    t.innerHTML = `<div class="table-wrap"><div class="empty">No entries match these filters.</div></div>`;
    document.getElementById("more").innerHTML = "";
    return;
  }
  const page = list.slice(0, state.shown);
  const head = state.view === "captures"
    ? ["Section / patient / study", "Cancer / stratum", "Site / treatment", "Technique", "Image level / tier / H&E access"]
    : state.view === "tcga" ? ["Patient", "Primary tumour (assay QC)", "Patient screen", "Normal reference", "Flagged aliquots"]
    : ["Resource", "Cancers", "Layer", "Status / access", "Counts"];
  t.innerHTML = `<div class="table-wrap"><table class="stack">
    <caption class="visually-hidden">${{ captures: "Spatial transcriptomics sections", cohorts: "Cohorts and resources", tcga: "TCGA patients" }[state.view]} matching the current filters</caption>
    <thead><tr>${head.map(h => `<th scope="col">${h}</th>`).join("")}</tr></thead>
    <tbody>${page.map({ captures: captureRow, cohorts: cohortRow, tcga: tcgaRow }[state.view]).join("")}</tbody></table></div>`;
  t.querySelectorAll("tr[data-id]").forEach(tr => {
    const open = () => (state.view === "captures" ? showCapture(D, tr.dataset.id)
      : state.view === "tcga" ? showTcgaPatient(D, T, tr.dataset.id) : showCohort(D, tr.dataset.id));
    tr.addEventListener("click", e => { if (!e.target.closest("a")) open(); });
    tr.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
  });
  const rest = list.length - page.length;
  const more = document.getElementById("more");
  more.innerHTML = rest > 0 ? `<button class="btn" type="button">Show ${Math.min(rest, PAGE)} more of ${rest}</button>` : "";
  if (rest > 0) more.querySelector("button").addEventListener("click", () => { state.shown += PAGE; renderTable(list); });
}

function renderSummary(list) {
  const el = document.getElementById("count");
  const note = document.getElementById("view-note");
  if (state.view === "captures") {
    const t = tally(list);
    const pl = (n, one, many) => `<strong>${fmt(n)}</strong> ${n === 1 ? one : many}`;
    const nOrig = list.filter(c => c.image_level === "original").length;
    el.innerHTML = `${pl(t.captures, "tissue section record", "tissue section records")} <span class="small muted">(${fmt(nOrig)} with original H&amp;E, ${fmt(t.captures - nOrig)} with a preview image)</span> from ${pl(t.patients, "known patient", "known patients")} in ${pl(t.cohorts, "study", "studies")}${t.unknown ? ` <span class="small muted">· ${fmt(t.unknown)} without a patient ID</span>` : ""}`;
    const counted = D.cohorts.filter(c => countedPreview(D, c)).length;
    note.textContent = "Each row is one tissue section record with measured spatial RNA and coordinates, such as one Visium capture area, and either the original H&E scan or only a preview image (see the image level; preview sections are not suited to whole-slide or tile models, morphology or distance measurements). Known patients are study-local IDs given by the source, counted once per study; sections without one are not counted as patients, and no patient is known to appear in more than one study. Records are not globally unique physical sections, and they are not eligible-patient counts. Counts are lower bounds before image registration and tissue QC."
      + (counted ? ` Checked preview packages of ${counted} ${counted === 1 ? "study are" : "studies are"} counted for their study on the spatial page and are not listed here.` : "");
  } else if (state.view === "tcga") {
    const t = tcgaTally(list);
    el.innerHTML = `<strong>${fmt(t.union)}</strong> tumour patients after assay QC → <strong>${fmt(t.eligible)}</strong> after the patient screen →
      <strong>${fmt(t.selected)}</strong> selected <span class="small muted">(${fmt(t.selPaired)} both · ${fmt(t.selRnaOnly)} RNA only · ${fmt(t.selMetOnly)} 450k only)</span> ·
      <strong>${fmt(t.normal)}</strong> normal RNA + H&amp;E after screening <span class="small muted">(${fmt(t.normalMet)} with 450k${t.withheldNormal ? `; ${fmt(t.withheldNormal)} withheld` : ""})</span> ·
      <strong>${fmt(t.either)}</strong> distinct patients <span class="small muted">of ${fmt(t.patients)} listed</span>`;
    note.textContent = `Assay states use current GDC files after exact aliquot matching to the PanCanAtlas quality annotations. The patient screen adds treatment, diagnosis, identity and recurrence decisions and does not change assay states. The selected set uses histology-defined cohorts for ESCC, PDAC and CSCC, pools TCGA-COAD and TCGA-READ as CRC, and pools TCGA-LGG and TCGA-GBM as the GLIOMA classification benchmark. Filter by analysis cohort or study role to count each patient once. Normal-reference patients are cancer patients, most of them also in the tumour set, so the two groups should not be added. Patients listed with nothing retained have only excluded or unresolved aliquots. Treatment-flagged patients are not a treated reference set.`;
  } else {
    const n = list.length;
    const byStatus = ["verified", "preview", "screened", "candidate", "reference", "listed"].map(s => [s, list.filter(c => c.status === s).length]).filter(([, k]) => k);
    el.innerHTML = `<strong>${fmt(n)}</strong> ${n === 1 ? "resource" : "resources"} <span class="small muted">(${byStatus.map(([s, k]) => `${k} ${LABELS.status[s].toLowerCase()}`).join(", ")})</span>`;
    note.textContent = "Each underlying study appears once, at its best image level. Counts are computed from catalogued tissue section records where they exist; otherwise the source's own count is shown and labelled. Candidate studies are listed without patient counts.";
  }
}

function update() {
  if (state.view === "tcga" && !T) {
    document.getElementById("table").innerHTML = '<div class="table-wrap"><div class="empty">Loading TCGA patients…</div></div>';
    loadTcgaPatients(D).then(t => { T = t; update(); }).catch(err => showError(document.getElementById("table"), err));
    return;
  }
  writeUrl();
  document.querySelectorAll(".tabs button").forEach(b => b.setAttribute("aria-selected", String(b.dataset.view === state.view)));
  document.getElementById("strict-wrap").style.display = state.view === "captures" ? "" : "none";
  document.getElementById("strict").checked = state.strict;
  document.getElementById("q").value = state.q;
  const list = filtered();
  renderFacets();
  renderSummary(list);
  renderTable(list);
}

// ---------------------------------------------------------------- export

function csvCell(v) {
  if (v === null || v === undefined) return "";
  const s = Array.isArray(v) ? v.join(" | ") : String(v);
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function captureRecord(c) {
  const co = D.cohortById.get(c.cohort);
  const cl = c.clinical || {};
  return {
    catalogue_release: D.release.version, record_id: c.id, cohort_id: c.cohort, cohort: co?.label,
    citation_doi: co?.citation?.doi ?? "", cancer: c.cancer, histology_stratum: c.stratum ? stratumLabel(D, c.stratum) : "",
    patient_id: c.patient, patient_id_mapping: c.donor_mapping ? LABELS.donorMapping[c.donor_mapping] : (c.patient ? "Curated from the source" : ""),
    capture_id: c.capture, accession: c.accession, image_level: LABELS.imageLevel[c.image_level],
    shared_array_area: c.assay_area_id ?? "", source_region: c.region_label ?? "",
    expression_subset: c.expression_subset ? `slide ${c.expression_subset.slide}, tissue ${c.expression_subset.tissues}` : "",
    catalogue_tier: LABELS.tier[c.tier],
    tier_reason: c.tier_reason, site: c.site, site_source: c.site_source, treatment_before_sampling: c.treatment,
    treatment_note: c.treatment_note, diagnosis_source: c.diagnosis, histology_source: c.histology,
    tissue: c.compartment ? (LABELS.compartment[c.compartment] ?? c.compartment) : "",
    technique: c.technique, preservation: c.preservation, he_rna_linkage: LABELS.linkage[c.linkage], expression_data: c.expression_type,
    out_of_tissue_expression_spots: c.out_of_tissue_expression_spots ?? "", recurrence_later_outcome: c.recurrence_outcome ?? "",
    sampled_recurrence: c.sampled_recurrence ?? "", frame_check: c.geometry_check ? geometryText(c.geometry_check) : "",
    response_label_source: cl.response ?? "", evidence_for_reviewed_fields: Object.entries(c.field_sources || {}).map(([f, u]) => `${f}: ${u}`),
    original_image_match_inferred: c.original_crosswalk_inferred ?? "", open_checks: c.open_checks || [],
    he_um_per_pixel: c.he_mpp, he_resolution_basis: c.he_mpp_basis, he_url: c.links.he, expression_url: c.links.expression,
    coordinates_url: c.links.coordinates, raw_urls: c.links.raw, access_he: LABELS.access[c.access.he],
    access_processed: LABELS.access[c.access.processed], access_raw: LABELS.access[c.access.raw],
    registration: c.registration, verification: LABELS.verification[c.verification], verified_on: c.verified_on,
    age_source: cl.age, sex_source: cl.sex, stage_source: cl.stage, grade_source: cl.grade, subsite_source: cl.subsite, markers_source: cl.markers,
  };
}

function cohortRecord(c) {
  const k = cohortCounts(D, c);
  return {
    catalogue_release: D.release.version, cohort_id: c.id, label: c.label, cancers: c.cancers, data_layer: LABELS.layer[c.layer],
    catalogue_status: LABELS.status[c.status], modalities: (c.modalities || []).map(m => LABELS.modality[m] ?? m),
    techniques: c.techniques, preservation: c.preservation, specimens: LABELS.specimen[c.specimen], linkage: LABELS.linkage[c.linkage],
    accession: c.accession, access: LABELS.access[c.access.category], access_route: c.access.route,
    access_links: (c.access.links || []).map(([, u]) => u), open_checks: (c.gates || []).map(g => LABELS.gate[g] ?? g),
    image_level: c.status === "verified" || c.status === "preview" ? LABELS.status[c.status] : "",
    known_patients: k?.all.patients ?? "", section_records: k?.all.captures ?? "",
    section_records_original_he: k?.original.captures ?? "", section_records_preview_image: k?.preview.captures ?? "",
    preview_sections_counted_without_records: countedPreview(D, c) || "", sections_without_patient_id: k?.all.unknown ?? "",
    core_patients: k?.core.patients ?? "", core_captures: k?.core.captures ?? "",
    reported_counts: (c.reported || []).map(([n, u, b, sc]) => `${n} ${u} (${b}${sc ? `; ${sc}` : ""})`),
    spatial_review_id: c.spatial_review?.id ?? "", spatial_review_date: c.spatial_review?.date ?? "",
    route_review_status: c.spatial_review?.route_review?.status ?? "",
    route_open_dependencies: (c.spatial_review?.route_review?.states || []).map(x => LABELS.routeState[x] ?? x),
    route_next_step: c.spatial_review?.route_review?.next_step ?? "",
    route_sections_with_matching_coordinates: c.spatial_review?.route_review?.sections_with_matching_coordinates ?? "",
    package_review_result: c.backlog_review ? LABELS.backlogOutcome[c.backlog_review.outcome] : "",
    package_review_depth: c.backlog_review?.depth ?? "", package_review_images: c.backlog_review?.image_finding ?? "",
    package_review_expression_and_coordinates: c.backlog_review?.molecular_finding ?? "",
    package_review_open_dependencies: (c.backlog_review?.states || []).map(x => LABELS.routeState[x] ?? x),
    package_review_next_step: c.backlog_review?.next_step ?? "",
    followup_review_result: c.followup_review ? (c.followup_review.outcome ? LABELS.followupOutcome[c.followup_review.outcome] : "checked again; no change") : "",
    followup_review_findings: c.followup_review?.findings ?? "", followup_review_next_step: c.followup_review?.next_step ?? "",
    followup_review_checks: (c.followup_review?.checks || []).map(x => `${x.check}: ${x.result}`),
    open_dependencies_latest: (c.followup_review?.states || c.backlog_review?.states || c.spatial_review?.route_review?.states || []).map(x => LABELS.routeState[x] ?? x),
    spatial_analysis_scope: c.spatial_review?.analysis_cohort ?? "",
    spatial_assay_classes: (c.spatial_review?.assay_classes || []).map(a => LABELS.assayClass[a]),
    spatial_platform_reported: c.spatial_review?.platform ?? "", spatial_image_status: c.spatial_review?.image_status ?? "",
    treatment_class: c.spatial_review ? LABELS.treatmentClass[c.spatial_review.treatment_class] : "",
    treatment_status_reported: c.spatial_review?.treatment_status ?? "",
    eligible_patients: c.spatial_review || c.backlog_review ? "unknown" : "",
    sample_ids: c.spatial_review ? Object.entries(c.spatial_review.sample_ids || {}).map(([k, v]) => `${LABELS.sampleIds[k] ?? k}: ${v.join(" ")}`) : [],
    notes: c.notes || [],
    compartments: (c.compartments || []).map(x => LABELS.compartment[x] ?? x),
    ...tcgaCohortFields(c),
    citation_authors: c.citation?.authors, citation_title: c.citation?.title, citation_journal: c.citation?.journal,
    citation_year: c.citation?.year, citation_doi: c.citation?.doi, citation_url: c.citation?.url,
    verification: LABELS.verification[c.verification], verified_on: c.verified_on, description: c.description,
  };
}

function tcgaRecord(r) {
  return {
    catalogue_release: D.release.version, screen_date: D.tcgaMeta.date, representation: "current GDC files",
    patient_id: r.patient, tcga_project: `TCGA-${r.project}`, gdc_case_id: r.case_id,
    analysis_cohort: r.analysisCohort in LABELS.analysisGroup ? "" : r.analysisCohort,
    study_role: LABELS.role[r.role] ?? r.role, study_scope_exclusion: r.panelExclusion === "none" ? "" : r.panelExclusion,
    subsets: r.subsets.filter(v => v !== "none"),
    gdc_case_url: `https://portal.gdc.cancer.gov/cases/${r.case_id}`,
    tumour_rna_seq: r.tumour_rna, tumour_450k: r.tumour_met, tumour_layers_retained: LABELS.tumourLayers[r.tumour_layers],
    normal_rna_seq: r.normal_rna, normal_450k: r.normal_met,
    normal_rna_with_he_same_sample: r.normal_rna_he, normal_rna_he_with_450k_same_sample: r.normal_rna_he_met,
    retained_compartments: r.compartments.filter(c => c !== "none"),
    patient_review_date: D.elig.meta.date, patient_screen: LABELS.disposition[r.disposition],
    primary_tumour_eligible_after_screen: r.tumour_layers === "none" ? "" : r.eligible,
    in_selected_analysis_set: r.selected === "na" ? "" : r.selected === "yes",
    withholding_reasons: r.reasons.map(x => LABELS.reason[x] ?? x), withholding_reason_codes: r.reasons,
    covariates: r.covariates.map(x => LABELS.reason[x] ?? x), treatment_context: r.treatmentContext.map(x => LABELS.treatmentContext[x]),
    study_primary_diagnosis: r.clinical?.primary_diagnosis ?? "", study_primary_morphology: r.clinical?.morphology ?? "",
    prior_treatment_field: r.clinical?.prior_treatment_field ?? "",
    normal_package_after_screen: r.normal_ref === "rna-he" || r.normal_ref === "rna-he-met",
    normal_package_in_excluded_project: r.normal_ref === "inactive",
    normal_donor_context: r.normalContext === "na" ? "" : LABELS.normalContext[r.normalContext],
    reported_tumour_site_gdc: r.clinical?.site_reported ?? "", reported_resection_site_gdc: r.clinical?.resection_site_reported ?? "",
    site_annotation_override: r.siteOverride === "none" ? "" : r.siteOverride,
    reviewed_histology_or_group: r.clinical?.histology_stratum ?? "", histology_source: r.clinical?.histology_evidence ?? "",
    histology_publication: r.clinical?.histology_publication ?? "", in_publication_table: r.clinical?.histology_publication_member ?? "",
    histology_gdc: r.clinical?.historical_histology_gdc ?? "", publication_gdc_histology_differ: r.clinical?.histology_label_conflict ?? "",
    grade_publication: r.clinical?.grade_publication ?? "", grade_gdc: r.clinical?.historical_grade_gdc ?? "",
    published_molecular_group: r.clinical?.molecular_group ?? "", published_subtype: r.clinical?.published_subtype ?? "",
    idh_status_raw: r.clinical?.idh_status ?? "", codeletion_1p19q_raw: r.clinical?.codeletion_1p19q ?? "",
    hpv_status_publication: r.clinical?.hpv_status_publication ?? "", endometrial_like_publication: r.clinical?.endometrial_like_publication ?? "",
    adrenal_cortical_admixture: r.clinical?.adrenal_cortical_admixture ?? "", head_neck_paraganglioma: r.clinical?.head_neck_sensitivity_flag ?? "",
    integrated_who_diagnosis: r.clinical?.who_diagnosis_status === "requires_independent_integrated_diagnosis_and_grade" ? "not adjudicated (required)" : "",
    histology_defined_cohort: r.cohort === "ESCC" || r.cohort === "PDAC" ? r.cohort : "",
    in_pdac_sensitivity_subset: r.cohort === "PDAC" ? r.sens === "included" : "",
    histology_stratum: r.histology ? (LABELS.stratum[r.histology.stratum] ?? r.histology.stratum) : "",
    gdc_primary_diagnosis: r.histology?.gdc_primary_diagnosis ?? "", gdc_morphology: r.histology?.gdc_morphology ?? "",
    gdc_diagnosis_id: r.histology?.gdc_diagnosis_id ?? "", gdc_site: r.histology?.gdc_site ?? "",
    reviewed_histology: r.histology?.reviewed_histology ?? "", histology_evidence: r.histology?.evidence ?? "",
    relation_to_gdc_label: r.histology ? LABELS.relation[r.histology.gdc_label_relation] : "",
    cohort_reason: r.histology ? (LABELS.analysisReason[r.histology.analysis_reason] ?? r.histology.analysis_reason) : "",
    publication_note: r.histology?.publication_notes ?? "", pathology_report_url: r.histology?.pathology_report_url ?? "",
    focal_squamous_flag: r.histology ? r.histology.focal_squamous_flag : "", specimen_note: r.histology?.specimen_note ?? "",
    earlier_scope_review: r.scope ? LABELS.scopeAction[r.scope.summary_action] : "",
    retained_assay_image_linkage: "not yet checked",
    flagged_aliquots: r.flags.length,
    flagged_aliquot_details: r.flags.map(f => `${f.aliquot} ${f.compartment} ${f.layer === "rna" ? "RNA-seq" : "450k"} ${f.disposition}${f.do_not_use ? " Do_not_use" : ""}${f.awg_pathology ? ` pathology${f.pathology_reason ? `: ${f.pathology_reason}` : ""}` : ""}`),
  };
}

function tcgaCohortFields(c) {
  const x = c.tcga_project && D.tcgaCounts[c.tcga_project];
  if (!x) return {};
  return {
    tcga_project: `TCGA-${c.tcga_project}`, screen_date: D.tcgaMeta.date, passes_molecular_screen: tcgaPasses(D, c.tcga_project),
    excluded_from_study: !!D.elig.projects[c.tcga_project]?.excluded_from_study,
    study_role: D.elig.projects[c.tcga_project] ? LABELS.role[D.elig.projects[c.tcga_project].role] : "",
    analysis_cohort: D.elig.projects[c.tcga_project]?.analysis_cohort ?? "",
    pooled_with: (D.tcga_counts.groups[x.group]?.projects || []).filter(p => p !== c.tcga_project).map(p => `TCGA-${p}`),
    pooled_cohort_passes_screen: (D.tcga_counts.groups[x.group]?.projects.length > 1) ? D.tcga_counts.groups[x.group].passes_screen : "",
    pre_qc_tumour_union: x.pre_qc.union, pre_qc_tumour_both: x.pre_qc.paired, pre_qc_rna_only: x.pre_qc.rna_only, pre_qc_450k_only: x.pre_qc.met_only,
    tumour_union: x.post_qc.union, tumour_both: x.post_qc.paired, tumour_rna_only: x.post_qc.rna_only, tumour_450k_only: x.post_qc.met_only,
    normal_rna_he: x.normal.rna_he, normal_rna_he_450k: x.normal.rna_he_met, normal_also_in_tumour_set: x.normal.also_in_tumour_union,
    distinct_patients_either_compartment: x.patients_either_compartment,
    historical_matrix_union: x.historical_matrix?.union, historical_matrix_both: x.historical_matrix?.paired,
    ...eligibilityFields(c.tcga_project),
  };
}

function eligibilityFields(project) {
  const e = D.elig.projects[project];
  if (!e) return {};
  const a = e.after_patient_screen, sl = e.selected_analysis;
  const pool = e.analysis_cohort ? D.elig.cohorts[e.analysis_cohort] : null;
  const pooled = pool && pool.projects.length > 1;
  return {
    patient_review_date: D.elig.meta.date,
    after_screen_total: a.total, after_screen_both: a.paired, after_screen_rna_only: a.rna_only, after_screen_450k_only: a.met_only,
    selected_set: e.analysis_cohort ?? "", selected_counts_are: e.excluded_from_study ? "none selected: project excluded from the study" : pooled ? `contribution of this project to the pooled ${e.analysis_cohort} cohort` : "this cohort",
    selected_total: sl.total, selected_both: sl.paired, selected_rna_only: sl.rna_only, selected_450k_only: sl.met_only,
    pooled_cohort_total: pooled ? pool.selected_analysis.total : "", pooled_cohort_both: pooled ? pool.selected_analysis.paired : "",
    withheld_treatment_exclusion: e.dispositions.known_treatment_exclusion || 0, withheld_treatment_hold: e.dispositions.treatment_unknown_hold || 0,
    withheld_diagnosis_identity_episode: e.dispositions.diagnosis_identity_or_episode_exclusion_hold || 0,
    normal_rna_he_after_screen: e.normal.rna_he_after, normal_rna_he_450k_after_screen: e.normal.rna_he_met_after,
    normal_in_active_totals: e.normal.in_active_scope, normal_donors_outside_cohort: e.normal.outside_cohort || [],
    normal_withheld_by_screen: e.normal.withheld,
  };
}

function download(name, text, type) {
  const blob = new Blob([text], { type });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 0);
}

function exportRows(kind) {
  const list = filtered();
  const toRecord = { captures: captureRecord, cohorts: cohortRecord, tcga: tcgaRecord }[state.view];
  const recs = list.map(toRecord);
  const base = `histology-multiomics-explorer-${{ tcga: "tcga-patients", captures: "spatial-transcriptomics", cohorts: "cohorts" }[state.view]}-v${D.release.version}`;
  if (kind === "json") {
    const extra = state.view === "tcga" ? { molecular_screen: D.tcgaMeta, histology_review: T.reviews.meta, flagged_aliquots: list.flatMap(r => r.flags),
      patient_review: { ...D.elig.meta, panel_counts: D.elig.panel, analysis_cohorts: D.elig.cohorts,
        note: "Patients count once in their analysis cohort; TCGA-COAD and TCGA-READ form the pooled CRC cohort and TCGA-LGG and TCGA-GBM the GLIOMA classification benchmark. Subsets are within cohorts and never added. Integrated WHO glioma diagnoses are not adjudicated. Treatment-flagged patients are not a treated reference set." },
      patient_scope_reviews: list.filter(r => r.scope).map(r => r.scope) } : {};
    download(`${base}.json`, JSON.stringify({ release: D.release, view: state.view, filters: location.search || null, ...extra, records: recs }, null, 2), "application/json");
  } else {
    if (state.view === "cohorts") {
      const keys = [...new Set(recs.flatMap(Object.keys))];
      recs.forEach(r => keys.forEach(k => { if (!(k in r)) r[k] = ""; }));
    }
    const cols = recs.length ? [...new Set(recs.flatMap(Object.keys))] : Object.keys(rows().length ? toRecord(rows()[0]) : {});
    const csv = [cols.join(","), ...recs.map(r => cols.map(k => csvCell(r[k])).join(","))].join("\r\n");
    download(`${base}.csv`, "﻿" + csv, "text/csv;charset=utf-8");
  }
}

// ---------------------------------------------------------------- init

try {
  D = await loadData();
  setFooter(D);
  const openId = new URLSearchParams(location.search).get("open");
  readUrl();
  if (window.matchMedia("(max-width: 979px)").matches) document.getElementById("filters").open = false;
  document.querySelectorAll(".tabs button").forEach(b => b.addEventListener("click", () => {
    if (state.view === b.dataset.view) return;
    state.view = b.dataset.view;
    state.shown = PAGE;
    update();
  }));
  let timer;
  document.getElementById("q").addEventListener("input", e => {
    clearTimeout(timer);
    timer = setTimeout(() => { state.q = e.target.value.trim(); state.shown = PAGE; update(); }, 150);
  });
  document.getElementById("strict").addEventListener("change", e => { state.strict = e.target.checked; state.shown = PAGE; update(); });
  document.getElementById("reset").addEventListener("click", () => { state.q = ""; state.strict = false; state.sel = {}; state.shown = PAGE; update(); });
  document.getElementById("export-csv").addEventListener("click", () => exportRows("csv"));
  document.getElementById("export-json").addEventListener("click", () => exportRows("json"));
  document.getElementById("copy-link").addEventListener("click", async e => {
    const btn = e.currentTarget;
    try { await navigator.clipboard.writeText(location.href); btn.textContent = "Link copied"; }
    catch { btn.textContent = "Copy failed"; }
    setTimeout(() => { btn.textContent = "Copy link to view"; }, 1600);
  });
  update();
  if (openId) {
    if (D.cohortById.has(openId)) showCohort(D, openId);
    else if (/^TCGA-/.test(openId)) loadTcgaPatients(D).then(t => { T = t; showTcgaPatient(D, T, openId); });
    else showCapture(D, openId);
  }
} catch (err) {
  showError(document.getElementById("table"), err);
}
