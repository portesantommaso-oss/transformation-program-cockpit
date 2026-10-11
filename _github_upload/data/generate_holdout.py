"""
Held-out test set for the extractor. Written AFTER the extraction rules were
frozen, in a deliberately different style (terse, bullet-like, fewer signal
words) to measure how the rules generalise beyond the data they were built next to.

    python data/generate_holdout.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

HOLDOUT = [
    ("wk42_pmo.txt", """Workstream: PMO
Week: 42 (16 October 2026)
Author: PMO Lead

Decision paper drafting started; structure agreed with the Sponsor. Still no written answer from Finance on the year-end freeze calendar, chased twice. Release management confirmed the 21 to 22 November slot; 28 to 29 November is the only fallback before the network freeze. The vendor invoice for the archiving tool extension is CHF 42k against CHF 30k budgeted. The SteerCo pre-read deadline was brought forward to 3 November at the Sponsor's request and workstreams were told today. The PMO analyst is on leave from 2 to 13 November and cover is not yet arranged.
""", [
        {"type": "dependency", "summary": "No written answer from Finance on freeze calendar", "anchor": "Still no written answer from Finance"},
        {"type": "issue", "summary": "Archiving invoice CHF 42k vs 30k budget", "anchor": "CHF 42k against CHF 30k budgeted"},
        {"type": "risk", "summary": "Pre-read deadline compressed to 3 Nov", "anchor": "brought forward to 3 November"},
        {"type": "risk", "summary": "PMO analyst leave, cover not arranged", "anchor": "cover is not yet arranged"},
    ]),
    ("wk42_data_migration.txt", """Workstream: Data Migration
Week: 42 (16 October 2026)
Author: Data Migration Lead

Mock 3 ran on 17 October on the new build. Reconciliation 99.4%, up from 99.1%; 61 breaks, all in structured products, root cause unchanged. DEF-114 closed on 15 October. DEF-121: 118 of 312 records enriched; advisors on the two largest desks have not started, the same desks as the training gap. At the current pace completion lands around 12 November, not 6 November. Treasury escalated the currency table change to the CFO office. Finance confirmed 13 November for reconciliation sign-off.
""", [
        {"type": "issue", "summary": "Largest desks have not started DEF-121 enrichment", "anchor": "have not started"},
        {"type": "slip", "summary": "DEF-121 completion around 12 Nov, not 6 Nov", "anchor": "lands around 12 November, not 6 November"},
        {"type": "risk", "summary": "Treasury escalated currency table change", "anchor": "escalated the currency table change"},
    ]),
    ("wk42_technology.txt", """Workstream: Technology Cut-over
Week: 42 (16 October 2026)
Author: Technology Delivery Lead

Regression on the batch fix: 212 of 240 cases passed, 28 outstanding, 3 failures under investigation. Deployment on 23 October is still planned, but the change advisory board meets on 21 October and has asked for the failure analysis beforehand. The DEF-209 fix is bundled into the same deployment. DR2 runbook v4 issued. Rollback scripts for the application layer are written but unreviewed. The network team flagged that the 1 December freeze may start on 24 November for the Zurich sites; written confirmation requested.
""", [
        {"type": "issue", "summary": "3 regression failures under investigation", "anchor": "3 failures under investigation"},
        {"type": "dependency", "summary": "CAB wants failure analysis before 23 Oct deployment", "anchor": "asked for the failure analysis beforehand"},
        {"type": "issue", "summary": "Application rollback scripts unreviewed", "anchor": "written but unreviewed"},
        {"type": "risk", "summary": "Freeze may start 24 Nov for Zurich", "anchor": "may start on 24 November"},
    ]),
    ("wk42_training_operations.txt", """Workstream: Training and Operations Readiness (joint)
Week: 42 (16 October 2026)
Author: Learning Lead, Operations Readiness Lead

Training completion 90%, up two points. Protected slots on 20 to 21 October held for desk A; desk B cancelled theirs for a client event and a rebooking has been requested. Floorwalkers 12 of 14, no change. Assessment: 220 of 410 advisors completed, 89% pass rate. Operations: the SteerCo chair asked for a third staffing option (hybrid: 4 partner FTE plus corporate actions deferred by two weeks) before 23 October. The service partner confirmed it can mobilise 8 FTE by 17 November if contracted by 23 October. Load test at 100% passed on 16 October; the 120% run is scheduled for 27 October. The BCP walkthrough moved to 4 November because the facilities contact is unavailable on 28 October.
""", [
        {"type": "issue", "summary": "Desk B cancelled protected training slot", "anchor": "desk B cancelled theirs"},
        {"type": "decision", "summary": "Chair asked for a third staffing option", "anchor": "asked for a third staffing option"},
        {"type": "dependency", "summary": "Partner mobilisation conditional on 23 Oct contract", "anchor": "if contracted by 23 October"},
        {"type": "slip", "summary": "BCP walkthrough moved to 4 Nov", "anchor": "moved to 4 November"},
    ]),
    ("wk42_risk_control.txt", """Workstream: Risk and Control
Week: 42 (16 October 2026)
Author: Risk and Control Lead

Control testing 90%, unchanged; the four-eyes control is still waiting for the DR2 build. Compliance approval on track for 30 October. Operational Risk reiterated its position in writing: no approval while DEF-121 is open, and a conditional approval would need the Head of Operational Risk to agree in person at the SteerCo. Records Management confirmed the retention approach in writing on 15 October. Internal Audit has scheduled a readiness review for 10 to 12 November; findings would arrive after the go/no-go.
""", [
        {"type": "dependency", "summary": "Four-eyes control waits for DR2 build", "anchor": "still waiting for the DR2 build"},
        {"type": "decision", "summary": "Conditional approval needs Head of Op Risk at SteerCo", "anchor": "would need the Head of Operational Risk"},
        {"type": "risk", "summary": "Audit findings arrive after go/no-go", "anchor": "findings would arrive after the go/no-go"},
    ]),
]


def main() -> None:
    d = HERE / "weekly_updates_holdout"
    d.mkdir(exist_ok=True)
    gt = {}
    for fname, text, items in HOLDOUT:
        (d / fname).write_text(text.strip() + "\n", encoding="utf-8")
        gt[fname] = items
    (HERE / "ground_truth_holdout.json").write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"holdout updates: {len(HOLDOUT)}  items: {sum(len(i) for *_, i in HOLDOUT)}")


if __name__ == "__main__":
    main()
