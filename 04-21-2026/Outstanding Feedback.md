# Outstanding Feedback — April 21, 2026 peer review

Feedback items from `04-21-2026/Summarized Feedback.md` that are **not yet addressed** in SAGE as of April 23, 2026. Each item links back to the reviewer who raised it, classifies severity, and proposes where the fix lives.

Legend:
- **Severity** — Blocker / High / Medium / Low (team judgment)
- **Status** — Open / In-plan (committed in Iteration Report §5) / Deferred (explicitly dropped this cycle)
- **Surface** — prompt / skill / UI / scenarios / docs

---

## 1. Opening question gets intercepted by onboarding

- **Reviewers:** Person 1 (S.G.)
- **Severity:** Blocker
- **Status:** In-plan (Iteration Report §5, item 1)
- **Surface:** session-router + onboarding skills
- **Evidence:** S.G. opened with "could you tell me more on how detailed prompts can be good…" — SAGE responded "let me check if we've worked together before. What's your name?" before answering. The question was only fully addressed after S.G. steered back to it explicitly.
- **Why it matters:** The first impression of SAGE is that it ignores the learner to run a form. CLAUDE.md already carries the "Re-check intent each turn" rule and onboarding has bail conditions — the rule exists but didn't fire.
- **Proposed fix:** Branch on the first message: if the opener is a content question, answer it in 1–2 sentences before offering a profile setup. Verify by re-running the exact S.G. transcript against the updated prompt.

## 2. Asking for name at session start feels invasive

