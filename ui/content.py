"""Demo chat content, upload helpers, and canned responses."""

from __future__ import annotations

import pandas as pd

FAQ_ITEMS = [
    ("Spend last month?", "What is the spend looking from last month?"),
    ("Top variance drivers", "Show me the top drivers between the variance"),
    ("Duplicate payments?", "Were there any duplications been recorded in payments from last month"),
    ("Q2 budget variance", "What is the budget variance for Q2 software infrastructure?"),
    ("Headcount overrun", "Show me the headcount cost overrun analysis"),
    ("Cloud by vendor", "Generate a cloud spend breakdown by vendor"),
    ("Top 3 drivers", "What are the top 3 cost drivers this quarter?"),
    ("Dept budget status", "Which departments exceeded their budget?"),
]

RESPONSES = {
    "What is the spend looking from last month?": """**Last Month Spend Overview**

**Total actual:** $3,096,000
**Budget plan:** $2,400,000
**Variance:** +$696,000 (+29.0%)

**Breakdown:**
• Cloud & infrastructure: $1,420K (+18% vs plan)
• Personnel & headcount: $890K (+12% vs plan)
• Vendor licensing: $485K (+22% vs plan)

**Trend:** Spend accelerated in the final 2 weeks — cloud migration invoices landed late.""",

    "Show me the top drivers between the variance": """**Top Variance Drivers — Last Period**

**1. Cloud migration acceleration** (+$340K)
   Unbudgeted lift-and-shift; data transfer 3× estimate

**2. Vendor licensing renewal** (+$240K)
   Oracle +$180K · AWS reserved instances +$60K

**3. Engineering headcount** (+$157K)
   7 unplanned FTEs · avg $22.4K per hire

**Net impact:** $737K combined — explains 106% of total overrun""",

    "Were there any duplications been recorded in payments from last month": """**Payment Duplicate Scan — Last Period**

**Records scanned:** 4,218 payment transactions
**Potential duplicates flagged:** 2

• **Professional Services — Vendor ACME Consulting**
  Same invoice #4821 posted twice: $142K + $142K
  Status: 1 confirmed duplicate · 1 pending AP review

• **Recommendation:** Hold further disbursements until reconciliation complete

**Recovery opportunity:** ~$142K if duplicate confirmed""",

    "What is the budget variance for Q2 software infrastructure?": """Based on the Q2 financial data:

**Budget:** $2,400,000
**Actual:** $3,096,000
**Variance:** +$696,000 (+29% overrun)

**Key Drivers:**
• Cloud migration acceleration: +$340K (unbudgeted)
• Unplanned vendor licensing: +$240K (Oracle, AWS)
• Engineering headcount expansion: +$116K (15% increase)

**Status:** 🔴 Critical — exceeds 25% threshold""",

    "Show me the headcount cost overrun analysis": """**Headcount Cost Analysis — Q2 2024**

**Budgeted FTE:** 45 engineers
**Actual FTE:** 52 engineers (+15.6%)

**Cost Impact:**
• Additional salaries: $116K over budget
• Onboarding & equipment: $23K
• Benefits & overhead: $18K
• **Total overrun: $157K**

**Root Cause:**
3 unplanned hires for cloud migration project + 2 backfills for attrition without budget revision.""",

    "Generate a cloud spend breakdown by vendor": """**Cloud Spend Breakdown — Q2 2024**

| Vendor | Budget | Actual | Variance |
|--------|--------|--------|----------|
| AWS | $800K | $1,120K | +$320K 🔴 |
| Azure | $400K | $380K | -$20K 🟢 |
| GCP | $200K | $245K | +$45K 🟡 |
| Oracle Cloud | $150K | $195K | +$45K 🟡 |
| Others | $50K | $66K | +$16K 🟡 |

**Total Cloud:** $1,600K budget → $2,006K actual (+25.4%)""",

    "What are the top 3 cost drivers this quarter?": """**Top 3 Cost Drivers — Q2 2024**

**1. Cloud Migration Acceleration** (+$340K)
   • Unbudgeted lift-and-shift project
   • Data transfer costs exceeded estimates by 3x

**2. Vendor Licensing Renewal** (+$240K)
   • Oracle enterprise license: +$180K
   • AWS reserved instances: +$60K

**3. Engineering Headcount Growth** (+$157K)
   • 7 additional FTEs hired without budget approval
   • Average cost per hire: $22.4K""",

    "Compare actuals vs budget for Engineering": """**Engineering Department — Q2 Variance Report**

| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Personnel | $1.2M | $1.42M | +18.3% 🔴 |
| Cloud Infra | $600K | $890K | +48.3% 🔴 |
| Software | $300K | $385K | +28.3% 🔴 |
| Training | $50K | $42K | -16.0% 🟢 |
| Travel | $30K | $18K | -40.0% 🟢 |

**Total Engineering:** $2.18M budget → $2.755M actual (+26.4%)""",

    "Show variance trend month-over-month": """**Monthly Variance Trend — 2024**

```
Jan:  85%  ████████▌    🟢 Under budget
Feb: 120%  ████████████ 🔴 +20% overrun
Mar:  95%  █████████▌   🟢 Near target
Apr: 110%  ███████████  🟡 +10% overrun
May:  75%  ███████▌     🟢 Under budget
Jun: 130%  █████████████🔴 +30% overrun (Q2 peak)
```

**Trend:** Escalating variance in Q2, peak in June. Recommend immediate corrective action.""",

    "Which departments exceeded their budget?": """**Department Budget Status — Q2 2024**

🔴 **Over Budget:**
• Engineering: +26.4% ($575K over)
• IT Operations: +18.2% ($145K over)
• Product: +12.1% ($67K over)

🟡 **At Risk (90-100%):**
• Marketing: 98.3% utilized
• Sales: 94.7% utilized

🟢 **Under Budget:**
• HR: 72.5%
• Finance: 68.1%
• Legal: 55.3%""",

    "Generate CFO summary for board meeting": """**CFO Executive Summary — Q2 2024**

**Overall Financial Health:** ⚠️ Requires Attention

**Key Metrics:**
• Total Budget: $8.5M | Actual: $9.8M (+15.3%)
• Cash runway impact: -2.3 months
• Largest variance: Engineering (+$575K)

**Critical Actions Required:**
1. Approve emergency budget reallocation ($400K from Q3)
2. Mandate pre-approval for all vendor contracts >$50K
3. Freeze non-essential hiring until September

**Board Recommendation:** Schedule special budget review session within 14 days."""
}

