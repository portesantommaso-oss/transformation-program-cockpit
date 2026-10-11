"""
Deterministic analysis: milestone slips, dependency conflicts, RAID hygiene,
readiness scoring and the go/no-go recommendation.

No AI is involved in anything in this module. Every output row carries a
`source` field pointing at the record it was derived from.
"""
from __future__ import annotations

import pandas as pd

from .loader import ProgramData

RAG_ORDER = {"Red": 0, "Amber": 1, "Green": 2}


# --------------------------------------------------------------------------- #
# Milestones
# --------------------------------------------------------------------------- #
def milestone_flags(pd_: ProgramData) -> pd.DataFrame:
    """One row per flag. Flags: slip, overdue, dependency_conflict, unowned, blocked_by_open."""
    ms = pd_.milestones
    by_id = ms.set_index("id")
    rows = []

    for _, m in ms.iterrows():
        slip_days = int((m.forecast_date - m.baseline_date).days)
        if m.status != "Complete" and slip_days > 0:
            rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner=m.owner,
                             flag="Slip", severity="High" if slip_days >= 7 else "Medium",
                             detail=f"Forecast {m.forecast_date.date()} is {slip_days} days after baseline {m.baseline_date.date()}",
                             source=f"milestone_plan.xlsx row {m.id}"))
        if m.status not in ("Complete",) and m.forecast_date < pd_.as_of:
            rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner=m.owner,
                             flag="Overdue", severity="High",
                             detail=f"Forecast {m.forecast_date.date()} is before as-of date {pd_.as_of.date()} and status is '{m.status}'",
                             source=f"milestone_plan.xlsx row {m.id}"))
        if not m.owner.strip():
            rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner="",
                             flag="Unowned", severity="High", detail="No owner recorded",
                             source=f"milestone_plan.xlsx row {m.id}"))
        for dep in [d for d in m.depends_on.split(";") if d]:
            if dep not in by_id.index:
                rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner=m.owner,
                                 flag="Unknown dependency", severity="Medium", detail=f"Depends on {dep}, not in plan",
                                 source=f"milestone_plan.xlsx row {m.id}"))
                continue
            d = by_id.loc[dep]
            if d.status != "Complete" and d.forecast_date > m.forecast_date:
                rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner=m.owner,
                                 flag="Dependency conflict", severity="High",
                                 detail=f"Depends on {dep} '{d.milestone}' forecast {d.forecast_date.date()}, "
                                        f"after own forecast {m.forecast_date.date()}",
                                 source=f"milestone_plan.xlsx rows {m.id}, {dep}"))
            elif d.status != "Complete" and d.forecast_date == m.forecast_date and m.status != "Complete":
                rows.append(dict(milestone_id=m.id, workstream=m.workstream, milestone=m.milestone, owner=m.owner,
                                 flag="Zero float", severity="Medium",
                                 detail=f"Depends on {dep} '{d.milestone}' due the same day",
                                 source=f"milestone_plan.xlsx rows {m.id}, {dep}"))
    cols = ["milestone_id", "workstream", "milestone", "owner", "flag", "severity", "detail", "source"]
    return pd.DataFrame(rows, columns=cols)


def milestone_summary(pd_: ProgramData) -> dict:
    ms = pd_.milestones
    return {
        "total": len(ms),
        "complete": int((ms.status == "Complete").sum()),
        "on_track": int((ms.status == "On track").sum()),
        "at_risk": int((ms.status == "At risk").sum()),
        "delayed": int((ms.status == "Delayed").sum()),
        "not_started": int((ms.status == "Not started").sum()),
        "slipping": int(((ms.status != "Complete") & (ms.forecast_date > ms.baseline_date)).sum()),
    }


