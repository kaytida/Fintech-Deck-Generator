/*
 * DeckGen AI — Demo tab
 * Drives the plain-English → deck flow against the FastAPI backend:
 *   POST /api/preview        → analysis + slide outline (for on-screen summary)
 *   POST /api/generate-deck  → downloadable .pptx
 * The backend is served from the same origin, so API === window.location.origin.
 */

(function () {
  "use strict";

  const API = window.location.origin;

  const SUGGESTIONS = [
    "Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ",
    "Create an executive deck on our Q2 cloud compute cost spike",
    "Summarize Q1 vs Q2 budget vs actual performance for leadership",
  ];

  const PIPELINE = [
    "Parsing your request",
    "Querying enterprise finance database",
    "Calculating budget vs. actual variances",
    "Running financial strategy analysis",
    "Synthesizing executive narrative",
    "Generating PowerPoint deck",
  ];

  // --- element refs ---
  const inputEl = document.getElementById("prompt-input");
  const sendBtn = document.getElementById("send-btn");
  const suggestionsEl = document.getElementById("suggestions");
  const agentPanel = document.getElementById("agent-panel");
  const agentSteps = document.getElementById("agent-steps");
  const agentStatus = document.getElementById("agent-status");
  const resultEl = document.getElementById("result");
  const resultBody = document.getElementById("result-body");
  const deckTitleLabel = document.getElementById("deck-title-label");
  const downloadBtn = document.getElementById("download-btn");
  const regenBtn = document.getElementById("regen-btn");
  const apiError = document.getElementById("api-error");

  let busy = false;
  let lastPrompt = "";

  // --- helpers ---
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const usd = (n) => "$" + Math.round(Number(n)).toLocaleString();
  const pct = (n) => `${Number(n) > 0 ? "+" : ""}${Number(n).toFixed(1)}%`;

  function renderSuggestions() {
    SUGGESTIONS.forEach((text) => {
      const chip = document.createElement("button");
      chip.className = "chip";
      chip.textContent = text.length > 46 ? text.slice(0, 46) + "…" : text;
      chip.title = text;
      chip.addEventListener("click", () => {
        inputEl.value = text;
        submit();
      });
      suggestionsEl.appendChild(chip);
    });
  }

  function renderPipeline(activeIndex) {
    agentSteps.innerHTML = PIPELINE.map((label, j) => {
      let cls = "agent-step";
      let icon = "○";
      if (j < activeIndex) {
        cls += " done";
        icon = "✓";
      } else if (j === activeIndex) {
        cls += " active";
        icon = "●";
      }
      return `<li class="${cls}"><span class="step-icon">${icon}</span>${label}${
        j === activeIndex ? "…" : ""
      }</li>`;
    }).join("");
  }

  function renderPipelineDone() {
    agentSteps.innerHTML = PIPELINE.map(
      (label) => `<li class="agent-step done"><span class="step-icon">✓</span>${label}</li>`
    ).join("");
  }

  function buildSummary(data) {
    const t = data.quarter_totals;
    const f = data.category_detail;

    let html = `<div class="analysis">`;
    html += `<h3 class="analysis-title">${data.quarter} Analysis — ${data.category}</h3>`;

    // KPI cards
    html += `<div class="kpi-row">`;
    html += `<div class="kpi"><span class="kpi-label">Portfolio actual</span><span class="kpi-value">${usd(
      t.actual
    )}</span><span class="kpi-sub">vs ${usd(t.budget)} budget</span></div>`;
    html += `<div class="kpi ${t.variance > 0 ? "bad" : "good"}"><span class="kpi-label">Portfolio variance</span><span class="kpi-value">${usd(
      t.variance
    )}</span><span class="kpi-sub">${pct(t.variance_pct)}</span></div>`;
    html += `<div class="kpi ${f.variance > 0 ? "bad" : "good"}"><span class="kpi-label">${
      data.category
    }</span><span class="kpi-value">${usd(f.variance)}</span><span class="kpi-sub">${pct(
      f.variance_pct
    )} vs budget</span></div>`;
    html += `</div>`;

    // Department drill-down
    if (f.by_department && f.by_department.length) {
      html += `<table class="dept-table"><thead><tr><th>Department</th><th>Budget</th><th>Actual</th><th>Variance</th></tr></thead><tbody>`;
      f.by_department.slice(0, 5).forEach((d) => {
        html += `<tr><td>${d.department}</td><td>${usd(d.budget)}</td><td>${usd(
          d.actual
        )}</td><td class="${d.variance > 0 ? "bad" : "good"}">${usd(d.variance)} (${pct(
          d.variance_pct
        )})</td></tr>`;
      });
      html += `</tbody></table>`;
    }

    // Slide outline
    if (data.slides && data.slides.length) {
      html += `<div class="slide-outline"><h4>Generated deck · ${data.slides.length} slides</h4><ol>`;
      data.slides.forEach((s) => {
        html += `<li><strong>${s.title}</strong>${
          s.subtitle ? `<span class="slide-sub">${s.subtitle}</span>` : ""
        }</li>`;
      });
      html += `</ol></div>`;
    }

    const src = data.narrative_source === "openai" ? "AI-generated narrative" : "Template narrative";
    html += `<p class="source-tag">Narrative source: ${src}</p>`;
    html += `</div>`;
    return html;
  }

  function resetView() {
    resultEl.hidden = true;
    agentPanel.hidden = true;
    apiError.hidden = true;
    resultBody.innerHTML = "";
    inputEl.focus();
  }

  async function submit() {
    const prompt = (inputEl.value || "").trim();
    if (!prompt || busy) return;
    if (prompt.length < 8) {
      apiError.hidden = false;
      apiError.textContent = "Please enter a more descriptive request (at least 8 characters).";
      return;
    }

    busy = true;
    sendBtn.disabled = true;
    lastPrompt = prompt;
    apiError.hidden = true;
    resultEl.hidden = true;

    // show pipeline
    agentPanel.hidden = false;
    agentStatus.textContent = "DeckGen agent is working…";
    for (let i = 0; i < PIPELINE.length; i++) {
      renderPipeline(i);
      await sleep(i === 0 ? 220 : 360);
    }

    try {
      const res = await fetch(`${API}/api/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      renderPipelineDone();
      agentStatus.textContent = "Analysis complete.";

      deckTitleLabel.textContent = `${data.quarter} · ${data.category}`;
      resultBody.innerHTML = buildSummary(data);
      resultEl.hidden = false;
      agentPanel.hidden = true;
    } catch (err) {
      agentPanel.hidden = true;
      apiError.hidden = false;
      apiError.textContent =
        "Something went wrong reaching the DeckGen API. Make sure the backend server is running. " +
        (err && err.message ? `(${err.message})` : "");
    } finally {
      busy = false;
      sendBtn.disabled = false;
    }
  }

  async function downloadDeck() {
    if (!lastPrompt) return;
    const original = downloadBtn.textContent;
    downloadBtn.disabled = true;
    downloadBtn.textContent = "Building .pptx…";
    try {
      const res = await fetch(`${API}/api/generate-deck`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: lastPrompt }),
      });
      if (!res.ok) throw new Error(await res.text());
      const blob = await res.blob();
      const disposition = res.headers.get("Content-Disposition") || "";
      const match = disposition.match(/filename="(.+)"/);
      const filename = match ? match[1] : "deckgen-deck.pptx";
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
      URL.revokeObjectURL(a.href);
    } catch (err) {
      apiError.hidden = false;
      apiError.textContent = "Could not generate the .pptx. " + (err && err.message ? `(${err.message})` : "");
    } finally {
      downloadBtn.disabled = false;
      downloadBtn.textContent = original;
    }
  }

  // --- events ---
  sendBtn.addEventListener("click", submit);
  downloadBtn.addEventListener("click", downloadDeck);
  regenBtn.addEventListener("click", resetView);

  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  });

  renderSuggestions();
})();
