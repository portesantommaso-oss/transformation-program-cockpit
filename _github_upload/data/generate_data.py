"""
Generates the synthetic dataset for the GWM Transformation Cockpit.

Everything produced here is fictional. Names are roles, not people.
Dates are relative to an "as of" date of Friday 9 October 2026 (ISO week 41).
Re-run this file to regenerate the dataset from scratch:

    python data/generate_data.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
AS_OF = "2026-10-09"

# --------------------------------------------------------------------------- #
# 1. Milestone plan
# --------------------------------------------------------------------------- #
# id, workstream, milestone, owner, baseline, forecast, status, pct_complete, depends_on
MILESTONES = [
    ("M01", "PMO", "Release 3 scope baseline approved", "Program Manager", "2026-06-26", "2026-06-26", "Complete", 100, ""),
    ("M02", "PMO", "Go/no-go decision paper issued", "PMO Lead", "2026-11-04", "2026-11-04", "On track", 35, "M12;M18;M22;M26"),
    ("M03", "PMO", "Go/no-go SteerCo", "Program Sponsor", "2026-11-06", "2026-11-06", "On track", 0, "M02"),
    ("M04", "PMO", "Final confirmation (T-3 days)", "Program Sponsor", "2026-11-18", "2026-11-18", "Not started", 0, "M03"),
    ("M05", "PMO", "Cut-over weekend", "Technology Delivery Lead", "2026-11-21", "2026-11-21", "Not started", 0, "M04"),
    ("M06", "Data Migration", "Reference data mapping sign-off", "Data Migration Lead", "2026-09-11", "2026-09-25", "Complete", 100, ""),
    ("M07", "Data Migration", "Mock migration 2", "Data Migration Lead", "2026-09-19", "2026-09-19", "Complete", 100, ""),
    ("M08", "Data Migration", "Mock migration 3", "Data Migration Lead", "2026-10-10", "2026-10-17", "At risk", 60, "M07;M21"),
    ("M09", "Data Migration", "Severity 1/2 data defects closed", "Data Migration Lead", "2026-10-30", "2026-11-06", "Delayed", 40, "M08"),
    ("M10", "Data Migration", "Reconciliation sign-off by Finance", "Finance Controller", "2026-11-13", "2026-11-13", "Not started", 0, "M09"),
    ("M11", "Business Change", "Client notification letters dispatched", "Business Change Lead", "2026-09-26", "2026-09-26", "Complete", 100, ""),
    ("M12", "Business Change", "Advisor briefings completed (all desks)", "Business Change Lead", "2026-10-16", "2026-10-16", "On track", 92, ""),
    ("M13", "Business Change", "Hypercare contact model published", "Business Change Lead", "2026-10-02", "2026-10-02", "Complete", 100, ""),
    ("M14", "Training", "Release 3 training content published", "Learning Lead", "2026-09-12", "2026-09-12", "Complete", 100, ""),
    ("M15", "Training", "Training environment refreshed with mock 2 data", "Technology Delivery Lead", "2026-09-26", "2026-10-03", "Complete", 100, "M07"),
    ("M16", "Training", "Mandatory training 95% complete", "Learning Lead", "2026-10-30", "2026-11-10", "Delayed", 88, "M15"),
    ("M17", "Training", "Floorwalker roster confirmed", "Learning Lead", "2026-10-23", "2026-10-23", "At risk", 55, "M28"),
    ("M18", "Training", "Competence assessment closed", "Learning Lead", "2026-11-06", "2026-11-06", "On track", 30, "M16"),
    ("M19", "Technology", "Dress rehearsal 1", "Technology Delivery Lead", "2026-10-03", "2026-10-04", "Complete", 100, ""),
    ("M20", "Technology", "Dress rehearsal 2", "Technology Delivery Lead", "2026-10-31", "2026-11-07", "At risk", 10, "M19;M21"),
    ("M21", "Technology", "Batch window performance fix deployed", "Platform Engineering Lead", "2026-10-16", "2026-10-23", "Delayed", 45, ""),
    ("M22", "Technology", "Rollback procedure tested end to end", "Technology Delivery Lead", "2026-10-31", "2026-11-07", "At risk", 50, "M20"),
    ("M23", "Technology", "Legacy archiving and access-removal plan approved", "Decommissioning Lead", "2026-10-23", "2026-10-23", "On track", 85, ""),
    ("M24", "Risk & Control", "Key control testing on target platform", "Risk and Control Lead", "2026-10-23", "2026-10-23", "On track", 90, "M20"),
    ("M25", "Risk & Control", "Compliance approval", "Compliance Officer", "2026-10-30", "2026-10-30", "On track", 50, "M24"),
    ("M26", "Risk & Control", "Operational risk approval", "Operational Risk Officer", "2026-10-30", "2026-11-13", "Delayed", 20, "M24;M09"),
    ("M27", "Risk & Control", "Record retention confirmation", "Records Management", "2026-10-16", "2026-10-16", "On track", 75, "M23"),
    ("M28", "Operations", "Hypercare staffing plan approved", "Operations Readiness Lead", "2026-10-09", "2026-10-23", "Delayed", 60, ""),
    ("M29", "Operations", "Load test at 120% of expected peak", "Platform Engineering Lead", "2026-10-16", "2026-10-23", "At risk", 30, "M21"),
    ("M30", "Operations", "BCP update walkthrough", "Operations Readiness Lead", "2026-10-30", "2026-10-30", "On track", 40, ""),
]

# --------------------------------------------------------------------------- #
# 2. RAID log
# --------------------------------------------------------------------------- #
# id, type, title, description, workstream, owner, severity, likelihood, status, due_date, mitigation, raised_on
RAID = [
    ("R01", "Risk", "Batch window fix late for dress rehearsal 2",
     "Position revaluation step serialises on the legacy pricing interface; fix deployment moved to 23 Oct. If regression fails, DR2 cannot run on 7-8 Nov.",
     "Technology", "Platform Engineering Lead", "High", "Medium", "Open", "2026-10-23",
     "Daily stand-up with Platform Engineering; fallback is DR2 on current build with reduced evidence.", "2026-10-05"),
    ("R02", "Risk", "Operational Risk approval after go/no-go SteerCo",
     "Operational Risk will not sign off while severity 2 data defects remain open; approval forecast 13 Nov, after the 6 Nov SteerCo.",
     "Risk & Control", "Risk and Control Lead", "High", "High", "Open", "2026-11-06",
     "Request conditional approval; close DEF-114 by 16 Oct and DEF-121 by 6 Nov.", "2026-10-02"),
    ("R03", "Risk", "Hypercare staffing below model requirement",
     "50 of 58 FTE confirmed (86%). Service centre teams carry year-end volumes in the same period.",
     "Operations", "Operations Readiness Lead", "High", "High", "Open", "2026-10-23",
     "SteerCo options: 8 temporary FTE from service partner (CHF 180k) or defer corporate actions module.", "2026-09-28"),
    ("R04", "Risk", "Mandatory training completion below 95% at cut-over",
     "88% completed vs 92% planned for week 41; two largest desks prioritising client review season.",
     "Training", "Learning Lead", "Medium", "Medium", "Open", "2026-11-10",
     "Protected training slots on 20-21 Oct agreed with desk heads.", "2026-09-25"),
    ("R05", "Risk", "Floorwalker coverage insufficient on day one",
     "12 of 14 floorwalkers confirmed; two Operations staff offered but release depends on hypercare staffing decision.",
     "Training", "Learning Lead", "Medium", "Medium", "Open", "2026-10-23",
     "Confirm two Operations staff once R03 is decided.", "2026-10-02"),
    ("R06", "Risk", "Network change freeze from 1 December",
     "Any deferral of cut-over beyond 28-29 Nov pushes go-live into January.",
     "Technology", "Technology Delivery Lead", "High", "Low", "Open", "2026-11-06",
     "Decision paper to present 28-29 Nov as the only fallback weekend.", "2026-10-09"),
    ("R07", "Risk", "Reference data mapping reopened by Treasury change",
     "Treasury requested a further change to the currency table after sign-off; accepting it would reopen mapping sign-off and mock 3 scope.",
     "Data Migration", "Data Migration Lead", "Medium", "Medium", "Open", "2026-10-16",
     "Declined pending SteerCo guidance; propose change for Release 4.", "2026-10-09"),
    ("R08", "Risk", "Mock runs on stale reference data",
     "Two of three mock runs used last quarter's reference data snapshot; reconciliation evidence may not reflect current mappings.",
     "Data Migration", "Data Migration Lead", "Medium", "Medium", "Open", "2026-10-17",
     "Mock 3 to run on current snapshot; document delta.", "2026-10-02"),
    ("A01", "Assumption", "Cut-over weekend 21-22 November holds",
     "No competing release on the target platform that weekend.", "PMO", "PMO Lead", "Medium", "", "Open", "2026-11-06",
     "Confirmed with release management on 3 Oct; re-confirm at T-3 weeks.", "2026-06-26"),
    ("A02", "Assumption", "Finance available for reconciliation sign-off on 13 Nov",
     "Finance month-end close does not conflict with the sign-off date.", "Data Migration", "Finance Controller", "Medium", "", "Open", "2026-11-13",
     "Confirm with Finance planning.", "2026-09-19"),
    ("A03", "Assumption", "No new regulatory notice period applies",
     "Client notifications sent on 26 Sep satisfy the notice period for all in-scope client segments.", "Business Change", "Compliance Officer", "Low", "", "Validated", "2026-10-02",
     "Validated by Compliance 1 Oct.", "2026-09-01"),
    ("A04", "Assumption", "Service partner can augment staff within four weeks",
     "Contract requires four weeks' notice for staff augmentation.", "Operations", "Operations Readiness Lead", "High", "", "Open", "2026-10-23",
     "Decision needed by 23 Oct to be effective for cut-over.", "2026-10-09"),
    ("I01", "Issue", "DEF-114 duplicate client identifiers for joint accounts",
     "Severity 2 data defect. Fix in test.", "Data Migration", "Data Migration Lead", "High", "", "In progress", "2026-10-16",
     "Fix in test; close by 16 Oct.", "2026-09-22"),
    ("I02", "Issue", "DEF-121 missing tax domicile on 312 legacy records",
     "Severity 2 data defect. Requires manual enrichment by client advisors.", "Data Migration", "", "High", "", "Open", "2026-11-06",
     "Business Change asked to coordinate; owner not yet confirmed.", "2026-09-22"),
    ("I03", "Issue", "DEF-209 incorrect FX rate display CHF/USD on day-one screens",
     "Severity 2 technical defect.", "Technology", "Technology Delivery Lead", "High", "", "In progress", "2026-10-23",
     "Fix targeted for 23 Oct deployment.", "2026-10-04"),
    ("I04", "Issue", "Dress rehearsal 1 batch overran by 2h40",
     "Friday night batch finished 06:40 instead of 04:00; margin to Sunday hard stop 1h15.", "Technology", "Technology Delivery Lead", "High", "", "In progress", "2026-11-07",
     "Performance fix (R01); re-measure in DR2.", "2026-10-04"),
    ("I05", "Issue", "Application-layer rollback not tested in DR1",
     "Only database rollback executed; window closed before application rollback.", "Technology", "Technology Delivery Lead", "High", "", "Open", "2026-11-07",
     "Include end-to-end rollback in DR2.", "2026-10-04"),
    ("I06", "Issue", "Translation vendor quote 40% above budget line",
     "Italian day-one client guide may be delivered after go-live unless variance approved.", "Business Change", "Business Change Lead", "Low", "", "Open", "2026-10-16",
     "Variance request to PMO; fallback is two of three languages on day one.", "2026-10-02"),
    ("D01", "Dependency", "Batch performance fix deployed before mock 3 and DR2",
     "Mock 3 (17 Oct) and DR2 (7-8 Nov) both require the fix in the production-like environment.", "Technology", "Platform Engineering Lead", "High", "", "Open", "2026-10-23",
     "Change calendar entry requested; verbal confirmation only so far.", "2026-10-02"),
    ("D02", "Dependency", "Control testing needs DR2 build",
     "Four-eyes check on manual payments cannot be tested until the DR2 build is available.", "Risk & Control", "Risk and Control Lead", "Medium", "", "Open", "2026-11-07",
     "Test in DR2 window.", "2026-10-02"),
    ("D03", "Dependency", "Finance year-end freeze calendar confirmation",
     "Need confirmation that no Finance system freeze overlaps 21-22 Nov.", "PMO", "", "Medium", "", "Open", "2026-10-16",
     "", "2026-09-30"),
    ("D04", "Dependency", "Floorwalker release depends on hypercare staffing decision",
     "Two Operations staff offered as floorwalkers conditional on staffing uplift approval.", "Training", "Operations Readiness Lead", "Medium", "", "Open", "2026-10-23",
     "Decide with R03.", "2026-10-09"),
    ("D05", "Dependency", "Archiving tool licence extension",
     "Licence expires 31 Dec; decommissioning archiving runs into January. Extension raised with Procurement 9 Oct.", "Technology", "", "Medium", "", "Open", "2026-11-13",
     "Procurement to confirm.", "2026-10-04"),
    ("D06", "Dependency", "Corporate actions procedures review by Operations",
     "Remaining 6% of procedure documents with Operations for review.", "Training", "Operations Readiness Lead", "Low", "", "In progress", "2026-10-16",
     "Publication expected 16 Oct.", "2026-10-02"),
]

# --------------------------------------------------------------------------- #
# 3. Readiness KPIs (current snapshot)
# --------------------------------------------------------------------------- #
# dimension_id, dimension, criterion_id, criterion, value, unit, direction, green, amber, source
KPIS = [
    ("D1", "Data quality and reconciliation", "D1.1", "Mock migration reconciliation", 99.1, "%", "higher_better", 99.5, 98.0, "Mock 2 reconciliation report, 19 Sep"),
    ("D1", "Data quality and reconciliation", "D1.2", "Open severity 1/2 data defects", 2, "count", "lower_better", 0, 3, "Defect register, extract 9 Oct (DEF-114, DEF-121)"),
    ("D1", "Data quality and reconciliation", "D1.3", "Reference data mapping signed off", 100, "%", "higher_better", 100, 90, "Mapping sign-off register, 25 Sep"),
    ("D1", "Data quality and reconciliation", "D1.4", "Full mock migrations completed", 2, "count", "higher_better", 3, 2, "Milestone plan M07, M08"),
    ("D2", "Client and advisor communication", "D2.1", "In-scope clients notified", 100, "%", "higher_better", 100, 97, "Communication tracker, 26 Sep dispatch"),
    ("D2", "Client and advisor communication", "D2.2", "Client advisors briefed", 96, "%", "higher_better", 95, 85, "Briefing attendance log, 9 Oct"),
    ("D2", "Client and advisor communication", "D2.3", "Hypercare contact model", "Published", "status", "categorical", "Published", "Draft", "Intranet publication record, 2 Oct"),
    ("D2", "Client and advisor communication", "D2.4", "Program-linked complaints, 4-week trend", "Flat", "status", "categorical", "Flat", "Up <20%", "Complaints dashboard, 9 Oct"),
    ("D3", "Training and enablement", "D3.1", "Mandatory training completion", 88, "%", "higher_better", 95, 85, "Learning management system, 9 Oct"),
    ("D3", "Training and enablement", "D3.2", "Competence assessment pass rate (pilot)", 91, "%", "higher_better", 90, 80, "Assessment pilot, 40 advisors, 8 Oct"),
    ("D3", "Training and enablement", "D3.3", "Advisor desks per trained floorwalker", 12, "ratio", "lower_better", 10, 15, "Floorwalker roster, 12 of 14 confirmed, 9 Oct"),
    ("D3", "Training and enablement", "D3.4", "Day-one procedures published", 94, "%", "higher_better", 100, 90, "Procedure library, 9 Oct"),
    ("D4", "Technology cut-over and decommissioning", "D4.1", "Dress rehearsal margin to hard stop", 1.25, "hours", "higher_better", 2, 0, "DR1 run log, 3-4 Oct"),
    ("D4", "Technology cut-over and decommissioning", "D4.2", "Open severity 1/2 technical defects", 1, "count", "lower_better", 0, 2, "Defect register, extract 9 Oct (DEF-209)"),
    ("D4", "Technology cut-over and decommissioning", "D4.3", "Rollback tested end to end", "Partially", "status", "categorical", "Yes", "Partially", "DR1 run log, database layer only"),
    ("D4", "Technology cut-over and decommissioning", "D4.4", "Legacy apps with approved archiving and access-removal plan", 92, "%", "higher_better", 100, 90, "Decommissioning register, 9 Oct"),
    ("D5", "Regulatory, risk and control sign-off", "D5.1", "Formal approvals obtained", "One pending with date", "status", "categorical", "All", "One pending with date", "Approval register: Compliance 30 Oct expected, Operational Risk 13 Nov"),
    ("D5", "Regulatory, risk and control sign-off", "D5.2", "Key controls tested with evidence", 90, "%", "higher_better", 100, 90, "Control testing tracker, 9 Oct"),
    ("D5", "Regulatory, risk and control sign-off", "D5.3", "Open high-rated audit or regulatory findings", 0, "count", "lower_better", 0, 1, "Audit findings register, 9 Oct"),
    ("D5", "Regulatory, risk and control sign-off", "D5.4", "Record retention confirmed", "Plan agreed", "status", "categorical", "Confirmed", "Plan agreed", "Records Management, written confirmation expected 16 Oct"),
    ("D6", "Operational capacity and service continuity", "D6.1", "Hypercare staffing vs model requirement", 86, "%", "higher_better", 100, 90, "Staffing plan, 50 of 58 FTE confirmed, 9 Oct"),
    ("D6", "Operational capacity and service continuity", "D6.2", "Week-1 backlog vs processing capacity", 78, "%", "lower_better", 70, 90, "Capacity model v3, 2 Oct"),
    ("D6", "Operational capacity and service continuity", "D6.3", "Load test at 120% of expected peak", "Not yet run", "status", "categorical", "Passed", "Passed at 100% only", "Test plan: 100% run 16 Oct, 120% after batch fix"),
    ("D6", "Operational capacity and service continuity", "D6.4", "Business continuity plan", "Drafted", "status", "categorical", "Done", "Drafted", "BCP v2 draft, walkthrough booked 28 Oct"),
]

# --------------------------------------------------------------------------- #
# 4. Weekly free-text updates and ground truth
# --------------------------------------------------------------------------- #
# Each entry: filename, text, ground truth items. Ground truth items have a type and an
# "anchor" substring that must appear in an extracted sentence for it to count as found.
UPDATES = [
    ("wk40_data_migration.txt", """Workstream: Data Migration
