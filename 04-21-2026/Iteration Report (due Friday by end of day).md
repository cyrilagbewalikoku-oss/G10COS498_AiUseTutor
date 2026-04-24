# Iteration Report — SAGE (Group 10)

## *End-of-sprint reflection and plan for the next cycle*

| Course | COS 598/498 — Generative AI Agents (Spring 2026) |
| :---- | :---- |
| **Team** | Group 10 — SAGE (Scaffolded AI Guidance for Engagement) |
| **Deliverable** | One report per team |
| **Format** | Markdown file in repo: `04-21-2026/Iteration Report (due Friday by end of day).md` |
| **Submit** | Link shared with instructor on Brightspace |
| **Due** | Friday, April 28, 2026 (end of day) |
| **Sprint window covered** | April 16 → April 23, 2026 |

---

## 1. Feedback inventory

Sources of feedback processed this sprint:

- **In-class peer review on Tuesday, April 21 (COS 490 Ethics class — 4 reviewers).** Primary feedback source this sprint. Each reviewer ran 1 session of ~10–15 minutes and filled out the Ethical Agent Analysis template. Raw feedback consolidated at `04-21-2026/Summarized Feedback.md`.
  - Person 1 (S.G.) — asked about detailed prompts; got onboarding first.
  - Person 2 (Matt) — practiced prompt crafting for grammar-only editing.
  - Person 3 (Nathaniel) — practiced prompt crafting on a data analysis scenario.
  - Person 4 (Victoria) — practiced appropriateness judgment for school tasks.
- **Cross-class peer review on Thursday, April 23 (COS 490 Ethics class).** Not yet synthesized at time of writing — will be added to `04-23-2026/` when raw notes are posted.
- **In-class peer review on Thursday, April 23 (COS 498).** Same — deferred to the 04-23 folder.
- **Instructor feedback.** Written comments in CollaborAITE channel messages and in-class conversations during the April 16 and April 21 sessions. No blocking issues flagged; instructor validated the CLI-first deployment strategy.
- **Outside-class use.** None reported this sprint.

Raw feedback is not duplicated here — see `04-21-2026/Summarized Feedback.md` (full reviewer transcripts and response bank).

---

## 2. Synthesis — what the feedback actually said

### What SAGE is doing well

- **Scaffolded nudging lands.** All four reviewers called out the "predict before I explain" move as the standout moment — S.G. said it "excited me a little," Victoria named the mRNA mental-model nudge as the strongest moment of the session, and Nathaniel said the anonymization nudge "reinforces better privacy practices." The ACKNOWLEDGE → NUDGE → EXPLAIN pattern is the core differentiator and it is reading as intended.
- **Self-aware tutor tone is working.** Matt called SAGE "self-aware about the flaws of AI usage" and "focuses on being more academic." Victoria described it as "encouraging and approachable." Nathaniel said responses are "to-the-point and don't have a lot of fluff like some AI Agents do."
- **Constrained output coaching transfers.** Matt went from a vague "clean up this text" prompt to one that bounded structure, flow, and word choice — and he named the transferable principle ("constraining the action") himself. The CRAFT-driven prompt coaching loop is producing real skill transfer in a single session.
- **Contextualization works when the learner supplies context.** Victoria told SAGE she wanted Socratic-style study support; SAGE picked appropriateness judgment (correct first module for her goal) and wove her stated learning style back into the scenario. Nathaniel asked about coding; SAGE honestly said "neither scenario is directly coding, but the skills transfer" — reviewers respected the honesty.

### What is breaking, confusing, or missing

