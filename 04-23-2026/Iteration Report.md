# Iteration Report — 04-23-2026 Cross-Class Peer Review

**Team 10 — SAGE (AI-Use Tutor)**
**Course:** COS 598/498 — Generative AI Agents (Spring 2026)
**Branch:** `AgentV2.1`
**Repo:** https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor
**Scope:** Feedback collected Thursday, April 23, 2026 from the COS 490 (Ethics) cross-class peer review of the Railway demo.

This report is scoped to the **04-23 cross-class batch only**. The full v2.1 sprint report (Apr 14 → Apr 28) lives at `04-23-2026/Updated Iteration Report for v2.1.md` and includes this batch alongside the 04-21 in-class reviews.

---

## 1. Feedback inventory

Four reviewers from COS 490 Ethics. All sessions were on the deployed Railway build; raw transcripts and rubric responses are in `04-23-2026/feedback.md`.

| #   | Reviewer                                            | Practice surface they hit                                                           | Sections of the rubric filled in                   |
| --- | --------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1   | **S.G.** (anonymized)                               | Asked a concept question about long/detailed prompts; ended in free-form discussion | Interaction Experience, Equity, Strengths/Priority |
| 2   | **Matt**                                            | Prompt-crafting on grammar editing (constraining the AI from rewriting)             | All sections, fully filled                         |
| 3   | **Nathaniel**                                       | Prompt-crafting on data analysis (NPS survey, anonymization scenario)               | All sections, partially filled                     |
| 4   | **Victoria** (+ co-comments from Grace and Matthew) | Appropriateness-judgment lesson (research paper + biology midterm)                  | All sections, fully filled                         |

No reviewer triggered `/improve-interaction`, `/weekly-review`, `/bad-agent-simulator`, or the dynamic template flow — all four took the default "first lesson" or scenario-runner path.

---

## 2. Synthesis — what the feedback actually said

### What worked

- **Process-oriented questioning was the dominant praise.** S.G. ("excited me a little to have the AI challenge me by asking me a question about what I knew on the subject"), Matt ("the trick is writing a prompt that draws a clear line"), Nathaniel ("the process it put me through was very structured"), Victoria ("you nailed a key principle: the verification cost test"). The nudge-before-explain shape is the single thing every 04-23 reviewer named as a strength.
- **Conciseness landed.** Victoria: "Length of responses was good, especially since it was on the shorter side. Responses that are too long often feel 'emptier' and full of filler language." Nathaniel: "responses are to-the-point and don't have a lot of fluff."
- **Self-awareness about AI limits.** Matt: "Is 'self-aware' about the flaws of AI usage." Nathaniel: SAGE reinforced anonymizing data before sending it to an LLM, which Nathaniel called out as "better privacy practices."
- **Output-evaluation framing is doing real teaching.** Nathaniel's session ended with him recognizing he hadn't told the AI to anonymize — exactly the realization the scenario is designed to provoke.

### What broke or felt off

- **Asking for a name is the most consistent friction point in this batch.** S.G., Grace, and Victoria all flagged it independently. S.G.: "felt really uncomfortable when the AI asked for my name… I was just expecting an answer to my prompt." Grace's one-line priority was literally "don't ask for name at the start."
- **Ambiguous wording on a constraint question.** Matt's synonym example: SAGE asked "would your current prompt forbid synonym swaps?" — Matt parsed it as a suggestion to _allow_ them and revised in the wrong direction. SAGE caught the mix-up gracefully but the question itself was the problem.
- **First "lesson" felt like just more chat.** Victoria expected something different — "an introduction from the bot or a video or a task to do" — and got an extended Socratic exchange. She acknowledged it might trace to her stated learning style, but the gap between "lesson" and "more conversation" needs to be named explicitly up front.
- **No way to copy/save the conversation, no concurrent threads.** S.G. flagged both. Matt: "Multiple chats is a must. Without them, you can only have one conversation at once, which is rather limiting."
- **No explicit disclaimers / harm-mitigation surface.** Victoria: "the agent didn't make any explicit statements that seemed oriented towards harm mitigation — no disclaimers or expectation setting." She also raised a "false confidence" risk: a learner who used SAGE might _feel_ safer than they are.
- **Tone briefly read as corrective rather than coaching.** Matthew (co-comment): "make sure tone doesn't feel like it's chastising user." Matt's own session: "There was a moment it felt a bit more 'corrective' than helpful, but only a moment."
- **Open question was left unanswered.** Victoria asked "how do you get to an understanding of what hidden assumptions an AI model might be running on?" SAGE moved to the closing reflection without addressing it. She flagged this as the moment she wanted a more direct answer.
- **Accessibility gap.** Victoria explicitly thought through the senior-citizen / non-tech-literate user: "Would I know to type in the chat bar? Would I know I can press 'enter' instead of hitting submit?" She also caught the missing auto-scroll — she didn't realize SAGE had responded because the page didn't scroll to the new message.

