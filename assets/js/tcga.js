import { loadData, LABELS, esc, fmt, setFooter, showError, formatDate, screenTable, pageForCohort, views } from "./common.js";

try {
  const d = await loadData();
  setFooter(d);
  const ep = d.elig.panel, m = d.elig.meta;
  const ed = ep.dispositions, ctx = ep.normal.context;
  const withheld = ep.assay_qc.total - ep.after_patient_screen.total;
  document.getElementById("panel-h").textContent = "Selected analysis panel";
  const stat = (value, label) => `<div class="stat"><div class="value">${value}</div><div class="label">${label}</div></div>`;
  const all = views(ep.selected_analysis);
  document.getElementById("tcga-stats").innerHTML = [
    stat(fmt(m.analysis_cohorts), "analysis cohorts"),
    stat(fmt(m.projects), "TCGA projects contributing"),
    stat(fmt(all.total), "patients in the selected panel"),
    stat(fmt(all.both), "patients with both RNA-seq and methylation"),
  ].join("");
  document.getElementById("tcga-note").innerHTML = `${m.discovery_cohorts} discovery cohorts and ${m.benchmark_cohorts} glioma classification benchmark. Counts are primary-tumour patients after assay-quality exclusions, a patient treatment and diagnosis screen and, for some cohorts, histology selection. <a href="methods.html#panel">How the panel was selected</a>.`;

  const cohorts = Object.entries(d.elig.cohorts).sort(([a], [b]) => a.localeCompare(b));
  const cell = (v, label) => `<td class="num" data-label="${label}"><div>${fmt(v)}</div></td>`;
  const rows = cohorts.map(([id, c]) => {
    const page = pageForCohort(d, id), v = views(c.selected_analysis);
    const name = page && page.code === id ? page.name : c.label;
    const sub = [c.projects.map(p => `TCGA-${p}`).join(" + "), c.role !== "discovery" ? LABELS.role[c.role].toLowerCase() : ""].filter(Boolean).join("; ");
    return `<tr>
      <td class="primary" data-label="Cancer cohort"><div>${page ? `<a href="cancers.html?c=${esc(page.code)}">${esc(name)}</a>` : esc(name)} <span class="mono muted small">${esc(id)}</span><span class="cell-sub">${esc(sub)}</span></div></td>
      ${cell(v.rna, "Patients with RNA-seq")}${cell(v.met, "Patients with methylation")}${cell(v.both, "Patients with both")}
      <td data-label="Explore"><div><a href="explore.html?view=tcga&group=${esc(id)}">Patients</a>${page ? ` · <a href="cancers.html?c=${esc(page.code)}">Cancer page</a>` : ""}</div></td>
    </tr>`;
  }).join("");
  const detail = cohorts.map(([id, c]) => {
    const x = c.selected_analysis;
    return `<tr><td class="primary" data-label="Cancer cohort"><div>${esc(id)}</div></td>
      ${cell(x.total, "RNA-seq and/or methylation")}${cell(x.rna_only, "RNA-seq only")}${cell(x.met_only, "Methylation only")}
      ${cell(c.normal.rna_he_after, "Normal RNA + H&E")}${cell(c.normal.rna_he_met_after, "Normal with 450k")}</tr>`;
  }).join("");
  document.getElementById("panel-table").innerHTML = `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Cancer cohort</th><th scope="col" class="num">Patients with RNA-seq</th><th scope="col" class="num">Patients with methylation (450k)</th><th scope="col" class="num">Patients with both</th><th scope="col">Explore</th></tr></thead>
    <tbody>${rows}
      <tr><td class="primary" data-label="Cancer cohort"><div><strong>All ${m.analysis_cohorts} cohorts</strong><span class="cell-sub">${m.projects} TCGA projects</span></div></td>
        ${cell(all.rna, "Patients with RNA-seq")}${cell(all.met, "Patients with methylation")}${cell(all.both, "Patients with both")}
        <td data-label="Explore"><div><a href="explore.html?view=tcga">All patients</a></div></td></tr>
    </tbody>
    <caption>Selected analysis panel only. Each patient belongs to one cohort, so the rows add up to the total. Patients with both assays also appear in the RNA-seq and methylation columns. Broader availability by project is in the next section.</caption>
  </table></div>
  <details class="disclosure"><summary>Detailed counts per cohort: single-assay patients and normal tissue</summary>
    <div class="table-wrap" style="margin-top:.5rem"><table class="stack compact"><thead><tr><th scope="col">Cancer cohort</th><th scope="col" class="num">RNA-seq and/or methylation</th><th scope="col" class="num">RNA-seq only</th><th scope="col" class="num">Methylation only</th><th scope="col" class="num">Normal RNA + H&amp;E</th><th scope="col" class="num">Normal with 450k</th></tr></thead>
    <tbody>${detail}</tbody>
    <caption>Unique patients in the selected panel. Normal columns count the cohort's own donors with same-sample normal RNA and H&amp;E after screening; normal tissue comes from patients with cancer, not healthy donors.</caption></table></div>
  </details>
  <details class="disclosure"><summary>The patient screen and normal reference across the panel</summary>
    <ul class="notes">
      <li>Of ${fmt(ep.assay_qc.total)} primary-tumour patients after assay QC, the treatment and diagnosis screen withholds ${fmt(withheld)}: ${ed.known_treatment_exclusion} treatment exclusions, ${ed.treatment_unknown_hold} treatment holds and ${ed.diagnosis_identity_or_episode_exclusion_hold} diagnosis, identity, recurrence or specimen cases. Reasons can overlap. Not all withheld patients were treated, and they do not form a treated reference set.</li>
      <li>Histology-defined cohorts: oesophageal squamous cell carcinoma (ESCC, 90 patients) from TCGA-ESCA, cervical squamous cell carcinoma (CSCC) from TCGA-CESC and pancreatic ductal adenocarcinoma (PDAC, 149, proposed) from TCGA-PAAD; ESCC and PDAC are the two exceptions to the size threshold. TCGA-COAD and TCGA-READ are pooled as colorectal cancer (CRC), and TCGA-LGG and TCGA-GBM as a diffuse glioma classification benchmark (GLIOMA) whose integrated WHO diagnoses are not yet adjudicated.</li>
      <li>Normal reference after screening: ${fmt(ep.normal.rna_he_after)} patients with same-sample normal RNA and H&amp;E, ${fmt(ep.normal.rna_he_met_after)} of them also with normal 450k. Donor context: ${ctx.target_project_donor} with a target-project tumour diagnosis, ${ctx.organ_specific_control} organ-specific controls, ${ctx.non_target_or_uncertain_or_recurrent_donor} with a non-target, uncertain or recurrent diagnosis and ${ctx.normal_only_donor_primary_diagnosis_unreported || 0} normal-only donors without a reported diagnosis.</li>
      <li>Assay states use current GDC file metadata after exact aliquot matching to the PanCanAtlas quality annotations; treatment and diagnosis annotations were reviewed for every retained patient.</li>
    </ul>
  </details>`;
  if (cohorts.reduce((a, [, c]) => a + c.selected_analysis.total, 0) !== ep.selected_analysis.total) throw new Error("Analysis cohort totals do not add up to the panel total");
  document.getElementById("screen-table").innerHTML = screenTable(d);
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
} catch (err) {
  showError(document.getElementById("panel-table"), err);
}