Week: 40 (2 October 2026)
Author: Data Migration Lead

Mock migration 2 closed on 19 September with 99.1% of records reconciled; the remaining breaks are concentrated in structured-product positions where the legacy valuation feed uses a different pricing time. Mapping sign-off for reference data was completed on 25 September, two weeks later than planned, after Treasury requested changes to the currency table. Mock migration 3 is scheduled for 10 October but we are waiting on Platform Engineering to deploy the batch window fix first. If the fix is not in by 7 October we will run mock 3 on the old build, which weakens the evidence for the go/no-go paper. Two severity 2 data defects remain open: DEF-114 (duplicate client identifiers for joint accounts) and DEF-121 (missing tax domicile on 312 legacy records). Two of the three mock runs used last quarter's reference data snapshot. Team capacity is stable. One contractor rolls off at the end of October and a replacement has been requested.
""", [
        {"type": "slip", "summary": "Mapping sign-off two weeks late", "anchor": "two weeks later than planned"},
        {"type": "dependency", "summary": "Mock 3 waits on batch window fix", "anchor": "waiting on Platform Engineering"},
        {"type": "risk", "summary": "Mock 3 on old build weakens go/no-go evidence", "anchor": "If the fix is not in by 7 October"},
        {"type": "issue", "summary": "Two severity 2 data defects open", "anchor": "Two severity 2 data defects remain open"},
        {"type": "risk", "summary": "Mock runs used stale reference data", "anchor": "last quarter's reference data snapshot"},
        {"type": "risk", "summary": "Contractor roll-off end of October", "anchor": "rolls off at the end of October"},
    ]),
    ("wk40_technology_cutover.txt", """Workstream: Technology Cut-over
