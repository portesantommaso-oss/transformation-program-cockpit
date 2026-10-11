"""Load program inputs from the data folder."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ProgramData:
    as_of: pd.Timestamp
    meta: dict
    milestones: pd.DataFrame
    raid: pd.DataFrame
    kpis: pd.DataFrame
    updates: dict[str, str]  # filename -> text


def load_program(data_dir: str | Path) -> ProgramData:
    data_dir = Path(data_dir)

    xls = pd.ExcelFile(data_dir / "milestone_plan.xlsx")
    ms = xls.parse("Milestones")
    meta_df = xls.parse("Meta")
    meta = dict(zip(meta_df["key"], meta_df["value"].astype(str)))
    for c in ("baseline_date", "forecast_date"):
        ms[c] = pd.to_datetime(ms[c])
    ms["depends_on"] = ms["depends_on"].fillna("").astype(str)
    ms["owner"] = ms["owner"].fillna("").astype(str)

    raid = pd.read_csv(data_dir / "raid_log.csv", dtype=str).fillna("")
    raid["due_date"] = pd.to_datetime(raid["due_date"], errors="coerce")
    raid["raised_on"] = pd.to_datetime(raid["raised_on"], errors="coerce")

    kpis = pd.read_csv(data_dir / "readiness_kpis.csv", dtype=str).fillna("")

    updates = {}
    upd_dir = data_dir / "weekly_updates"
    if upd_dir.exists():
        for p in sorted(upd_dir.glob("*.txt")):
            updates[p.name] = p.read_text(encoding="utf-8")

    as_of = pd.Timestamp(meta.get("as_of", pd.Timestamp.today().date()))
    return ProgramData(as_of=as_of, meta=meta, milestones=ms, raid=raid, kpis=kpis, updates=updates)
