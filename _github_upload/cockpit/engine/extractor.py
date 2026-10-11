"""
Reads free-text weekly updates and proposes RAID candidates.

Two engines:
  * rules  : deterministic pattern matching (default, no network, reproducible,
             this is what the evaluation in eval/run_eval.py measures)
  * llm    : optional, uses the Anthropic API when ANTHROPIC_API_KEY is set.
             Output is forced to quote the exact source sentence so that every
             proposal remains traceable to the text it came from.

Both engines return the same structure. Nothing here writes to the RAID log:
a human reviewer accepts or rejects each proposal in the app.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict

TYPES = ("decision", "slip", "dependency", "issue", "risk")


@dataclass
class Candidate:
    file: str
    workstream: str
    week: str
    type: str
    severity: str
    sentence: str          # exact source sentence (the trace)
    signals: list[str]     # which patterns fired
    engine: str

    def to_dict(self) -> dict:
        return asdict(self)


# --------------------------------------------------------------------------- #
# Sentence handling
# --------------------------------------------------------------------------- #
_HEADER_RE = re.compile(r"^(Workstream|Week|Author):\s*(.*)$", re.M)
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def parse_header(text: str) -> dict:
    return {m.group(1).lower(): m.group(2).strip() for m in _HEADER_RE.finditer(text)}


def split_sentences(text: str) -> list[str]:
    body = _HEADER_RE.sub("", text).strip()
    body = re.sub(r"\s+", " ", body)
    return [s.strip() for s in _SENT_SPLIT.split(body) if s.strip()]


# --------------------------------------------------------------------------- #
# Rule engine
# --------------------------------------------------------------------------- #
PATTERNS: dict[str, list[tuple[str, str]]] = {
    "decision": [
        (r"\b(need|needs|ask|asked)\b.*\b(SteerCo|committee|sponsor)\b.*\b(decide|decision|approv)", "ask to committee"),
        (r"\bpropose (two|three|\d+) options\b|\boptions for the (SteerCo|committee)\b", "options proposed"),
        (r"\bpending (SteerCo|committee|sponsor) (guidance|decision|approval)\b", "pending guidance"),
        (r"\bdecision is needed by\b|\bdecision (is )?required\b", "decision deadline"),
        (r"\bunless the variance is approved\b|\bvariance (request|approval)\b", "variance approval"),
    ],
    "slip": [
        (r"\b(now expected|re-?planned|moved|moves|pushed|deferred|postponed) (on|from|to)\b", "date moved"),
        (r"\brather than \d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December)\b", "rather than <date>"),
        (r"\b(later than planned|behind (plan|schedule)|one week late|\d+ (days|weeks) late)\b", "late vs plan"),
        (r"\bheld until\b|\bis therefore held\b", "approval held"),
        (r"\bslip(ped|s|page)?\b|\bdelay(ed)?\b", "slip/delay keyword"),
    ],
    "dependency": [
        (r"\bdepend(s|ed|ent)? (on|upon)\b", "depends on"),
        (r"\bwaiting (on|for)\b", "waiting on"),
        (r"\bcannot be (tested|scheduled|started|run|completed) until\b", "cannot ... until"),
        (r"\b(requires?|needs?) .* (from|by) (Platform Engineering|Finance|Operations|Treasury|Procurement|Compliance|Business Change)\b", "requires from team"),
        (r"\bwith (Operations|Finance|Compliance|Procurement|Treasury) for review\b", "with team for review"),
    ],
    "issue": [
        (r"\b(defects?|findings?) (remain|remains|are|is) open\b|\bremains? open\b", "open defect"),
        (r"\b(not attempted|not tested|not executed|not completed|failed|overran|outage|breach)\b", "not done / failed"),
        (r"\b\d+% (against|vs\.?|versus) (a |the )?plan\b|\bbelow plan\b|\bbelow (the )?(target|requirement|model)\b", "below plan"),
        (r"\b\d+% of the requirement\b|\b\d+ of \d+ FTE\b", "staffing gap"),
        (r"\binstead of\b", "actual vs expected"),
        (r"\babove (the )?budget\b|\bover budget\b|\bcost overrun\b", "budget variance"),
        (r"\bno owner\b|\bowner (has )?not (yet )?been (confirmed|assigned)\b|\bunowned\b", "no owner"),
    ],
    "risk": [
        (r"\brisk\b", "risk keyword"),
        (r"\bif\b.*\b(not|fails?|cannot|slips?)\b", "conditional"),
        (r"\b(may|might|could) (not |therefore )?\b(be|miss|push|require|reopen|weaken|delay|fail)", "modal verb"),
        (r"\bwould (push|reopen|require|delay|mean|leave)\b", "would + consequence"),
        (r"\bunless\b", "unless"),
        (r"\bonly \d+ (have|of|are)\b|\b\d+ confirmed of \d+\b|\b\d+ of \d+ (confirmed|required)\b", "shortfall count"),
        (r"\bstays (red|amber)\b|\bremains (red|amber)\b", "RAG stays"),
        (r"\b(expires?|rolls? off|runs? out|ends?) (on|at|in|by) (the )?(end of )?\w+", "expiry"),
        (r"\bhas not yet been (raised|confirmed|approved|signed)\b|\bnot in the change calendar\b|\bverbally\b", "not formalised"),
        (r"\bneeded by \d{1,2} \w+ to be effective\b", "hard deadline"),
    ],
}
_COMPILED = {t: [(re.compile(p, re.I), label) for p, label in pats] for t, pats in PATTERNS.items()}

# Sentences that look risky but are explicitly reassuring.
_NEGATION = re.compile(
    r"\b(no risk|no change|no open|there are no|is stable|as planned|within tolerance|on plan|has been approved|"
    r"inside the notice period|remain flat|are flat|is flat|closed on|has been raised with|is confirmed for)\b", re.I)

_HIGH = re.compile(r"\b(severity 1|SteerCo|go/no-go|hard stop|rollback|freeze|regulat|Operational Risk|Compliance|"
                   r"sign[- ]?off|cut-over|go-live|January)\b", re.I)


def extract_rules(text: str, filename: str) -> list[Candidate]:
    hdr = parse_header(text)
    out: list[Candidate] = []
    for s in split_sentences(text):
        fired: list[tuple[str, str]] = []
        for t in TYPES:
            for rx, label in _COMPILED[t]:
                if rx.search(s):
                    fired.append((t, label))
        if not fired:
            continue
        # Negation: only drop the sentence if the only signals are weak keyword hits
        weak = {"risk keyword", "slip/delay keyword", "modal verb", "conditional", "expiry"}
        if _NEGATION.search(s) and all(lbl in weak for _, lbl in fired):
            continue
        primary = next(t for t in TYPES if any(ft == t for ft, _ in fired))
        sev = "High" if _HIGH.search(s) else "Medium"
        out.append(Candidate(file=filename, workstream=hdr.get("workstream", ""), week=hdr.get("week", ""),
                             type=primary, severity=sev, sentence=s,
                             signals=[f"{t}:{lbl}" for t, lbl in fired], engine="rules"))
    return out


# --------------------------------------------------------------------------- #
# Optional LLM engine
# --------------------------------------------------------------------------- #
LLM_SYSTEM = """You read weekly status updates from a bank transformation program and propose entries for a RAID log.
Return ONLY a JSON array. Each element: {"type": one of ["risk","issue","slip","dependency","decision"],
"severity": "High" or "Medium", "sentence": the exact sentence copied verbatim from the update that supports the item}.
Rules: never paraphrase the sentence; never invent facts; skip sentences that are purely positive or informational;
one element per distinct item. If a sentence supports two items, list it twice with different types."""


def llm_available() -> bool:
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def extract_llm(text: str, filename: str, model: str = "claude-sonnet-4-5") -> list[Candidate]:
    import anthropic

    hdr = parse_header(text)
    client = anthropic.Anthropic()
    msg = client.messages.create(model=model, max_tokens=2000, system=LLM_SYSTEM,
                                 messages=[{"role": "user", "content": text}])
    raw = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    raw = raw[raw.find("["): raw.rfind("]") + 1]
    items = json.loads(raw)
    sentences = split_sentences(text)
    out = []
    for it in items:
        sent = str(it.get("sentence", "")).strip()
        # Trace check: the quoted sentence must exist in the source. Drop anything that does not.
        match = next((s for s in sentences if sent and (sent in s or s in sent)), None)
        if match is None:
            continue
        t = it.get("type", "risk")
        out.append(Candidate(file=filename, workstream=hdr.get("workstream", ""), week=hdr.get("week", ""),
                             type=t if t in TYPES else "risk", severity=it.get("severity", "Medium"),
                             sentence=match, signals=["llm:quoted"], engine="llm"))
    return out


def extract_all(updates: dict[str, str], engine: str = "rules") -> list[Candidate]:
    fn = extract_llm if engine == "llm" else extract_rules
    out: list[Candidate] = []
    for name, text in updates.items():
        out.extend(fn(text, name))
    return out