Week: 40 (2 October 2026, updated 5 October after DR1)
Author: Technology Delivery Lead

Dress rehearsal 1 ran over the weekend of 3 to 4 October. The full sequence completed, but the Friday night batch finished at 06:40 instead of 04:00, which leaves a margin of about 1 hour 15 minutes against the Sunday 18:00 hard stop. Root cause is the position revaluation step, which serialises on the legacy pricing interface. Platform Engineering has a fix in development; deployment is now expected on 23 October rather than 16 October. Rollback was executed for the database layer only; the application layer rollback was not attempted because the window had closed. Dress rehearsal 2 is planned for 31 October and depends on the fix being deployed and regression-tested. Two severity 2 technical defects are open: DEF-203 (session timeout on the advisor dashboard) and DEF-209 (incorrect FX rate display for CHF/USD on day-one screens). The decommissioning plan for the legacy cluster is 85% complete. The archiving tool licence expires on 31 December and the extension request has not yet been raised.
""", [
        {"type": "issue", "summary": "DR1 batch overran", "anchor": "finished at 06:40 instead of 04:00"},
        {"type": "slip", "summary": "Batch fix deployment moved to 23 Oct", "anchor": "now expected on 23 October rather than 16 October"},
        {"type": "issue", "summary": "Application-layer rollback not tested", "anchor": "application layer rollback was not attempted"},
        {"type": "dependency", "summary": "DR2 depends on fix deployment", "anchor": "depends on the fix being deployed"},
        {"type": "issue", "summary": "Two severity 2 technical defects open", "anchor": "Two severity 2 technical defects are open"},
        {"type": "risk", "summary": "Archiving licence extension not raised", "anchor": "extension request has not yet been raised"},
    ]),
    ("wk40_training.txt", """Workstream: Training and Enablement
