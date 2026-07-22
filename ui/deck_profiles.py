"""Per-question PowerPoint deck content profiles."""

from __future__ import annotations

from typing import Any

# severity: "red" | "green" | "amber" | "accent"
_DEFAULT_PROFILE: dict[str, Any] = {
    "filename": "DeckGen_Executive_Summary.pptx",
    "s1_headline": "Q2 portfolio spend exceeded plan — immediate leadership review required.",
    "s1_number": "+15.3%",
    "s1_sub": "Total budget $8.5M → Actual $9.8M",
    "s2_bullets": [
        "Engineering: +26.4% vs budget ($575K over)",
        "IT Operations: +18.2% vs budget",
        "Cloud & infrastructure largest category overrun",
        "Peer GCC benchmark: 12% avg vs our 15.3%",
    ],
    "s2_chart_title": "Variance by Department",
    "s2_chart_bars": [("Engineering", 126), ("IT Ops", 118), ("Product", 112), ("Marketing", 98), ("HR", 72)],
    "s3_waterfall": [
        ("Baseline", "$8,500K", "accent"),
        ("Cloud", "+$340K", "red"),
        ("Headcount", "+$157K", "red"),
        ("Licensing", "+$240K", "red"),
        ("Savings", "-$180K", "green"),
        ("Net", "$9,800K", "red"),
    ],
    "s3_note": "Identified $180K recoverable via contract renegotiation.",
    "s4_audiences": [
        ("CFO", "Portfolio overrun of 15.3% compresses cash runway. Approve Q3 reallocation."),
        ("Ops Lead", "Engineering and IT Ops drive 80% of variance. Tighten monthly checkpoints."),
        ("Board", "Schedule emergency budget review within 14 days."),
    ],
    "s5_risks": [
        ("Cost escalation", "High", "High", "red"),
        ("Budget delay", "Medium", "High", "amber"),
        ("Headcount creep", "High", "Medium", "amber"),
        ("Vendor expiry", "Low", "Medium", "green"),
    ],
    "s6_steps": [
        "Approve Q3 budget reallocation",
        "Mandate vendor pre-approval >$50K",
        "Renegotiate cloud contracts",
        "Deploy real-time spend alerts",
        "Schedule board review within 14 days",
    ],
}