- **Onboarding overrides the learner's opening request.** S.G. opened with a substantive content question ("tell me more on how detailed prompts can be good") and was immediately routed through "What's your name? / Have you used ChatGPT before? / What's the #1 risk…" before the original question was answered. The onboarding skill's "bail conditions" (April 20 CLAUDE.md update) are supposed to handle this — they did not fire in the live session. The same transcript also shows SAGE jumping to "Want to try a scenario?" *before* finishing the answer to the original question, then circling back after the learner corrected the flow.
- **Asking for name up front feels invasive.** Named explicitly by S.G. ("It felt really uncomfortable when the AI asked for my name") and Grace ("don't ask for name at the start") as a priority fix. Victoria's equity analysis pointed at the same root issue from a different angle (a senior citizen would feel intimidated before the first answer).
- **No way to export / copy / keep parallel chats.** Called out by S.G. ("There also wasn't an option I could see to copy my discussion" + "Should have more than one chat to save and keep track of at a time") and Matt ("Multiple chats is a must. Without them, you can only have one conversation at once, which is rather limiting"). This is the single most-repeated concrete request.
- **Teaching style is implicit.** Victoria's top priority suggestion: name the pedagogy explicitly at the start ("we'll learn today by using hypothetical thought experiments to…"). Currently SAGE just starts doing it. Victoria also felt surprised that the "first lesson" *was* a conversation rather than being introduced by a walkthrough / video / task.
- **Unanswered learner question.** Victoria asked "how do you get to an understanding of what hidden assumptions an AI model might be running on?" at the closing-reflection stage. SAGE saved her profile and moved on without answering. The April 21 CLAUDE.md update added the rule "Answer first, then ask" specifically for this — it didn't fire.
- **Phrasing slippage around negatives.** Matt got confused when SAGE said "if the AI replaced a word with a fancier synonym, would your current prompt technically forbid that?" — he read it as permission rather than a gap to close. This is a wording problem in how SAGE constructs "closes that gap" nudges.
- **No harm-mitigation surface.** Victoria noticed the absence of disclaimers or expectation-setting. No visible guardrails, no statement about what SAGE will and won't do, no "this is a learning tool, not an authority" framing.
- **Tech-onboarding gap for non-technical users.** Victoria's equity reflection: a senior citizen or low-tech-literacy user would not know the scroll behavior (messages don't auto-scroll into view after send), would not know to press Enter, would not know they can clear the conversation. No tool tips or first-run walkthrough.
- **Scenario library feels thin.** Nathaniel: "Limited amount of scenarios for it to go through (seemingly, I might be wrong)." He's half right — there are 8 scenarios in `data/scenarios/` but when he picked coding as his goal, neither offered scenario matched his stated interest. The felt-shallow problem is really a coverage problem: we don't have domain-matched scenarios for common learner goals.

### Where reviewers disagreed / traded off

- **Direct answer vs. teaching loop.** Victoria wanted her last question ("how do I know what hidden assumptions an AI is running on?") answered; SAGE is designed to end with a reflection, not an explanation. This is a real tension: the pedagogy says "let the learner reflect," but if the learner's reflection *is* a genuine unanswered question, the closing-reflection pattern papers over a real information gap. Our tentative resolution: if the learner's reflection is itself a question, answer it briefly, then ask whether they want to keep going.
- **More starters vs. less upfront clutter.** Matt wants more starter prompts in the sidebar. Victoria's equity analysis wants less friction / more guidance for the tech-illiterate. These aren't opposed but they point at different surface areas — starter buttons help Matt; a first-run walkthrough helps Victoria.

### Functionality not getting discovered

- `/improve-interaction` (paste a prompt you already used and get coached on it) — no reviewer found or used it. It's in the starter-button list as "Help me improve this prompt I used" but no one clicked it. Possibly because all four reviewers were placed on the onboarding → first-lesson track and never returned to the menu.
- `/weekly-review` — same. No reviewer used it.
- `/prompt-lab` — not surfaced in the sidebar starter list; only reachable via SAGE suggesting it mid-conversation.
- `/bad-agent-simulator` — same, no learner discovered it.

This is a discoverability problem, not a feature gap — four skills exist and aren't being tried because the default flow pulls everyone into the same onboarding → scenario path.

### Ideas for improvements