Week: 40 (2 October 2026)
Author: Learning and Adoption Lead

Release 3 content has been live since 12 September. Completion of mandatory modules stands at 81% against a plan of 88% for this week; the gap is concentrated in the two largest advisor desks, where line managers report that client review season is taking priority. The training environment was refreshed with mock 2 data on 3 October, one week late, because the refresh depended on the mock 2 extract being signed off. Competence assessment opens on 19 October. We are planning for 14 floorwalkers; only 11 have confirmed availability for the cut-over week. Procedure documentation is 94% published; the remaining documents cover corporate actions and are with Operations for review. No change to the budget.
""", [
        {"type": "issue", "summary": "Training completion below plan", "anchor": "81% against a plan of 88%"},
        {"type": "slip", "summary": "Training environment refresh one week late", "anchor": "one week late"},
        {"type": "risk", "summary": "Only 11 of 14 floorwalkers confirmed", "anchor": "only 11 have confirmed availability"},
        {"type": "dependency", "summary": "Corporate actions procedures with Operations", "anchor": "with Operations for review"},
    ]),
    ("wk40_risk_control.txt", """Workstream: Risk and Control
Week: 40 (2 October 2026)
Author: Risk and Control Lead

Key control testing on the target platform is 90% complete with evidence filed; the remaining controls relate to the four-eyes check on manual payments and cannot be tested until the dress rehearsal 2 build is available. Compliance has indicated approval is likely by 30 October subject to the client notification evidence pack, which Business Change has provided. Operational Risk has stated it will not sign off while severity 2 data defects remain open, so its approval now moves from 30 October to 13 November, which is after the go/no-go SteerCo on 6 November. We need the SteerCo to decide whether a conditional approval from Operational Risk is acceptable for the decision on 6 November. Record retention: the archiving approach is agreed in principle and written confirmation from Records Management is expected by 16 October. There are no open audit findings linked to the release.
""", [
        {"type": "dependency", "summary": "Control testing needs DR2 build", "anchor": "cannot be tested until the dress rehearsal 2 build"},
        {"type": "slip", "summary": "Operational Risk approval moves to 13 Nov", "anchor": "moves from 30 October to 13 November"},
        {"type": "decision", "summary": "SteerCo to decide on conditional approval", "anchor": "We need the SteerCo to decide"},
    ]),
    ("wk40_operations.txt", """Workstream: Operations Readiness