EXPLORING = {
    "What is the spend looking from last month?": [
        "Connecting to <span class='exploring-detail'>enterprise_finance_db</span>… connected.",
        "Pulling last period spend from <span class='exploring-detail'>operational_budgets</span>…",
        "Total actual: <span class='exploring-detail'>$3,096,000</span> vs plan <span class='exploring-detail'>$2,400,000</span> (+29%).",
        "Breakdown by category — cloud, personnel, licensing…",
    ],
    "Show me the top drivers between the variance": [
        "Running variance decomposition across <span class='exploring-detail'>12</span> cost centers…",
        "Driver 1 — Cloud migration: <span class='exploring-detail'>+$340K</span>.",
        "Driver 2 — Vendor licensing: <span class='exploring-detail'>+$240K</span>.",
        "Driver 3 — Headcount growth: <span class='exploring-detail'>+$157K</span>.",
    ],
    "Were there any duplications been recorded in payments from last month": [
        "Connecting to <span class='exploring-detail'>accounts_payable</span> ledger… connected.",
        "Scanning <span class='exploring-detail'>4,218</span> payment transactions from last period…",
        "Flagged <span class='exploring-detail'>2 potential duplicates</span> in Professional Services.",
        "Cross-referencing invoice IDs… <span class='exploring-detail'>1 confirmed</span>, 1 pending review.",
    ],
    "What is the budget variance for Q2 software infrastructure?": [
        "Connecting to <span class='exploring-detail'>enterprise_finance_db</span>… connected.",
        "Scanning <span class='exploring-detail'>Q2</span> software infrastructure ledger — <span class='exploring-detail'>23</span> line items found.",
        "Budget: <span class='exploring-detail'>$2,400,000</span> · Actual: <span class='exploring-detail'>$3,096,000</span> · Variance: <span class='exploring-detail'>+29%</span>.",
        "Flagging critical threshold breach (>25%)…",
    ],
    "Show me the headcount cost overrun analysis": [
        "Connecting to <span class='exploring-detail'>HRMS + finance_db</span>… connected.",
        "Pulling headcount records — budgeted <span class='exploring-detail'>45 FTE</span>, actual <span class='exploring-detail'>52 FTE</span>.",
        "Cost impact: salaries <span class='exploring-detail'>+$116K</span>, onboarding <span class='exploring-detail'>+$23K</span>, benefits <span class='exploring-detail'>+$18K</span>.",
        "Total headcount overrun: <span class='exploring-detail'>$157K</span>.",
    ],
    "Generate a cloud spend breakdown by vendor": [
        "Connecting to <span class='exploring-detail'>cloud_billing_api</span>… connected.",
        "Pulling vendor invoices — AWS, Azure, GCP, Oracle Cloud…",
        "AWS: <span class='exploring-detail'>$1,120K</span> actual vs <span class='exploring-detail'>$800K</span> budget (+40%).",
        "Total cloud spend: <span class='exploring-detail'>$2,006K</span> vs <span class='exploring-detail'>$1,600K</span> plan (+25.4%).",
    ],
    "What are the top 3 cost drivers this quarter?": [
        "Running variance decomposition across <span class='exploring-detail'>12</span> cost centers…",
        "Driver 1 — Cloud migration: <span class='exploring-detail'>+$340K</span>.",
        "Driver 2 — Vendor licensing: <span class='exploring-detail'>+$240K</span>.",
        "Driver 3 — Headcount growth: <span class='exploring-detail'>+$157K</span>.",
    ],
    "Compare actuals vs budget for Engineering": [
        "Querying <span class='exploring-detail'>Engineering</span> department cost centers…",
        "Personnel: <span class='exploring-detail'>+18.3%</span> · Cloud: <span class='exploring-detail'>+48.3%</span> · Software: <span class='exploring-detail'>+28.3%</span>.",
        "Total Engineering: <span class='exploring-detail'>$2.755M</span> vs <span class='exploring-detail'>$2.18M</span> budget (+26.4%).",
    ],
    "Show variance trend month-over-month": [
        "Pulling monthly utilization series from <span class='exploring-detail'>Jan–Jun 2024</span>…",
        "Peak overrun detected in <span class='exploring-detail'>June: 130%</span> utilization.",
        "Trend: escalating variance in Q2 — corrective action recommended.",
    ],
    "Which departments exceeded their budget?": [
        "Scanning all department budgets vs actuals…",
        "Over budget: Engineering <span class='exploring-detail'>(+26.4%)</span>, IT Ops <span class='exploring-detail'>(+18.2%)</span>, Product <span class='exploring-detail'>(+12.1%)</span>.",
        "At risk: Marketing <span class='exploring-detail'>98.3%</span>, Sales <span class='exploring-detail'>94.7%</span> utilized.",
    ],
    "Generate CFO summary for board meeting": [
        "Aggregating portfolio-level metrics for board pack…",
        "Total: <span class='exploring-detail'>$9.8M</span> actual vs <span class='exploring-detail'>$8.5M</span> budget (+15.3%).",
        "Cash runway impact: <span class='exploring-detail'>-2.3 months</span>. Largest variance: Engineering <span class='exploring-detail'>+$575K</span>.",
    ],
}

