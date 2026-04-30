# Intrinsic Evaluation — Design Plan

## Context

Step 3 of the SAGE evaluation assignment requires defining 1–3 intrinsic metrics, implementing them, and scoring at least 3 example interactions with the agent. This plan defines **what we evaluate and how we generate the inputs** — file layout, branch strategy, and CHANGELOG/CI updates are deferred to the implementation phase.

The team has already chosen two metrics. We are also opting for the assignment's stretch path (Co-Gym-style simulated LLM personas) so the eval is reproducible and stresses different parts of the agent rather than relying on hand-curated examples.

The two metrics test **stated rules in `CLAUDE.md`**, which keeps the rubric anchored in real design intent rather than abstract notions of "good output."

---

## Metric 1 — Front-loading discipline (code-based)

**What it tests** — two rules in `CLAUDE.md`, in combination:
> "Keep responses SHORT. Max 3-5 sentences **before asking a question or pausing for input**."
> "ONE question per message. Ask, wait, continue."

**Why this framing instead of plain sentence count:** the literal rule is about *not front-loading before pausing*, not about total length. A response with "long answer → question → more elaboration" passes a naive sentence-count metric while still violating the rule. We measure pre-pause length specifically, and pair it with the one-question rule so a 3-sentence response with 4 questions doesn't slip through.

**Scope** — every SAGE turn in every transcript.

**Computation (deterministic, no LLM):**

Two sub-checks per SAGE turn, both code-based:

| Sub-check | What it counts | Pass condition |
|---|---|---|
| **A. Pre-pause length** | Sentences from start of SAGE's message up to the first `?` (or end of turn if no `?`) | ≤ 5 |
| **B. Question discipline** | Number of `?` in the turn | Exactly 1 |

Sentence-counting heuristic (applied within sub-check A):
1. Strip fenced code blocks (` ``` ... ``` `) and markdown tables before counting.
2. Treat each top-level bullet/list item as one sentence.
3. Treat markdown headers as 0 sentences.
4. Split the remaining prose on `[.!?]` followed by whitespace or end-of-string.

**Per-turn scoring:** `pass` only if **both** sub-checks pass.
**Per-transcript scoring:** pass-rate across SAGE turns.
**Overall scoring:** mean of per-transcript pass-rates.

**Gradient reporting (alongside pass-rate):** mean pre-pause sentence count, max pre-pause sentence count, question-count distribution per transcript. Lets the writeup say "median was 3.2 sentences before pausing; one outlier at 9" rather than just "85% pass."

**Edge cases — documented, not solved:** rhetorical `?` (e.g. "really?") gets counted as a question; inline `e.g.` may inflate sentence counts; nested lists only count top-level items. We document the heuristic and accept the noise — this is a coarse signal, not a precise one.

---

## Metric 2 — Answer-first adherence (LLM-as-judge)

**What it tests** — the rule in `CLAUDE.md`:
> "Answer first, then ask. If the learner asked something, answer it before adding your next question."

The original metric name "task completeness" was awkward for a tutor (SAGE has no per-turn task to complete in the task-agent sense). We rename it to describe what we're actually testing: when the learner asks a direct question, did SAGE answer it *before* nudging? This is the literal failure mode `CLAUDE.md` warns against.

**Scope — only SAGE turns that immediately follow a learner direct question.**

### Direct-question detection — judge-based, not regex

Regex detection is too fragile (a learner can ask without `?` — "tell me what hallucinations are"; `?` shows up in non-questions — "really?"). We move detection to the judge:

1. **Pre-call (per turn):** judge sees the learner's previous message and answers `yes`/`no` to *"Is this a direct question seeking factual information or explanation, as opposed to a conversational response or chitchat?"*
2. Only `yes` turns proceed to the scoring step. `no` turns are excluded from the metric.

This costs one extra cheap call per turn but eliminates both regex false-positive directions.

### Scoring — `judges` library

- **Judge model:** Claude Opus 4.7 (stronger than the agent under test, which runs Opus 4.6 — mitigates judge-self-preference bias).
- **Inputs to judge:** the learner's direct-question message, the previous SAGE turn (for context), and the SAGE response being scored.
- **Output:** integer score 1–5 + 1-sentence justification.

**Rubric (ordinal anchors):**