Week: 40 (2 October 2026)
Author: Operations Readiness Lead

The hypercare staffing plan was due for approval on 9 October. The model requires 58 FTE for the first three weeks; current confirmed staffing is 50 FTE, which is 86% of the requirement, because two teams in the service centre carry year-end volumes in the same period. Approval is therefore held until the gap is closed or a mitigation is agreed. Backlog projection for week 1 after go-live is 78% of processing capacity, within tolerance but with little room. The load test is now planned at 100% of expected peak on 16 October; the 120% run cannot be scheduled until Platform Engineering's batch fix is in, which is 23 October at the earliest. The BCP update has been drafted and the walkthrough is booked for 28 October. Client complaint volumes linked to the program are flat week on week.
""", [
        {"type": "issue", "summary": "Hypercare staffing at 86% of requirement", "anchor": "86% of the requirement"},
        {"type": "slip", "summary": "Staffing plan approval held", "anchor": "Approval is therefore held"},
        {"type": "dependency", "summary": "120% load test waits on batch fix", "anchor": "cannot be scheduled until Platform Engineering's batch fix"},
    ]),
    ("wk40_business_change.txt", """Workstream: Business Change and Communication
Week: 40 (2 October 2026)
Author: Business Change Lead

Client notification letters were dispatched on 26 September to 100% of in-scope clients, inside the notice period. Advisor briefings have reached 92% of desks; the two remaining desks are booked for 14 and 15 October. The hypercare contact model (hotline, escalation tree, FAQ) was published on 2 October. We received 14 client calls about the letter in the first week, mostly asking whether account numbers change, and the FAQ has been updated. There is no risk to the communication timeline at this point. One item to watch: the Italian-language version of the day-one client guide is with the translation vendor and the vendor's revised quote arrived 40% above the budget line. The guide may therefore be delivered in two of the three languages on day one unless the variance is approved.
""", [
        {"type": "issue", "summary": "Translation vendor quote 40% over budget", "anchor": "40% above the budget line"},
        {"type": "risk", "summary": "Italian guide may miss day one unless variance approved", "anchor": "two of the three languages on day one"},
    ]),
    ("wk41_data_migration.txt", """Workstream: Data Migration