- **Reviewers:** Person 1 (S.G.), Grace (Person 4's priority suggestion)
- **Severity:** High
- **Status:** In-plan (Iteration Report §5, item 1 — bundled with #1)
- **Surface:** onboarding skill
- **Evidence:** S.G. — "It felt really uncomfortable when the AI asked for my name, which is personal information to me, when I was just expecting an answer to my prompt." Grace's one-line priority: "don't ask for name at the start."
- **Proposed fix:** Allow pseudonym / skip entirely. Don't prompt for a name before the first value-delivering exchange. Explicitly offer "you can skip this if you want."

## 3. Unanswered learner question at closing reflection

- **Reviewers:** Person 4 (Victoria)
- **Severity:** High
- **Status:** In-plan (Iteration Report §5, item 2)
- **Surface:** reflection-facilitator skill
- **Evidence:** Victoria's final message — "I'm really not sure — how do you get to an understanding of what hidden assumptions an AI model might be running on?" SAGE responded by saving her profile and presenting the next module, leaving the genuine question unanswered. Victoria explicitly flagged this in her written review.
- **Why it matters:** The closing-reflection pattern is designed for the learner to *reflect*. When their reflection is itself a substantive question, the pattern papers over a real gap. CLAUDE.md now says "Answer first, then ask" — the reflection-facilitator skill doesn't implement that branch.
- **Proposed fix:** In `reflection-facilitator`, detect when the learner's reflection is a question and answer briefly (2–3 sentences) before closing.

## 4. Confusing double-negative phrasing around "closing the gap"

- **Reviewers:** Person 2 (Matthew)
- **Severity:** Medium
- **Status:** In-plan (Iteration Report §5, item 2 — bundled)
- **Surface:** prompt-coaching skill (nudge templates)
- **Evidence:** SAGE: "if the AI replaced a word with a fancier synonym, would your current prompt technically forbid that?" Matt read this as *permission* and added "You are allowed to replace words with fancier synonyms, however." to his prompt — the opposite of the intended reading.
- **Proposed fix:** Rewrite the nudge template so the question is positively framed ("Does your current prompt tell the AI to keep your original word choices?") rather than double-negative ("would it technically forbid…?").

## 5. Teaching style is implicit / not named

- **Reviewers:** Person 4 (Victoria — top priority)
- **Severity:** Medium
- **Status:** In-plan (Iteration Report §5, item 3)
- **Surface:** onboarding + lesson-start (concept-explainer, scenario-runner)
- **Evidence:** Victoria: "The agent should be more specific and explicit about naming the learning style being used in the conversation. It will feel more transparent and collaborative if a user is told, explicitly 'we'll learn today by using hypothetical thought experiments to…'"
- **Proposed fix:** At the start of a lesson, add a compact "here's how we'll work together" line that names the approach — e.g., "I'll ask you to predict what the AI will do before I explain anything. You do the thinking, I label the patterns."

## 6. No visible harm-mitigation / disclaimer

- **Reviewers:** Person 4 (Victoria)
- **Severity:** Medium
- **Status:** In-plan (Iteration Report §5, item 3 — bundled)
- **Surface:** UI (sidebar) + session-router welcome
- **Evidence:** Victoria — "the agent didn't make any explicit statements that seemed oriented towards harm mitigation — no disclaimers or expectation setting." She also raised the "false confidence" risk: users may feel *less* at risk after using SAGE simply because they've now interacted with a tool framed as a safety educator.
- **Proposed fix:** Compact persistent sidebar disclaimer: "SAGE is a learning tool, not an authority. It can be wrong. Don't paste sensitive personal data." Plus one sentence in the welcome surface.

## 7. No multi-chat support

- **Reviewers:** Person 1 (S.G.), Person 2 (Matt — top priority)
- **Severity:** High (most-requested feature)
- **Status:** **Deferred** (Iteration Report §5 — acknowledged, pushed to v-next)
- **Surface:** Streamlit UI
- **Evidence:** S.G. — "Should have more than one chat to save and keep track of at a time." Matt — "Multiple chats is a must. Without them, you can only have one conversation at once, which is rather limiting."
- **Rationale for deferral:** This is a Streamlit surface feature, not an agent-behavior issue. Final-sprint hours will be spent on pedagogy first. Will be reconsidered if the three pedagogical fixes (§5 items 1–3) land early.

## 8. No way to copy / export a conversation

- **Reviewers:** Person 1 (S.G.)
- **Severity:** Medium
- **Status:** **Deferred** (bundled with #7)
- **Surface:** Streamlit UI
- **Evidence:** S.G. — "There also wasn't an option I could see to copy my discussion."
- **Proposed fix (if taken up):** "Export transcript as markdown" button in the Streamlit sidebar — one day of work.

## 9. More sidebar starter prompts

- **Reviewers:** Person 2 (Matt)
- **Severity:** Low
- **Status:** **Deferred** (tracked, can pick up opportunistically)
- **Surface:** Streamlit UI (`sage/app.py`)
- **Evidence:** Matt — "More chat starters, like the ones listed currently. Perhaps about 2-3 more."
- **Proposed fix:** Add 2–3 more — candidates: "Show me a common AI mistake," "What shouldn't I use AI for?", "Quiz me on what we've covered."

## 10. Scenario library feels thin; no domain match for coding learners

- **Reviewers:** Person 3 (Nathaniel — top priority: "More scenarios in the future")
- **Severity:** Medium
- **Status:** Partially in-plan (one coding scenario to add — Iteration Report §5 "Dropped / deferred" section)
- **Surface:** `data/scenarios/`
- **Evidence:** Nathaniel picked coding as his goal; SAGE offered email-drafting or data-analysis with the (honest) caveat "Neither is directly about coding." Nathaniel flagged "Limited amount of scenarios" as a realistic-risk concern *and* his priority suggestion.
- **Proposed fix:** Add at least one coding-focused prompt-crafting scenario. Then stop — scenario count is not the actual constraint, domain coverage is.

## 11. Tech-literacy onboarding gap (scroll, tooltips, chat clearing, Enter key)

- **Reviewers:** Person 4 (Victoria — equity analysis + secondary priority)
- **Severity:** Medium (equity dimension)
- **Status:** **Deferred** (Iteration Report §5 explicitly drops this for this cycle)
- **Surface:** Streamlit UI
- **Evidence:** Victoria — "I was imagining using this tool as a senior citizen wanting to learn about AI — would I know to type in the chat bar? … Even I had a moment where I didn't realize that the AI had responded because the display doesn't automatically scroll to the most recent message."
- **Rationale for deferral:** Real equity concern, real UX gap, but UI polish is downstream of the behavior fixes. Documented here so it doesn't fall off the radar.

## 12. "Corrective rather than helpful" tone in one moment

- **Reviewers:** Person 2 (Matthew)
- **Severity:** Low
- **Status:** In-plan (addressed narrowly via #4 phrasing rewrite)
- **Surface:** prompt-coaching nudge templates
- **Evidence:** Matthew — "There was a moment it felt a bit more 'corrective' than helpful, but only a moment." Traces to the same synonym-rule exchange as #4.
- **Proposed fix:** The phrasing fix in #4 should also soften the corrective feel. If it doesn't, we'll consider a broader nudge-tone pass — but only with more than one reviewer's signal.

## 13. Lesson format expectation mismatch (first lesson *is* conversation)

- **Reviewers:** Person 4 (Victoria)
- **Severity:** Low
- **Status:** Partially addressed by #5 (naming the style explicitly); otherwise Deferred
- **Surface:** onboarding + concept-explainer
- **Evidence:** Victoria — "It felt a little bit strange that the first 'lesson' in using AI was presented through an extended discussion with the AI chat bot. I had kind of expected something beyond just continued conversing." She later noted this was consistent with her stated learning style, so partially self-corrected.
- **Proposed fix:** Naming the teaching style upfront (#5) likely resolves the mismatch. If not, consider offering a brief framed overview ("here's what we're covering in 3 bullets") before jumping into the dialogue.

---

## Items that do NOT appear on this list

These were raised in the feedback but **do not need to be addressed** — either because they are not actually problems, or they are downstream of items already listed:

- **Praise for the nudging pattern, tone, and conciseness** (all reviewers) — these are strengths to preserve, not fixes.
- **"Agent applies context well"** (Matt, Nathaniel) — affirmation; no action.
- **"No confabulation noticed"** (Matt, Victoria) — affirmation; keep running quality checks but no specific fix.
- **"Privacy-conscious users might not like it"** (S.G.) — this is a symptom of #2 (name request). Fixing #2 addresses it.

---

## Tracking

When final-sprint work begins, each in-plan item above becomes a GitHub Project issue with a reviewer-name tag so we can close the loop by reporting back to the class: *"Victoria, here's the change we made based on your feedback."* This is the single most important outcome — that every reviewer sees their feedback reflected somewhere concrete.
