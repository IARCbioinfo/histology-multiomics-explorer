import { loadData, esc, setFooter, showError } from "./common.js";

try {
  const d = await loadData();
  setFooter(d);
  document.getElementById("evidence-list").innerHTML = `<ul class="notes">${d.evidence.map(e => `<li><strong>${esc(e.short)}.</strong> ${esc(e.definition)}
    <span class="cell-sub">${esc(e.citation)} <a href="${esc(e.url)}" rel="noopener">doi:${esc(e.doi)}</a> · Cancer pages: ${e.cancers.map(c => `<a href="cancers.html?c=${esc(c)}">${esc(c)}</a>`).join(", ")}</span></li>`).join("")}</ul>
    <p class="muted small">Each cancer page shows the finding for that cancer and its limits.</p>`;
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
} catch (err) {
  showError(document.getElementById("evidence-list"), err);
}
