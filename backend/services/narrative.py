"""Build executive slide copy from computed finance data."""

from __future__ import annotations

import json
import os
from typing import Any

from .data import DataStore
from .prompt_parser import ParsedPrompt


def _usd(amount: float) -> str:
    return f"${amount:,.0f}"


def _template_narrative(store: DataStore, parsed: ParsedPrompt) -> dict[str, Any]:
    totals = store.quarter_totals(parsed.quarter)
    focus = store.category_detail(parsed.quarter, parsed.category)
    top = store.top_overrun(parsed.quarter)
    qoq = None
    quarters = store.quarters()
    if len(quarters) >= 2 and parsed.quarter == quarters[-1]:
        qoq = store.quarter_over_quarter(parsed.category, quarters[-2], quarters[-1])

    dept_lines = focus["by_department"][:4]
    dept_bullets = [
        f"{row['department']}: {_usd(row['actual'])} actual vs {_usd(row['budget'])} budget "
        f"({row['variance_pct']:+.1f}%)"
        for row in dept_lines
    ]

    category_bullets = []
    for row in store.aggregate_by_category(parsed.quarter)[:5]:
        category_bullets.append(
            f"{row['category']}: {_usd(row['variance'])} variance ({row['variance_pct']:+.1f}%)"
        )

    recommendation = (
        f"Initiate a cross-functional review of {parsed.category.lower()} spend in "
        f"{parsed.quarter}, prioritizing departments with the largest overruns."
    )
    if focus["variance"] > 0:
        recommendation += " Consider re-baselining Q3 budgets and tightening approval gates."

    slides = [
        {
            "title": f"{parsed.quarter} Finance Review — {parsed.category}",
            "subtitle": "DeckGen AI · Executive Brief for HQ Leadership",
            "bullets": [],
        },
        {
            "title": f"{parsed.quarter} spend landed {_usd(totals['variance'])} vs plan",
            "subtitle": f"Total budget {_usd(totals['budget'])} · Actual {_usd(totals['actual'])}",
            "bullets": [
                f"Portfolio variance: {totals['variance_pct']:+.1f}% ({_usd(totals['variance'])})",
                f"Largest overrun category: {top['category']} at {_usd(top['variance'])} "
                f"({top['variance_pct']:+.1f}%)"
                if top
                else "No category overruns detected.",
                f"Focus area for this deck: {parsed.category}",
            ],
        },
        {
            "title": f"{parsed.category} drove a {_usd(focus['variance'])} overrun in {parsed.quarter}",
            "subtitle": f"Budget {_usd(focus['budget'])} · Actual {_usd(focus['actual'])} "
            f"({focus['variance_pct']:+.1f}%)",
            "bullets": dept_bullets
            or ["No departmental breakdown available for this category."],
        },
        {
            "title": "Recommended actions for HQ",
            "subtitle": "Generated from enterprise finance data",
            "bullets": [
                recommendation,
                *category_bullets[:3],
                (
                    f"{parsed.category} spend grew {qoq['change_pct']:+.1f}% "
                    f"from {qoq['from_quarter']} to {qoq['to_quarter']} "
                    f"({_usd(qoq['from_actual'])} → {_usd(qoq['to_actual'])})."
                    if qoq
                    else "Quarter-over-quarter trend unavailable for this selection."
                ),
            ],
        },
    ]

    return {
        "slides": slides,
        "meta": {
            "quarter": parsed.quarter,
            "category": parsed.category,
            "source": "template",
        },
    }


def _openai_narrative(store: DataStore, parsed: ParsedPrompt) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    context = {
        "prompt": parsed.raw_prompt,
        "quarter_totals": store.quarter_totals(parsed.quarter),
        "category_detail": store.category_detail(parsed.quarter, parsed.category),
        "top_categories": store.aggregate_by_category(parsed.quarter)[:5],
    }

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You write concise executive PowerPoint slide copy for finance leadership. "
                    "Return JSON with shape: "
                    '{"slides":[{"title":"...","subtitle":"...","bullets":["..."]}]} '
                    "Use exactly 4 slides: title, quarter overview, focus category drill-down, "
                    "and recommendations. Keep bullets short and numeric where possible."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(context),
            },
        ],
    )

    payload = json.loads(response.choices[0].message.content or "{}")
    payload["meta"] = {
        "quarter": parsed.quarter,
        "category": parsed.category,
        "source": "openai",
    }
    return payload


def build_narrative(store: DataStore, parsed: ParsedPrompt) -> dict[str, Any]:
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return _openai_narrative(store, parsed)
        except Exception:
            pass
    return _template_narrative(store, parsed)