# --------------------------------------------------------------------------- #
# RAID
# --------------------------------------------------------------------------- #
def raid_flags(pd_: ProgramData) -> pd.DataFrame:
    rows = []
    for _, r in pd_.raid.iterrows():
        if r.status in ("Closed", "Validated"):
            continue
        if not str(r.owner).strip():
            rows.append(dict(raid_id=r.id, type=r.type, title=r.title, owner="", flag="Unowned", severity="High",
                             detail="No owner recorded", source=f"raid_log.csv row {r.id}"))
        if pd.notna(r.due_date) and r.due_date < pd_.as_of:
            rows.append(dict(raid_id=r.id, type=r.type, title=r.title, owner=r.owner, flag="Past due", severity="High",
                             detail=f"Due {r.due_date.date()}, status '{r.status}'", source=f"raid_log.csv row {r.id}"))
        if not str(r.mitigation).strip():
            rows.append(dict(raid_id=r.id, type=r.type, title=r.title, owner=r.owner, flag="No mitigation", severity="Medium",
                             detail="Mitigation field empty", source=f"raid_log.csv row {r.id}"))
        if r.type == "Risk" and r.severity == "High" and r.likelihood == "High":
            rows.append(dict(raid_id=r.id, type=r.type, title=r.title, owner=r.owner, flag="High/High risk", severity="High",
                             detail=r.description, source=f"raid_log.csv row {r.id}"))
    cols = ["raid_id", "type", "title", "owner", "flag", "severity", "detail", "source"]
    return pd.DataFrame(rows, columns=cols)


def top_risks(pd_: ProgramData, n: int = 5) -> pd.DataFrame:
    rank = {"High": 3, "Medium": 2, "Low": 1, "": 0}
    r = pd_.raid[(pd_.raid.type.isin(["Risk", "Issue"])) & (~pd_.raid.status.isin(["Closed", "Validated"]))].copy()
    r["score"] = r.severity.map(rank).fillna(0) * 2 + r.likelihood.map(rank).fillna(1)
    r = r.sort_values(["score", "due_date"], ascending=[False, True]).head(n)
    r["source"] = "raid_log.csv row " + r["id"]
    return r[["id", "type", "title", "owner", "severity", "likelihood", "due_date", "mitigation", "source"]]


# --------------------------------------------------------------------------- #
# Readiness scoring
# --------------------------------------------------------------------------- #
def _rag(value: str, direction: str, green: str, amber: str) -> str:
    if direction == "categorical":
        if value == green:
            return "Green"
        if value == amber:
            return "Amber"
        return "Red"
    v, g, a = float(value), float(green), float(amber)
    if direction == "higher_better":
        return "Green" if v >= g else "Amber" if v >= a else "Red"
    if direction == "lower_better":
        return "Green" if v <= g else "Amber" if v <= a else "Red"
    raise ValueError(f"unknown direction {direction}")


def readiness_scorecard(pd_: ProgramData) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (criteria table with RAG, dimension table with RAG)."""
    k = pd_.kpis.copy()
    k["rag"] = [_rag(r.value, r.direction, r.green, r.amber) for r in k.itertuples()]
    k["display"] = [f"{r.value}{'' if r.unit in ('status',) else (' ' + r.unit if r.unit not in ('%',) else '%')}"
                    for r in k.itertuples()]
    dims = (k.groupby(["dimension_id", "dimension"], sort=True)
              .agg(rag=("rag", lambda s: min(s, key=lambda x: RAG_ORDER[x])),
                   red=("rag", lambda s: int((s == "Red").sum())),
                   amber=("rag", lambda s: int((s == "Amber").sum())),
                   green=("rag", lambda s: int((s == "Green").sum())))
              .reset_index())
    return k, dims


def go_no_go(dims: pd.DataFrame) -> dict:
    """Apply section 4 of the readiness framework."""
    red = set(dims.loc[dims.rag == "Red", "dimension_id"])
    amber = set(dims.loc[dims.rag == "Amber", "dimension_id"])
    critical_red = red & {"D1", "D4", "D5"}
    if not red and not amber:
        rec, rule = "Go", "All six dimensions green"
    elif critical_red:
        rec, rule = "No-go, re-plan", f"Red in critical dimension(s) {', '.join(sorted(critical_red))}"
    elif red:
        rec, rule = "Conditional go", f"Red in {', '.join(sorted(red))} only; requires SteerCo-approved mitigation tracked daily"
    else:
        rec, rule = "Go with conditions", f"Amber in {', '.join(sorted(amber))}; each needs owner and closure date before cut-over"
    return {"recommendation": rec, "rule": rule, "red": sorted(red), "amber": sorted(amber),
            "source": "01_Readiness_Framework.md section 4"}
