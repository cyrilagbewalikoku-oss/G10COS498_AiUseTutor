# SAGE Roadmap — CollaborAITE-Dependent Features

This file lists features described in the specification (see `#MAIN Group 10 Draft of Agent Project Specification and Planning Document_Assignment.md`) that **are not present in the v2 Claude Code CLI build** because they depend on the CollaborAITE platform. They are documented here so the codebase reflects what is actually shipped vs. what remains deferred.

Each entry states:
- What it would do on CollaborAITE
- Why it isn't in v2
- What the current CLI analog is (if any)
- What would need to exist before it could ship

---

## Nudge Detector (spec §5, Path A)

**On CollaborAITE:** A background agent watches the learner's AI interactions in their CollaborAITE channels. When it detects a teachable moment — a prompt that could be improved, an AI output that warrants verification, a task where AI is a poor fit — it surfaces a subtle sidebar suggestion the learner can engage with or dismiss.

**Why deferred in v2:** No channel observability surface in the Claude Code CLI. No sidebar UI primitive. No event stream to subscribe to.

**Current CLI analog:** `/improve-interaction` skill — the learner explicitly pastes an AI interaction they had elsewhere. Same coaching logic, manual trigger.

**To ship on CollaborAITE:**
- CollaborAITE event hook for "learner sent AI a message in channel X"
- A throttling/relevance layer so SAGE doesn't nudge every message (detection precision matters more than recall)
- Sidebar UI primitive for non-invasive suggestions
- Dismissal telemetry to tune detection thresholds over time

---

## Scheduled Weekly Reflection (spec §4d Path C)

**On CollaborAITE:** SAGE proactively sends the learner a reflection prompt on a weekly cadence. Tone is peer-like and low-pressure. SAGE has access to the learner's channel AI interactions from the past week to anchor the reflection in concrete examples.

**Why deferred in v2:** No cron/scheduling surface in Claude Code CLI. No background process. The CLI is entirely user-initiated.

**Current CLI analog:** `/weekly-review` skill — the learner invokes the same flow manually when they're ready. They describe or paste 2–3 recent interactions instead of SAGE auto-surfacing them.

**To ship on CollaborAITE:**
- Scheduled trigger (CollaborAITE's equivalent of cron) that invokes the weekly-review flow
- Read access to the learner's recent channel AI interactions for the 7-day window
- A deferral mechanism ("remind me tomorrow") so the prompt doesn't become nagging
- Rate-limit so a learner can't accidentally trigger three reviews in a week

---

## Channel Conversation RAG (spec §4b)

**On CollaborAITE:** SAGE retrieves the learner's own channel AI interactions and uses anonymized patterns across peers to inform scenarios and reflection prompts. Example: "I noticed several people in your channel ran into the same fabricated-sources issue this week — you all might benefit from practicing verification."

**Why deferred in v2:** No channel data in the CLI build. Anonymized peer-pattern retrieval has privacy requirements a local file system doesn't enforce.

**Current CLI analog:** None direct. Fixed curated examples in `examples/interactions/` stand in for anonymized peer content when a scenario needs authentic material.

**To ship on CollaborAITE:**
- Vector index over the learner's own channel content (per-learner scope)
- Separately: an anonymized cohort-level index (stripped of identifying information, aggregated across learners)
- Strict access control: the learner-scoped index is readable only when that learner is the requesting user; the cohort-level index never surfaces individual interactions to other learners
- Retention policy (how long channel content stays in the index)

---

## Course Slides / Materials RAG (spec §4b)

**On CollaborAITE:** SAGE reads the current course's slides and activity descriptions to contextualize practice scenarios. A learner in a SOC 101 course sees scenarios framed around social science tasks; a learner in a CS course sees technical tasks.

**Why deferred in v2:** No course-materials surface in the CLI. The learner can attach a specific document but there is no persistent course corpus.

**Current CLI analog:** The learner can describe their course verbally during session start; scenarios are loosely tailored from that description. Specific documents can be attached at interaction time.

**To ship on CollaborAITE:**
- Read access to course documents via CollaborAITE's RAG
- A scenario-templating layer that substitutes course-specific examples into generic practice templates

---

## Anonymized Cohort Reflections (spec §4b)

**On CollaborAITE:** When running a weekly review, SAGE can note cohort-level patterns: "Most people in your section pushed back on AI output at least once this week — you have so far not. Worth a moment to think about why."

**Why deferred in v2:** No cohort context. Individual-only.

**Current CLI analog:** None. Weekly review is purely individual.

**To ship on CollaborAITE:**
- Cohort-level aggregation over anonymized interaction metadata
- Threshold logic so patterns are only surfaced when statistically meaningful (not "1 out of 3 peers did X")
- Framing that avoids surveillance feel — "here's a pattern across the class" is fine, "you specifically are an outlier" is not

---

## @mention Trigger (spec overview)

**On CollaborAITE:** Learners invoke SAGE by @mentioning the agent in a channel. Multi-turn dialogue happens in a thread. SAGE can display plans in threaded step-by-step format.

**Why deferred in v2:** The Claude Code CLI is the invocation surface. No channels, no @mentions, no threads.

**Current CLI analog:** Slash commands (`/onboarding`, `/scenario-runner`, etc.) or conversational intent routing via `session-router`.

**To ship on CollaborAITE:**
- CollaborAITE's bot-integration protocol (@mention handling, thread management)
- A "display a plan" primitive equivalent to threaded step-by-step in CollaborAITE's UI

---

## What v2 *does* deliver

Everything listed above is a delivery-surface feature. The **pedagogy** described in the spec — ACKNOWLEDGE → NUDGE → EXPLAIN, Learner Predicts, CRAFT, four practice types, single closing reflection, Merrill + Bloom scaffolding, IMPACT ethical audit, learner-predicts misconception catalog — is fully present in v2 CLI. Evaluators should target the pedagogy in their evaluation; deployment-surface gaps are documented here and not part of the April 21 deliverable.
