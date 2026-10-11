// Builds 03_SteerCo_Deck.pptx. Run: node deck/build_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");
// applyTheme writes the theme colours into the .pptx; it is an optional helper. Without it the deck
// still builds, with Office's stock palette for scheme colours.
let applyTheme = async () => {};
try { ({ applyTheme } = require("./apply_theme.js")); } catch (e) { /* optional */ }

const OUT = path.join(__dirname, "..", "03_SteerCo_Deck.pptx");

const THEME = {
  name: "Cockpit Charcoal",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "212121", lt1: "FFFFFF", dk2: "36454F", lt2: "F2F2F2",
    accent1: "36454F", accent2: "C62828", accent3: "EF6C00", accent4: "2E7D32",
    accent5: "7A8C99", accent6: "B0BEC5", hlink: "36454F", folHlink: "7A8C99",
  },
};
const RAG = { Red: "C62828", Amber: "EF6C00", Green: "2E7D32" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Tommaso Portesan";
pres.title = "Program HORIZON Release Wave 3, SteerCo pre-read";
const C = pres.SchemeColor;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "DARK", background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.3, w: 11.9, h: 1.4, fontSize: 40, bold: true, color: C.background1, margin: 0, align: "left" } } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 3.8, w: 11.9, h: 1.6, fontSize: 18, color: C.background2, margin: 0 } } },
    { text: { text: "Synthetic illustrative case. Program, figures and names are fictional.", options: { x: 0.7, y: 6.8, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
});
pres.defineSlideMaster({
  title: "LIGHT", background: { color: THEME.colors.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.8, fontSize: 28, bold: true, color: C.text2, margin: 0, align: "left" } } },
    { text: { text: "Program HORIZON (fictional) | Release Wave 3 | SteerCo pre-read | as of 9 Oct 2026 | synthetic data", options: { x: 0.6, y: 7.0, w: 10, h: 0.3, fontSize: 9, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 9, color: THEME.colors.accent5 },
});

const T = (slide, text, o) => slide.addText(text, { isTextBox: true, margin: 0, fontFace: undefined, ...o });

// ---------- 1. Title ----------
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" });
s.addText("Release Wave 3: go/no-go preparation", { placeholder: "title" });
s.addText("Steering Committee pre-read, readiness as of 9 October 2026\nCut-over weekend 21 to 22 November | decision meeting 6 November", { placeholder: "body" });
T(s, "Prepared with the Transformation Cockpit prototype", { x: 0.7, y: 6.3, w: 9, h: 0.35, fontSize: 12, color: C.accent6 });
s.addNotes("Pre-read for the go/no-go preparation checkpoint (T-3 weeks per the readiness framework). Everything in this deck traces to a row in the cockpit data folder.");

// ---------- 2. Where we stand ----------
pres.addSection({ title: "Status" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Status" });
s.addText("Five dimensions amber, one red: recommendation is a conditional go", { placeholder: "title" });
const dims = [
  ["D1", "Data quality and reconciliation", "Amber", "Reconciliation 99.1% vs 99.5% target; 2 open S2 data defects; 2 of 3 mock runs done"],
  ["D2", "Client and advisor communication", "Green", "100% clients notified; 96% advisors briefed; hypercare model published"],
  ["D3", "Training and enablement", "Amber", "Training 88% vs 95%; 12 of 14 floorwalkers; procedures 94% published"],
  ["D4", "Technology cut-over and decommissioning", "Amber", "DR1 margin 1h15 vs 2h target; rollback partially tested; DEF-209 open"],
  ["D5", "Regulatory, risk and control sign-off", "Amber", "Op Risk approval forecast 13 Nov; controls tested 90%; retention plan agreed"],
  ["D6", "Operational capacity and service continuity", "Red", "Hypercare staffing 86% of model (50 of 58 FTE); 120% load test not yet run"],
];
dims.forEach((d, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.6 + col * 4.1, y = 1.45 + row * 2.35;
  s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.9, h: 2.1, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `card ${d[0]}` });
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.25, y: y + 0.25, w: 0.5, h: 0.5, fill: { color: RAG[d[2]] }, line: { color: RAG[d[2]] }, objectName: `rag ${d[0]}` });
  T(s, d[2], { x: x + 0.3, y: y + 0.25, w: 0.4, h: 0.5, fontSize: 9, bold: true, color: C.background1, align: "center", valign: "middle" });
  T(s, `${d[0]}  ${d[1]}`, { x: x + 0.9, y: y + 0.22, w: 2.85, h: 0.6, fontSize: 13, bold: true, color: C.text2, valign: "middle" });
  T(s, d[3], { x: x + 0.25, y: y + 0.95, w: 3.4, h: 1.05, fontSize: 11.5, color: C.text1, valign: "top" });
});
T(s, "Rule applied: red in D6 only, which is not a critical dimension (D1, D4, D5). A conditional go requires a SteerCo-approved mitigation for D6, tracked daily, and owners plus closure dates for every amber before cut-over. Source: readiness_kpis.csv, framework section 4.",
  { x: 0.6, y: 6.25, w: 12.1, h: 0.6, fontSize: 11, color: C.accent5, italic: true });
