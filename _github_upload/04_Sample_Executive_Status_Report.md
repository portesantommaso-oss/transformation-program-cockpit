# Program HORIZON (fictional) | Release Wave 3 | Executive status
As of 2026-10-09 | Cut-over 2026-11-21 | Go/no-go SteerCo 2026-11-06 | Status: **DRAFT, not for distribution** | Reviewer: PMO Lead (sample)

## Headline
- Readiness recommendation: **Conditional go**. Rule applied: Red in D6 only; requires SteerCo-approved mitigation tracked daily. [source: 01_Readiness_Framework.md section 4]
- Weakest dimension: D6 Operational capacity and service continuity (Red). [source: readiness_kpis.csv, D6]
- Milestones: 8 of 30 complete, 9 slipping, 5 marked delayed. [source: milestone_plan.xlsx]

## Readiness scorecard
| Dimension | RAG | Red / Amber / Green criteria | Weakest criterion |
|---|---|---|---|
| D1 Data quality and reconciliation | Amber | 0 / 3 / 1 | Mock migration reconciliation: 99.1% [source: Mock 2 reconciliation report, 19 Sep] |
| D2 Client and advisor communication | Green | 0 / 0 / 4 | In-scope clients notified: 100% [source: Communication tracker, 26 Sep dispatch] |
| D3 Training and enablement | Amber | 0 / 3 / 1 | Mandatory training completion: 88% [source: Learning management system, 9 Oct] |
| D4 Technology cut-over and decommissioning | Amber | 0 / 4 / 0 | Dress rehearsal margin to hard stop: 1.25 hours [source: DR1 run log, 3-4 Oct] |
| D5 Regulatory, risk and control sign-off | Amber | 0 / 3 / 1 | Formal approvals obtained: One pending with date [source: Approval register: Compliance 30 Oct expected, Operational Risk 13 Nov] |
| D6 Operational capacity and service continuity | Red | 2 / 2 / 0 | Hypercare staffing vs model requirement: 86% [source: Staffing plan, 50 of 58 FTE confirmed, 9 Oct] |

## Schedule: slips and dependency conflicts
- Dependency conflict (High): M02 Go/no-go decision paper issued, owner PMO Lead. Depends on M18 'Competence assessment closed' forecast 2026-11-06, after own forecast 2026-11-04. [source: milestone_plan.xlsx rows M02, M18]
- Dependency conflict (High): M02 Go/no-go decision paper issued, owner PMO Lead. Depends on M22 'Rollback procedure tested end to end' forecast 2026-11-07, after own forecast 2026-11-04. [source: milestone_plan.xlsx rows M02, M22]
- Dependency conflict (High): M02 Go/no-go decision paper issued, owner PMO Lead. Depends on M26 'Operational risk approval' forecast 2026-11-13, after own forecast 2026-11-04. [source: milestone_plan.xlsx rows M02, M26]
- Dependency conflict (High): M08 Mock migration 3, owner Data Migration Lead. Depends on M21 'Batch window performance fix deployed' forecast 2026-10-23, after own forecast 2026-10-17. [source: milestone_plan.xlsx rows M08, M21]
- Dependency conflict (High): M18 Competence assessment closed, owner Learning Lead. Depends on M16 'Mandatory training 95% complete' forecast 2026-11-10, after own forecast 2026-11-06. [source: milestone_plan.xlsx rows M18, M16]
- Dependency conflict (High): M24 Key control testing on target platform, owner Risk and Control Lead. Depends on M20 'Dress rehearsal 2' forecast 2026-11-07, after own forecast 2026-10-23. [source: milestone_plan.xlsx rows M24, M20]
- Dependency conflict (High): M27 Record retention confirmation, owner Records Management. Depends on M23 'Legacy archiving and access-removal plan approved' forecast 2026-10-23, after own forecast 2026-10-16. [source: milestone_plan.xlsx rows M27, M23]
- Slip (High): M08 Mock migration 3, owner Data Migration Lead. Forecast 2026-10-17 is 7 days after baseline 2026-10-10. [source: milestone_plan.xlsx row M08]
- Slip (High): M09 Severity 1/2 data defects closed, owner Data Migration Lead. Forecast 2026-11-06 is 7 days after baseline 2026-10-30. [source: milestone_plan.xlsx row M09]
- Slip (High): M16 Mandatory training 95% complete, owner Learning Lead. Forecast 2026-11-10 is 11 days after baseline 2026-10-30. [source: milestone_plan.xlsx row M16]
- Slip (High): M20 Dress rehearsal 2, owner Technology Delivery Lead. Forecast 2026-11-07 is 7 days after baseline 2026-10-31. [source: milestone_plan.xlsx row M20]
- Slip (High): M21 Batch window performance fix deployed, owner Platform Engineering Lead. Forecast 2026-10-23 is 7 days after baseline 2026-10-16. [source: milestone_plan.xlsx row M21]
- Slip (High): M22 Rollback procedure tested end to end, owner Technology Delivery Lead. Forecast 2026-11-07 is 7 days after baseline 2026-10-31. [source: milestone_plan.xlsx row M22]
- Slip (High): M26 Operational risk approval, owner Operational Risk Officer. Forecast 2026-11-13 is 14 days after baseline 2026-10-30. [source: milestone_plan.xlsx row M26]
- Slip (High): M28 Hypercare staffing plan approved, owner Operations Readiness Lead. Forecast 2026-10-23 is 14 days after baseline 2026-10-09. [source: milestone_plan.xlsx row M28]
- Slip (High): M29 Load test at 120% of expected peak, owner Platform Engineering Lead. Forecast 2026-10-23 is 7 days after baseline 2026-10-16. [source: milestone_plan.xlsx row M29]

