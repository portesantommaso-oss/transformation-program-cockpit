# Two-minute screen recording script

Record with the app running (`streamlit run cockpit/app.py`), 1440 px wide or more. Speak plainly; no music.

| Time | On screen | Say |
|------|-----------|-----|
| 0:00 | Overview tab, header with "Conditional go" | "This is a program cockpit for a release go/no-go. Fictional program, synthetic data. One question: is this release ready, and what does the committee need to decide?" |
| 0:15 | Readiness by dimension cards | "Six readiness dimensions, each scored against fixed thresholds from a written framework. No AI touches the scoring. D6, operational capacity, is red: 50 of 58 hypercare staff confirmed." |
| 0:30 | Schedule tab, Flags filtered to Dependency conflict | "The plan itself has seven dependency conflicts. The decision paper is due on 4 November but three of its inputs land after that date. The tool found this from the milestone file alone." |
| 0:50 | Weekly updates tab | "Workstreams send free-text updates. The tool proposes RAID items and quotes the exact sentence for each. Nothing goes into the log until I accept it." Accept two or three items, including a decision. |
| 1:10 | Executive report tab | "The one-page report is generated from the data, every line with a source tag, and it stays marked DRAFT until a named reviewer releases it." Type a reviewer name, tick release. |
| 1:30 | Evaluation tab | "I measured the extractor. On updates written next to the rules it finds 95 per cent. On a held-out set in a different style it finds 17 per cent. That is the honest number, and it is why the production design is an LLM extractor with the same controls: quoted source and human review." |
| 1:50 | SteerCo deck slide 5 | "The output is a six-slide pre-read ending in one decision: close the staffing gap by 23 October, option A, B or C." |
| 2:00 | End | "Framework, prototype, evaluation and deck are in the repository." |

Tips: hide the sidebar data path before recording; set the reviewer name beforehand so the release checkbox is enabled; keep the cursor still while speaking.
