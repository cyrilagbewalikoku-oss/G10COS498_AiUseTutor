# Intrinsic Evaluation — Design Spec

**Date:** 2026-05-04
**Author:** AgentV2.1 branch work
**Source assignment:** `evaluation/intrinsic-evaluation.md`

## Goal

Build a small, repeatable benchmark suite that scores SAGE's adherence to its own pedagogical contract. Two metrics, the first rule-based, the second LLM-as-judge. Run against existing authored transcripts plus three persona-simulated live sessions, then save dated results.

## Non-goals

- Measuring learner learning outcomes (impossible without longitudinal data).
- Replacing the rubrics in `data/rubrics/` (those grade the *learner*; these grade *SAGE*).
- General-purpose evaluation framework. This is one assignment, one branch.

## Metrics

### Metric 1 — Front-Loading Discipline (rule-based)

Two sub-checks, applied per SAGE turn.

**1a. Question Discipline.** `passed = turn.text.count("?") <= 1`. Catches stacked questions in a single turn ("What did you mean? And why did that surprise you?"). Per the assignment, raw `?` count — no semantic disambiguation.

**1b. Pre-Pause Length.** Sentence count up to the first `?`. If the turn has no `?`, count all sentences. `passed = sentences <= 4`. Catches walls of text before SAGE invites the learner in. Sentence splitter: `re.split(r'(?<=[.!?])\s+', text.strip())`, drop empty strings. Known limitation: mis-splits on abbreviations like "Dr." — accepted for rule-based simplicity.

**Combined turn pass:** both sub-checks pass. Per-sub-check booleans preserved in the JSON output.

### Metric 2 — Answer-First Adherence (LLM-as-judge)

Two-stage judge, scored only on SAGE turns where the immediately preceding learner turn qualifies as a direct question.

**Stage 1 — Classifier (Haiku 4.5).** Given the prior learner message, returns `{kind: "yes_no" | "factual" | "open" | "not_a_question", reasoning: str}`. Qualifying kinds: `yes_no` and `factual`.

**Interpretation note:** the assignment text says "Requiring a yes/no". CLAUDE.md treats "answer first" as applying to any direct question, including `"what is X?"` and `"how does X work?"`. We default to the broader interpretation and expose `kind` in the output so a strict-yes/no aggregate can be derived without rerunning.

**Stage 2 — Grader (Sonnet 4.6, only on qualifying turns).** Given the learner question and SAGE's reply, returns `{behavior, reasoning}` where `behavior` is one of:
- `answered_first` — substantive answer, may stop there.
- `answered_and_followed_up` — substantive answer, then a coaching question.
- `redirected_without_answer` — responded with a question/new topic without addressing substance.
- `non_answer` — text doesn't address the question (evasive, off-topic, or restatement).

**Pass condition:** `behavior in {answered_first, answered_and_followed_up}`.

**Cost control:** `max_tokens=300` per call. JSON cache at `results/.judge-cache.json` keyed by `sha256(model | prompt_template_version | learner_message | sage_message)` — re-runs after metric-prompt edits invalidate automatically because the template version changes; re-runs against unchanged transcripts cost zero API calls.

## Architecture

```
evaluation/
  intrinsic-evaluation.md          # assignment doc (exists)
  README.md                        # how to run
  metrics/
    __init__.py
    transcript.py                  # markdown -> Transcript[Turn]
    front_loading.py               # Metric 1
    answer_first.py                # Metric 2
    judge.py                       # Anthropic client + JSON-output helper
  personas/
    __init__.py
    personas.json                  # 3 persona definitions
    simulator.py                   # persona-LLM <-> SAGE conversation driver
  fixtures/
    transcripts/                   # 6 transcripts copied from examples/interactions/
    simulated/                     # outputs of the simulator
  run_evaluation.py                # CLI entry
  results/
    YYYY-MM-DD-results.json
    YYYY-MM-DD-summary.md
    .judge-cache.json              # gitignored
```

### Boundaries

- Each metric module takes `Transcript` (or a `Turn` + adjacent context) and returns `MetricResult` dicts. Metrics never call each other.
- `transcript.py` is the only parser of the markdown shape.
- `judge.py` is the only thing that talks to the Anthropic SDK from the metrics.
- Personas produce transcripts; metrics consume transcripts. No coupling.

### Data shapes