## Top risks and issues
- R03 (Risk, High/High, due 23 Oct): Hypercare staffing below model requirement. Owner: Operations Readiness Lead. Mitigation: SteerCo options: 8 temporary FTE from service partner (CHF 180k) or defer corporate actions module. [source: raid_log.csv row R03]
- R02 (Risk, High/High, due 06 Nov): Operational Risk approval after go/no-go SteerCo. Owner: Risk and Control Lead. Mitigation: Request conditional approval; close DEF-114 by 16 Oct and DEF-121 by 6 Nov. [source: raid_log.csv row R02]
- R01 (Risk, High/Medium, due 23 Oct): Batch window fix late for dress rehearsal 2. Owner: Platform Engineering Lead. Mitigation: Daily stand-up with Platform Engineering; fallback is DR2 on current build with reduced evidence. [source: raid_log.csv row R01]
- R06 (Risk, High/Low, due 06 Nov): Network change freeze from 1 December. Owner: Technology Delivery Lead. Mitigation: Decision paper to present 28-29 Nov as the only fallback weekend. [source: raid_log.csv row R06]
- R07 (Risk, Medium/Medium, due 16 Oct): Reference data mapping reopened by Treasury change. Owner: Data Migration Lead. Mitigation: Declined pending SteerCo guidance; propose change for Release 4. [source: raid_log.csv row R07]

RAID hygiene:
- Unowned: I02 DEF-121 missing tax domicile on 312 legacy records. No owner recorded. [source: raid_log.csv row I02]
- Unowned: D03 Finance year-end freeze calendar confirmation. No owner recorded. [source: raid_log.csv row D03]
- Unowned: D05 Archiving tool licence extension. No owner recorded. [source: raid_log.csv row D05]

## New items from weekly updates (reviewer-accepted only)
- [DECISION, Medium] Business Change and Communication: "The guide may therefore be delivered in two of the three languages on day one unless the variance is approved." [source: wk40_business_change.txt]
- [DECISION, High] Risk and Control: "We need the SteerCo to decide whether a conditional approval from Operational Risk is acceptable for the decision on 6 November." [source: wk40_risk_control.txt]
- [DECISION, High] Data Migration: "Treasury has asked for one further change to the currency table, which would reopen the mapping sign-off; we have declined pending SteerCo guidance." [source: wk41_data_migration.txt]
- [DECISION, High] Operations Readiness: "We propose two options for the SteerCo: approve 8 temporary FTE from the service partner for three weeks at an estimated CHF 180,000, or reduce day-one scope by deferring the corporate actions module to a December release." [source: wk41_operations.txt]
- [DECISION, High] Operations Readiness: "We have identified that the service partner contract requires four weeks' notice for staff augmentation, so the decision is needed by 23 October to be effective for cut-over." [source: wk41_operations.txt]

## Decisions requested from the SteerCo
- Approve mitigation for red dimension(s) D6 or defer cut-over. [source: 01_Readiness_Framework.md section 4]
- Business Change and Communication: "The guide may therefore be delivered in two of the three languages on day one unless the variance is approved." [source: wk40_business_change.txt]
- Risk and Control: "We need the SteerCo to decide whether a conditional approval from Operational Risk is acceptable for the decision on 6 November." [source: wk40_risk_control.txt]
- Data Migration: "Treasury has asked for one further change to the currency table, which would reopen the mapping sign-off; we have declined pending SteerCo guidance." [source: wk41_data_migration.txt]
- Operations Readiness: "We propose two options for the SteerCo: approve 8 temporary FTE from the service partner for three weeks at an estimated CHF 180,000, or reduce day-one scope by deferring the corporate actions module to a December release." [source: wk41_operations.txt]
- Operations Readiness: "We have identified that the service partner contract requires four weeks' notice for staff augmentation, so the decision is needed by 23 October to be effective for cut-over." [source: wk41_operations.txt]

---
Generated by the Transformation Cockpit from structured program data. Synthetic data; no client information. Every bullet carries a source reference. A named reviewer must release this report before distribution.