| Score | Meaning |
|-------|---------|
| **1** | SAGE deflected — answered with a nudge/question instead of the learner's question. (The failure mode `CLAUDE.md` warns about explicitly.) |
| **2** | SAGE eventually answered, but only after another back-and-forth or behind heavy caveats. |
| **3** | Partial answer present, but obscured by caveats or buried after the next question. |
| **4** | Clear answer, but the follow-up question came too tightly coupled or before the answer landed. |
| **5** | Clear, accurate answer first; optional follow-up question after. |

### Calibration: anchor with worked examples

The rubric prompt for the judge includes **two worked examples** drawn from `examples/interactions/`:

- One scored **1** — a deflection (SAGE asks a nudge instead of answering).
- One scored **5** — a clean answer-first response.

Each example shows the learner question, the SAGE response, and a one-sentence rationale tied to the rubric. This is the single biggest reliability win in LLM-as-judge per the HF cookbook (combats scale-compression toward the middle).

### Reliability check: two-shot judging

Each scored turn is judged **twice**:
- **Pass A:** judge sees the prior SAGE turn for full context.
- **Pass B:** judge sees only the learner question + SAGE's response under test (no prior context).

**Aggregation rule:**
- If `|score_A − score_B| ≤ 1`: take the mean.
- If `|score_A − score_B| > 1`: flag the turn as `judge-uncertain` and report both scores in results without averaging — these get called out in the writeup as cases where the rubric needs sharpening.

**Per-transcript scoring:** mean of judge scores across direct-question turns (judge-uncertain turns excluded from the mean but reported separately).
**Overall scoring:** mean of per-transcript means + overall judge-uncertain rate.

---

## Three simulated LLM personas (Co-Gym-style)

Each persona is its own Anthropic SDK call given a system prompt that defines its character, goal, and stop condition. The persona converses with SAGE (also an Anthropic call) for up to **8 turns** or until the persona signals "done." We log the full transcript.

| # | Persona | What it stresses |
|---|---------|------------------|
| **1** | **Curious novice** — never used AI agents; asks several "what is X?", "how do I", "is X the same as Y" questions in plain language. | Metric 2 surface (lots of direct-question turns to score); register-matching to a beginner. |
| **2** | **Skeptical practitioner** — has used ChatGPT, pushes back on SAGE's framing, asks meta-questions ("why are you asking me that?"), uses jargon. | Metric 1 (does SAGE stay brief under intellectual pressure?); also tests whether SAGE over-explains or front-loads when challenged. |
| **3** | **Ethics-curious learner** — brings a real dilemma ("is it okay to use AI to draft an apology to my friend?"); mixes one direct question and one scenario. | Both metrics together; also exercises the ethical-guidance pathway. |

**Persona system-prompt skeleton:**
```
You are simulating a {persona_name} interacting with an AI tutor named SAGE.
Your goal: {persona_goal}. Stay in character.
Style: {style_notes — e.g., "short messages, plain language, no jargon"}.
Do not reveal you are an AI persona.
Stop when {stop_condition — e.g., "you've gotten an answer to your main question and SAGE has asked one closing reflection"}.
Send one message at a time, then wait.
```

---

## Conversation simulation mechanics

1. **Driver loop** runs three independent simulations (one per persona):
   - Initialize empty message history for the SAGE side and an empty history for the persona side.
   - Persona speaks first (its opening message).
   - Loop: SAGE responds → append to both histories → persona responds → append → repeat.
   - Stop when persona emits an end-of-conversation signal (configurable token in its system prompt) or 8 turns reached.
2. **Same `claude-opus-4-6` model and full SAGE system prompt** are used for the SAGE side — eval the *real* agent, not a stripped-down version.
3. **Persona side** uses Claude Opus 4.7 (separate call, different system prompt) so persona stays consistent without bleeding SAGE's instructions.
4. **Transcripts** are saved as `{persona}.jsonl` — one JSON object per message (`{role, content, turn_index}`).

---

## Judging procedure

1. Run all 3 simulated conversations → save transcripts.
2. For each transcript:
   - **Metric 1 (code, no LLM):** per-turn pre-pause sentence count + question count → pass/fail per sub-check, combined per turn, aggregated to transcript.
   - **Metric 2 detection pass:** for each SAGE turn, ask the judge whether the *previous* learner message was a direct question (yes/no). Skip `no` turns.
   - **Metric 2 scoring pass:** for each `yes` turn, run the judge twice (with and without prior SAGE turn as context) using the worked-example-anchored rubric. Aggregate per the `≤1` / `>1` disagreement rule.
