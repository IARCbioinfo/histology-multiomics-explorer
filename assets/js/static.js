import { loadData, setFooter, screenTable } from "./common.js";

loadData().then(d => {
  setFooter(d);
  const el = document.getElementById("screen-table");
  if (el) el.innerHTML = screenTable(d);
}).catch(() => {});
