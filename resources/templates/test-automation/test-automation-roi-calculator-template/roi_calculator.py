"""Test automation ROI calculator.

Implements the model from the QAPractices ROI calculator template:
manual cost eliminated + defect prevention vs setup + annual automation cost.

Usage:
    python roi_calculator.py                  # runs the worked e-commerce example
    python roi_calculator.py inputs.csv       # runs your own numbers from a CSV

The CSV mirrors Sections 1-2 of the template: two columns, ``input,value``.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field


@dataclass
class Inputs:
    """Sections 1-2 of the template, as plain numbers (USD / hours / counts)."""

    manual_cases: int = 500
    minutes_per_case: float = 10
    runs_per_release: float = 2
    releases_per_year: int = 24
    manual_rate: float = 40
    production_defects_per_year: int = 60
    cost_per_defect: float = 2000
    escape_reduction_pct: float = 40
    cases_to_automate: int = 400
    setup_hours: float = 400
    automation_rate: float = 65
    tool_licenses_annual: float = 6000
    infrastructure_annual: float = 4000
    maintenance_hours_annual: float = 100
    one_time_tool_cost: float = 10000
    extra: dict = field(default_factory=dict)


def load_inputs(path: str) -> Inputs:
    """Load inputs from a two-column CSV (``input,value``)."""
    values: dict[str, float] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row.get("input") or "").strip()
            raw = (row.get("value") or "").strip()
            if not key or not raw:
                continue
            values[key] = float(raw.replace(",", "").replace("$", ""))
    known = {f for f in Inputs.__dataclass_fields__ if f != "extra"}
    base = {k: v for k, v in values.items() if k in known}
    extra = {k: v for k, v in values.items() if k not in known}
    inp = Inputs(**base)
    inp.extra = extra
    return inp


def calculate(inp: Inputs) -> dict:
    """Sections 3-4 of the template. Automated execution is machine time on
    CI, so no labor line is charged per run (add one via ``extra`` if your
    runners are billed per minute)."""
    manual_hours = inp.cases_to_automate * inp.minutes_per_case * inp.runs_per_release * inp.releases_per_year / 60
    manual_cost = manual_hours * inp.manual_rate
    defects_prevented = inp.production_defects_per_year * inp.escape_reduction_pct / 100
    defect_value = defects_prevented * inp.cost_per_defect
    gross_savings = manual_cost + defect_value

    setup_cost = inp.setup_hours * inp.automation_rate + inp.one_time_tool_cost
    annual_cost = inp.maintenance_hours_annual * inp.automation_rate + inp.tool_licenses_annual + inp.infrastructure_annual
    net_savings = gross_savings - annual_cost

    return {
        "manual_hours_eliminated": manual_hours,
        "manual_cost_eliminated": manual_cost,
        "defects_prevented": defects_prevented,
        "defect_prevention_value": defect_value,
        "gross_annual_savings": gross_savings,
        "setup_cost": setup_cost,
        "annual_automation_cost": annual_cost,
        "net_annual_savings": net_savings,
        "payback_months": setup_cost / (net_savings / 12) if net_savings > 0 else float("inf"),
        "first_year_roi_pct": (net_savings - setup_cost) / setup_cost * 100 if setup_cost else 0,
        "subsequent_year_roi_pct": net_savings / annual_cost * 100 if annual_cost else 0,
    }


def sensitivity(inp: Inputs, delta: float) -> dict:
    """Re-run the model scaling manual savings and defect prevention by delta."""
    scaled = Inputs(**{f: getattr(inp, f) for f in Inputs.__dataclass_fields__ if f != "extra"})
    scaled.minutes_per_case *= 1 + delta
    scaled.escape_reduction_pct *= 1 + delta
    return calculate(scaled)


def report(inp: Inputs, r: dict) -> str:
    lines = [
        "== Section 3: Projected savings ==",
        f"Manual hours eliminated : {r['manual_hours_eliminated']:,.0f} hrs/yr",
        f"Manual cost eliminated  : ${r['manual_cost_eliminated']:,.0f}/yr",
        f"Defects prevented       : {r['defects_prevented']:.0f}/yr (${r['defect_prevention_value']:,.0f})",
        f"Gross annual savings    : ${r['gross_annual_savings']:,.0f}",
        "",
        "== Section 4: ROI metrics ==",
        f"Setup cost              : ${r['setup_cost']:,.0f}",
        f"Annual automation cost  : ${r['annual_automation_cost']:,.0f}",
        f"Net annual savings      : ${r['net_annual_savings']:,.0f}",
        f"Payback period          : {r['payback_months']:.1f} months",
        f"First-year ROI          : {r['first_year_roi_pct']:.0f}%",
        f"Subsequent-year ROI     : {r['subsequent_year_roi_pct']:.0f}%",
        "",
        "== Section 5: Sensitivity ==",
    ]
    for label, delta in (("Conservative (-20%)", -0.2), ("Expected", 0.0), ("Optimistic (+20%)", 0.2)):
        s = sensitivity(inp, delta)
        lines.append(f"{label:24}: manual ${s['manual_cost_eliminated']:,.0f} | net ${s['net_annual_savings']:,.0f} | payback {s['payback_months']:.1f} mo")
    return "\n".join(lines)


if __name__ == "__main__":
    inputs = load_inputs(sys.argv[1]) if len(sys.argv) > 1 else Inputs()
    print(report(inputs, calculate(inputs)))