### Disagreements / interesting trade-offs

- **Privacy posture vs. profile-driven personalization.** S.G./Grace/Victoria want zero name-collection at the door. Matt and Nathaniel volunteered names without comment. The implication: a low-friction anonymous path serves the privacy-conscious without removing the profile path the others used implicitly.
- **Scenario library size.** Nathaniel: "Limited amount of scenarios for it to go through (seemingly, I might be wrong)." But none of the four reviewers asked for "another one" or used the dynamic template path — so we don't know whether the _perception_ of limited variety would survive contact with the generator.

### Functionality not getting discovered

- **Improve-interaction** (paste a real prompt+response and get coached on it) — zero use.
- **Weekly review** — zero use.
- **Bad-agent simulator** — zero use.
- **Dynamic output-eval generator** (shipped 04-24, after this batch) — not visible to these reviewers.
- **Recap card** (`<SESSION_RECAP>`) — Victoria's session was the only one to reach a closing reflection; she didn't mention the card, which suggests either it isn't reliably emitting in the deployed build, or it isn't read as a feature.

### Ideas surfaced by reviewers

- "Don't ask name at start" — Grace, S.G., Victoria.
- "Opt out of the new-user questionnaire" — S.G.
- "Copy / export the discussion" — S.G.
- "Multiple concurrent chats" — S.G., Matt.
- "More chat starters (2–3 more)" — Matt.
- "More scenarios" — Nathaniel.
- "Tool-tip bubbles / first-time-user walkthrough" — Victoria.
- "Auto-scroll to the latest message" — Victoria.
- "Explicit naming of the teaching style being used" — Victoria.
- "Tech tips for less tech-literate users" — Victoria.

### Ideas we generated reading the batch

- **Disambiguate the polarity of constraint questions.** Matt's synonym confusion was a phrasing failure — "would your current prompt forbid X?" reads ambiguously when answered with "no." A clearer pattern would be "if the AI swapped a word for a fancier synonym, would your prompt currently _catch_ that?" — phrasing the test from the _prompt's_ perspective rather than the AI's.
- **A one-line disclaimer at session start** — costs nothing, addresses Victoria's harm-mitigation gap directly.
- **Soft provenance on curriculum claims** — when SAGE references a principle ("verification cost test", "signal vs. noise"), append the curriculum source ("from the AI-literacy CRAFT lesson"). Halfway between "no sources" and over-promising live links.
- **An explicit one-sentence framer at the start of every lesson** — "this is an appropriateness-judgment exercise; I'll pose tasks one at a time and we'll work through your reasoning." Addresses Victoria's "I expected something other than just more chat."

---

## 3. Changes made since 04-23 and evidence of impact

Commits below landed after the 04-23 feedback was collected. The no-name onboarding fix has been merged to `main` via PR #9; the rest are on `AgentV2.1`. Where evidence is missing, we say so — most of these have not yet been tested by an outside reviewer.