3. Aggregate to per-transcript and overall scores.
4. Save results in two formats: `results.json` (machine-readable, for any downstream analysis) and `results.md` (human-readable summary for the writeup, including any flagged judge-uncertain turns).

---

## Results format (sketch)

```json
{
  "run_date": "2026-04-29",
  "agent_model": "claude-opus-4-6",
  "judge_model": "claude-opus-4-7",
  "transcripts": [
    {
      "persona": "curious_novice",
      "turns": 8,
      "metric_1_front_loading": {
        "combined_pass_rate": 0.75,
        "sub_check_a_pre_pause_pass_rate": 0.875,
        "sub_check_b_question_count_pass_rate": 0.875,
        "mean_pre_pause_sentences": 3.2,
        "max_pre_pause_sentences": 6,
        "question_counts_per_turn": [1, 1, 1, 2, 1, 0, 1, 1]
      },
      "metric_2_answer_first": {
        "scored_turns": 4,
        "judge_uncertain_turns": 1,
        "mean_score": 4.33,
        "scores": [
          {"turn_index": 1, "score_a": 5, "score_b": 5, "aggregated": 5, "justification_a": "...", "justification_b": "..."},
          {"turn_index": 3, "score_a": 4, "score_b": 2, "aggregated": "uncertain", "justification_a": "...", "justification_b": "..."}
        ]
      }
    }
  ],
  "overall": {
    "metric_1_combined_pass_rate": 0.78,
    "metric_2_mean_score": 4.1,
    "metric_2_judge_uncertain_rate": 0.15
  }
}
```

---

## Critical files & utilities to reuse

- **`sage/export.py`** — already produces `(role, content)`-style transcripts; the simulator's logger should match this shape so transcripts are interoperable with the existing tooling.
- **`sage/agent.py:run`** — current CLI entry point; the simulator wraps the same Anthropic call pattern (full SAGE system prompt, same model, same tools) rather than reinventing it. **Do not bypass tools** — if SAGE invokes a tool mid-turn, the simulator must run it just like the live agent does, or the eval is testing a different agent than the one we ship.
- **`sage/prompts.py` + `.claude/skills/`** — the loaded SAGE system prompt. The eval should pull from the same source the live agent uses.
- **`examples/interactions/` (positive/negative)** — reference for what a "good" SAGE conversation looks like; useful as eyeball calibration for the rubric, not as eval inputs.

---

## Verification plan

- **Sanity-check Metric 1 (sub-check A):** hand-count pre-pause sentences for one SAGE turn and compare to the code's count. Disagreement >1 means the heuristic needs adjustment.
- **Sanity-check Metric 1 (sub-check B):** spot-check one rhetorical-`?` case to confirm we're treating it as a question (we are, by design — it's a noise we accept).
- **Sanity-check Metric 2 detection pass:** read each turn the judge tagged `no` (not a direct question). If any are obvious direct questions, the detection prompt needs tightening.
- **Sanity-check Metric 2 scoring pass:** for one `yes` turn, manually score it 1–5 and compare to both judge passes. Disagreement >1 with the human means the rubric is under-anchored — tighten the wording or add a third worked example.
- **Sanity-check personas:** read each transcript end-to-end. If the persona breaks character, mentions being an AI, or the conversation feels mechanical, flag for the writeup and re-run with a tightened persona prompt.
- **Reproducibility check:** re-run the full eval; Metric 1 must be identical (fully deterministic), Metric 2 mean per transcript should be within ±0.5 (LLM noise) and the judge-uncertain set should be largely the same turns each time. Persistent uncertainty on the same turns is real ambiguity, not noise — discuss in writeup.

---

## What this plan deliberately does NOT cover

- **File layout / branch strategy.** Deferred to implementation. (Likely `evaluation/` at repo root + new branch off `AgentV2.1`, but not committing yet.)
- **Adding `judges` to `pyproject.toml`.** Deferred.
- **CHANGELOG entry.** Will be appended when implementation lands, per the standing rule.
- **CI integration.** Out of scope for this assignment.
- **Extrinsic evaluation.** Separate step; this plan is intrinsic only.
