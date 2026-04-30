# Plan: Thinking-aid for the v2.2 extrinsic-evaluation protocol (N=3)

## Context

The course assignment caps this round at **3 participants, all first-time SAGE users**, and "extrinsic" here means **purely human-subjects** — no LLM-as-judge, no transcript-only audits as primary evidence. The TODO in [`04-21-2026/Updated Iteration Report for v2.1.md`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/04-21-2026/Updated%20Iteration%20Report%20for%20v2.1.md) needs filling under those constraints.

What this changes from a normal study design:
- **No statistical inference.** N=3 supports descriptive case-study reporting only. No Wilcoxon, no significance tests, no p-values. Effect sizes are unhelpful at this scale; report each case individually.
- **No within-participant version comparison.** Participants have no prior SAGE experience to compare against. Any "did v2.1 fixes land?" claim has to come from a **cross-cohort comparison**: your 3 v2.2 first-time users vs. the 12 first-time users from April 21 + April 23. That comparison is the researcher's, not the participant's.
- **Deep qualitative is the right tool.** N=3 with rich interview + observation data can produce sharper insight than N=20 with shallow surveys. Lean into think-aloud, semi-structured interview, and case-by-case reporting.
- **No LLM-as-judge.** Anything machine-coded is intrinsic by your definition; keep it out of this round.

This document is a thinking-aid. Each section names the decisions, the SAGE-specific facts that constrain them, and 2–3 options to pick between. Output is the filled TODO, not this file.

---

## Evaluation objective — what to think about

**Decision to make:** the *one* question this round answers. At N=3 you cannot answer many; pick one and answer it well.

**Constraints from SAGE specifics:**
- Participants are new — they cannot personally compare v2.1 to v2.0. Anything framed as "did the fixes land" is a researcher-side cross-cohort comparison against the April 21/23 reviewer data, not a participant-experienced one.
- The April 21/23 cohort produced concrete qualitative themes (scaffolding-as-helpful, name-discomfort, output-eval-overwhelm, want-the-answer impulse, only 1/8 reached closing reflection). These are the natural anchors to compare against.
- A single session of 45–60 min cannot honestly support a transfer claim.
- Three participants is enough for case-by-case usability description, theme triangulation, and a few descriptive rates ("2 of 3 reached the closing reflection") — nothing more.

**Options for the objective (pick one):**
1. **First-impression usability and engagement of v2.1+** — does the agent feel useful, paced right, and worth returning to for a first-time user? Pure descriptive; honest at N=3.
2. **Cross-cohort theme comparison against April 21/23** — do the v2.1 fixes show up as the *absence* of prior themes (no name-discomfort if anonymous-mode is used, less output-eval-overwhelm) or *presence* of new ones (closing reflection actually reached)? Case-by-case, descriptive, builds on what was shipped.
3. **In-session pedagogical experience** — does each participant report (and demonstrate in interview) that ANE scaffolding helped them think rather than rushing them? Tests the central pedagogical claim experientially, not as a transcript audit.

**Recommended frame for v2.2 at N=3:** option 2 or 3, not 1. Option 1 is fine but uses N=3 to learn what a 5-person UX test would tell you faster. Options 2 and 3 ask SAGE-specific questions that the existing intrinsic / transcript data alone cannot answer.

---

## Participant type — what to think about

**Decision to make:** who the 3 are and how you recruit them given the cap and the first-time constraint.

**Constraints from SAGE specifics:**
- **Hard cap of 3.** That makes diversity per slot extremely valuable. Three CS peers tell you less than one CS peer + one non-CS undergrad + one grad student or non-student.
- **First-time users only** — no one who has seen v2.0/v2.1 demos, no April 21/23 reviewers, no one who has read the iteration report.
- SAGE is built to scale across levels (Novice → Critical Thinker). At N=3, varying participant level deliberately is the cheapest way to test whether level adaptation works.
- Streamlit + CLI deployment — accessible to anyone you can put in front of a browser; no public-URL constraint.

