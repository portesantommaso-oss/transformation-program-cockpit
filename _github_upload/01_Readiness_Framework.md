# Release Readiness Framework
## GWM Transformation Cockpit, illustrative case

**Scenario (fictional):** Program HORIZON, Release Wave 3. A Global Wealth Management (GWM) booking center in Switzerland consolidates advisor workflows onto the target platform and decommissions a legacy application cluster. Go-live is planned for a weekend cut-over. The Steering Committee (SteerCo) must take a go/no-go decision two weeks before cut-over.

**Why this scenario.** UBS completed the transfer of former Credit Suisse clients in Switzerland onto its own platforms in March 2026 and has said the next phase is decommissioning legacy infrastructure, with the integration to be substantially complete by end of 2026 (see `SOURCES.md`). The program management disciplines below (readiness assessment, milestone control, RAID governance, executive reporting) are the ones that phase relies on. All names, dates, figures and data in this project are synthetic.

---

## 1. Purpose

Give the SteerCo one page that answers three questions before any cut-over:

1. Are we ready on every dimension that can hurt a client or breach a control?
2. Where are we not ready, who owns the gap, and when does it close?
3. What decision is being asked of the committee today?

The framework is deliberately simple: six dimensions, measurable criteria, named owners, numeric thresholds, and one rule that turns the numbers into red / amber / green (RAG). Anything that cannot be measured is recorded as an assumption in the RAID log rather than scored.

## 2. Readiness dimensions

| # | Dimension | What it protects | Accountable owner (role) |
|---|-----------|------------------|--------------------------|
| D1 | Data quality and reconciliation | Correct positions, balances and client records on the target platform | Data Migration Lead |
| D2 | Client and advisor communication | Clients and client advisors know what changes, when, and whom to call | Business Change Lead |
| D3 | Training and enablement | Advisors and operations staff can execute day-one processes | Learning and Adoption Lead |
| D4 | Technology cut-over and decommissioning | The cut-over runbook works, rollback exists, legacy exit is safe | Technology Delivery Lead |
| D5 | Regulatory, risk and control sign-off | Required approvals, controls and audit evidence are in place | Risk and Control Lead |
| D6 | Operational capacity and service continuity | Volumes on day one and the following weeks can be absorbed | Operations Readiness Lead |

## 3. Criteria, thresholds and RAG rules

Each dimension has three to four criteria. Each criterion has a metric, a green threshold and an amber threshold; anything below amber is red. The dimension RAG is the worst criterion RAG (no averaging: one red criterion makes the dimension red, because the committee needs to see the weakest link, not the mean).

### D1 Data quality and reconciliation
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Mock migration reconciliation | % of records reconciled with zero breaks in the latest mock run | ≥ 99.5% | 98.0 to 99.5% | < 98.0% |
| Open data defects | Count of open severity 1 and 2 data defects | 0 | 1 to 3 | > 3 |
| Reference data alignment | % of mapping tables signed off by data owners | 100% | 90 to 99% | < 90% |
| Mock runs completed | Number of full mock migrations completed as planned | ≥ 3 | 2 | ≤ 1 |

### D2 Client and advisor communication
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Client notifications sent | % of in-scope clients notified per regulatory notice period | 100% | 97 to 99% | < 97% |
| Advisor briefings | % of client advisors who attended a release briefing | ≥ 95% | 85 to 94% | < 85% |
| Hypercare contact model | Hypercare hotline, escalation tree and FAQ published | Published | Draft | Not started |
| Client complaint trend | Complaints linked to the program, last 4 weeks vs prior 4 | Flat or down | Up < 20% | Up ≥ 20% |

### D3 Training and enablement
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Training completion | % of mandatory modules completed by in-scope staff | ≥ 95% | 85 to 94% | < 85% |
| Competence check | % passing the day-one process assessment | ≥ 90% | 80 to 89% | < 80% |
| Floorwalker coverage | Ratio of trained floorwalkers to advisor desks on day one | ≥ 1:10 | 1:11 to 1:15 | < 1:15 |
| Procedure documentation | % of day-one procedures published in the target format | 100% | 90 to 99% | < 90% |