DECK_PROFILES: dict[str, dict[str, Any]] = {
    "What is the spend looking from last month?": {
        "filename": "DeckGen_Last_Month_Spend.pptx",
        "s1_headline": "Last month spend landed 29% above plan — cloud and licensing invoices drove the spike.",
        "s1_number": "$3.1M",
        "s1_sub": "Actual $3,096K vs budget $2,400K · +$696K variance",
        "s2_bullets": [
            "Cloud & infrastructure: $1,420K (+18% vs plan)",
            "Personnel & headcount: $890K (+12% vs plan)",
            "Vendor licensing: $485K (+22% vs plan)",
            "Spend accelerated in final 2 weeks of period",
        ],
        "s2_chart_title": "Spend by Category — Last Period",
        "s2_chart_bars": [("Cloud", 118), ("Headcount", 112), ("Licenses", 122), ("Ops", 95), ("Other", 88)],
        "s3_waterfall": [
            ("Budget", "$2,400K", "accent"),
            ("Cloud", "+$340K", "red"),
            ("Headcount", "+$116K", "amber"),
            ("Licensing", "+$240K", "red"),
            ("Late invoices", "+$80K", "amber"),
            ("Actual", "$3,096K", "red"),
        ],
        "s3_note": "Late-arriving cloud migration invoices explain 40% of the period-end spike.",
        "s4_audiences": [
            ("CFO", "29% overrun requires Q3 re-baseline. Hold discretionary spend until reconciliation."),
            ("FP&A", "Break down late invoices by cost center. Update forecast model by Friday."),
            ("Board", "One-line: spend discipline needed before next funding review."),
        ],
        "s5_risks": [
            ("Continued spend acceleration", "High", "High", "red"),
            ("Forecast miss", "High", "Medium", "amber"),
            ("Vendor payment timing", "Medium", "Low", "green"),
        ],
        "s6_steps": [
            "Reconcile last-period cloud invoices by cost center",
            "Update Q3 forecast with actual run-rate",
            "Brief CFO on 29% variance drivers",
            "Implement weekly spend flash reports",
        ],
    },
    "Show me the top drivers between the variance": {
        "filename": "DeckGen_Variance_Drivers.pptx",
        "s1_headline": "Three drivers explain 106% of total variance — cloud, licensing, headcount.",
        "s1_number": "+$737K",
        "s1_sub": "Combined impact of top 3 drivers vs total overrun",
        "s2_bullets": [
            "Driver 1 — Cloud migration: +$340K (unbudgeted lift-and-shift)",
            "Driver 2 — Vendor licensing: +$240K (Oracle + AWS renewals)",
            "Driver 3 — Engineering headcount: +$157K (7 unplanned FTEs)",
            "Remaining categories net to minor offsets",
        ],
        "s2_chart_title": "Variance Driver Contribution",
        "s2_chart_bars": [("Cloud", 160), ("Licenses", 140), ("Headcount", 115), ("Other", 45), ("Ops", 30)],
        "s3_waterfall": [
            ("Plan", "$2,400K", "accent"),
            ("Cloud mig.", "+$340K", "red"),
            ("Licensing", "+$240K", "red"),
            ("Headcount", "+$157K", "amber"),
            ("Other", "+$59K", "amber"),
            ("Actual", "$3,096K", "red"),
        ],
        "s3_note": "Addressing top 3 drivers recovers ~80% of recoverable overrun.",
        "s4_audiences": [
            ("CFO", "Prioritize cloud contract renegotiation — largest single driver at $340K."),
            ("Engineering VP", "Headcount growth without budget revision added $157K."),
            ("Procurement", "Oracle renewal alone accounts for $180K of licensing overrun."),
        ],
        "s5_risks": [
            ("Cloud cost runaway", "High", "High", "red"),
            ("Uncontrolled hiring", "High", "High", "red"),
            ("License auto-renewal", "Medium", "High", "amber"),
        ],
        "s6_steps": [
            "Root-cause review on cloud migration scope",
            "Freeze unbudgeted headcount additions",
            "Renegotiate Oracle and AWS contracts",
            "Assign owner per top-3 driver",
        ],
    },
    "Were there any duplications been recorded in payments from last month": {
        "filename": "DeckGen_Payment_Duplicates.pptx",
        "s1_headline": "2 potential duplicate payments flagged — $142K confirmed recovery opportunity.",
        "s1_number": "$142K",
        "s1_sub": "4,218 transactions scanned · 1 confirmed duplicate",
        "s2_bullets": [
            "ACME Consulting — invoice #4821 posted twice ($142K × 2)",
            "1 confirmed duplicate · 1 pending AP review",
            "Professional Services category affected",
            "Recommend hold on vendor disbursements until cleared",
        ],
        "s2_chart_title": "Duplicate Scan Results",
        "s2_chart_bars": [("Confirmed", 142), ("Pending", 142), ("Clean", 85), ("Review", 60), ("OK", 40)],
        "s3_waterfall": [
            ("Paid", "$4,218 txns", "accent"),
            ("Flagged", "2 dupes", "red"),
            ("Confirmed", "$142K", "red"),
            ("Recovery", "-$142K", "green"),
            ("Pending", "1 case", "amber"),
            ("Net risk", "$142K", "amber"),
        ],
        "s3_note": "Implement duplicate detection rules in AP workflow before next close.",
        "s4_audiences": [
            ("CFO", "$142K confirmed duplicate — recover before month-end close."),
            ("AP Manager", "Hold ACME Consulting disbursements pending reconciliation."),
            ("Audit", "Document duplicate detection controls for SOX compliance."),
        ],
        "s5_risks": [
            ("Repeat duplicate posting", "Medium", "High", "amber"),
            ("Recovery delay", "Low", "Medium", "green"),
            ("Vendor dispute", "Low", "Low", "green"),
        ],
        "s6_steps": [
            "Reverse confirmed $142K duplicate entry",
            "Complete pending AP review within 48 hours",
            "Add duplicate-check rule to AP system",
            "Brief CFO on recovery status",
        ],
    },
    "What is the budget variance for Q2 software infrastructure?": {
        "filename": "DeckGen_Q2_Software_Infra.pptx",
        "s1_headline": "Q2 software infrastructure exceeded budget by 29% — critical threshold breach.",
        "s1_number": "+29%",
        "s1_sub": "Budget $2.4M → Actual $3.1M · +$696K overrun",
        "s2_bullets": [
            "Cloud migration acceleration: +$340K (unbudgeted)",
            "Unplanned vendor licensing: +$240K",
            "Engineering headcount: +$116K (+15% FTE growth)",
            "Status: exceeds 25% critical threshold",
        ],
        "s2_chart_title": "Software Infra — Budget vs Actual",
        "s2_chart_bars": [("Cloud", 142), ("Licenses", 160), ("Headcount", 115), ("Ops", 98), ("Other", 88)],
        "s3_waterfall": [
            ("Budget", "$2,400K", "accent"),
            ("Cloud", "+$340K", "red"),
            ("Licenses", "+$240K", "red"),
            ("Headcount", "+$116K", "amber"),
            ("Actual", "$3,096K", "red"),
        ],
        "s3_note": "Immediate cost optimization review required with Engineering leadership.",
        "s4_audiences": [
            ("CFO", "29% infra overrun threatens Q3 cash runway. Approve $400K reallocation."),
            ("Engineering VP", "Cloud migration drove 48% of infra overspend."),
            ("Board", "Schedule emergency budget review within 14 days."),
        ],
        "s5_risks": [
            ("Cloud cost escalation", "High", "High", "red"),
            ("Vendor contract expiry", "Medium", "High", "amber"),
            ("Headcount creep", "High", "Medium", "amber"),
        ],
        "s6_steps": [
            "Approve emergency Q3 reallocation",
            "Renegotiate AWS/Oracle contracts",
            "Implement monthly infra checkpoints",
            "Freeze non-essential hiring until September",
        ],
    },
    "Show me the headcount cost overrun analysis": {
        "filename": "DeckGen_Headcount_Analysis.pptx",
        "s1_headline": "Headcount grew 15.6% above plan — 7 unplanned FTEs drove $157K overrun.",
        "s1_number": "+7 FTE",
        "s1_sub": "Budgeted 45 engineers → Actual 52 · $157K cost impact",
        "s2_bullets": [
            "Additional salaries: $116K over budget",
            "Onboarding & equipment: $23K",
            "Benefits & overhead: $18K",
            "Root cause: cloud migration hires + attrition backfills",
        ],
        "s2_chart_title": "Headcount Cost Breakdown",
        "s2_chart_bars": [("Salaries", 130), ("Onboarding", 85), ("Benefits", 72), ("Overhead", 60), ("Plan", 100)],
        "s3_waterfall": [
            ("Plan (45 FTE)", "$910K", "accent"),
            ("New hires", "+$116K", "red"),
            ("Onboarding", "+$23K", "amber"),
            ("Benefits", "+$18K", "amber"),
            ("Actual (52 FTE)", "$1,067K", "red"),
        ],
        "s3_note": "Require budget revision before any further engineering hires.",
        "s4_audiences": [
            ("CFO", "7 unplanned FTEs added $157K. Freeze hiring until Q3 re-baseline."),
            ("HR", "Implement headcount approval gate for all backfills >$50K cost."),
            ("Engineering VP", "Cloud migration staffing plan was not budget-approved."),
        ],
        "s5_risks": [
            ("Continued unplanned hiring", "High", "High", "red"),
            ("Attrition backfill cost", "Medium", "Medium", "amber"),
            ("Retention spend", "Low", "Low", "green"),
        ],
        "s6_steps": [
            "Freeze non-essential engineering hires",
            "Re-baseline Q3 headcount plan",
            "Audit cloud migration staffing justification",
            "Report FTE variance to board",
        ],
    },
    "Generate a cloud spend breakdown by vendor": {
        "filename": "DeckGen_Cloud_Vendor_Spend.pptx",
        "s1_headline": "Total cloud spend 25.4% over plan — AWS alone accounts for 80% of overrun.",
        "s1_number": "+$406K",
        "s1_sub": "Budget $1,600K → Actual $2,006K across 5 vendors",
        "s2_bullets": [
            "AWS: $1,120K actual vs $800K budget (+40%)",
            "Azure: $380K actual vs $400K budget (-5%)",
            "GCP: $245K vs $200K budget (+22.5%)",
            "Oracle Cloud: $195K vs $150K budget (+30%)",
        ],
        "s2_chart_title": "Cloud Spend by Vendor",
        "s2_chart_bars": [("AWS", 140), ("Azure", 95), ("GCP", 122), ("Oracle", 130), ("Other", 105)],
        "s3_waterfall": [
            ("Budget", "$1,600K", "accent"),
            ("AWS", "+$320K", "red"),
            ("GCP", "+$45K", "amber"),
            ("Oracle", "+$45K", "amber"),
            ("Azure", "-$20K", "green"),
            ("Actual", "$2,006K", "red"),
        ],
        "s3_note": "Renegotiate AWS reserved instances — rates 23% above market benchmark.",
        "s4_audiences": [
            ("CFO", "AWS overrun of $320K is the single largest vendor variance."),
            ("Cloud Architect", "Right-size reserved instances and eliminate idle resources."),
            ("Procurement", "Initiate AWS enterprise discount renegotiation this quarter."),
        ],
        "s5_risks": [
            ("AWS rate increase", "High", "High", "red"),
            ("Multi-cloud sprawl", "Medium", "Medium", "amber"),
            ("Reserved instance expiry", "Medium", "High", "amber"),
        ],
        "s6_steps": [
            "Renegotiate AWS contract — target 20% reduction",
            "Audit idle cloud resources across all vendors",
            "Consolidate GCP and Oracle workloads where possible",
            "Set monthly cloud spend cap alerts",
        ],
    },
    "What are the top 3 cost drivers this quarter?": {
        "filename": "DeckGen_Top3_Drivers.pptx",
        "s1_headline": "Top 3 cost drivers account for $737K of overrun this quarter.",
        "s1_number": "$737K",
        "s1_sub": "Cloud migration · Licensing · Headcount",
        "s2_bullets": [
            "1. Cloud Migration Acceleration: +$340K",
            "2. Vendor Licensing Renewal: +$240K",
            "3. Engineering Headcount Growth: +$157K",
            "Combined: 106% of total quarter overrun",
        ],
        "s2_chart_title": "Top 3 Driver Impact",
        "s2_chart_bars": [("Cloud", 160), ("Licenses", 140), ("Headcount", 115), ("Other", 50), ("Ops", 35)],
        "s3_waterfall": [
            ("Q2 Budget", "$2,400K", "accent"),
            ("Driver 1", "+$340K", "red"),
            ("Driver 2", "+$240K", "red"),
            ("Driver 3", "+$157K", "amber"),
            ("Actual", "$3,096K", "red"),
        ],
        "s3_note": "Focus recovery efforts on cloud and licensing for maximum impact.",
        "s4_audiences": [
            ("CFO", "Three drivers explain entire overrun — assign executive owners today."),
            ("Engineering", "Cloud migration scope must be re-baselined before Q3."),
            ("Board", "Quarter overrun is concentrated, not systemic — actionable recovery plan ready."),
        ],
        "s5_risks": [
            ("Driver 1 escalation", "High", "High", "red"),
            ("License auto-renewal", "High", "Medium", "amber"),
            ("Unplanned hiring", "Medium", "High", "amber"),
        ],
        "s6_steps": [
            "Assign executive owner per top-3 driver",
            "Cloud migration scope review by Friday",
            "License renewal pre-approval workflow",
            "Report progress at next board meeting",
        ],
    },
    "Which departments exceeded their budget?": {
        "filename": "DeckGen_Dept_Budget_Status.pptx",
        "s1_headline": "3 departments over budget — Engineering leads at +26.4% ($575K over).",
        "s1_number": "+26.4%",
        "s1_sub": "Engineering · IT Ops · Product exceed plan",
        "s2_bullets": [
            "Engineering: +26.4% ($575K over budget)",
            "IT Operations: +18.2% ($145K over)",
            "Product: +12.1% ($67K over)",
            "Marketing at 98.3% — at risk threshold",
        ],
        "s2_chart_title": "Department Budget Utilization",
        "s2_chart_bars": [("Engineering", 126), ("IT Ops", 118), ("Product", 112), ("Marketing", 98), ("HR", 72)],
        "s3_waterfall": [
            ("Total budget", "$8,500K", "accent"),
            ("Engineering", "+$575K", "red"),
            ("IT Ops", "+$145K", "red"),
            ("Product", "+$67K", "amber"),
            ("Under-budget depts", "-$487K", "green"),
            ("Actual", "$9,800K", "red"),
        ],
        "s3_note": "Reallocate under-budget department slack to cover Engineering gap.",
        "s4_audiences": [
            ("CFO", "Engineering variance alone requires $575K Q3 reallocation or cut."),
            ("Dept Heads", "Monthly budget checkpoint mandatory for all over-budget units."),
            ("Board", "3 of 8 departments over plan — concentrated, not portfolio-wide."),
        ],
        "s5_risks": [
            ("Engineering overrun continuation", "High", "High", "red"),
            ("Marketing threshold breach", "Medium", "Medium", "amber"),
            ("Cross-dept reallocation delay", "Low", "High", "amber"),
        ],
        "s6_steps": [
            "Engineering variance review with VP this week",
            "Reallocate HR/Legal under-budget surplus",
            "Set 95% threshold alerts for Marketing and Sales",
            "Publish department scorecard to leadership",
        ],
    },
}