Week: 41 (9 October 2026)
Author: Data Migration Lead

Mock migration 3 has been moved from 10 October to 17 October to run on the build that includes the batch window fix. This depends on Platform Engineering holding the 23 October deployment date for the production-like environment, which they have confirmed verbally but not in the change calendar. DEF-114 (duplicate client identifiers) has a fix in test and is expected to close by 16 October. DEF-121 (missing tax domicile) requires manual enrichment of 312 records by the client advisors concerned; Business Change has been asked to coordinate and no owner has been confirmed yet. Reconciliation sign-off by Finance remains planned for 13 November. The contractor replacement request has been approved. Treasury has asked for one further change to the currency table, which would reopen the mapping sign-off; we have declined pending SteerCo guidance.
""", [
        {"type": "slip", "summary": "Mock 3 moved to 17 Oct", "anchor": "moved from 10 October to 17 October"},
        {"type": "dependency", "summary": "Depends on 23 Oct deployment date, verbal only", "anchor": "depends on Platform Engineering holding the 23 October"},
        {"type": "issue", "summary": "DEF-121 enrichment has no owner", "anchor": "no owner has been confirmed yet"},
        {"type": "decision", "summary": "Treasury change pending SteerCo guidance", "anchor": "pending SteerCo guidance"},
    ]),
    ("wk41_technology_cutover.txt", """Workstream: Technology Cut-over
