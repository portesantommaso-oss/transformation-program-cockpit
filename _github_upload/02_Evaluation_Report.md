# Evaluation Report: reading weekly updates with AI
## Does the extractor find the risks a program manager would log?

**Question.** When a workstream sends a free-text weekly update, can the cockpit propose the right RAID entries (risks, issues, slips, dependencies, decisions) with a source sentence for each?

**Set-up.** 15 synthetic weekly updates, labelled by hand with 57 items a PMO analyst would be expected to log. Each label has an anchor phrase; a proposal counts as correct if it quotes a sentence containing that phrase. The rule-based engine (`cockpit/engine/extractor.py`) was written once and then frozen. Nothing was changed after the held-out run.

Two test sets:

| Set | Updates | Labelled items | How it was written |
|-----|---------|----------------|--------------------|
| Development | 10 (weeks 40 and 41, six workstreams) | 39 | Written alongside the extraction rules, in full prose |
| Held-out | 5 (week 42) | 18 | Written after the rules were frozen, terser style, fewer signal words |

Run: `python eval/run_eval.py --set dev` and `python eval/run_eval.py --set holdout`. Raw results are in `eval/results_rules_dev.json` and `eval/results_rules_holdout.json`.

## Results

| Set | Recall | Precision | F1 | Type accuracy (on found items) | Missed | False positives |
|-----|--------|-----------|----|-------------------------------|--------|-----------------|
| Development | 94.9% (37 of 39) | 97.3% (36 of 37) | 0.96 | 91.9% | 2 | 1 |
| Held-out | 16.7% (3 of 18) | 100% (3 of 3) | 0.29 | 66.7% | 15 | 0 |

## What this means

1. **The development score is not evidence of anything.** The person who wrote the rules also wrote the updates, in the same week. Recall of 95% there measures how consistently one author uses words such as "delayed", "depends on" and "remains open", not how well the method generalises.

2. **The held-out score is the real number.** When the week-42 authors wrote tersely ("3 failures under investigation", "written but unreviewed", "cover is not yet arranged", "lands around 12 November, not 6 November"), the rules missed 15 of 18 items. Precision stayed at 100%, so the rules are safe but blind: what they propose is right, but they propose very little.

3. **Keyword rules cannot be the production engine.** Status updates are written by many people in many styles. A rule set tuned to one style will fail on the next workstream. This is the case for an LLM-based extractor, which reads meaning rather than vocabulary, with two controls kept from this prototype: the model must quote the exact source sentence (any proposal whose quote is not found in the text is discarded), and a human reviewer accepts or rejects every proposal before it reaches the RAID log.

4. **The LLM engine is built but not yet measured.** `cockpit/engine/extractor.py` contains the LLM path with the quote check. Running `python eval/run_eval.py --engine llm --set holdout` with an API key produces the comparable number. Until that has been run, no claim is made about the LLM engine's accuracy.

## Detail: what the rules missed and why

**Development set, 2 misses**

| Update | Item | Why missed |
|--------|------|-----------|
| wk40_data_migration | Two of three mock runs used last quarter's reference data snapshot | Plain statement of fact; the risk is implied, no signal word |
| wk41_technology_cutover | Committee will be asked to decide on DR1 evidence or defer | Passive voice ("will therefore be asked to decide"); the decision pattern expects "we need/ask ... SteerCo ... decide" |

**Development set, 1 false positive**

| Update | Sentence | Comment |
|--------|----------|---------|
| wk41_operations | "Confirmed hypercare staffing is unchanged at 50 of 58 FTE." | Flagged as an issue by the "N of M FTE" pattern. Arguably a correct flag that the labeller did not mark because the same gap is labelled in week 40. Kept as a false positive to avoid adjusting labels after the run. |

**Development set, 3 type mismatches** (found, but classified as decision or dependency where the label said risk). The sentences carried both meanings; the engine picks one primary type by fixed priority (decision > slip > dependency > issue > risk). A reviewer would correct the type in one click.

**Held-out set, 15 misses, grouped by cause**

| Cause | Count | Examples |
|-------|-------|----------|
| Fact stated without a signal word | 6 | "3 failures under investigation"; "CHF 42k against CHF 30k budgeted"; "desk B cancelled theirs"; "have not started" |
| Negated or passive phrasing not covered | 4 | "written but unreviewed"; "cover is not yet arranged"; "Still no written answer from Finance"; "asked for the failure analysis beforehand" |
| Date change phrased without "moved/delayed" | 2 | "lands around 12 November, not 6 November"; "brought forward to 3 November" |
| Conditional phrased with "if contracted" | 1 | "if contracted by 23 October" |
| Decision phrased as a request from a person | 1 | "asked for a third staffing option" |
| Consequence phrased with "would arrive after" | 1 | "findings would arrive after the go/no-go" |

Each of these could be patched with another pattern. That is the point: patching is endless, and every patch is tuned to the last update that broke it.

## Estimated effort effect, with assumptions

This is an estimate, not a measurement. Assumptions are listed so they can be challenged.

| Item | Assumption | Basis |
|------|-----------|-------|
| Weekly updates received | 6 workstreams, one update each | Program structure in this scenario |
| Manual processing per update | 20 minutes to read, extract RAID candidates, cross-check the plan | Typical PMO analyst task; to be validated with a real team |
| Manual executive report | 3 hours per week to compile scorecard, slips, risks, decisions | Includes chasing sources and formatting |
| With cockpit, review of AI proposals | 5 minutes per update (accept/reject, fix types) | Proposals arrive pre-sorted with the source sentence |
| With cockpit, report | 30 minutes to review the generated draft and release it | Structured data already in place |

Weekly effort: manual about 5 hours (6 × 20 min + 3 h); with the cockpit about 1 hour (6 × 5 min + 30 min). Saving of roughly 4 hours per week per program, or around 80% of reporting effort, **only if** the extractor reaches recall above 85% on real updates, which the rules engine does not. The saving should be re-estimated after the LLM engine is measured on the held-out set and after a two-week trial on real (anonymised) updates.

## Limits of this evaluation

- Synthetic data, one author. Real updates are noisier, longer, and include tables and attachments.
- 57 labelled items is a small sample; the held-out figures have wide uncertainty.
- Labels reflect one person's judgement of what should be logged. A second labeller and an agreement score would be the next step.
- The anchor-phrase matching is strict: a proposal quoting a neighbouring sentence counts as a miss.

## Next steps

1. Run the LLM engine on both sets and add the row to the table above.
2. Have a second person label the held-out set; report inter-rater agreement.
3. Trial on two weeks of anonymised real updates with a PMO analyst reviewing every proposal; measure recall, precision and review time.
4. Only then decide whether the tool enters the weekly reporting cycle.
