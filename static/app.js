const form = document.getElementById("searchForm");
const statusEl = document.getElementById("status");
const table = document.getElementById("results");
const tbody = table.querySelector("tbody");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusEl.textContent = "Buscando...";
  table.style.display = "none";
  tbody.innerHTML = "";

  const data = Object.fromEntries(new FormData(form));
  data.adults = Number(data.adults || 1);
  data.non_stop = form.elements["non_stop"].checked;
  if (!data.return_date) data.return_date = null;

  try {
    const res = await fetch("/flights/search/summary", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    });
    const json = await res.json();

    if (!json.ok) {
      statusEl.textContent = json.reason || "Error";
      return;
    }

    statusEl.textContent = `OK - ${json.offers.length} ofertas`;
    for (const o of json.offers) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${o.currency} ${o.price_total}</td>
        <td>${o.outbound_from} → ${o.outbound_to}</td>
        <td>${o.outbound_departure}</td>
        <td>${o.outbound_arrival}</td>
        <td>${o.outbound_stops}</td>
        <td>${(o.airlines || []).join(", ")}</td>
        <td>${o.duration}</td>
      `;
      tbody.appendChild(tr);
    }
    table.style.display = "";
  } catch (err) {
    statusEl.textContent = "Error en fetch: " + err;
  }
});