```python
@dataclass
class Turn:
    index: int
    speaker: Literal["learner", "sage"]
    text: str

@dataclass
class Transcript:
    source_id: str           # e.g. "positive/01-novice-learns-prompting"
    origin: Literal["authored", "simulated"]
    turns: list[Turn]
```

`MetricResult` for a turn (denormalized in the JSON output):
```json
{
  "turn_index": 1,
  "speaker": "sage",
  "front_loading": {
    "question_discipline": {"question_marks": 1, "passed": true},
    "pre_pause": {"sentences": 3, "passed": true},
    "passed": true
  },
  "answer_first": {
    "applicable": true,
    "kind": "yes_no",
    "behavior": "answered_and_followed_up",
    "reasoning": "...",
    "passed": true
  }
}
```

`answer_first` is `null` when the prior learner turn doesn't qualify as a direct question.

### Markdown parser rules

- Split on lines matching `^\*\*(LEARNER|SAGE)\*\*:` (case-sensitive).
- Body of a turn is everything after the marker up to the next marker or `---`.
- Discard the meta sections after `---` (e.g., the "Why This Interaction Is Beneficial" prose in the positive examples).
- Whitespace-trim each turn body.

## Persona simulator

Three persona profiles in `personas/personas.json`:

1. **novice-curious** — first-year sociology student, asks short yes/no questions. Exercises Metric 2's yes/no branch.
2. **skeptical-engineer** — senior engineer, asks pointed factual questions ("What is a hallucination, technically?"). Exercises Metric 2's factual branch and tests whether SAGE answers tersely.
3. **fatigued-returner** — short on time, terse replies, sometimes asks to wrap up. Triggers the in-turn intent re-check rules in CLAUDE.md and tests whether SAGE keeps front-loading or gracefully closes (exercises Metric 1).

Loop: persona-LLM (Haiku 4.5) and SAGE (Opus 4.7, the deployed config) alternate. SAGE's system prompt is imported from `sage.prompts` so the simulator tests the deployed prompt, not a paraphrase. Stop condition: persona emits a wrap-up phrase or hits `max_turns`. Transcript saved to `fixtures/simulated/<persona_id>-<timestamp>.json`.

## Results format

**`results/<date>-results.json`:**
```json
{
  "run_id": "2026-05-04T14-22Z",
  "sage_version": "<git-rev-parse-HEAD>",
  "transcripts": [
    {
      "source_id": "...",
      "origin": "authored" | "simulated",
      "turn_results": [ ...MetricResult... ]
    }
  ]
}
```

**`results/<date>-summary.md`:** aggregate pass-rates per metric, per-transcript breakdown table (positive vs negative authored, plus simulated), commentary section noting which transcripts the metrics correctly flagged, judge-disagreement spot-checks, and edge cases the rule-based metric missed.

## Test plan

- **Sanity check:** the 3 negative authored examples must fail Metric 1 or Metric 2 noticeably more often than the 3 positive ones. Asserted as a printed line in the summary, not a unit test — if it fails, the metric needs rework, not the harness.
- **Parser regression test (`tests/test_transcript.py`):** parse one authored markdown file, assert turn count and alternating speakers.
- **Judge cache test:** run Metric 2 twice on the same transcript, assert the second run makes zero Anthropic calls.

## What this design does not do

- No scoring threshold for "SAGE passes overall." Each turn is pass/fail per metric; aggregates are reported but no global gate.
- No automatic regression on every commit. The runner is a manual script. CI integration is out of scope.
- No web UI for browsing results. Markdown summary is the report surface.

## Cost estimate

With ~50 SAGE turns across 9 transcripts and Metric 2's filtering: ≤ 50 Haiku classifier calls + ≤ 15 Sonnet grader calls per evaluation run. With caching, repeat runs after metric tweaks cost only the new turns. Persona simulation: 3 conversations × ~6 turns × 2 calls/turn ≈ 36 calls (mix of Opus and Haiku). Total per fresh run: well under $1.

## Open questions

- Do we want a strict `yes_no`-only aggregate alongside the broader `yes_no + factual` aggregate in the summary? (Easy add — both views from the same data.)
- Do we want to seed the persona LLM with deterministic prompts for replayability, or accept run-to-run variation? Default plan: accept variation, save each run's transcript with timestamp so old runs remain re-scoreable.