**Things to specify:**
- A small inclusion/exclusion list (no prior SAGE exposure, no review of iteration reports).
- Whether to deliberately span levels (one Novice / one Practitioner / one Advanced as you'd guess them) or keep level constant for comparable observations.
- Disclosure script: what you tell participants about the study before they start, written in a way that doesn't seed demand effects ("we want to see what works and what doesn't" rather than "we want to know if SAGE helps").
- Whether participants are class peers (faster, higher demand-effect risk) or recruited from outside the course (slower, less biased).

**Options:**
1. **3 class peers** — fastest, highest demand-effect risk. Acceptable only if explicitly named.
2. **2 class peers + 1 non-CS or non-student** — slightly more effort, materially better cross-coverage.
3. **3 deliberately different levels** — one self-rated novice, one practitioner, one advanced. Highest information-per-participant at N=3.

**To name explicitly in the writeup:** sample bias, recruitment channel, and what each participant was told before starting.

---

## Tasks — what to think about

**Decision to make:** what each of the 3 participants does, in what order, and over how long.

**Constraints from SAGE specifics:**
- The four practice types (Prompt Crafting, Output Evaluation, Appropriateness Judgment, Workflow Design) are the natural anchor.
- Anonymous "just chat" path is shipped — forcing anonymous mode reduces one confound (name-discomfort) but also makes you unable to observe whether the optional-name flow still bothers people. Either is defensible; choose deliberately.
- Sidebar export controls and `.md` / `.txt` export are shipped — useful as a participant-facing artifact at end of session.
- **Think-aloud is feasible at N=3** and free. With higher N it is impractical; here it is the cheapest way to capture in-session reasoning.

**Things to specify:**
- Whether participants do a **pre-task** (5–10 min, before SAGE — e.g., write a prompt for a sample task; rate own AI-use confidence). At N=3, this is descriptive, not inferential.
- Whether the SAGE session is **assigned a practice type** (cleaner across-participant comparison) or **participant-chosen** (more naturalistic, harder to compare).
- Whether to use **think-aloud during the session** (recommend yes — N=3 makes this affordable and high-value) or rely on the post-session interview only.
- Whether the post-session task includes anything beyond the interview (e.g., a single prompt-rewrite as a case-study Δ).

**Options for the task structure:**
1. **Single SAGE session with think-aloud + post-interview** — simplest. Produces 3 deep case studies.
2. **Pre-task → SAGE session (think-aloud) → post-task → interview** — adds a per-participant before/after artifact. Reports as 3 case-comparisons, not statistically.
3. **Two practice types within one session** — tests whether SAGE handles a topic shift well. Risk: 60-minute ceiling cuts each one short.

**Recommended:** option 1 unless you have specific reason to want the post-task artifact. The interview is the highest-information-density portion at N=3.

**SAGE-specific decisions to lock:**
- Anonymous mode — force it (recommended; reduces one confound) or let participant choose (lets you observe the optional-name flow under real conditions).
- Practice type — assign one (recommend Prompt Crafting since it's the most observable in think-aloud) or let participant choose.
- Scenario — standard scenario across participants (cleaner cross-case comparison) or contextualized to participant's course/work (richer engagement, harder to compare).
- Whether participants get to keep the `.md` export of their session as part of the debrief.

---

## Metrics and analysis — what to think about

**Decision to make:** what numbers and what coded text come out at N=3, and how you report them.

**Constraints from SAGE specifics:**
- "Extrinsic" rules out LLM-as-judge. Anything machine-coded belongs in the intrinsic round.
- N=3 rules out inferential statistics. Report each participant individually; aggregate only as descriptive rates ("2 of 3").
- Auto-instrumented per session: full transcript, turn count, duration, closing-reflection text + reach flag, dimension scores (5), competency scores (4). These are *researcher-side* observations of the session, not LLM judgments — they remain in scope for extrinsic reporting as descriptive context.
- The April 21/23 reviewer data is the natural cross-cohort baseline (12 first-time users on a prior version, qualitative themes already coded).
- Cohen's κ at N=3 is unstable; if you human-double-code, report % agreement on a small sample rather than κ.

**Things to specify:**
- Primary observations — pick 1–3. Anything more dilutes a report on 3 cases.
- For each: what scale, how it's captured, who observes/codes it, and how it's reported (per-case vs. as a 0/3, 1/3, 2/3 descriptive rate).

**Candidate primary observations (pick 1–3):**
1. **Closing-reflection-reached** per session (binary, observable). Compared descriptively against the 1/8 anchor from April 23. At N=3, "2 of 3 reached the closing reflection" is meaningful descriptive evidence; "0 of 3" tells you the recap fix is still not landing.
2. **Theme presence** in each participant's interview, against the April 21/23 theme list — present, absent, or qualified. Especially: name-discomfort, output-eval-overwhelm, want-the-answer impulse, scaffolding-as-helpful, transferable-principle-named.
3. **Self-reported helpfulness of nudges** — single forced-choice survey item ("the nudges helped me reason" / "the nudges felt rushed" / "neutral") + interview probe.
4. **Participant-named transferable principle** — did the participant, unprompted in the post-interview, name something concrete they'd carry to their next AI interaction? Yes/no per participant.

**Candidate descriptive context (appendix, not analyzed):**
- Session duration, turn count, point of disengagement if any.
- Auto-instrumented dimension and competency scores from `skill-evaluator` — reported but not used as evidence at N=3.
- Quote-level evidence per theme.

**Reporting template (recommended):**
- One short narrative per participant: who they were, what happened in the session, what they said in the interview, what was notable.
- One cross-case section: "across the 3 cases, X happened in N of 3; Y theme appeared in N of 3; the historical anchor for X was 1/8 in the April 23 cohort."
- One limitations paragraph that names: N=3 cap, peer-sample bias, single-session scope, no version-comparison from the participant's view.

**What not to do at N=3:**
- Don't run statistical tests.
- Don't claim transfer from a single session.
- Don't report a Likert mean across 3 people as if it's a measurement.
- Don't fold LLM-as-judge into the headline findings.

---

## Baselines — what to think about

**Decision to make:** what each observation is being compared against.

**Constraints from SAGE specifics:**
- **Within-participant baseline** is impossible — participants are first-time users with no prior version exposure.
- **Cross-cohort baseline against April 21/23** is the strongest available anchor: 12 first-time users on the prior version, qualitative themes coded, one quantitative anchor (1/8 closing-reflection rate). The comparison is researcher-side, descriptive only.
- **A no-tutor / ChatGPT-only condition is not feasible at N=3** — you'd need to split N (1 vs. 2 or similar) and the comparison would be uninterpretable.

**Options:**
1. **April 21/23 cohort as the only baseline** — descriptive cross-cohort theme + closing-reflection-rate comparison. Cheapest and most honest at this scale.
2. **April 21/23 cohort + a single self-anchored pre-task per participant** — adds a per-case before/after artifact. Useful only if you commit to the pre-task in the task structure.
3. **No formal baseline, frame as exploratory case studies** — defensible but throws away the v2.0/v2.1 anchor that's already in the repo.

**Recommended:** option 1. The April 21/23 themes are already coded — this is essentially free historical comparison.

---

## Interview questions / pre or post survey design — what to think about

**Decision to make:** what qualitative + self-report data captures the most signal across 3 deep cases.

**Constraints from SAGE specifics:**
- At N=3, the interview is the primary evidence. Make it long enough (15–20 min) and structured enough to triangulate themes.
- Peer participants will hit the Likert ceiling; forced-choice items break it.
- The April 21/23 themes are available as deductive seeds for the interview codebook — that makes coding faster and lets you say directly "this v2.1 theme was / was not present in the v2.2 cases."
- The closing reflection inside SAGE is part of the *intervention*. The post-session debrief is separate and is your study artifact.

**Pre-survey (5 min, ≤5 items):**
- How often do you use AI tools in your coursework? (Never / Monthly / Weekly / Daily)
- Self-rated AI-prompting ability (1–5).
- Comfort with anonymous transcript storage (Yes / No / Need more info).
- Brief self-description of the participant's level (Novice / Practitioner / Advanced) — useful for matching SAGE's level-adaptation against perceived level.
- Attention check (one item).

**Post-survey (5 min) — at N=3 this is structured prompt material, not aggregate data:**
- 3–4 forced-choice items rather than Likert. Sample:
  - "Which moment in the session was *most* useful?" (onboarding / a specific nudge / the practice scenario / the closing reflection / something else — specify).
  - "Which moment was *least* useful?" (same options).
  - "If you could change one thing about how SAGE asked questions, what would it be?" (1 sentence).
  - "Would you use SAGE again on a different topic this week?" (Yes / No / Maybe + 1-sentence why).

**Semi-structured interview (15–20 min, 5–6 prompts):**
- Walk me through a moment where SAGE's question changed how you were thinking.
- Was there a point you wanted SAGE to just give the answer? What happened?
- Compared to how you usually use ChatGPT or Claude, what felt different?
- Did the session feel paced right — too fast, too slow, just right? Where specifically?
- Imagine a peer at your level new to AI — would you recommend SAGE? For what specifically?
- One change that would have made it better for you?
- (If you noticed level-adaptation behavior) Did SAGE feel like it was matching your level? Where did it match, where did it miss?

**Optional:** ask each participant to keep the `.md` export of their session and email it back the next day with one sentence on what they remembered. Cheap, descriptive only.

**Coding approach:**
- Use the April 21/23 themes as deductive seed codes: scaffolding-as-helpful, scaffolding-as-rushing, name-discomfort, output-eval-overwhelm, want-the-answer impulse, transferable-principle-named.
- Add inductive codes during pass 1 if new themes emerge.
- For each theme, report presence/absence per participant + quote-level evidence.
- At N=3, don't compute κ; if double-coding, report % agreement.

---

## Critical files (for the report writeup)

- [`04-21-2026/Updated Iteration Report for v2.1.md`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/04-21-2026/Updated%20Iteration%20Report%20for%20v2.1.md) — the TODO being filled.
- [`04-21-2026/Iteration Report (due Friday by end of day).md`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/04-21-2026/Iteration%20Report%20(due%20Friday%20by%20end%20of%20day).md) — the April 21 reviewer feedback that anchors the cross-cohort baseline.
- [`docs/pedagogical-model.md`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/docs/pedagogical-model.md) — anchors the claims under test.
- [`.claude/skills/reflection-facilitator/SKILL.md`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/.claude/skills/reflection-facilitator/SKILL.md) — defines the closing-reflection signature you're checking for in observation.
- [`sage/session_store.py`](../../Documents/G10_AIUseTutor/G10COS498_AiUseTutor/sage/session_store.py) and the `.md` export feature — confirm what artifact each participant leaves behind.

---

## Verification (before participant 1)

- **Pilot the full flow on yourself.** Confirm the pre-survey + SAGE session + post-interview fits in 75–90 min and the transcript / closing-reflection auto-logs correctly.
- **Lock the codebook before coding.** Pre-write the deductive theme list (seeded from April 21/23) and the participant case-narrative template. Don't decide what counts as a theme after seeing the data.
- **Disclosure script frozen.** Before participant 1, write down exactly what you'll tell each participant about the study and stick to it across all 3 — variation is its own confound at N=3.
- **Think-aloud script frozen.** If you're using think-aloud, write the prompt phrasing once and use it consistently ("say what you're thinking as you go; if you hit a question that's hard, say what's hard about it before answering").
- **Schedule all 3 sessions within ~5 days** to limit between-participant contamination via Slack/class chat. Ask participants in writing not to discuss specifics until the window closes.
- **Privacy / instructor-gaze protocol.** Decide what the instructor sees (full transcripts? redacted? summary only?) and tell participants up front.

---

## Honest framing for the writeup

The report section must be explicit about:

- **N=3 supports descriptive case-study reporting only.** No statistical claims.
- **Participants are first-time users**, so any "did the fixes land" claim is a researcher-side cross-cohort comparison against April 21/23, not a participant-experienced before/after.
- **Single-session scope** — no transfer claim, no retention claim. If a participant names a transferable principle in the interview, that is suggestive, not evidence of behavior change.
- **Peer-sample bias** is high. Demand effects on self-report are the dominant signal source; the interview-coded themes and observable behaviors (closing-reflection-reached, point of disengagement) are more trustworthy than the survey items.
- **What this round can honestly support:** updated themes against the April 21/23 codebook, descriptive rates on a few observable behaviors, three rich case studies, and a pre-registered anchor for v2.3.

---

## Summary — the four decisions that shape the rest

If only four decisions are made, these are the load-bearing ones for the N=3 round:

1. **Primary objective:** first-impression usability, cross-cohort theme comparison, or in-session pedagogical experience?
2. **Recruitment shape:** 3 similar peers, 3 deliberately different levels, or mix peers and outside-class?
3. **Task structure:** SAGE session + interview, or add pre/post tasks for case-by-case before/after?
4. **Anonymous mode:** force it, or let each participant choose?

Everything else in this document follows from those four.
