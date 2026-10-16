import { loadData, esc, fmt, setFooter, showError, spatialResourcesFor, LABELS, tally, countedPreview, chip } from "./common.js";

try {
  const d = await loadData();
  setFooter(d);
  const spatial = d.cohorts.filter(c => c.layer === "matched-spatial");
  const located = spatial.filter(c => c.status === "verified").length, preview = spatial.filter(c => c.status === "preview").length;
  const caps = d.captures, counted = spatial.reduce((a, c) => a + countedPreview(d, c), 0);
  const secOrig = caps.filter(x => x.image_level === "original"), secPrev = caps.filter(x => x.image_level === "preview");
  const pages = d.cancers.filter(c => c.group !== "aggregate" && c.group !== "excluded");
  // Cancer types represented: each resource's cancers, counting pooled colorectal and glioma pages through their constituents.
  const codes = new Set(spatial.flatMap(c => c.cancers));
  for (const p of pages.filter(p => p.includes)) if (codes.has(p.code) && p.includes.some(k => codes.has(k))) codes.delete(p.code);
  const represented = pages.filter(p => !p.includes && codes.has(p.code)).length + pages.filter(p => p.includes && codes.has(p.code)).length;
  const stat = (value, label) => `<div class="stat"><div class="value">${value}</div><div class="label">${label}</div></div>`;
  document.getElementById("stats").innerHTML = [
    stat(fmt(spatial.length), "catalogued spatial resources"),
    stat(fmt(located), "resources with original H&amp;E located"),
    stat(fmt(preview), "more with matched data and a preview image"),
    stat(fmt(secOrig.length), "tissue sections with original H&amp;E"),
    stat(fmt(secPrev.length + counted), "tissue sections with a preview image"),
    stat(fmt(represented), "cancer types represented"),
  ].join("");

  const rows = pages.map(c => {
    const list = spatialResourcesFor(d, c);
    const nLoc = list.filter(x => x.status === "verified").length, nPrev = list.filter(x => x.status === "preview").length;
    const url = `explore.html?view=cohorts&layer=matched-spatial&cancer=${[c.code, ...(c.includes || [])].join(",")}`;
    return `<tr>
      <td class="primary" data-label="Cancer type"><div><a href="cancers.html?c=${c.code}#spatial">${esc(c.name)}</a> <span class="mono muted small">${c.code}</span>${c.includes ? `<span class="cell-sub">pooled: includes ${c.includes.join(" and ")}</span>` : ""}</div></td>
      <td class="num" data-label="Catalogued resources"><div>${list.length ? fmt(list.length) : '<span class="muted">None catalogued</span>'}</div></td>
      <td class="num" data-label="Original H&amp;E located"><div>${!list.length ? '<span class="muted">—</span>' : fmt(nLoc)}</div></td>
      <td class="num" data-label="Matched data with preview image"><div>${!list.length ? '<span class="muted">—</span>' : fmt(nPrev)}</div></td>
      <td data-label="Explore resources"><div>${list.length ? `<a href="${url}">View resources</a>` : '<span class="muted">—</span>'}</div></td>
    </tr>`;
  }).join("");
  document.getElementById("spatial-table").innerHTML = `<p class="small">Catalogued resources are all listed spatial studies and vendor examples, including those not yet verified and those that need an access request. A resource with matched data counts once, at its best <a href="#levels">image level</a>; registration, calibration and tissue QC may still be pending at either level.</p>
    <div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Cancer type</th><th scope="col" class="num">Catalogued resources</th><th scope="col" class="num">Original H&amp;E located</th><th scope="col" class="num">Matched data with preview image</th><th scope="col">Explore resources</th></tr></thead>
    <tbody>${rows}</tbody>
    <caption>Counts are resources, not patients. The pooled colorectal and glioma rows reuse the resources of their constituent cancers, and some studies cover several cancers, so the rows should not be summed. The headline figures count each resource once.</caption>
  </table></div>`;
  // Image levels: resources, section records and known patients.
  const lv = (label, tone, res, secs, extra) => `<tr><td class="primary" data-label="Level"><div>${chip("imageLevel", tone, label)}</div></td>
    <td class="num" data-label="Resources"><div>${fmt(res)}</div></td><td class="num" data-label="Section records"><div>${fmt(secs.length + (extra || 0))}${extra ? `<span class="cell-sub">${fmt(secs.length)} listed one by one, ${fmt(extra)} counted for their study</span>` : ""}</div></td>
    <td class="num" data-label="Known patients"><div>${fmt(tally(secs).patients)}</div></td><td class="num" data-label="Sections without a patient ID"><div>${fmt(tally(secs).unknown)}</div></td></tr>`;
  document.getElementById("levels-counts").innerHTML = `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Image level</th><th scope="col" class="num">Resources</th><th scope="col" class="num">Section records</th><th scope="col" class="num">Known patients</th><th scope="col" class="num">Sections without a patient ID</th></tr></thead>
    <tbody>${lv(LABELS.imageLevel.original, "original", located, secOrig)}${lv(LABELS.imageLevel.preview, "preview", preview, secPrev, counted)}</tbody>
    <caption>Resources count at their best level, so a resource with both original and preview sections is counted once under original H&amp;E and its preview sections are counted under the preview level. ${fmt(tally(caps).patients)} known study-local patients in all; they are not eligible patients, and checked packages counted for their study add no patients.</caption>
  </table></div>`;

  // Package review: outcome of each candidate checked file by file.
  const pkg = spatial.filter(c => c.backlog_review);
  const outcomes = Object.keys(LABELS.backlogOutcome).map(k => [k, pkg.filter(c => c.backlog_review.outcome === k)]).filter(([, l]) => l.length);
  document.getElementById("package-table").innerHTML = `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Result</th><th scope="col" class="num">Resources</th><th scope="col">Now shown as</th><th scope="col">Explore</th></tr></thead>
    <tbody>${outcomes.map(([k, l]) => `<tr><td class="primary" data-label="Result"><div>${esc(LABELS.backlogOutcome[k])}</div></td><td class="num" data-label="Resources"><div>${fmt(l.length)}</div></td>
      <td data-label="Now shown as"><div>${esc([...new Set(l.map(c => LABELS.status[c.status]))].join("; "))}</div></td>
      <td data-label="Explore"><div><a href="explore.html?view=cohorts&outcome=${k}">View resources</a></div></td></tr>`).join("")}</tbody>
    <caption>${fmt(pkg.length)} resources reviewed. Results describe what the public records and packages showed, not the scientific value of a study. Each resource's image and molecular findings and its next step are in its details in the data explorer.</caption>
  </table></div>`;

  // Open dependencies from both reviews.
  const statesOf = c => c.backlog_review?.states || c.spatial_review?.route_review?.states || [];
  const reviewed = spatial.filter(c => statesOf(c).length);
  const sections = spatial.reduce((a, c) => a + (c.spatial_review?.route_review?.sections_with_matching_coordinates || 0), 0);
  document.getElementById("route-table").innerHTML = `<div class="table-wrap"><table class="stack compact">
    <thead><tr><th scope="col">Open dependency</th><th scope="col" class="num">Resources</th><th scope="col">Explore</th></tr></thead>
    <tbody>${Object.entries(LABELS.routeState).map(([k, label]) => {
      const n = reviewed.filter(c => statesOf(c).includes(k)).length;
      return `<tr><td class="primary" data-label="Open dependency"><div>${esc(label)}</div></td><td class="num" data-label="Resources"><div>${fmt(n)}</div></td>
        <td data-label="Explore"><div>${n ? `<a href="explore.html?view=cohorts&route=${k}">View resources</a>` : '<span class="muted">—</span>'}</div></td></tr>`;
    }).join("")}</tbody>
    <caption>${fmt(reviewed.length)} resources reviewed (${fmt(reviewed.filter(c => c.spatial_review).length)} in the public-route review and ${fmt(pkg.length)} in the package review); a resource can have several open dependencies, so the rows are not added. In the public-route review, ${fmt(sections)} tissue sections have expression barcodes that match their coordinates exactly, which is not a patient count or final QC.</caption>
  </table></div>`;
  document.getElementById("leads-list").innerHTML = `<ul class="notes">${(d.leads || []).map(x => `<li><a href="${esc(x.url)}" rel="noopener"><strong>${esc(x.label)}</strong></a>. ${esc(x.description)} <span class="muted">${esc(x.not_counted)}</span></li>`).join("")}</ul>`;
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
} catch (err) {
  showError(document.getElementById("spatial-table"), err);
}