Week: 41 (9 October 2026)
Author: Technology Delivery Lead

The batch performance fix passed unit testing; regression starts 12 October and deployment to the production-like environment is confirmed for 23 October. Dress rehearsal 2 is accordingly re-planned from 31 October to the weekend of 7 to 8 November, one day after the go/no-go SteerCo. The committee will therefore be asked to decide on the basis of dress rehearsal 1 plus the fix test evidence, or to defer the decision by one week. The rollback test will be included in dress rehearsal 2 end to end. DEF-203 closed. DEF-209 remains open with a fix targeted for the 23 October deployment. One new item: the network change freeze for the Swiss data centres starts 1 December, so any deferral of the cut-over beyond 28 to 29 November would push go-live into January. The archiving licence extension has been raised with Procurement.
""", [
        {"type": "slip", "summary": "DR2 re-planned to 7-8 Nov", "anchor": "re-planned from 31 October to the weekend of 7 to 8 November"},
        {"type": "decision", "summary": "SteerCo to decide on DR1 evidence or defer", "anchor": "asked to decide on the basis of dress rehearsal 1"},
        {"type": "issue", "summary": "DEF-209 still open", "anchor": "DEF-209 remains open"},
        {"type": "risk", "summary": "Change freeze pushes any deferral into January", "anchor": "would push go-live into January"},
    ]),
    ("wk41_training.txt", """Workstream: Training and Enablement