**From the feedback directly:**
- Add an opt-out / "skip the intro, just answer my question" path to onboarding (S.G., Grace).
- Add multi-chat + export in the Streamlit UI (S.G., Matt).
- State the teaching style explicitly at session start (Victoria).
- Answer the learner's question when their reflection *is* a question (Victoria, supported by the "Answer first, then ask" rule already in CLAUDE.md).
- Add 2–3 more starter prompts in the sidebar (Matt).
- Add more scenarios, especially for common learner goals like coding (Nathaniel).

**From processing the feedback as a team:**
- Audit the onboarding bail-conditions in live transcripts, not just the skill spec. The spec says bail on "unrelated question" but the live S.G. session didn't bail. Either the bail logic isn't reaching the live prompt, or the model is overriding it. Worth tracing.
- Add a pre-onboarding branch point: the *first* message is what decides whether to ask for a name at all. If the opener is a question about AI use, answer it first, then offer to set up a profile.
- Add a brief visible "what SAGE is / isn't" disclaimer either in the welcome screen or as a persistent sidebar note, closing Victoria's harm-mitigation gap without cluttering the conversation.
- Rewrite the "closes-that-gap" nudge template to avoid the double-negative trap Matt hit. (E.g., "Does your current prompt prevent the AI from swapping in fancier synonyms?" instead of "would your current prompt technically forbid that?")

---

## 4. Changes made this sprint and evidence of impact

Sprint window for this table: April 16 → April 23. Several of these landed in response to earlier (April 16) peer review feedback; the April 21 feedback is addressed in §5 *Plan for the final cycle*.

| Design problem / issue or opportunity | Change made | Evidence of impact | Remaining gap |
| :---- | :---- | :---- | :---- |
| Onboarding ran too long; learners felt quizzed before getting value. | Hard cap at 3 calibration questions + added "bail conditions" that short-circuit onboarding when the learner goes terse, asks an unrelated question, or says "skip" / "just show me" (`.claude/skills/onboarding/SKILL.md`, commit `6957f1e`, `d30d0db`). | Partial — S.G.'s April 21 session still routed through full onboarding despite her opening with a content question. The rule exists in the prompt but did not fire live. | Need to verify the bail logic reaches the deployed prompt and that the model honors it. Also: onboarding still asks for name before the first exchange. |
| Prompt drift between Claude Code dev and the deployed Streamlit / CLI app. | Build-time generator `scripts/build_prompts.py` rebuilds `sage/prompts.py` from `CLAUDE.md` + `.claude/skills/` at image build. Live app can also rebuild at startup (`sage/app.py` + `sage/skill_loader.py`). CI drift check fails PRs that desync (commits `b9f4325`, `95ad42a`, `9fe8cb5`, `73cd5b2`). | Confirmed — manually edited a skill, rebuilt the image, observed the new behavior in the deployed Streamlit app. CI blocks the stale-snapshot case. | None — this one worked. Keep it. |
| Skills were "bulldozing" — plowing through their internal scripts even when the learner had moved on. | Added the "Re-check intent each turn" rule to CLAUDE.md and propagated it into each skill (commit `6957f1e`, `8259a1c`, v2.1 release notes in README). | Partial — Victoria's session showed improvement (SAGE honored her "Socratic-style" stated preference and matched the module to it). S.G.'s session shows the rule still fails under some openings. | Need to verify with more live transcripts; the rule reads as advisory and the model sometimes under-weights it. |
| Answers got buried after "let me ask you something first" / meta-transitions. | Explicit rule in CLAUDE.md: *"Cut meta-transitions like 'let me ask you something before I go further.' Just ask, or just say the thing"* + *"Answer first, then ask"* (April 21 CLAUDE.md update, commit `6957f1e`). | Partial — Victoria's final question about hidden assumptions was still left unanswered in the April 21 session. The rule is in the prompt but doesn't fire in the closing-reflection step. | The closing-reflection skill (`reflection-facilitator`) needs to branch: if the learner's reflection is itself a question, answer before closing. |
| SAGE on Railway / production ran an out-of-date prompt. | Fix `sage-ui` to rebuild prompt at app startup in local dev, use frozen snapshot in prod; Dockerfile + Procfile for Railway (commits `08ae1f4`, `7c5492d`, `3a4d09c`). | Confirmed — the deployed app now starts up with the current prompt, verified by printed `[sage] prompt source:` log line. | None for deploy wiring. (The *content* of that prompt is still the open question — see S.G. transcript.) |
| Scenario library too narrow. | Added 3 scenarios (`output-evaluation-errors.json`, `misinformation-detection.json`, `research-synthesis.json`) — `data/scenarios/` now has 8 scenarios across all 4 practice types (commits in `4a6d24b`). | Unverified — none of the 4 April 21 reviewers hit the new scenarios in their single sessions. Nathaniel still felt the library was "limited." | Coverage is thin for common learner goals (e.g., coding). Need at least one domain-matched scenario for each of the top 3 learner goals we see (school, work, coding). |
| `save_user_profile` accepted unsafe filenames. | Hardened filename validation — rejects traversal and unsafe chars (commit `eaae257`). | Confirmed — unit test added, adversarial inputs are rejected. | None. |
| Streamlit UI had no starter prompts; new users stared at an empty input. | Added 6 one-click starter buttons in the sidebar (`sage/app.py`, commit `5da6cce` / `36b8303`). | Partial — all four April 21 reviewers found a starter easily. Matt suggested 2–3 more; Victoria still faced a cold-start usability gap for non-technical users (no scroll, no tool tips). | Sidebar is dense for first-time users; no first-run walkthrough; Matt's request for more starters is unmet. |

