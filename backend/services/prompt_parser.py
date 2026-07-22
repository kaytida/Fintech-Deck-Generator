"""Extract quarter and spend category from a plain-English deck request."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .data import DataStore


@dataclass(frozen=True)
class ParsedPrompt:
    quarter: str
    category: str
    raw_prompt: str


CATEGORY_ALIASES: dict[str, str] = {
    "software infrastructure": "Software Infrastructure",
    "software infra": "Software Infrastructure",
    "infrastructure": "Software Infrastructure",
    "cloud compute": "Cloud Compute",
    "cloud": "Cloud Compute",
    "headcount": "Headcount",
    "hardware": "Hardware",
    "licenses": "Licenses & Subscriptions",
    "subscriptions": "Licenses & Subscriptions",
    "licenses & subscriptions": "Licenses & Subscriptions",
    "training": "Training",
    "professional services": "Professional Services",
    "consulting": "Professional Services",
    "travel": "Travel",
    "marketing": "Marketing",
    "facilities": "Facilities",
}


def _detect_quarter(text: str, store: DataStore) -> str:
    lowered = text.lower()
    match = re.search(r"\bq([12])\b", lowered)
    if match:
        return f"Q{match.group(1)}"
    match = re.search(r"\bquarter\s*([12])\b", lowered)
    if match:
        return f"Q{match.group(1)}"

    quarters = store.quarters()
    return quarters[-1] if quarters else "Q2"


def _detect_category(text: str, store: DataStore) -> str:
    lowered = text.lower()
    for alias, canonical in sorted(CATEGORY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if alias in lowered:
            return canonical

    for category in store.categories():
        if category.lower() in lowered:
            return category

    top = store.top_overrun(_detect_quarter(text, store))
    return top["category"] if top else store.categories()[0]


def parse_prompt(prompt: str, store: DataStore) -> ParsedPrompt:
    quarter = _detect_quarter(prompt, store)
    category = _detect_category(prompt, store)
    return ParsedPrompt(quarter=quarter, category=category, raw_prompt=prompt.strip())
