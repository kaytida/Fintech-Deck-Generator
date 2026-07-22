const API = window.location.origin;

const WELCOME =
  "Hi — <strong>we can help you generate insights</strong> from your enterprise finance data.<br><br>" +
  "Ask me to explain a variance, summarize a quarter, or build a boardroom deck for HQ. " +
  "I'll query your budget vs. actual data, run the financial analysis, and deliver executive-ready output.<br><br>" +
  "<em>Try: Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ.</em>";

const SUGGESTIONS = [
  "Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ.",
  "What's driving the Q2 cloud compute variance?",
  "Summarize Q2 marketing overrun for DTC growth leadership.",
];

const PIPELINE = [
  "Parsing your request",
  "Querying enterprise finance database",
  "Calculating budget vs. actual variances",
  "Running financial strategy analysis",
  "Synthesizing executive narrative",
  "Generating PowerPoint deck",
];

const messagesEl = document.getElementById("messages");
const suggestionsEl = document.getElementById("suggestions");
const inputEl = document.getElementById("prompt-input");
const sendBtn = document.getElementById("send-btn");

let busy = false;
let lastPrompt = "";

function usd(n) {
  return "$" + Math.round(n).toLocaleString();
}

function addMessage(role, html) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="avatar">${role === "assistant" ? "AI" : "You"}</div>
    <div class="bubble">${html}</div>
  `;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div.querySelector(".bubble");
}

function renderSuggestions() {
  suggestionsEl.innerHTML = "";
  SUGGESTIONS.forEach((text) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.textContent = text.length > 52 ? text.slice(0, 52) + "…" : text;
    chip.title = text;
    chip.onclick = () => {
      inputEl.value = text;
      submit();
    };
    suggestionsEl.appendChild(chip);
  });
}

function buildSummary(data) {
  const t = data.quarter_totals;
  const f = data.category_detail;
  let html = `<h3>${data.quarter} Analysis — ${data.category}</h3>`;
  html += `<p><strong>Portfolio:</strong> ${usd(t.actual)} actual vs ${usd(t.budget)} budget `;
  html += `(${usd(t.variance)} variance, ${t.variance_pct > 0 ? "+" : ""}${t.variance_pct}%)</p>`;
  html += `<p><strong>Focus area:</strong> ${data.category} at ${usd(f.actual)} vs ${usd(f.budget)} budget (${f.variance_pct > 0 ? "+" : ""}${f.variance_pct}%)</p>`;
  html += `<p><strong>Your deck is ready</strong> — 4 slides with overview, drill-down, and HQ recommendations.</p>`;
  if (data.slides?.length) {
    html += "<p>";
    data.slides.forEach((s, i) => {
      html += `<strong>Slide ${i + 1}:</strong> ${s.title}<br>`;
    });
    html += "</p>";
  }
  return html;
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function submit() {
  const prompt = inputEl.value.trim();
  if (!prompt || busy) return;

  busy = true;
  sendBtn.disabled = true;
  suggestionsEl.classList.add("hidden");
  lastPrompt = prompt;
  inputEl.value = "";

  addMessage("user", prompt);

  const bubble = addMessage("assistant", '<div class="pipeline-steps" id="live-steps"></div>');
  const stepsEl = bubble.querySelector("#live-steps");

  for (let i = 0; i < PIPELINE.length; i++) {
    stepsEl.innerHTML = PIPELINE.map((label, j) => {
      let cls = "pipeline-step";
      if (j < i) cls += " done";
      else if (j === i) cls += " active";
      const icon = j < i ? "✓" : j === i ? "●" : "○";
      return `<div class="${cls}"><span class="dot"></span>${icon} ${label}${j === i ? "…" : ""}</div>`;
    }).join("");
    messagesEl.scrollTop = messagesEl.scrollHeight;
    await sleep(i === 0 ? 200 : 350);
  }

  try {
    const res = await fetch(`${API}/api/preview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    stepsEl.innerHTML = PIPELINE.map(
      (label) => `<div class="pipeline-step done"><span class="dot"></span>✓ ${label}</div>`
    ).join("");

    const summary = buildSummary(data);
    bubble.innerHTML = stepsEl.outerHTML + summary;

    const dlBtn = document.createElement("button");
    dlBtn.className = "btn-download";
    dlBtn.textContent = "⬇ Download PowerPoint (.pptx)";
    dlBtn.onclick = downloadDeck;
    bubble.appendChild(dlBtn);
  } catch (err) {
    bubble.innerHTML = `<p style="color:var(--red)">Something went wrong. Make sure the API server is running.<br><small>${err.message}</small></p>`;
  }

  messagesEl.scrollTop = messagesEl.scrollHeight;
  busy = false;
  sendBtn.disabled = false;
  suggestionsEl.classList.remove("hidden");
}

async function downloadDeck() {
  if (!lastPrompt) return;
  const res = await fetch(`${API}/api/generate-deck`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: lastPrompt }),
  });
  if (!res.ok) return;
  const blob = await res.blob();
  const disposition = res.headers.get("Content-Disposition") || "";
  const match = disposition.match(/filename="(.+)"/);
  const filename = match ? match[1] : "deckgen-deck.pptx";
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

sendBtn.addEventListener("click", submit);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submit();
  }
});

inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + "px";
});

addMessage("assistant", WELCOME);
renderSuggestions();