s.addNotes("Dimension RAG is the worst criterion, no averaging. D6 is red on staffing; D1, D4, D5 are amber and under control with dates. D2 is green.");

// ---------- 3. Critical path ----------
pres.addSection({ title: "Schedule" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Schedule" });
s.addText("Three inputs to the decision paper now land after the paper is due", { placeholder: "title" });
// timeline
const t0 = new Date("2026-10-09"), t1 = new Date("2026-11-22");
const X0 = 0.9, X1 = 12.4, Y = 3.2;
const px = (i, n) => X0 + (i / (n - 1)) * (X1 - X0); // evenly spaced, not to scale
s.addShape(pres.ShapeType.line, { x: X0, y: Y, w: X1 - X0, h: 0, line: { color: C.accent6, width: 2 }, objectName: "timeline" });
const events = [
  ["2026-10-09", "Today", "accent5", "up"],
  ["2026-10-17", "Mock 3\n(was 10 Oct)", "accent3", "down"],
  ["2026-10-23", "Batch fix deployed\n(was 16 Oct)", "accent3", "up"],
  ["2026-11-04", "Decision paper due", "accent1", "down"],
  ["2026-11-06", "Go/no-go SteerCo", "accent1", "up"],
  ["2026-11-08", "DR2 + rollback\n(was 31 Oct)", "accent2", "down"],
  ["2026-11-13", "Op Risk approval\n(was 30 Oct)", "accent2", "up"],
  ["2026-11-18", "Final confirmation", "accent1", "down"],
  ["2026-11-21", "Cut-over", "accent4", "up"],
];
events.forEach(([d, label, col, dir], i) => {
  const x = px(i, events.length);
  s.addShape(pres.ShapeType.ellipse, { x: x - 0.11, y: Y - 0.11, w: 0.22, h: 0.22, fill: { color: C[col] }, line: { color: C[col] }, objectName: `ev ${i}` });
  const ly = dir === "up" ? Y - 1.25 : Y + 0.25;
  T(s, label, { x: x - 0.8, y: ly, w: 1.6, h: 0.95, fontSize: 10.5, color: C.text1, align: "center", valign: dir === "up" ? "bottom" : "top", bold: col !== "accent5" });
  T(s, new Date(d).toLocaleDateString("en-GB", { day: "numeric", month: "short" }), { x: x - 0.5, y: dir === "up" ? Y + 0.2 : Y - 0.45, w: 1.0, h: 0.25, fontSize: 9, color: C.accent5, align: "center" });
});
// legend-free explanation: three callouts
const calls = [
  ["Dress rehearsal 2 (7 to 8 Nov)", "One day after the SteerCo. Rollback is only partially tested until then. The committee decides on DR1 evidence plus fix test results, or defers one week."],
  ["Operational Risk approval (13 Nov)", "Op Risk will not sign off while DEF-121 (312 records, manual enrichment, no owner yet) is open. A conditional approval needs the Head of Op Risk at the meeting."],
  ["Network change freeze (1 Dec)", "28 to 29 Nov is the only fallback weekend. Any later deferral moves go-live to January."],
];
calls.forEach(([h, b], i) => {
  const x = 0.6 + i * 4.1;
  s.addShape(pres.ShapeType.roundRect, { x, y: 4.75, w: 3.9, h: 1.95, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `call ${i}` });
  T(s, h, { x: x + 0.25, y: 4.9, w: 3.4, h: 0.4, fontSize: 13, bold: true, color: C.text2 });
  T(s, b, { x: x + 0.25, y: 5.3, w: 3.4, h: 1.3, fontSize: 11, color: C.text1, valign: "top" });
});
T(s, "Source: milestone_plan.xlsx (M02, M20, M22, M26), weekly updates wk41. Red markers: forecast after the decision paper. Orange: slipped but before it. Timeline not to scale.", { x: 0.6, y: 1.35, w: 12.1, h: 0.4, fontSize: 11, color: C.accent5, italic: true });
s.addNotes("The cockpit flags seven dependency conflicts. The three that matter for the decision are DR2, Op Risk approval and the competence assessment, all forecast after the decision paper is issued on 4 Nov.");

// ---------- 4. Top risks ----------
pres.addSection({ title: "Risks" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Risks" });
s.addText("Three risks drive the recommendation; each is owned and dated", { placeholder: "title" });
const risks = [
  ["R03", "Hypercare staffing below model", "High / High", "Operations Readiness Lead", "23 Oct",
   "50 of 58 FTE confirmed. Service centre teams carry year-end volumes in the same window. Service partner needs four weeks' notice."],
  ["R02", "Op Risk approval after the SteerCo", "High / High", "Risk and Control Lead", "6 Nov",
   "Close DEF-114 by 16 Oct (fix in test). Assign an owner to DEF-121 enrichment this week. Ask for conditional approval in person."],
  ["R01", "Batch fix late for DR2", "High / Medium", "Platform Engineering Lead", "23 Oct",
   "Fix passed unit tests; regression from 12 Oct; deployment 23 Oct confirmed in the change calendar. Fallback: DR2 on current build, weaker evidence."],
];
risks.forEach((r, i) => {
  const y = 1.5 + i * 1.75;
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: 1.55, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `risk ${r[0]}` });
  s.addShape(pres.ShapeType.ellipse, { x: 0.85, y: y + 0.42, w: 0.7, h: 0.7, fill: { color: i === 2 ? RAG.Amber : RAG.Red }, line: { color: i === 2 ? RAG.Amber : RAG.Red }, objectName: `risk dot ${r[0]}` });
  T(s, r[0], { x: 0.85, y: y + 0.42, w: 0.7, h: 0.7, fontSize: 12, bold: true, color: C.background1, align: "center", valign: "middle" });
  T(s, r[1], { x: 1.8, y: y + 0.15, w: 5.2, h: 0.4, fontSize: 15, bold: true, color: C.text2 });
  T(s, r[5], { x: 1.8, y: y + 0.58, w: 6.6, h: 0.9, fontSize: 11, color: C.text1, valign: "top" });
  T(s, [{ text: "Severity / likelihood  ", options: { color: C.accent5 } }, { text: r[2], options: { bold: true, breakLine: true } },
        { text: "Owner  ", options: { color: C.accent5 } }, { text: r[3], options: { bold: true, breakLine: true } },
        { text: "Mitigation due  ", options: { color: C.accent5 } }, { text: r[4], options: { bold: true } }],
    { x: 8.7, y: y + 0.2, w: 3.8, h: 1.2, fontSize: 11, color: C.text1, valign: "top", paraSpaceAfter: 4 });
});
T(s, "Source: raid_log.csv, ranked by severity and likelihood. Full register of 24 items in the cockpit, Schedule tab.", { x: 0.6, y: 6.75, w: 12.1, h: 0.3, fontSize: 11, color: C.accent5, italic: true });
s.addNotes("R03 is what makes D6 red. R02 is the one that can turn the recommendation into a no-go if Op Risk will not attend. R01 is improving.");

// ---------- 5. Decision ----------
pres.addSection({ title: "Decision" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Decision" });
s.addText("Decision requested: close the hypercare staffing gap by 23 October", { placeholder: "title" });
const opts = [
  ["Option A", "Contract 8 temporary FTE from the service partner for three weeks", "Cost about CHF 180,000. Lifts staffing to 100% of model. Needs sign-off by 23 Oct (four weeks' notice). Keeps full day-one scope.", "Recommended"],
  ["Option B", "Defer the corporate actions module to a December release", "No cost. Reduces day-one volume so 50 FTE meets the reduced model. Adds a second cut-over inside the change freeze window, which needs its own approval.", ""],
  ["Option C", "Hybrid: 4 partner FTE plus corporate actions deferred by two weeks", "About CHF 90,000. Requested by the chair for comparison. Same freeze-window exposure as B, smaller.", ""],
];
opts.forEach((o, i) => {
  const x = 0.6 + i * 4.1;
  const rec = o[3] !== "";
  s.addShape(pres.ShapeType.roundRect, { x, y: 1.5, w: 3.9, h: 3.2, rectRadius: 0.08, fill: { color: rec ? C.text2 : C.background2 }, line: { color: rec ? C.text2 : C.background2 }, objectName: `opt ${i}` });
  T(s, o[0] + (rec ? "  |  " + o[3] : ""), { x: x + 0.25, y: 1.65, w: 3.4, h: 0.4, fontSize: 12, bold: true, color: rec ? C.accent6 : C.accent5 });
  T(s, o[1], { x: x + 0.25, y: 2.05, w: 3.4, h: 0.9, fontSize: 14, bold: true, color: rec ? C.background1 : C.text2, valign: "top" });
  T(s, o[2], { x: x + 0.25, y: 3.0, w: 3.4, h: 1.6, fontSize: 11.5, color: rec ? C.background2 : C.text1, valign: "top" });
});
T(s, "Conditions attached to a conditional go, whichever option is chosen", { x: 0.6, y: 4.95, w: 12.1, h: 0.35, fontSize: 14, bold: true, color: C.text2 });
s.addText([
  { text: "Owner named for DEF-121 enrichment by 16 Oct; DEF-114 closed by 16 Oct (D1).", options: { bullet: true, breakLine: true } },
  { text: "Protected training slots held on 20 to 21 Oct; 95% completion by 10 Nov; two Operations floorwalkers released with the staffing decision (D3).", options: { bullet: true, breakLine: true } },
  { text: "Batch fix deployed 23 Oct; DR2 with end-to-end rollback on 7 to 8 Nov; committee reconvenes by email on 9 Nov to confirm (D4).", options: { bullet: true, breakLine: true } },
  { text: "Head of Operational Risk attends on 6 Nov to give or refuse a conditional approval; written retention confirmation by 16 Oct (D5).", options: { bullet: true } },
], { x: 0.6, y: 5.3, w: 12.1, h: 1.45, fontSize: 11.5, color: C.text1, paraSpaceAfter: 3, valign: "top", isTextBox: true, margin: 0 });
s.addNotes("The committee is asked to choose A, B or C and to accept the four conditions. Without a choice by 23 Oct, option A is no longer available and D6 stays red into the 6 Nov meeting.");

// ---------- 6. How produced + next steps ----------
pres.addSection({ title: "Close" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Close" });
s.addText("How this pre-read was produced, and what we measured", { placeholder: "title" });
// left: process
T(s, "Transformation Cockpit prototype", { x: 0.6, y: 1.45, w: 6.0, h: 0.4, fontSize: 15, bold: true, color: C.text2 });
const steps = [
  ["1", "Ingest", "Milestone plan (xlsx), RAID log, readiness KPIs, free-text weekly updates"],
  ["2", "Analyse, no AI", "Slips, dependency conflicts, unowned items, deterministic RAG scoring against framework thresholds"],
  ["3", "Propose, with AI", "Weekly updates read for risks, slips, decisions. Each proposal quotes its source sentence. A reviewer accepts or rejects"],
  ["4", "Draft and release", "Executive report and talking points generated with a source tag on every line. DRAFT until a named reviewer releases"],
];
steps.forEach((st, i) => {
  const y = 1.95 + i * 1.05;
  s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: y + 0.08, w: 0.55, h: 0.55, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: `step ${st[0]}` });
  T(s, st[0], { x: 0.6, y: y + 0.08, w: 0.55, h: 0.55, fontSize: 13, bold: true, color: C.background1, align: "center", valign: "middle" });
  T(s, st[1], { x: 1.35, y, w: 5.2, h: 0.35, fontSize: 13, bold: true, color: C.text2 });
  T(s, st[2], { x: 1.35, y: y + 0.35, w: 5.2, h: 0.65, fontSize: 11, color: C.text1, valign: "top" });
});
// right: evaluation stats
T(s, "What we measured", { x: 7.1, y: 1.45, w: 5.6, h: 0.4, fontSize: 15, bold: true, color: C.text2 });
s.addShape(pres.ShapeType.roundRect, { x: 7.1, y: 1.95, w: 5.6, h: 2.35, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "eval card" });
T(s, "95%", { x: 7.3, y: 2.05, w: 2.6, h: 0.9, fontSize: 44, bold: true, color: RAG.Green, align: "center", valign: "middle" });
T(s, "recall on the 10 updates the rules were written next to", { x: 7.3, y: 2.95, w: 2.6, h: 0.6, fontSize: 10.5, color: C.text1, align: "center", valign: "top" });
T(s, "17%", { x: 9.95, y: 2.05, w: 2.6, h: 0.9, fontSize: 44, bold: true, color: RAG.Red, align: "center", valign: "middle" });
T(s, "recall on 5 held-out updates in a different writing style", { x: 9.95, y: 2.95, w: 2.6, h: 0.6, fontSize: 10.5, color: C.text1, align: "center", valign: "top" });
T(s, "Keyword rules are precise (97 to 100%) but blind to new phrasing. That is the case for an LLM extractor with the same two controls: quoted source sentence, human review of every proposal. The LLM engine is built and not yet measured.",
  { x: 7.3, y: 3.5, w: 5.2, h: 0.78, fontSize: 10.5, color: C.text1, valign: "top" });
T(s, "Effort estimate, to be validated", { x: 7.1, y: 4.5, w: 5.6, h: 0.35, fontSize: 13, bold: true, color: C.text2 });
T(s, "About 5 hours per week of manual reading and report compilation today; about 1 hour with the cockpit, if the extractor reaches 85% recall on real updates. Assumptions in 02_Evaluation_Report.md.",
  { x: 7.1, y: 4.85, w: 5.6, h: 0.75, fontSize: 10.5, color: C.text1, valign: "top" });
T(s, "Next steps", { x: 7.1, y: 5.7, w: 5.6, h: 0.35, fontSize: 13, bold: true, color: C.text2 });
s.addText([
  { text: "Measure the LLM engine on the held-out set; second labeller for agreement", options: { bullet: true, breakLine: true } },
  { text: "Two-week trial on anonymised real updates with a PMO analyst reviewing", options: { bullet: true, breakLine: true } },
  { text: "Decide on entry into the weekly reporting cycle only after that", options: { bullet: true } },
], { x: 7.1, y: 6.05, w: 5.6, h: 0.9, fontSize: 10.5, color: C.text1, paraSpaceAfter: 2, valign: "top", isTextBox: true, margin: 0 });
s.addNotes("Closing: the tool is a draft assistant with controls, not a decision maker. The honest evaluation number is 17%, and the next step is to measure the LLM engine the same way.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
