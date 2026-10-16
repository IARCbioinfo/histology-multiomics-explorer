import { loadData, esc, fmt, setFooter, showError, spatialResourcesFor, LABELS } from "./common.js";

try {
  const d = await loadData();
  setFooter(d);
  const spatial = d.cohorts.filter(c => c.layer === "matched-spatial");
  const located = spatial.filter(c => c.status === "verified").length;
  const pages = d.cancers.filter(c => c.group !== "aggregate" && c.group !== "excluded");
  // Cancer types represented: each resource's cancers, counting pooled colorectal and glioma pages through their constituents.
  const codes = new Set(spatial.flatMap(c => c.cancers));
  for (const p of pages.filter(p => p.includes)) if (codes.has(p.code) && p.includes.some(k => codes.has(k))) codes.delete(p.code);
  const represented = pages.filter(p => !p.includes && codes.has(p.code)).length + pages.filter(p => p.includes && codes.has(p.code)).length;
  const stat = (value, label) => `<div class="stat"><div class="value">${value}</div><div class="label">${label}</div></div>`;
  document.getElementById("stats").innerHTML = [
    stat(fmt(spatial.length), "catalogued spatial resources"),
    stat(fmt(located), "resources with matched data located"),
    stat(fmt(represented), "cancer types represented"),
  ].join("");

  const rows = pages.map(c => {
    const list = spatialResourcesFor(d, c);
    const nLoc = list.filter(x => x.status === "verified").length;
    const url = `explore.html?view=cohorts&layer=matched-spatial&cancer=${[c.code, ...(c.includes || [])].join(",")}`;
    return `<tr>
      <td class="primary" data-label="Cancer type"><div><a href="cancers.html?c=${c.code}#spatial">${esc(c.name)}</a> <span class="mono muted small">${c.code}</span>${c.includes ? `<span class="cell-sub">pooled: includes ${c.includes.join(" and ")}</span>` : ""}</div></td>
      <td class="num" data-label="Catalogued resources"><div>${list.length ? fmt(list.length) : '<span class="muted">None catalogued</span>'}</div></td>
      <td class="num" data-label="With matched data located"><div>${!list.length ? '<span class="muted">—</span>' : nLoc ? fmt(nLoc) : '<span class="muted">Verification pending</span>'}</div></td>
      <td data-label="Explore resources"><div>${list.length ? `<a href="${url}">View resources</a>` : '<span class="muted">—</span>'}</div></td>
    </tr>`;
  }).join("");
  document.getElementById("spatial-table").innerHTML = `<p class="small">Catalogued resources are all listed spatial studies and vendor examples, including those not yet verified and those that need an access request. A resource counts as having matched data located once its image and molecular files have been found; image registration and tissue QC may still be pending.</p>
    <div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Cancer type</th><th scope="col" class="num">Catalogued resources</th><th scope="col" class="num">With matched data located</th><th scope="col">Explore resources</th></tr></thead>
    <tbody>${rows}</tbody>
    <caption>The pooled colorectal and glioma rows reuse the resources of their constituent cancers, and some studies cover several cancers, so the rows should not be summed. The headline figures count each resource once.</caption>
  </table></div>`;
  const reviewed = spatial.filter(c => c.spatial_review?.route_review);
  const sections = reviewed.reduce((a, c) => a + (c.spatial_review.route_review.sections_with_matching_coordinates || 0), 0);
  document.getElementById("route-table").innerHTML = `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Open dependency</th><th scope="col" class="num">Resources</th><th scope="col">Explore</th></tr></thead>
    <tbody>${Object.entries(LABELS.routeState).map(([k, label]) => {
      const n = reviewed.filter(c => c.spatial_review.route_review.states.includes(k)).length;
      return `<tr><td class="primary" data-label="Open dependency"><div>${esc(label)}</div></td><td class="num" data-label="Resources"><div>${fmt(n)}</div></td>
        <td data-label="Explore"><div>${n ? `<a href="explore.html?view=cohorts&route=${k}">View resources</a>` : '<span class="muted">—</span>'}</div></td></tr>`;
    }).join("")}</tbody>
    <caption>${fmt(reviewed.length)} resources reviewed; a resource can have several open dependencies, so the rows are not added. ${fmt(sections)} tissue sections have expression barcodes that match their coordinates exactly, which is not a patient count or final QC. Each resource's status and next step are in its details in the data explorer.</caption>
  </table></div>`;
  document.getElementById("leads-list").innerHTML = `<ul class="notes">${(d.leads || []).map(x => `<li><a href="${esc(x.url)}" rel="noopener"><strong>${esc(x.label)}</strong></a>. ${esc(x.description)} <span class="muted">${esc(x.not_counted)}</span></li>`).join("")}</ul>`;
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
} catch (err) {
  showError(document.getElementById("spatial-table"), err);
}