DEFAULT_EXPLORING = [
    "Connecting to <span class='exploring-detail'>enterprise_finance_db</span>… connected.",
    "Parsing your question and mapping to cost centers…",
    "Running variance analysis across connected sources…",
    "Synthesizing executive summary…",
]

_DEFAULT_RESPONSE = """**Analysis Complete**

Based on your query, I analyzed the enterprise finance database:

**Key Findings:**
• Data retrieved from ERP, Cloud, and HRMS sources
• Variance analysis across 12 cost centers
• Critical anomalies flagged for review

*Click **Generate PPT** for the 6-slide executive deck.*"""


def load_upload(file) -> pd.DataFrame:
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    raise ValueError("Unsupported file type. Upload CSV or Excel.")


def summarize_upload(df: pd.DataFrame, filename: str) -> str:
    lines = [
        f"**Uploaded:** `{filename}`",
        f"**Rows:** {len(df):,} · **Columns:** {', '.join(df.columns[:6])}{'…' if len(df.columns) > 6 else ''}",
        "",
    ]
    budget_col = next((c for c in df.columns if "budget" in c.lower()), None)
    actual_col = next((c for c in df.columns if "actual" in c.lower()), None)
    if budget_col and actual_col:
        budget = pd.to_numeric(df[budget_col], errors="coerce").sum()
        actual = pd.to_numeric(df[actual_col], errors="coerce").sum()
        variance = actual - budget
        pct = (variance / budget * 100) if budget else 0
        lines += [
            f"**Total budget:** ${budget:,.0f}",
            f"**Total actual:** ${actual:,.0f}",
            f"**Variance:** ${variance:,.0f} ({pct:+.1f}%)",
            "",
        ]
    cat_col = next((c for c in df.columns if "category" in c.lower()), None)
    if cat_col and actual_col:
        top = df.groupby(cat_col)[actual_col].sum().sort_values(ascending=False).head(3)
        lines.append("**Top spend categories:**")
        for cat, val in top.items():
            lines.append(f"• {cat}: ${val:,.0f}")
        lines.append("")
    lines.append("*Click **Generate PPT** to build a 6-slide executive deck from this data.*")
    return "\n".join(lines)


def extract_upload_meta(df: pd.DataFrame, filename: str) -> dict:
    meta: dict = {"filename": filename, "budget": None, "actual": None, "top_categories": []}
    budget_col = next((c for c in df.columns if "budget" in c.lower()), None)
    actual_col = next((c for c in df.columns if "actual" in c.lower()), None)
    cat_col = next((c for c in df.columns if "category" in c.lower()), None)
    if budget_col:
        meta["budget"] = float(pd.to_numeric(df[budget_col], errors="coerce").sum())
    if actual_col:
        meta["actual"] = float(pd.to_numeric(df[actual_col], errors="coerce").sum())
    if cat_col and actual_col:
        top = df.groupby(cat_col)[actual_col].sum().sort_values(ascending=False).head(5)
        meta["top_categories"] = [(str(k), float(v)) for k, v in top.items()]
    return meta


def get_response(question: str, upload_summary: str | None) -> str:
    if question.startswith("__upload__:"):
        return upload_summary or "**Upload processed.**"
    return RESPONSES.get(question, _DEFAULT_RESPONSE)


def get_exploring_lines(question: str) -> list[str]:
    return EXPLORING.get(question, DEFAULT_EXPLORING)
