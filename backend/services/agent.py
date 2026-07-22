"""Text-to-SQL agent over the finance data.

Uses an OpenAI-compatible endpoint (LLMFoundry by default). The model is given a
`finance` SQLite table and writes its own read-only SQL to fetch exactly the data
it needs, then returns a structured review + 5-6 slide outline. If no token is
configured (or the call fails), callers fall back to the deterministic template.
"""

from __future__ import annotations

import json
import os
import sqlite3
from typing import Any

from .data import DataStore

BASE_URL = os.environ.get("LLMFOUNDRY_BASE_URL", "https://llmfoundry.straive.com/openai/v1")
MODEL = os.environ.get("LLMFOUNDRY_MODEL", "gpt-4o-mini")

MAX_ROWS = 200  # cap rows returned to the model per query


def _token() -> str | None:
    return os.environ.get("LLMFOUNDRY_TOKEN") or os.environ.get("OPENAI_API_KEY")


def llm_available() -> bool:
    return bool(_token())


def _client():
    from openai import OpenAI

    return OpenAI(api_key=_token(), base_url=BASE_URL)


SCHEMA = (
    "TABLE finance  (one row per department × category × quarter)\n"
    "  quarter       TEXT   -- e.g. 'Q1', 'Q2'\n"
    "  department    TEXT   -- e.g. 'Engineering'\n"
    "  category      TEXT   -- spend category, e.g. 'Software Infrastructure'\n"
    "  budget        REAL   -- planned spend in USD\n"
    "  actual        REAL   -- actual spend in USD\n"
    "  variance      REAL   -- actual - budget (positive = OVER budget)\n"
    "  variance_pct  REAL   -- percent over/under budget for that row\n"
    "SQLite dialect. Aggregate with SUM(...) and GROUP BY. For an aggregated percent use "
    "ROUND((SUM(actual)-SUM(budget))*100.0/SUM(budget), 1)."
)

# ---------------------------------------------------------------- tools
TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_schema",
            "description": "Return the finance table schema plus the distinct quarters and categories available.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": (
                "Run a single READ-ONLY SQL SELECT query against the `finance` table and return "
                "the rows. Only SELECT/WITH statements are allowed. Use this to fetch exactly the "
                "data you need (totals, variances, top overruns, quarter-over-quarter, etc.)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A single SQLite SELECT statement (no semicolons, no writes).",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def _run_sql(conn: sqlite3.Connection, query: str) -> dict[str, Any]:
    q = (query or "").strip().rstrip(";").strip()
    low = q.lower()
    if not (low.startswith("select") or low.startswith("with")):
        return {"error": "Only read-only SELECT (or WITH ... SELECT) queries are allowed."}
    if ";" in q:
        return {"error": "Only a single statement is allowed (remove the semicolon)."}
    forbidden = ("insert", "update", "delete", "drop", "alter", "create", "attach", "pragma", "replace", "vacuum")
    if any(word in low for word in forbidden):
        return {"error": "Write/DDL keywords are not allowed; use a plain SELECT."}
    try:
        cur = conn.execute(q)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchmany(MAX_ROWS)
        return {
            "columns": cols,
            "rows": [dict(zip(cols, r)) for r in rows],
            "row_count": len(rows),
            "truncated": len(rows) == MAX_ROWS,
        }
    except Exception as exc:  # noqa: BLE001
        return {"error": f"SQL error: {exc}"}


def _dispatch(conn: sqlite3.Connection, name: str, args: dict[str, Any]) -> Any:
    if name == "get_schema":
        quarters = [r[0] for r in conn.execute("SELECT DISTINCT quarter FROM finance ORDER BY quarter")]
        categories = [r[0] for r in conn.execute("SELECT DISTINCT category FROM finance ORDER BY category")]
        return {"schema": SCHEMA, "quarters": quarters, "categories": categories}
    if name == "run_sql":
        return _run_sql(conn, args.get("query", ""))
    return {"error": f"unknown tool {name}"}


SYSTEM_PROMPT = (
    "You are DeckGen AI, an autonomous finance analyst for GCC / CFO leadership. "
    "A user asks a plain-English question about enterprise budget-vs-actual data. "
    "You have a SQLite table called `finance`. First call get_schema to learn the columns "
    "and the available quarters/categories, then write your own read-only SQL via run_sql to "
    "fetch EXACTLY the numbers you need — totals, per-category variances, per-department detail, "
    "top overruns, quarter-over-quarter trends, etc. Issue as many queries as you need and reason "
    "step by step. Never invent figures; every number must come from a query result."
)

FINAL_INSTRUCTION = (
    "You now have all the data you need. Respond with ONLY a JSON object (no prose) of shape:\n"
    "{\n"
    '  "headline": "one-line executive takeaway",\n'
    '  "quarter": "the primary quarter analyzed, e.g. Q2",\n'
    '  "category": "the primary focus category",\n'
    '  "review": ["3-5 short, numeric finding bullets for on-screen review"],\n'
    '  "slides": [\n'
    '    {"title": "...", "subtitle": "...", "bullets": ["..."]}\n'
    "  ]\n"
    "}\n"
    "Produce EXACTLY 5 or 6 slides in this order: (1) title slide (bullets may be empty), "
    "(2) quarter overview, (3) focus-category drill-down by department, "
    "(4) quarter-over-quarter / trend, (5) recommended actions, and optionally (6) appendix or risks. "
    "Keep bullets short and numeric. Use $ and % formatting. Base every number on your SQL results."
)


def _serialize_tool_calls(tool_calls) -> list[dict[str, Any]]:
    return [
        {
            "id": tc.id,
            "type": "function",
            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
        }
        for tc in tool_calls
    ]


def run_agent(prompt: str, store: DataStore, *, max_steps: int = 8) -> dict[str, Any]:
    """Run the text-to-SQL tool-calling loop and return the review + slide payload.

    Raises on any failure so the caller can fall back to the template narrative.
    """
    client = _client()
    conn = store.to_sqlite()
    try:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        for _ in range(max_steps):
            resp = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.2,
            )
            msg = resp.choices[0].message
            if not msg.tool_calls:
                messages.append({"role": "assistant", "content": msg.content or ""})
                break

            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": _serialize_tool_calls(msg.tool_calls),
                }
            )
            for tc in msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                result = _dispatch(conn, tc.function.name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result, default=float),
                    }
                )

        # Force a final structured JSON answer (no tools this time).
        messages.append({"role": "user", "content": FINAL_INSTRUCTION})
        final = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        payload = json.loads(final.choices[0].message.content or "{}")
    finally:
        conn.close()

    slides = payload.get("slides") or []
    if not slides:
        raise ValueError("Agent returned no slides")

    payload["meta"] = {
        "quarter": payload.get("quarter", ""),
        "category": payload.get("category", ""),
        "source": "agent",
    }
    return payload