def _merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    merged.update(override)
    return merged


def deck_context_from_upload(
    filename: str,
    budget: float | None,
    actual: float | None,
    top_categories: list[tuple[str, float]] | None = None,
) -> dict[str, Any]:
    variance = (actual - budget) if budget and actual else 0
    pct = (variance / budget * 100) if budget else 0
    sign = "+" if variance >= 0 else ""
    num = f"{sign}{pct:.1f}%" if budget else "N/A"
    safe_name = filename.rsplit(".", 1)[0].replace(" ", "_")[:30]

    bullets = [f"Source file: {filename}"]
    if budget and actual:
        bullets += [
            f"Total budget: ${budget:,.0f}",
            f"Total actual: ${actual:,.0f}",
            f"Variance: ${variance:,.0f} ({pct:+.1f}%)",
        ]
    if top_categories:
        for cat, val in top_categories[:3]:
            bullets.append(f"{cat}: ${val:,.0f}")

    chart_bars = [(c[:12], min(int(v / max(actual or 1, 1) * 100), 160)) for c, v in (top_categories or [])[:5]]
    if not chart_bars:
        chart_bars = [("Uploaded", 100)]

    return _merge(_DEFAULT_PROFILE, {
        "filename": f"DeckGen_{safe_name}.pptx",
        "s1_headline": f"Uploaded dataset analysis — {filename} shows {pct:+.1f}% variance vs plan."
        if budget else f"Uploaded dataset analysis — {filename} ready for executive review.",
        "s1_number": num,
        "s1_sub": f"Budget ${budget:,.0f} → Actual ${actual:,.0f}" if budget and actual else f"Rows analyzed from {filename}",
        "s2_bullets": bullets[:5],
        "s2_chart_title": "Top Categories from Upload",
        "s2_chart_bars": chart_bars,
        "s3_note": "Deck generated from uploaded enterprise finance data.",
        "s4_audiences": [
            ("CFO", f"Uploaded data shows {pct:+.1f}% portfolio variance — review before board pack." if budget else "Review uploaded dataset summary before distribution."),
            ("FP&A", "Validate category mappings against ERP source system."),
            ("Board", "One-page summary attached from uploaded finance extract."),
        ],
        "s6_steps": [
            "Validate uploaded data against source system",
            "Share deck with finance leadership",
            "Schedule follow-up on largest variances",
            "Archive source file with deck version",
        ],
    })


def get_deck_context(prompt: str, upload_meta: dict[str, Any] | None = None) -> dict[str, Any]:
    if prompt.startswith("__upload__:") and upload_meta:
        return deck_context_from_upload(
            upload_meta.get("filename", "upload.csv"),
            upload_meta.get("budget"),
            upload_meta.get("actual"),
            upload_meta.get("top_categories"),
        )
    profile = DECK_PROFILES.get(prompt)
    if profile:
        return _merge(_DEFAULT_PROFILE, profile)
    return dict(_DEFAULT_PROFILE)