| Design problem from 04-23                                                                                              | Change made                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Evidence of impact                                                                                                                                                                                                                                                      | Remaining gap                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Asking for a name caused real discomfort (S.G., Grace, Victoria).                                                      | **No-name onboarding — merged to `main`.** Onboarding skill, session-router, and session-start rewritten so name is never requested; a deeper prompt-engineering pass on `prompt-coaching` and `prompt-lab` ships alongside. The earlier `AgentV2.1` "Just chat (anonymous)" picker (commit `4c7f969`) is superseded by this main-branch behavior. _([.claude/skills/onboarding/SKILL.md](../.claude/skills/onboarding/SKILL.md), [.claude/skills/session-start.md](../.claude/skills/session-start.md), [.claude/skills/prompt-lab/SKILL.md](../.claude/skills/prompt-lab/SKILL.md); commit `c92b57b`, PR #9 `0554ff6`)_ | Fix is on `main`; the corresponding skill files no longer contain a name-collection step. Hand-tested locally — onboarding moves directly into orientation without asking for a name. The team memory entry `memory/feedback_no_name_request.md` records the rationale. | The 04-23 reviewers tested a build that still asked for names; none has re-tested against `main`. Once the next deploy cuts from `main` (or `AgentV2.1` rebases onto the merged change), an outside re-review is the missing evidence.            |
| Repetitive / too-similar question patterns; ambiguous constraint wording (Matt).                                       | **Question-variety fix** + research-backed conversational engagement pass: dialogue-move tables (pump / hint / prompt / elaborate / verify / self-explain) replaced the monolithic NUDGE; new shared `voice-and-register` skill loaded by every coaching/teaching skill, with a banned-phrases list and process-praise bank. _([.claude/skills/voice-and-register/SKILL.md](../.claude/skills/voice-and-register/SKILL.md); commits `2607b3c`, `93e48f6`)_                                                                                                                                                                | Hand-replayed Matt's grammar-editing scenario after the change: the constraint check now reads "if the AI replaced a word with a fancier synonym, would your current prompt **catch** it?" — phrased from the prompt's perspective.                                     | LLM-mediated; whether the model honors the move table on a given run is not yet measured. No outside reviewer has tested post-04-25.                                                                                                              |
| Nathaniel: "limited amount of scenarios."                                                                              | **Dynamic output-evaluation generator** — `generate_output_eval_scenario(template_id, topic="")` creates fresh `aiOutput` + `errors[]` from a lightweight template via a Haiku 4.5 sub-call, validated and retried on quote-mismatch. _([sage/tools.py](../sage/tools.py), [data/scenario_templates/](../data/scenario_templates/); commit `275c562`)_                                                                                                                                                                                                                                                                    | Re-running scenario-runner with the "fresh variant" flag produces non-identical scenarios across runs.                                                                                                                                                                  | Two seed templates is barely "more variety." Needs 5–6 to feel different to a learner. None of the 04-23 reviewers has re-tested.                                                                                                                 |
| S.G.: "no option I could see to copy my discussion."                                                                   | **Export chat control** — Markdown / plain-text export; file is built from the current session transcript and downloaded directly. _([sage/export.py](../sage/export.py), [sage/app.py](../sage/app.py); commits `4d14221`, `82cc0fd`, `ccd509a`)_                                                                                                                                                                                                                                                                                                                                                                        | Hand-tested both formats against an active session — file downloads correctly and renders cleanly.                                                                                                                                                                      | Shipped 04-28, after the review window. No reviewer has tested it. Anonymous and identified sessions both export, which means identified sessions can be reconstructed from two surfaces (export + persisted JSON) — duplicative but not harmful. |
| Conversations vanished on refresh; learners had no way to pick up where they left off (S.G., Matt — "multiple chats"). | **Per-session transcript persistence + resume-or-fresh prompt** for identified learners. Writes `data/interactions/<userId>/<sessionId>.json`. _([sage/session_store.py](../sage/session_store.py); commit `99c61fc` — pre-04-23, but relevant context for the multi-chat ask)_                                                                                                                                                                                                                                                                                                                                           | Pre-04-23 functionality; the 04-23 reviewers tested a build that already had it.                                                                                                                                                                                        | Solves single-thread resume, **not** multiple concurrent chats. S.G. and Matt's request for parallel chat history is still open.                                                                                                                  |

### Items not acted on this sprint, with reason

- **Multiple concurrent chats** (S.G., Matt) — UI redesign; held for next sprint. Single-thread persistence was the higher-leverage build first.
- **Explicit disclaimers / source-provenance** (Victoria) — not started; proposed as priority (1) below.
- **Lesson framing / "what kind of session is this"** (Victoria) — not started; proposed as priority (2) below.
- **Accessibility / auto-scroll / tech tips** (Victoria) — accessibility audit is a separate workstream; we did not have time to do it justice and didn't want to ship a token gesture.
- **Answer Victoria's open question** ("how do you understand an AI's hidden assumptions?") — this is curriculum content we need to write, not just a UX fix. Held.

---

## 4. Plan for the next cycle [TEAM REVIEW]

> These three priorities are scoped specifically to what the 04-23 batch surfaced. The full v2.1 plan (covering both 04-21 and 04-23 batches) lives in the master sprint report. **The team should edit this section before submission to reflect what we actually intend to ship.**

| What we will work on                                                                                                                                                                                                                                                                                                                                                                                                                                                   | How we will know it worked                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **(1) One-line disclaimer + soft provenance.** Add a single in-chat opener at every session start: "I'm SAGE — an LLM tutor. I can be wrong; verify important claims." When SAGE references a curriculum concept (CRAFT, signal-vs-noise, verification-cost test), append a short provenance tag ("from the AI-literacy CRAFT lesson").                                                                                                                                | Re-review by an outside person should not produce a "no disclaimers / no harm mitigation" comment, and at least 5 distinct curriculum references in transcripts carry consistent provenance tags. |
| **(2) Explicit lesson framing.** At the start of every scenario or lesson, emit one sentence naming the teaching shape — e.g., "This is an appropriateness-judgment exercise — I'll pose tasks one at a time and we'll work through your reasoning together." Addresses Victoria's "I expected something other than just more chat" and is a near-zero-cost win.                                                                                                       | A re-review user can say what kind of session they are in without asking.                                                                                                                         |
| **(3) Answer-then-deepen pattern enforcement.** Victoria's "how do you understand AI's hidden assumptions?" never got an answer because SAGE moved to the closing reflection. CLAUDE.md already specifies "answer first, then ask." We need an automated check: scan transcripts for learner direct-questions (`?` at end of a learner turn following a content-question word) that are followed by SAGE turns containing only another question — flag as a violation. | The check runs on a fixed transcript sample with a reproducible count. We expect to see violations and use them to tune the skills, not to declare "0 violations" and call it done.               |

**Stretch (only if we finish (1)–(3) early):**

- More chat starters (Matt asked for 2–3 more; current count is 6 — bring to 8–9 with two coding-context starters since a coding intent surfaced in Nathaniel's session).
- Add 2 more scenario templates so the dynamic generator has 4 instead of 2.
- Auto-scroll on new assistant message (Victoria) — Streamlit has a one-line fix for this.

**What we are deferring:**

- Multiple concurrent chats (UI redesign — too big for this cycle).
- Tech-tip / first-time-user walkthrough (Victoria) — accessibility workstream, separate from this iteration.
- Curriculum content for "interpreting AI assumptions" (Victoria's unanswered question) — content authoring task, not a feature.

---

## 5. Feedback over time [TEAM REVIEW]

The pattern this batch sharpens — and that the master v2.1 report also flagged — is **disclaimers / source-provenance**. Benny (04-21) and Cameron (04-21) raised it; Victoria (04-23) raised it independently. Three reviewers across two class sessions have now flagged the same gap, and we have not acted. This is the single piece of cross-batch repeated feedback this report wants to highlight, and it is exactly priority (1) above.

A second cross-batch pattern is **tone reading as corrective**. Earlier sprints surfaced it; Matthew named it again on 04-23 ("make sure tone doesn't feel chastising"). The 04-25 voice-and-register pass should help, but until a fresh outside reviewer tests post-04-25, we cannot claim it is fixed.

The CollaborAITE `#rg10-iteration-report` channel and AI-run analysis the assignment describes have not yet been set up; that step is owed for the final cycle.

---

## 6. AI use disclosure

Cyril used Claude Code to draft this report. Specifically: (a) read every reviewer entry in `04-23-2026/feedback.md`, (b) cross-referenced each piece of feedback against `git log` on both `AgentV2.1` and `main` for what shipped after 04-23, (c) drafted §2 (synthesis) and §3 (changes-made table), (d) proposed — but did not decide — the priorities in §4. The team should read the full draft and edit §4 to match what we actually intend to ship.

**Why this use was appropriate:**

- The feedback corpus for 04-23 alone is ~40 pages of free text across four reviewers; manual synthesis would have used time better spent shipping priorities (1)–(3).
- Claude was given access to the actual feedback file and the actual repository — every change-row in §3 cites a real commit SHA and a real file path, not a guess.
- §4 is explicitly flagged for team review, in line with the instructor's instruction that "the plan section should represent your team's actual decisions."
- All evidence-of-impact claims are conservative — wherever we hand-tested, we say so; wherever we did not, the cell says "no reviewer has tested this yet" rather than overclaiming.
- Direct quotes from reviewers are reproduced verbatim from `feedback.md` so the synthesis can be audited line-by-line against the source.