**Feedback we chose not to act on this sprint (and why):**

- **Multi-chat / export.** Called out by 2 of 4 reviewers on April 21. Deferred because it's a Streamlit-surface feature, not an agent-quality feature, and the team's remaining hours are better spent on the agent's actual behavior. We will revisit in the final sprint (see §5).
- **Auto-scroll / tooltips for low-tech users.** Deferred for the same reason — UI polish is downstream of pedagogy.
- **Tone-felt-chastising (Matthew).** Narrow and anecdotal — one reviewer, in one specific moment (the synonym correction). We will rewrite the specific nudge template next sprint but not do a broader tone pass without more signal.

---

## 5. Plan for the final cycle

Three focused workstreams for the final sprint. Everything else is explicitly deferred.

| What we will work on | How we'll know we did a good job — what would make us comfortable handing this to someone outside the class |
| :---- | :---- |
| **(1) Fix the onboarding-intercepts-the-opening-question bug.** Rework the session entry so the learner's *first* message is the signal: if it's a content question, answer it in 1–2 sentences, then offer to set up a profile. Stop asking for a name before the first exchange; allow a pseudonym or skip entirely. | Re-run S.G.'s transcript verbatim against the updated prompt and get a response that answers the detailed-prompts question first. Two new outside users run 5-minute sessions with a content-question opener and neither gets quizzed first. |
| **(2) Close the "unanswered learner question" gap in the closing reflection.** Update `reflection-facilitator` so that if the learner's closing reflection is itself a genuine question (like Victoria's "how do I know what hidden assumptions…"), SAGE answers it in 2–3 sentences before closing. Pair with a rewrite of the "closes-that-gap" nudge template to eliminate the double-negative phrasing that confused Matt. | Replay Victoria's transcript: her final question now gets a concrete answer. Replay Matt's synonym-rule exchange: the corrective phrasing reads as a gap to close, not permission to keep swapping words. |
| **(3) State the teaching style + harm-mitigation framing once, visibly.** Add a compact "here's what we're doing today" line at the start of a lesson, naming the method (e.g., "I'll nudge you to predict before I explain"). Add a small persistent sidebar disclaimer about what SAGE is and isn't (a learning tool, not an authority; it may be wrong; don't paste sensitive data). | A first-time outside user can, after one session, describe in their own words how SAGE teaches. The sidebar disclaimer is visible without hijacking the conversation. |
| **(4) Implement 2–4 key automated evaluation metrics to a level that the metrics are useful but not perfect.** Candidate metrics: (a) onboarding-length distribution (flag runaway sessions), (b) rule-compliance checks on "answer before ask" and "nudge before explain" via LLM-as-judge on sampled transcripts, (c) scenario-completion rate, (d) average learner message length over a session (proxy for engagement). | We can take any 10 sampled sessions and get a numeric read-out. Numbers visibly move when we change a skill. |
| **(5) Implement 1 "human rated" evaluation of conversations.** A rubric (5–7 items) and a spreadsheet where two team members independently rate 8 sampled transcripts. | Inter-rater agreement is above 70% on the "did the nudge precede the explanation?" item. We have a baseline number to compare against post-change. |

