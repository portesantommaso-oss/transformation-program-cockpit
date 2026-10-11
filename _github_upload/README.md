# GWM Transformation Cockpit

A working prototype of the weekly program-management cycle for a large transformation release: readiness assessment, milestone and RAID control, executive reporting and SteerCo preparation, with AI used in two narrow, reviewed places and measured rather than assumed.

Built as a portfolio project for the UBS 2026 Internship, GWM Transformation, Zurich (ref. 344205BR). Fictional program, synthetic data, public sources only. See `SOURCES.md`.

## What is in the folder

| File | What it is |
|------|-----------|
| `01_Readiness_Framework.md` | Go/no-go readiness framework: six dimensions, 24 criteria with thresholds, RAG rules, decision logic, governance cadence, where AI is and is not used |
| `02_Evaluation_Report.md` | How well the AI extractor works, measured on a development set and a held-out set, with every miss listed and an effort estimate with stated assumptions |
| `03_SteerCo_Deck.pptx` (and `.pdf`) | Six-slide Steering Committee pre-read built from the cockpit outputs, ending in one decision |
| `04_Sample_Executive_Status_Report.md` / `.pdf` | The one-page report the cockpit generates, every line with a source tag |
| `05_Sample_SteerCo_Talking_Points.md` | Draft talking points generated from the same data |
| `06_Demo_Script.md` | Script for a two-minute screen recording |
| `cockpit/` | Streamlit application and analysis engine |
| `data/` | Synthetic inputs: milestone plan (xlsx), RAID log, readiness KPIs, 15 free-text weekly updates, labelled ground truth; generator scripts |
| `eval/` | Evaluation script and raw results |
| `screenshots/` | Screenshots of the running app |

## Run it

```bash
cd UBS
python3 -m venv .venv && source .venv/bin/activate      # optional
pip install -r cockpit/requirements.txt
streamlit run cockpit/app.py
```

Regenerate data, evaluation, sample report and deck:

```bash
python data/generate_data.py
python data/generate_holdout.py
python eval/run_eval.py --set dev
python eval/run_eval.py --set holdout
python cockpit/make_sample_report.py
node deck/build_deck.js        # needs pptxgenjs; the committed .pptx is already built
```

Optional LLM extraction engine (not required for anything above):

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...
python eval/run_eval.py --engine llm --set holdout
```

## What the cockpit does

1. **Ingest**: milestone plan (Excel), RAID log (CSV), readiness KPIs (CSV), free-text weekly updates (TXT).
2. **Analyse, deterministic**: slips (forecast after baseline), overdue items, dependency conflicts (predecessor forecast after the milestone that needs it), unowned milestones and RAID entries, past-due mitigations. Readiness RAG per criterion from framework thresholds; dimension RAG is the worst criterion; recommendation from the framework's decision rules.
3. **Propose, with AI**: each weekly update is read for risks, issues, slips, dependencies and decisions. Every proposal quotes the exact source sentence. A reviewer accepts or rejects; only accepted items reach the report.
4. **Draft and release**: one-page executive status report and SteerCo talking points, each line tagged with its source record. Marked DRAFT until a named reviewer releases it.

## Responsible use of AI, as built

| Control | Where |
|---------|-------|
| Scoring and recommendation are rule-based, not AI | `cockpit/engine/analysis.py` |
| AI output is a proposal, never a record; human accept/reject per item | Weekly updates tab |
| Every AI proposal quotes its source sentence; LLM proposals whose quote is not found in the text are discarded | `cockpit/engine/extractor.py` |
| Every line of generated reporting carries a `[source: ...]` tag | `cockpit/engine/report.py` |
| Reports are DRAFT until a named reviewer releases them | Executive report tab |
| Synthetic data only; no client, employee or internal information | `data/` |
| Accuracy measured on a held-out set and reported including failures | `02_Evaluation_Report.md` |

## The main finding

The keyword-rule extractor scores 95% recall on the updates it was written alongside and 17% on a held-out set in a different writing style (precision 97 to 100% on both). Rules are precise but blind to new phrasing; a production version needs an LLM extractor with the same two controls (quoted source, human review), which is built here but not yet measured. Details and every missed item are in `02_Evaluation_Report.md`.

## Why this scenario

UBS completed the Swiss client migration from Credit Suisse platforms in March 2026 and has said the next phase is decommissioning legacy infrastructure, with the integration substantially complete by end 2026. The fictional "Program HORIZON, Release Wave 3" is a platform consolidation and legacy decommissioning release in a GWM booking center, which is the kind of program the posted role supports: business analysis, executive reporting, stakeholder coordination, readiness assessments.

## Limits

- One author wrote the data, the labels and the rules; the development-set numbers prove nothing on their own, which is why the held-out set exists.
- 57 labelled items is small; the figures carry wide uncertainty.
- The effort estimate is an estimate; the assumptions are listed so they can be challenged.
- Thresholds in the framework are illustrative, not UBS values.

## How it was built

Designed and reviewed by the author; code, synthetic data and documents drafted with AI assistance (Claude), then tested and checked by hand. The evaluation numbers are the output of `eval/run_eval.py`, not edited.

## Author

Tommaso (Roby) Portesan, Zurich. portesantommaso@gmail.com