Week: 41 (9 October 2026)
Author: Learning and Adoption Lead

Mandatory completion rose to 88%, four points below plan for the week. The two largest desks have agreed protected training slots on 20 and 21 October; if these are held, 95% is reachable by 10 November rather than 30 October. The floorwalker roster stands at 12 confirmed of 14 required; Operations has offered two senior staff but their release depends on the hypercare staffing decision. The competence assessment pilot ran with 40 advisors and 91% passed. The corporate actions procedures were returned by Operations with comments and are being revised; publication is expected on 16 October.
""", [
        {"type": "issue", "summary": "Training completion four points below plan", "anchor": "four points below plan"},
        {"type": "slip", "summary": "95% completion moves to 10 Nov", "anchor": "by 10 November rather than 30 October"},
        {"type": "risk", "summary": "12 of 14 floorwalkers confirmed", "anchor": "12 confirmed of 14 required"},
        {"type": "dependency", "summary": "Floorwalker release depends on staffing decision", "anchor": "depends on the hypercare staffing decision"},
    ]),
    ("wk41_operations.txt", """Workstream: Operations Readiness
Week: 41 (9 October 2026)
Author: Operations Readiness Lead

Confirmed hypercare staffing is unchanged at 50 of 58 FTE. We propose two options for the SteerCo: approve 8 temporary FTE from the service partner for three weeks at an estimated CHF 180,000, or reduce day-one scope by deferring the corporate actions module to a December release. Without one of these the staffing criterion stays red. The 100% load test is on 16 October as planned. The BCP walkthrough is booked for 28 October. We have identified that the service partner contract requires four weeks' notice for staff augmentation, so the decision is needed by 23 October to be effective for cut-over. Complaint volumes remain flat.
""", [
        {"type": "decision", "summary": "Two staffing options for SteerCo", "anchor": "We propose two options for the SteerCo"},
        {"type": "risk", "summary": "Staffing criterion stays red without decision", "anchor": "staffing criterion stays red"},
        {"type": "risk", "summary": "Decision needed by 23 Oct (four weeks' notice)", "anchor": "decision is needed by 23 October"},
    ]),
]


def main() -> None:
    # Milestones -> xlsx (a typical PMO input format)
    cols = ["id", "workstream", "milestone", "owner", "baseline_date", "forecast_date", "status", "pct_complete", "depends_on"]
    ms = pd.DataFrame(MILESTONES, columns=cols)
    with pd.ExcelWriter(HERE / "milestone_plan.xlsx", engine="openpyxl") as xw:
        ms.to_excel(xw, sheet_name="Milestones", index=False)
        pd.DataFrame({"key": ["as_of", "program", "release", "cutover_weekend", "go_no_go_steerco"],
                      "value": [AS_OF, "Program HORIZON (fictional)", "Release Wave 3", "2026-11-21", "2026-11-06"]}
                     ).to_excel(xw, sheet_name="Meta", index=False)

    # RAID -> csv
    raid_cols = ["id", "type", "title", "description", "workstream", "owner", "severity", "likelihood", "status", "due_date", "mitigation", "raised_on"]
    with open(HERE / "raid_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(raid_cols)
        w.writerows(RAID)

    # KPIs -> csv
    kpi_cols = ["dimension_id", "dimension", "criterion_id", "criterion", "value", "unit", "direction", "green", "amber", "source"]
    with open(HERE / "readiness_kpis.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kpi_cols)
        w.writerows(KPIS)

    # Weekly updates -> txt, ground truth -> json
    upd_dir = HERE / "weekly_updates"
    upd_dir.mkdir(exist_ok=True)
    gt = {}
    for fname, text, items in UPDATES:
        (upd_dir / fname).write_text(text.strip() + "\n", encoding="utf-8")
        gt[fname] = items
    (HERE / "ground_truth.json").write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"milestones: {len(MILESTONES)}  raid: {len(RAID)}  kpis: {len(KPIS)}  updates: {len(UPDATES)}  "
          f"ground-truth items: {sum(len(i) for _, _, i in UPDATES)}")


if __name__ == "__main__":
    main()