**Dropped / deferred explicitly:**

- Multi-chat and export UI — acknowledged as the most-requested feature, but it's a Streamlit-surface problem. If the three pedagogical fixes above land early, we pick this up; otherwise it's v-next.
- Auto-scroll and low-tech-user tooltips — same reasoning. Victoria's equity point is real; we're deferring because the agent-behavior fixes have higher expected value for the final grade.
- Additional scenarios beyond the 8 already shipped — we'll add one coding scenario (Nathaniel's gap) and stop.
- "Chastising tone" broad pass — addressed narrowly via the #2 rewrite, not broadly.

**Usability bar:** We want at least one learner from the April 21 cohort to come back and use SAGE unprompted on their own time. If that happens, we've hit the A-/A bar Greg mentioned.

**Next step — project management:** Open these as tasks in the team's GitHub Project board with staggered due dates (Apr 25, Apr 29, May 2). Link will be posted in the CollaborAITE `rg#-iteration-report` channel once created.

---

## 6. Feedback over time

A public channel `rg#-iteration-report` will be created in CollaborAITE. It will contain, in separate labeled posts:

- **April 9 → April 16 feedback + changes** — in-class review on April 16, prompted the v2.1 release and the skill-drift fix.
- **April 16 → April 21 feedback + changes** — CLAUDE.md tightening (April 21), onboarding bail conditions, expanded scenario library.
- **April 21 feedback (current)** — full raw reviews at `04-21-2026/Summarized Feedback.md`; synthesis above.

### AI-assisted repeated-feedback scan

A meta-prompt will be run against the combined feedback corpus with the goal: "identify any feedback themes that appeared in two or more of the three review windows and are *not* reflected in the intervening changelog." A team member will manually read the same corpus in parallel and list anything they see.

**Manual review results:** *(To be filled in by team member — one of Elvis or teammate — after manual read.)*

**AI results:** *(Link to the Claude output doc in CollaborAITE.)*

**Short summary / 3–5 bullets of the most important results + evaluation of each:** *(To be filled in after both reads complete. For each bullet, state whether the team agrees the pattern is real, a confabulation, or inaccurate — with rationale.)*

---

## Format, length, logistics

- **Length:** ~3.5 pages excluding session logs. Session logs live at `04-21-2026/Summarized Feedback.md`.
- **Location:** Markdown file in the repo at `04-21-2026/Iteration Report (due Friday by end of day).md` — link submitted on Brightspace.
- **Author:** Elvis drafted; full team to read and sign off before submission.

### AI use in producing this report

Claude Code (Opus 4.7) was used to cross-reference the raw reviewer feedback against the current SAGE codebase, `.claude/skills/`, `CLAUDE.md`, and the git log, then draft the synthesis and table above.

- The team read the raw feedback ourselves before Claude touched it. Claude's job was pattern-matching against code state, not inventing the themes.
- Every claim in the "Changes made this sprint" table is anchored to a specific commit hash or file path that a reader can open and verify.
- Every claim in the "What is breaking" section cites a specific reviewer by pseudonym so the source is auditable.
- The "Plan for the final cycle" reflects the team's actual decisions about trade-offs (multi-chat deferred, evaluation metrics prioritized) — not a Claude-generated wish list.
- Where a claim is speculative ("the rule exists but does not fire live"), it is labeled as such and flagged as "verify in the final sprint" rather than asserted as fact.
