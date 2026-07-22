"""Load and query mock enterprise finance CSV data."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CSV_PATHS = [DATA_DIR / "q1.csv", DATA_DIR / "q2.csv"]


@dataclass(frozen=True)
class Record:
    quarter: str
    department: str
    category: str
    budget: float
    actual: float

    @property
    def variance(self) -> float:
        return self.actual - self.budget

    @property
    def variance_pct(self) -> float:
        if self.budget == 0:
            return 0.0
        return round((self.variance / self.budget) * 100, 1)


def _parse_row(row: dict[str, str]) -> Record:
    return Record(
        quarter=row["quarter"].strip(),
        department=row["department"].strip(),
        category=row["category"].strip(),
        budget=float(row["budget_usd"]),
        actual=float(row["actual_usd"]),
    )


def load_records(paths: list[Path] | None = None) -> list[Record]:
    paths = paths or CSV_PATHS
    records: list[Record] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as fh:
            records.extend(_parse_row(row) for row in csv.DictReader(fh))
    return records


class DataStore:
    def __init__(self, records: list[Record]) -> None:
        self._records = records

    def quarters(self) -> list[str]:
        return sorted({r.quarter for r in self._records})

    def categories(self) -> list[str]:
        return sorted({r.category for r in self._records})

    def filter(
        self,
        *,
        quarter: str | None = None,
        category: str | None = None,
        department: str | None = None,
    ) -> list[Record]:
        return [
            r
            for r in self._records
            if (quarter is None or r.quarter == quarter)
            and (category is None or r.category == category)
            and (department is None or r.department == department)
        ]

    def aggregate_by_category(self, quarter: str) -> list[dict]:
        totals: dict[str, dict[str, float]] = {}
        for r in self.filter(quarter=quarter):
            bucket = totals.setdefault(r.category, {"budget": 0.0, "actual": 0.0})
            bucket["budget"] += r.budget
            bucket["actual"] += r.actual

        rows = []
        for category, vals in totals.items():
            variance = vals["actual"] - vals["budget"]
            pct = 0.0 if vals["budget"] == 0 else round((variance / vals["budget"]) * 100, 1)
            rows.append(
                {
                    "category": category,
                    "budget": vals["budget"],
                    "actual": vals["actual"],
                    "variance": variance,
                    "variance_pct": pct,
                }
            )
        rows.sort(key=lambda x: x["variance"], reverse=True)
        return rows

    def quarter_totals(self, quarter: str) -> dict:
        rows = self.filter(quarter=quarter)
        budget = sum(r.budget for r in rows)
        actual = sum(r.actual for r in rows)
        variance = actual - budget
        pct = 0.0 if budget == 0 else round((variance / budget) * 100, 1)
        return {
            "quarter": quarter,
            "budget": budget,
            "actual": actual,
            "variance": variance,
            "variance_pct": pct,
        }

    def category_detail(self, quarter: str, category: str) -> dict:
        rows = sorted(
            self.filter(quarter=quarter, category=category),
            key=lambda r: r.variance,
            reverse=True,
        )
        budget = sum(r.budget for r in rows)
        actual = sum(r.actual for r in rows)
        variance = actual - budget
        pct = 0.0 if budget == 0 else round((variance / budget) * 100, 1)
        return {
            "quarter": quarter,
            "category": category,
            "budget": budget,
            "actual": actual,
            "variance": variance,
            "variance_pct": pct,
            "by_department": [
                {
                    "department": r.department,
                    "budget": r.budget,
                    "actual": r.actual,
                    "variance": r.variance,
                    "variance_pct": r.variance_pct,
                }
                for r in rows
            ],
        }

    def top_overrun(self, quarter: str) -> dict | None:
        rows = self.aggregate_by_category(quarter)
        return rows[0] if rows else None

    def quarter_over_quarter(self, category: str, from_quarter: str, to_quarter: str) -> dict:
        from_actual = sum(r.actual for r in self.filter(quarter=from_quarter, category=category))
        to_actual = sum(r.actual for r in self.filter(quarter=to_quarter, category=category))
        change = to_actual - from_actual
        pct = 0.0 if from_actual == 0 else round((change / from_actual) * 100, 1)
        return {
            "category": category,
            "from_quarter": from_quarter,
            "to_quarter": to_quarter,
            "from_actual": from_actual,
            "to_actual": to_actual,
            "change": change,
            "change_pct": pct,
        }


def get_store() -> DataStore:
    return DataStore(load_records())
