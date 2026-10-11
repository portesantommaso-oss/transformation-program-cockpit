"""
GWM Transformation Cockpit, prototype.

Run from the project root:
    streamlit run cockpit/app.py

Synthetic data only. See README.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import analysis, report  # noqa: E402
from engine.extractor import TYPES, extract_all, llm_available  # noqa: E402
from engine.loader import load_program  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

st.set_page_config(page_title="Transformation Cockpit", layout="wide", page_icon="▦")

RAG_COLOR = {"Green": "#2e7d32", "Amber": "#ef6c00", "Red": "#c62828"}


def rag_badge(rag: str) -> str:
    return f'<span style="background:{RAG_COLOR[rag]};color:white;padding:2px 10px;border-radius:12px;font-weight:600">{rag}</span>'


@st.cache_data(show_spinner=False)
def _load(data_dir: str):
    return load_program(data_dir)


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.title("Transformation Cockpit")
    st.caption("Program HORIZON (fictional) | Release Wave 3 | synthetic data")
    data_dir = st.text_input("Data folder", value="data", help="Relative to the project root, or an absolute path")
    if not Path(data_dir).is_absolute():
        data_dir = str(ROOT / data_dir)
    engine = st.radio("Extraction engine for weekly updates",
                      options=["rules", "llm"],
                      format_func=lambda e: {"rules": "Rules (deterministic baseline)",
                                             "llm": "LLM (Anthropic API, quoted sources)"}[e],
                      help="The rules engine is what the evaluation report measures. The LLM engine needs ANTHROPIC_API_KEY.")
    if engine == "llm" and not llm_available():
        st.warning("LLM engine unavailable: install `anthropic` and set ANTHROPIC_API_KEY. Falling back to rules.")
        engine = "rules"
    reviewer = st.text_input("Reviewer name (required to release the report)", value="")
    st.divider()
    st.markdown("**Controls in this prototype**")
    st.markdown("- Readiness scoring is deterministic (framework thresholds)\n"
                "- AI only proposes items; a reviewer accepts or rejects\n"
                "- Every line of output carries a source reference\n"
                "- Report stays DRAFT until released by a named reviewer\n"
                "- No client or employee data is used")

prog = _load(data_dir)
mflags = analysis.milestone_flags(prog)
rflags = analysis.raid_flags(prog)
crit, dims = analysis.readiness_scorecard(prog)
gng = analysis.go_no_go(dims)
ms_sum = analysis.milestone_summary(prog)

# Proposals from weekly updates
cache_key = f"cands_{engine}_{len(prog.updates)}"
if cache_key not in st.session_state:
    st.session_state[cache_key] = [c.to_dict() for c in extract_all(prog.updates, engine=engine)]
cands = st.session_state[cache_key]
if "decisions" not in st.session_state:
    st.session_state["decisions"] = {}  # sentence -> "Accept" | "Reject" | ""

accepted = [c for c in cands if st.session_state["decisions"].get(c["sentence"]) == "Accept"]

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
h1, h2 = st.columns([3, 2])
with h1:
    st.header(f"{prog.meta.get('program')} | {prog.meta.get('release')}")
    st.caption(f"As of {prog.as_of.date()} | Cut-over {prog.meta.get('cutover_weekend')} | "
               f"Go/no-go SteerCo {prog.meta.get('go_no_go_steerco')}")
with h2:
    st.markdown(f"**Readiness recommendation**<br><span style='font-size:1.6em;font-weight:700;color:"
                f"{RAG_COLOR['Red'] if gng['red'] else RAG_COLOR['Amber'] if gng['amber'] else RAG_COLOR['Green']}'>"
                f"{gng['recommendation']}</span><br><small>{gng['rule']} [source: {gng['source']}]</small>",
                unsafe_allow_html=True)

tabs = st.tabs(["Overview", "Schedule", "Readiness", "Weekly updates (AI proposals)", "Executive report",
                "SteerCo talking points", "Evaluation", "Method"])

# --------------------------------------------------------------------------- #
# Overview
# --------------------------------------------------------------------------- #
with tabs[0]:
    c = st.columns(6)
    c[0].metric("Milestones", ms_sum["total"])
    c[1].metric("Complete", ms_sum["complete"])
    c[2].metric("Slipping", ms_sum["slipping"])
    c[3].metric("Dependency conflicts", int((mflags.flag == "Dependency conflict").sum()))
    c[4].metric("Unowned RAID items", int((rflags.flag == "Unowned").sum()))
    c[5].metric("AI proposals pending review", len([x for x in cands if not st.session_state["decisions"].get(x["sentence"])]))

    st.subheader("Readiness by dimension")
    cols = st.columns(6)
    for col, d in zip(cols, dims.itertuples()):
        with col:
            st.markdown(f"**{d.dimension_id}**<br>{d.dimension}<br>{rag_badge(d.rag)}<br>"
                        f"<small>{d.red} red / {d.amber} amber / {d.green} green</small>", unsafe_allow_html=True)

    st.subheader("Top risks and issues")
    tr = analysis.top_risks(prog, 5).copy()
    tr["due_date"] = tr["due_date"].dt.date
    st.dataframe(tr, width="stretch", hide_index=True)

    st.subheader("Milestones by workstream")
    piv = prog.milestones.pivot_table(index="workstream", columns="status", values="id", aggfunc="count", fill_value=0)
    st.bar_chart(piv, horizontal=True)

# --------------------------------------------------------------------------- #
# Schedule
# --------------------------------------------------------------------------- #
with tabs[1]:
    st.subheader("Milestone plan")
    ms = prog.milestones.copy()
    ms["slip_days"] = (ms.forecast_date - ms.baseline_date).dt.days
    ms["baseline_date"] = ms.baseline_date.dt.date
    ms["forecast_date"] = ms.forecast_date.dt.date

    def _color_status(v):
        return {"Complete": "background-color:#e8f5e9", "On track": "background-color:#f1f8e9",
                "At risk": "background-color:#fff3e0", "Delayed": "background-color:#ffebee"}.get(v, "")

    st.dataframe(ms.style.map(_color_status, subset=["status"]), width="stretch", hide_index=True, height=600)

    st.subheader("Flags")
    st.caption("Slip = forecast after baseline. Dependency conflict = a predecessor is forecast to finish after the milestone that needs it. "
               "Zero float = predecessor due the same day.")
    sel = st.multiselect("Flag type", sorted(mflags.flag.unique()), default=sorted(mflags.flag.unique()))
    st.dataframe(mflags[mflags.flag.isin(sel)], width="stretch", hide_index=True)

    st.subheader("RAID log")
    raid = prog.raid.copy()
    raid["due_date"] = raid.due_date.dt.date
    raid["raised_on"] = raid.raised_on.dt.date
    st.dataframe(raid, width="stretch", hide_index=True, height=500)
    st.markdown("**RAID hygiene flags**")
    st.dataframe(rflags, width="stretch", hide_index=True)

# --------------------------------------------------------------------------- #
# Readiness
# --------------------------------------------------------------------------- #
with tabs[2]:
    st.subheader("Go/no-go scorecard")
    st.caption("Dimension RAG is the worst criterion RAG (no averaging). Rules from 01_Readiness_Framework.md, section 3 and 4.")
    for d in dims.itertuples():
        with st.expander(f"{d.dimension_id}  {d.dimension}   |   {d.rag}", expanded=(d.rag != "Green")):
            c = crit[crit.dimension_id == d.dimension_id][["criterion_id", "criterion", "display", "rag", "green", "amber", "direction", "source"]]
            c = c.rename(columns={"display": "value", "green": "green threshold", "amber": "amber threshold"})

            def _c(v):
                return f"color:{RAG_COLOR.get(v, 'inherit')};font-weight:700"

            st.dataframe(c.style.map(_c, subset=["rag"]), width="stretch", hide_index=True)
    st.markdown(f"**Recommendation: {gng['recommendation']}.** {gng['rule']}. [source: {gng['source']}]")

# --------------------------------------------------------------------------- #
# Weekly updates and AI proposals
# --------------------------------------------------------------------------- #
with tabs[3]:
    st.subheader("Proposed RAID items from free-text weekly updates")
    st.caption(f"Engine: **{engine}**. Each proposal quotes the exact sentence it came from. Nothing enters the RAID log "
               "until a reviewer accepts it. Accepted items flow into the executive report and talking points.")
    left, right = st.columns([3, 2])
    with left:
        fsel = st.selectbox("Filter by update", ["All"] + sorted(prog.updates))
        tsel = st.multiselect("Type", list(TYPES), default=list(TYPES))
        view = [c for c in cands if (fsel == "All" or c["file"] == fsel) and c["type"] in tsel]
        for i, c in enumerate(view):
            key = c["sentence"]
            with st.container(border=True):
                a, b = st.columns([5, 1])
                a.markdown(f"**{c['type'].upper()}** · {c['severity']} · {c['workstream']} · <small>{c['file']}</small>",
                           unsafe_allow_html=True)
                a.markdown(f"> {c['sentence']}")
                a.caption("signals: " + ", ".join(c["signals"]))
                opts = ["Pending", "Accept", "Reject"]
                cur = st.session_state["decisions"].get(key, "") or "Pending"
                choice = b.radio("Decision", opts, index=opts.index(cur), key=f"dec_{engine}_{i}_{hash(key)}",
                                 label_visibility="collapsed")
                st.session_state["decisions"][key] = "" if choice == "Pending" else choice
        if not view:
            st.info("No proposals for this filter.")
    with right:
        st.markdown("**Source text**")
        show = fsel if fsel != "All" else sorted(prog.updates)[0]
        st.text_area(show, prog.updates[show], height=420, disabled=True)
        n_acc = sum(1 for v in st.session_state["decisions"].values() if v == "Accept")
        n_rej = sum(1 for v in st.session_state["decisions"].values() if v == "Reject")
        st.metric("Accepted / rejected", f"{n_acc} / {n_rej}")
        if st.button("Export accepted items as RAID candidates (CSV)"):
            df = pd.DataFrame(accepted)
            st.download_button("Download", df.to_csv(index=False).encode(), "raid_candidates.csv", "text/csv")

# --------------------------------------------------------------------------- #
# Executive report
# --------------------------------------------------------------------------- #
with tabs[4]:
    released = st.checkbox("Release this report (requires reviewer name)", value=False, disabled=not reviewer)
    md = report.executive_report(prog, accepted, reviewer=reviewer, released=released)
    st.download_button("Download report (Markdown)", md.encode(), "executive_status_report.md", "text/markdown")
    st.markdown(md)

# --------------------------------------------------------------------------- #
# Talking points
# --------------------------------------------------------------------------- #
with tabs[5]:
    tp = report.steerco_talking_points(prog, accepted)
    st.download_button("Download talking points (Markdown)", tp.encode(), "steerco_talking_points.md", "text/markdown")
    st.markdown(tp)

# --------------------------------------------------------------------------- #
# Evaluation
# --------------------------------------------------------------------------- #
with tabs[6]:
    st.subheader("How well does the extractor work?")
    st.caption("Results from eval/run_eval.py. Re-run with `python eval/run_eval.py --set dev|holdout [--engine llm]`.")
    rows = []
    for p in sorted((ROOT / "eval").glob("results_*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        rows.append({"engine": r["engine"], "set": r.get("dataset", "dev"), "updates": r["updates"],
                     "labelled items": r["ground_truth_items"], "recall": r["recall"], "precision": r["precision"],
                     "F1": r["f1"], "type accuracy": r["type_accuracy_on_found"], "missed": r["missed_items"],
                     "false positives": r["false_positive_sentences"]})
    if rows:
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    else:
        st.info("No results yet. Run eval/run_eval.py.")
    st.markdown((ROOT / "02_Evaluation_Report.md").read_text(encoding="utf-8")
                if (ROOT / "02_Evaluation_Report.md").exists() else "")

# --------------------------------------------------------------------------- #
# Method
# --------------------------------------------------------------------------- #
with tabs[7]:
    st.markdown((ROOT / "01_Readiness_Framework.md").read_text(encoding="utf-8"))
