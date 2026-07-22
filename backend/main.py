"""DeckGen AI — FastAPI backend + static frontend."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from services.data import get_store
from services.narrative import build_narrative
from services.prompt_parser import parse_prompt
from services.pptx_builder import build_pptx

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

DEFAULT_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

extra_origins = [
    origin.strip()
    for origin in os.environ.get("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]

app = FastAPI(title="DeckGen AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*DEFAULT_ORIGINS, *extra_origins, "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str = Field(
        min_length=8,
        examples=[
            "Generate a 4-slide deck explaining our Q2 software infrastructure overrun for HQ."
        ],
    )


class PreviewResponse(BaseModel):
    quarter: str
    category: str
    narrative_source: str
    slides: list[dict[str, Any]]
    quarter_totals: dict[str, Any]
    category_detail: dict[str, Any]


@app.get("/api/health")
def health() -> dict[str, str]:
    store = get_store()
    return {
        "status": "ok",
        "quarters": ", ".join(store.quarters()),
    }


@app.post("/api/preview", response_model=PreviewResponse)
def preview_deck(body: GenerateRequest) -> PreviewResponse:
    store = get_store()
    parsed = parse_prompt(body.prompt, store)
    narrative = build_narrative(store, parsed)
    return PreviewResponse(
        quarter=parsed.quarter,
        category=parsed.category,
        narrative_source=narrative["meta"]["source"],
        slides=narrative["slides"],
        quarter_totals=store.quarter_totals(parsed.quarter),
        category_detail=store.category_detail(parsed.quarter, parsed.category),
    )


@app.post("/api/generate-deck")
def generate_deck(body: GenerateRequest) -> Response:
    store = get_store()
    parsed = parse_prompt(body.prompt, store)
    narrative = build_narrative(store, parsed)

    try:
        pptx_bytes = build_pptx(narrative, store, parsed.quarter)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to build deck: {exc}") from exc

    filename = f"deckgen-{parsed.quarter.lower()}-{parsed.category.lower().replace(' ', '-')}.pptx"
    return Response(
        content=pptx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/")
def serve_home() -> FileResponse:
    # Single-page app: Home and Demo are tabs within index.html.
    return FileResponse(FRONTEND_DIR / "index.html")


if FRONTEND_DIR.is_dir():
    app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
    app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
