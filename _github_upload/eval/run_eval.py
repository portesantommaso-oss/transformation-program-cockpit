"""
Evaluate the rule-based extractor against the labelled ground truth.

    python eval/run_eval.py                      # rules engine, dev set (default)
    python eval/run_eval.py --set holdout        # rules engine, held-out set
    python eval/run_eval.py --engine llm         # requires ANTHROPIC_API_KEY

Matching: a ground-truth item counts as found if its anchor substring appears
(case-insensitive) in any extracted sentence from the same file. An extracted
sentence counts as a true positive if it contains at least one anchor.
Type accuracy is measured on true positives only.

Writes eval/results.json and prints a summary. Nothing here is tuned on the
test set after the fact: the patterns were written first, then run.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cockpit"))

from engine.extractor import extract_all  # noqa: E402
from engine.loader import load_program  # noqa: E402


def evaluate(engine: str = "rules", dataset: str = "dev") -> dict:
    prog = load_program(ROOT / "data")
    if dataset == "holdout":
        upd_dir = ROOT / "data" / "weekly_updates_holdout"
        updates = {p.name: p.read_text(encoding="utf-8") for p in sorted(upd_dir.glob("*.txt"))}
        gt = json.loads((ROOT / "data" / "ground_truth_holdout.json").read_text(encoding="utf-8"))
    else:
        updates = prog.updates
        gt = json.loads((ROOT / "data" / "ground_truth.json").read_text(encoding="utf-8"))
    cands = extract_all(updates, engine=engine)

    found, missed, tp, fp = [], [], [], []
    type_correct = 0
    for fname, items in gt.items():
        file_cands = [c for c in cands if c.file == fname]
        for it in items:
            hits = [c for c in file_cands if it["anchor"].lower() in c.sentence.lower()]
            if hits:
                found.append({**it, "file": fname, "predicted_type": hits[0].type,
                              "type_match": hits[0].type == it["type"]})
                type_correct += hits[0].type == it["type"]
            else:
                missed.append({**it, "file": fname})
    for c in cands:
        anchors = [it["anchor"].lower() for it in gt.get(c.file, [])]
        (tp if any(a in c.sentence.lower() for a in anchors) else fp).append(c.to_dict())

    n_gt = sum(len(v) for v in gt.values())
    recall = len(found) / n_gt if n_gt else 0
    precision = len(tp) / len(cands) if cands else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {
        "engine": engine,
        "dataset": dataset,
        "updates": len(updates),
        "ground_truth_items": n_gt,
        "extracted_sentences": len(cands),
        "true_positive_sentences": len(tp),
        "false_positive_sentences": len(fp),
        "found_items": len(found),
        "missed_items": len(missed),
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "f1": round(f1, 3),
        "type_accuracy_on_found": round(type_correct / len(found), 3) if found else 0,
        "missed": missed,
        "false_positives": fp,
        "found": found,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="rules", choices=["rules", "llm"])
    ap.add_argument("--set", dest="dataset", default="dev", choices=["dev", "holdout"],
                    help="dev = the 10 updates the rules were written next to; holdout = 5 updates written after the rules were frozen")
    args = ap.parse_args()
    res = evaluate(args.engine, args.dataset)
    out = ROOT / "eval" / f"results_{args.engine}_{args.dataset}.json"
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"engine={res['engine']}  set={res['dataset']}  updates={res['updates']}  gt_items={res['ground_truth_items']}")
    print(f"recall={res['recall']}  precision={res['precision']}  f1={res['f1']}  "
          f"type_acc={res['type_accuracy_on_found']}")
    print(f"found={res['found_items']}  missed={res['missed_items']}  "
          f"extracted={res['extracted_sentences']}  fp={res['false_positive_sentences']}")
    print("\nMISSED:")
    for m in res["missed"]:
        print(f"  [{m['type']}] {m['file']}: {m['summary']}  (anchor: '{m['anchor']}')")
    print("\nFALSE POSITIVES:")
    for f in res["false_positives"]:
        print(f"  [{f['type']}] {f['file']}: {f['sentence'][:110]}")
    print("\nTYPE MISMATCHES:")
    for f in res["found"]:
        if not f["type_match"]:
            print(f"  {f['file']}: expected {f['type']}, got {f['predicted_type']}: {f['summary']}")
    print(f"\nwritten: {out}")


if __name__ == "__main__":
    main()
