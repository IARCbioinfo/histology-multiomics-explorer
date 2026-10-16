import { loadData, LABELS, esc, chip, setFooter, showError, citationText, showCohort } from "./common.js";

const root = document.getElementById("sources");

function entry(d, c) {
  const links = (c.access.links || []).map(([label, url]) => `<a href="${esc(url)}" rel="noopener" target="_blank">${esc(label)}</a>`).join(" · ");
  const cites = [c.citation, ...(c.related_citations || [])].map(citationText).filter(Boolean).join("<br>");
  return `<div class="source" data-text="${esc([c.label, c.citation?.authors, c.citation?.title, c.citation?.journal, c.citation?.doi, c.accession, ...(c.access.links || []).map(l => l.join(" ")), ...c.cancers].join(" ").toLowerCase())}">
    <div><button class="btn small" type="button" data-cohort="${esc(c.id)}" style="margin-right:.4rem">${esc(c.label)}</button>
      <span class="chips" style="display:inline-flex">${c.cancers.map(x => `<span class="chip outline">${esc(x)}</span>`).join("")} ${chip("status", c.status)} ${chip("access", c.access.category)}</span></div>
    <div class="cite small" style="margin-top:.35rem">${cites}</div>
    ${c.access.route ? `<div class="small muted" style="margin-top:.2rem">${esc(c.access.route)}</div>` : ""}
    ${links ? `<div class="small" style="margin-top:.2rem">${links}</div>` : ""}
  </div>`;
}

try {
  const d = await loadData();
  setFooter(d);
  const ev = `<section><h2>Published archetype evidence (selection history)</h2>${d.evidence.map(e => `<div class="source" data-text="${esc((e.citation + " " + e.doi).toLowerCase())}">
      <div class="chips">${e.cancers.map(x => `<span class="chip outline">${esc(x)}</span>`).join("")}</div>
      <div class="cite small" style="margin-top:.35rem">${esc(e.citation)} <a href="${esc(e.url)}" rel="noopener">doi:${esc(e.doi)}</a></div></div>`).join("")}</section>`;
  const order = ["verified", "preview", "reference", "listed", "candidate"];
  const layers = Object.keys(LABELS.layer).map(l => {
    const list = d.cohorts.filter(c => c.layer === l).sort((a, b) => order.indexOf(a.status) - order.indexOf(b.status));
    if (!list.length) return "";
    return `<section><h2>${esc(LABELS.layer[l])} <span class="small muted">(${list.length})</span></h2>${list.map(c => entry(d, c)).join("")}</section>`;
  }).join("");
  const GROUPS = [["current", "Current GDC data (source of the counts)"], ["pancanatlas", "PanCanAtlas final files (historical harmonized representation)"],
    ["histology", "Histology and molecular-annotation sources"], ["excluded", "Listed but not used"], ["mirror", "Mirrors"], ["publication", "Reference publications"]];
  const res = d.tcga_resources;
  const tcga = `<section id="tcga-data"><h2>TCGA and PanCanAtlas data</h2>
    <p class="small muted">The TCGA counts use current GDC file metadata joined to the PanCanAtlas quality annotations. The PanCanAtlas matrices are a separate, historical representation; do not mix their counts with current GDC files.</p>
    ${GROUPS.map(([g, title]) => {
      const items = res.filter(x => x.group === g);
      if (!items.length) return "";
      return `<h3>${esc(title)}</h3>${items.map(x => `<div class="source" data-text="${esc([x.label, x.file, x.url, x.use].join(" ").toLowerCase())}">
        <div class="cite small"><strong>${esc(x.label)}</strong>${x.file ? ` · <span class="mono">${esc(x.file)}</span>` : ""}</div>
        <div class="small muted" style="margin-top:.2rem">${esc(x.use)}</div>
        <div class="small" style="margin-top:.2rem"><a href="${esc(x.url)}" rel="noopener" target="_blank">${esc(x.url)}</a>${x.docs ? ` · <a href="${esc(x.docs)}" rel="noopener" target="_blank">documentation</a>` : ""}</div></div>`).join("")}`;
    }).join("")}</section>`;
  const leads = (d.leads || []).length ? `<section id="leads"><h2>Related leads, not counted <span class="small muted">(${d.leads.length})</span></h2>
    <p class="small muted">Releases that add no resources or patients to the explorer's totals.</p>
    ${d.leads.map(x => `<div class="source" data-text="${esc([x.label, x.url, x.doi, x.description].join(" ").toLowerCase())}">
      <div class="cite small"><strong>${esc(x.label)}</strong></div>
      <div class="small muted" style="margin-top:.2rem">${esc(x.not_counted)}</div>
      <div class="small" style="margin-top:.2rem">${[["Record", x.url], ...(x.links || [])].map(([l, u]) => `<a href="${esc(u)}" rel="noopener" target="_blank">${esc(l)}</a>`).join(" · ")}</div></div>`).join("")}</section>` : "";
  root.innerHTML = ev + tcga + layers + leads;
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
  root.querySelectorAll("[data-cohort]").forEach(b => b.addEventListener("click", () => showCohort(d, b.dataset.cohort)));
  const q = document.getElementById("sq");
  q.addEventListener("input", () => {
    const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    root.querySelectorAll(".source").forEach(s => { s.hidden = !terms.every(t => s.dataset.text.includes(t)); });
    root.querySelectorAll("section").forEach(sec => { sec.hidden = !sec.querySelector(".source:not([hidden])"); });
  });
} catch (err) {
  showError(root, err);
}
