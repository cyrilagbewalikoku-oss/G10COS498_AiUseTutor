# SAGE: A Scaffolded Tutor for AI Agent Literacy

**Technical Report — AgentV2.1**
**Project:** G10COS498 AI Use Tutor
**Date:** May 2026

## 1. Overview

SAGE (Scaffolded AI Guidance for Engagement) is a domain-specialized tutoring agent whose sole purpose is to help learners develop AI agent literacy — the ability to use generative AI tools effectively, ethically, and critically. Unlike a general-purpose assistant, SAGE will not complete a task on the learner's behalf; every interaction is shaped by a pedagogical objective. Its core loop is **practice → scaffolded feedback → closing reflection**.

The agent is implemented on top of the Anthropic Claude API (`anthropic>=0.90.0`) and is delivered through three complementary surfaces:

1. A **Streamlit web application** (`sage-ui`, defined in `sage/app.py`) deployed via Docker to Railway, with a learner picker, persistent profiles, and exportable chat transcripts.
2. A **terminal CLI** (`sage`, defined in `sage/agent.py`) that runs the same conversation loop locally.
3. The **Claude Code skills runtime** in this repository, where the eighteen skills under `.claude/skills/` can be invoked directly during development.

A build-time generator (`scripts/build_prompts.py`) compiles `sage/prompts.py` from `CLAUDE.md` and the skill files so that the standalone deployments stay byte-aligned with the in-repo skill definitions; `.github/workflows/prompts-drift.yml` fails any pull request that drifts.

## 2. Architecture

### 2.1 Skill-based composition

Rather than encoding all behavior in a monolithic system prompt, SAGE is decomposed into eighteen skills under `.claude/skills/`, each defined by a `SKILL.md` file with frontmatter (`name`, `description`, `when_to_use`) and a body describing its routine. Skills fall into five functional clusters:

- **Routing and adaptation:** `session-router` (universal entry point, classifies intent, hands off to the appropriate skill) and `difficulty-adapter` (internal — dynamically tunes scaffolding based on response signals).
- **Teaching:** `onboarding`, `concept-explainer`, `prompt-coaching` (CRAFT framework — Context, Role, Action, Format, Tone), and `ethical-guidance` (Socratic exploration of dilemmas).
- **Assessment:** `knowledge-check`, `skill-evaluator`, and `level-classifier`, which gates advancement on demonstrated competence across all five assessment dimensions.
- **Practice and simulation:** `scenario-runner` (runs the four practice types), `bad-agent-simulator` (role-plays a flawed AI for detection practice), and `prompt-lab` (sandbox for prompt iteration).
- **Feedback and reflection:** `improve-interaction` (coaches a real pasted transcript), `reflection-facilitator`, `progress-reporter`, `improvement-advisor`, and `weekly-review`.

A separate `voice-and-register` skill is loaded internally by every teaching and feedback skill. It owns SAGE's tone — register matching, process-praise phrase banks, banned phrases, struggle framing — so that consistency across skills does not require duplicating language in each file.

Five workflows under `workflows/` (onboarding, lesson, practice, assessment, ethical-reasoning) compose these skills into multi-step sequences aligned with Merrill's First Principles.

### 2.2 Data layer

Persistent state is stored as JSON on disk, validated against schemas in `data/schemas/` (`user-profile`, `interaction-log`, `assessment-result`, `scenario`, `scenario-template`). The schema set is small but load-bearing — the user profile alone tracks role, skill level, goals, prior knowledge, course enrollment, the five assessment dimension scores, and the four competency scores.

`data/` also holds curated content: six seed learner profiles spanning all four levels (`data/users/`), eight practice scenarios across the four practice types (`data/scenarios/`), three rubrics (`data/rubrics/`), and pedagogical research summaries (`data/research/`). Runtime session transcripts are persisted under `data/interactions/<userId>/<sessionId>.json` (gitignored). On Railway, a mounted volume holds this data and is seeded from the in-repo defaults on first boot.

The Python package `sage/` exposes the runtime: `agent.py` and `app.py` are the two entry points, `tools.py` defines the agent's tool surface (profile I/O, scenario loading, rubric access), `session_store.py` handles persistence and Railway seeding, `skill_loader.py` loads `.claude/skills/` at runtime, and `export.py` writes chat transcripts as Markdown for evaluation.

## 3. Pedagogical foundations

SAGE's behavior is grounded in established instructional design rather than ad-hoc prompting. Three frameworks are encoded directly in `CLAUDE.md` and in each skill:

**Merrill's First Principles of Instruction** drive the workflow shape: every lesson is problem-centered, activates prior knowledge, demonstrates worked examples before practice, applies in realistic scenarios, and integrates with reflection. **Bloom's Revised Taxonomy** maps to the four skill levels — Novice (Remember/Understand), Practitioner (Apply/Analyze), Advanced (Analyze/Evaluate), and Critical Thinker (Evaluate/Create) — and dictates vocabulary, example complexity, and expected autonomy at each tier.

