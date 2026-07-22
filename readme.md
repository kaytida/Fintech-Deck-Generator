# DeckGen AI — INVENT' 26 Hackathon POC

**Hackathon Matrix:** [The Deal Closer](https://nsushanthkumar.github.io/rhapsody-hackathon/init_pitch.html) × **Financial Planning & Analysis (FP&A)**

Autonomous narrative reporting engine for **GCC FP&A teams** — turns plain-English variance questions into downloadable, boardroom-ready PowerPoint decks for offshore HQ leadership reviews.

## The story (for judges)

GCC clients in FP&A don't lack data — they lack **shareable insight**. Dashboards are too dense for executive calls. Chatbot answers can't be presented to HQ. Analysts burn 10–15 hours/month rebuilding slides.

**DeckGen AI** is the live demo that closes the deal: ask *"What's driving the Q2 software infrastructure overrun?"*, get the executive summary, click **Generate PPT**, walk into the HQ meeting with a data-driven deck.

| Axis | Selection |
|---|---|
| **Strategic Prompt** | D — *The Deal Closer* |
| **GCC Domain** | FP&A — automated variance analysis & narrative reporting |
| **Pain point** | Last-mile communication friction (GCC → HQ) |
| **Output** | Working Streamlit app + downloadable `.pptx` |

## Quick Start (Streamlit — primary UI)

```bash
pip install -r requirements.txt
py -m streamlit run app.py
```

Open **Home** for the pitch → **Demo** for the live chat (FAQs, upload, 6-slide PPT).

## Demo flow

1. Landing page frames the INVENT' 26 matrix pairing and GCC pain point
2. **Demo** opens a Kimi-style chat with FP&A FAQ questions
3. Click a question → variance summary from enterprise finance data
4. Click **Generate PPT** → auto-downloads a 4-slide executive deck

## Sample prompt

> Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ.

## Optional: FastAPI backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

- `GET /api/health`
- `POST /api/preview` — JSON preview (quarter, variances, slide copy)
- `POST /api/generate-deck` — downloadable `.pptx`

## Project structure

```
app.py              Streamlit app (Home + Demo) — primary submission UI
ui/                 Home pitch, Kimi-style demo chat, theme
backend/
  main.py           FastAPI API
  services/         Pipeline (parser, data, narrative, pptx)
data/               Mock media-industry finance CSVs (Q1, Q2)
```

## Hackathon context

Built for [INVENT' 26](https://nsushanthkumar.github.io/rhapsody-hackathon/init_pitch.html) — Gramener's 18-hour internal hackathon targeting real GCC client pain points sourced from Sales.