### D4 Technology cut-over and decommissioning
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Dress rehearsal result | Latest dress rehearsal completed within the cut-over window | Yes, with margin ≥ 2h | Yes, margin < 2h | Not completed or overran |
| Open defects | Count of open severity 1 and 2 technical defects | 0 | 1 to 2 | > 2 |
| Rollback tested | Rollback executed end to end in a rehearsal | Yes | Partially | No |
| Decommissioning gate | Legacy applications with archiving and access-removal plan approved | 100% | 90 to 99% | < 90% |

### D5 Regulatory, risk and control sign-off
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Formal approvals | Required internal approvals obtained (risk, compliance, legal, operational risk) | All | One pending with date | Any pending without date |
| Control testing | % of key controls tested on the target platform with evidence | 100% | 90 to 99% | < 90% |
| Open audit or regulatory findings | Findings rated high linked to the release | 0 | 1 with agreed action | > 1 or no action |
| Record retention | Archiving of legacy records confirmed to retention policy | Confirmed | Plan agreed | Open |

### D6 Operational capacity and service continuity
| Criterion | Metric | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Day-one staffing | Planned staff on hypercare vs model requirement | ≥ 100% | 90 to 99% | < 90% |
| Backlog headroom | Projected open-items backlog in week 1 vs processing capacity | ≤ 70% | 71 to 90% | > 90% |
| Performance test | Target platform load test at 120% of expected peak | Passed | Passed at 100% only | Failed |
| Service continuity plan | Business continuity plan updated and walked through | Done | Drafted | Not started |

## 4. From RAG to a go/no-go recommendation

| Pattern | Recommendation |
|---------|----------------|
| All six dimensions green | Go |
| Any amber, no red | Go with conditions: each amber has a named owner and a closure date before cut-over |
| Any red in D1, D4 or D5 | No-go, re-plan: these dimensions protect client data, the cut-over itself and regulatory obligations |
| Red in D2, D3 or D6 only | Conditional: cut-over may proceed if a mitigation is approved by the SteerCo (for example extended hypercare, phased advisor onboarding) and the red is tracked daily |

The recommendation is advisory. The SteerCo takes the decision and the minutes record the rationale and the conditions.

## 5. Governance cadence

| Checkpoint | Timing | Input | Output |
|------------|--------|-------|--------|
| Weekly readiness review | Every week from T-8 | Workstream updates, RAID log, milestone plan | Updated scorecard, flagged items |
| Go/no-go preparation | T-3 weeks | Scorecard trend, open ambers and reds | Draft recommendation, decision paper |
| Go/no-go SteerCo | T-2 weeks | Decision paper | Decision, conditions, owners |
| Final confirmation | T-3 days | Re-run of all red/amber criteria | Confirm or defer |
| Post go-live review | T+4 weeks | Hypercare metrics | Lessons learned, framework updates |

## 6. Data sources behind each criterion

Every scorecard value must trace to a system record or a signed document. In the cockpit prototype the trace is the `source` column in `data/readiness_kpis.csv`. In a real program the sources would be the test management tool, the learning management system, the communication tracker, the RAID log and the approval register. No value is entered without a source.

## 7. Role of AI in this process

AI is used in three narrow places, each with a human check:

1. **Reading weekly free-text updates** and proposing risks, slipping milestones and decisions for the RAID log. A reviewer accepts or rejects each proposal; nothing enters the log automatically.
2. **Drafting the executive status report** from structured data. Every sentence carries a reference to the row or document it came from. The report is marked DRAFT until a named reviewer releases it.
3. **Drafting SteerCo talking points.** Same rule: draft only, source trace on each point.

What AI is not used for: scoring readiness (the thresholds above are deterministic), taking the go/no-go recommendation, or any processing of client data. The prototype runs on synthetic data and never needs client or employee records.

The evaluation in `02_Evaluation_Report.md` measures how well step 1 works on this dataset and lists what it missed.