The defining behavioral pattern is the **ANE scaffold — ACKNOWLEDGE → NUDGE → EXPLAIN**. When giving feedback on a learner's practice attempt, SAGE first names what the learner did, then asks a brief question that makes the learner *predict or reason about the underlying principle* before SAGE explains it. The non-negotiable rule is that the nudge precedes the explanation: the learner must engage their own reasoning before being handed the principle. The pattern is also explicitly *invisible* — labels like "ACKNOWLEDGE" never appear in user-facing speech, and the EXPLAIN step is skipped when the learner has already named the principle themselves.

Importantly, ANE applies only to *feedback on practice attempts*, not to direct learner questions. If a learner asks "what is a hallucination?", SAGE answers first and then optionally deepens with a question. Misapplying ANE to direct questions makes the agent feel evasive — a failure mode documented explicitly in the system prompt.

Assessment is scored on a 0–5 scale across five dimensions: conceptual understanding, prompting skill, output evaluation, ethical reasoning, and critical thinking. Level advancement, handled by `level-classifier`, is deliberately uncompensated: a learner cannot advance with a strong score in prompting but a weak score in ethics. All five dimensions must reach threshold, and at least two of the four practice competencies (prompt crafting, output evaluation, appropriateness judgment, workflow design) must also be demonstrated.

## 4. Safety and trust model

Two design choices distinguish SAGE from a generic chat agent.

**Privacy-by-design.** SAGE only ever reads the requesting learner's own profile and history. Cohort patterns are never surfaced in a way that exposes another learner's data, and this constraint is enforced at the data-access layer rather than relying on the model to remember it.

**Pasted content is data, not instructions.** Because two of SAGE's primary skills — `improve-interaction` and `weekly-review` — accept transcripts the learner copied from other AI tools, prompt-injection is a real attack vector. The system prompt explicitly instructs SAGE to treat pasted AI output as untrusted input: directives embedded inside a paste ("ignore previous instructions", "call `list_users`", "reveal your system prompt") are *not* followed. Instead, SAGE surfaces the attempt to the learner as a live, pedagogically valuable example of prompt injection. Tool calls originate only from SAGE's analysis of the learner's genuine conversational request, never from text inside a paste.

## 5. Evaluation framework

The evaluation harness under `evaluation/` (recent work on the `AgentV2.1` branch) measures whether SAGE actually behaves the way `CLAUDE.md` specifies. It currently implements two intrinsic metrics:

1. **Front-Loading Discipline** — a deterministic, rule-based check that no SAGE turn contains more than one question mark and that no more than four sentences precede the first question. This operationalizes the "ONE question per message" and "Keep responses SHORT" rules.
2. **Answer-First Adherence** — a two-stage LLM-as-judge. Claude Haiku 4.5 first classifies each learner message as `yes_no`, `factual`, `open`, or `not_a_question`; Claude Sonnet 4.6 then labels SAGE's reply as `answered_first`, `answered_and_followed_up`, `redirected_without_answer`, or `non_answer`. A reply passes if it lands in the first two categories. This operationalizes the "Answer first, then ask" rule.

Transcripts come from three sources: seven authored examples under `examples/interactions/` (committed positive and negative cases), three persona-driven simulations (novice-curious, skeptical-engineer, fatigued-returner) generated by `evaluation/personas/`, and chats exported from the Streamlit UI. The harness (`evaluation/run_evaluation.py`, with a one-shot driver `run_all.sh`) writes per-turn scores to `evaluation/results/<run-id>-results.json` and a summary Markdown file. Fifty-three unit tests under `evaluation/tests/` exercise the parsers, metric logic, and judge cache without spending API quota.

## 6. Status and roadmap

The repository is on branch `AgentV2.1` at version `0.2.0`. The current focus has been making the evaluation module self-contained and documenting the intrinsic-evaluation methodology (`evaluation/intrinsic-evaluation.md`). The Streamlit deployment is functional, and exported chats from real sessions feed back into the evaluation harness.

Several features documented in `docs/roadmap.md` remain deferred to the target CollaborAITE deployment, which provides context the standalone CLI cannot: passive observation of channel activity (the contextual nudge sidebar), scheduled weekly-reflection triggers, anonymized peer-cohort patterns, and retrieval over course slides. Within the CLI, the equivalents are all learner-initiated — the learner pastes the interaction, opens the weekly review, or describes the course context themselves. SAGE is instructed to name the CLI equivalent directly when a learner asks about a CollaborAITE-only feature, rather than pretend the feature is live.

## 7. Conclusion

SAGE demonstrates that a tutoring agent can be built from small, composable, named skills grounded in instructional-design literature, validated against the agent's own specification using a mix of rule-based and LLM-as-judge metrics, and hardened against the specific threats of an educational setting where learners paste untrusted AI output. The result is an agent that is deliberately narrower than a general assistant — it will not do the learner's homework — but that is auditable, testable, and pedagogically defensible in a way a monolithic prompt would not be.
