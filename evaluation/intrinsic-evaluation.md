# Intrinsic Evaluation — SAGE

This is our intrinsic evaluation of SAGE, the AI-use tutor. We define two metrics, implement them in `evaluation/`, and run them against three transcript sources: 7 authored examples, 3 persona-simulated sessions, and any chats exported from the deployed Streamlit app.

**Branch link:** https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor/tree/AgentV2.1

---

## Metric definitions

### Metric 1 — Front-Loading Discipline (rule-based)

Two sub-checks per SAGE turn.

**Question Discipline**

- *How it's computed:* count the `?` characters in the agent's turn. A turn passes when the count is ≤ 1.
- *What it hopes to reflect:* whether SAGE is stacking multiple questions in one turn instead of asking one focused question at a time. CLAUDE.md rule: "ONE question per message. Ask, wait, continue."

**Pre-Pause Length**

- *How it's computed:* count the sentences before the first `?`. If the turn has no `?`, count all sentences. Passes when the count is ≤ 4.
- *What it hopes to reflect:* whether SAGE front-loads content before inviting the learner in. CLAUDE.md rule: "Max 3-5 sentences before asking a question or pausing."

A turn passes Metric 1 when both sub-checks pass.

### Metric 2 — Answer-First Adherence (LLM-as-judge)

Two-stage judge applied only to SAGE turns whose immediately preceding learner turn is a direct question.

- *Stage 1 (classifier, Haiku 4.5):* labels the prior learner message as `yes_no`, `factual`, `open`, or `not_a_question`. Only `yes_no` and `factual` qualify for grading.
- *Stage 2 (grader, Sonnet 4.6):* labels SAGE's reply as `answered_first`, `answered_and_followed_up`, `redirected_without_answer`, or `non_answer`.
- *Pass condition:* `behavior in {answered_first, answered_and_followed_up}`.
- *What it hopes to reflect:* whether SAGE actually addresses the learner's question before redirecting. CLAUDE.md rule: "Answer first, then ask. If the learner asked something, answer it before adding your next question."

---

## Implementation

Full code lives under `evaluation/`. Key modules and the actual scoring logic:

### Metric 1 (`evaluation/metrics/front_loading.py`)

```python
import re
from evaluation.metrics.transcript import Transcript

_SENTENCE_END_RE = re.compile(r"[.!]")
_PRE_PAUSE_THRESHOLD = 4


def _count_sentences(text: str) -> int:
    return len(_SENTENCE_END_RE.findall(text))


def _score_turn(text: str) -> dict:
    qmarks = text.count("?")
    qd_passed = qmarks <= 1

    pre_pause_text = text[: text.index("?")] if "?" in text else text
    sentences = _count_sentences(pre_pause_text)
    pp_passed = sentences <= _PRE_PAUSE_THRESHOLD

    return {
        "question_discipline": {"question_marks": qmarks, "passed": qd_passed},
        "pre_pause": {"sentences": sentences, "passed": pp_passed},
        "passed": qd_passed and pp_passed,
    }


def score_front_loading(transcript: Transcript) -> list[dict]:
    """Score every SAGE turn in the transcript. Learner turns are skipped."""
    results = []
    for turn in transcript.turns:
        if turn.speaker != "sage":
            continue
        scored = _score_turn(turn.text)
        scored["turn_index"] = turn.index
        results.append(scored)
    return results
```

### Metric 2 (`evaluation/metrics/answer_first.py`)

The two judge prompts:

```python
CLASSIFIER_SYSTEM = """You classify whether a learner's message to a tutor is
a "direct question" that requires a substantive answer before any follow-up
coaching question.

Categories:
- "yes_no":   a question whose natural answer is yes/no
- "factual":  a question asking for a definition or explanation
- "open":     an open-ended invitation
- "not_a_question": statement, reaction, or compliance message.

Return ONLY a JSON object with keys "kind" and "reasoning"."""

GRADER_SYSTEM = """You grade whether a tutor answered a learner's direct
question before redirecting.

Categories for the tutor's reply:
- "answered_first":            tutor gave a substantive answer; may have stopped there.
- "answered_and_followed_up":  tutor answered substantively, THEN asked a coaching question.
- "redirected_without_answer": tutor responded with a question or new topic
                               without addressing the substance of the learner's question.
- "non_answer":                tutor produced text but it doesn't address the question.

Return ONLY a JSON object with keys "behavior" and "reasoning"."""

QUALIFYING_KINDS = {"yes_no", "factual"}
PASSING_BEHAVIORS = {"answered_first", "answered_and_followed_up"}
```

The orchestrator (one result per SAGE turn):

```python
def score_answer_first(transcript: Transcript, judge: JudgeProtocol) -> list[dict]:
    results = []
    turns = transcript.turns

    for i, turn in enumerate(turns):
        if turn.speaker != "sage":
            continue

        prior = turns[i - 1] if i > 0 else None
        if prior is None or prior.speaker != "learner":
            results.append({
                "turn_index": turn.index, "applicable": False,
                "kind": None, "behavior": None,
                "reasoning": "no prior learner turn", "passed": None,
            })
            continue

        classification = judge.classify(prior.text)
        kind = classification.get("kind")
        if kind not in QUALIFYING_KINDS:
            results.append({
                "turn_index": turn.index, "applicable": False, "kind": kind,
                "behavior": None,
                "reasoning": classification.get("reasoning", ""), "passed": None,
            })
            continue

        grading = judge.grade(prior.text, turn.text)
        behavior = grading.get("behavior")
        results.append({
            "turn_index": turn.index, "applicable": True, "kind": kind,
            "behavior": behavior,
            "reasoning": grading.get("reasoning", ""),
            "passed": behavior in PASSING_BEHAVIORS,
        })
    return results
```

The judge wraps the Anthropic SDK with a hash-keyed JSON cache so re-runs against unchanged transcripts cost zero tokens. Full code: `evaluation/metrics/judge.py`.

### Three transcript sources

Parsed by `evaluation/metrics/transcript.py`. The same `Transcript[Turn]` shape feeds both metrics regardless of source.

| Source | Path | Format |
|---|---|---|
| Authored | `examples/interactions/{positive,negative}/*.md` | `**LEARNER**:` / `**SAGE**:` markers (or named-learner: `**JAKE**:`, `**PRIYA**:`, `**CHEN**:`) |
| Simulated | `evaluation/fixtures/simulated/*.json` | Generated by `evaluation.personas.simulator` driving Claude Opus 4.7 (SAGE) against Claude Haiku 4.5 (persona learner) |
| Exported | `evaluation/fixtures/exports/*.{md,txt}` | Chats downloaded from the SAGE Streamlit app's "Export chat" button |

### End-to-end runner

```python
# evaluation/run_evaluation.py (excerpt)
transcripts = _load_authored() + _load_simulated() + _load_exported()
judge = AnthropicJudge(cache_path=JUDGE_CACHE_PATH) if not args.no_judge else None

scored = []
for t in transcripts:
    fl = score_front_loading(t)
    af = score_answer_first(t, judge=judge) if judge is not None else []
    scored.append(TranscriptScored(transcript=t, front_loading=fl, answer_first=af))

aggregates = _aggregate(scored)
# write Experiment Results/<run_id>-results.json + summary.md
```

---

## Running it

```bash
pip install -e ".[dev]"

# unit tests (no API spend)
pytest evaluation/tests -v

# rule-based scoring on authored transcripts (no API spend)
python -m evaluation.run_evaluation --no-judge

# full eval: persona simulation + both metrics on all sources
export ANTHROPIC_API_KEY="sk-ant-..."
./evaluation/run_all.sh

# score a single exported chat
mv ~/Downloads/sage-chat-*.md evaluation/fixtures/exports/
python -m evaluation.run_evaluation --exports-only
```

See `evaluation/README.md` for the five-case walkthrough.

---

## Results from a real run

Run `2026-05-05T14-11Z` (committed at `f6d6d76`). 10 transcripts evaluated: 7 authored + 3 persona-simulated.

### Overall pass rates

| Metric | Applicable turns | Passed | Pass rate |
|---|---|---|---|
| front_loading | 53 | 23 | 0.434 |
| answer_first | 13 | 9 | 0.692 |

### Pass rates by source label

| Label | Front-Loading | Answer-First |
|---|---|---|
| negative | 6/18 (0.333) | 2/2 (1.0) |
| positive | 8/16 (0.5) | 0/1 (0.0) |
| simulated | 9/19 (0.474) | 7/10 (0.7) |

### Reading the results

**Front-Loading discriminates positive vs negative** (0.5 vs 0.333) — the rule-based metric correctly flags the negative authored examples as more likely to violate the question/pre-pause discipline.

**Answer-First on authored looks inverted** (positive 0% vs negative 100%), but that's a small-sample artifact: only 1 positive applicable turn vs 2 negative. The classifier filtered out most learner messages because they weren't direct questions to SAGE — they were the learner *demonstrating a practice prompt* (e.g., "Find me 5 academic sources..."). On the simulated sessions where the learner personas ask real direct questions, SAGE passes 7/10 (70%).

**The simulated transcripts are the most useful test bed for Metric 2.** With more direct-question turns (13 applicable across 3 sessions), they let the judge actually exercise its grading logic.

### Three example interactions exercising the metrics

The assignment requires testing on at least 3 example interactions. Beyond the 7 authored transcripts already shipped under `examples/interactions/`, three live persona-driven sessions were generated by `evaluation/personas/simulator.py`:

1. **`novice-curious`** (8 SAGE turns, 5 applicable answer-first, 3 pass) — a first-year sociology student asking short yes/no questions like "Is it bad if I just paste my essay in?". Stress-tests Metric 2's `yes_no` branch.
2. **`skeptical-engineer`** (6 SAGE turns, 4 applicable answer-first, 3 pass) — opens with "What is a hallucination, technically? Don't sugarcoat it." Stress-tests Metric 2's `factual` branch and whether SAGE answers tersely.
3. **`fatigued-returner`** (5 SAGE turns, 1 applicable answer-first, 1 pass) — terse, asks to wrap up. Stress-tests SAGE's in-turn intent re-check rule (CLAUDE.md: "If the learner moves on, the skill does too").

Each session is reproducible by running `python -m evaluation.personas.simulator --persona <id>`. Saved artifacts live under `evaluation/fixtures/simulated/`.

---

## Saved artifacts

- Metric definitions and code: `evaluation/metrics/`
- Persona simulator + persona definitions: `evaluation/personas/`
- 53 unit tests covering parser, both metrics, judge cache, JSON extraction: `evaluation/tests/`
- Per-run JSON + markdown summaries: `Experiment Results/<run-id>-{results.json,summary.md}`
- Hash-keyed judge cache (free re-runs): `Experiment Results/.judge-cache.json`
- One-shot driver: `evaluation/run_all.sh`

Design rationale: `docs/superpowers/specs/2026-05-04-intrinsic-evaluation-design.md`
Implementation plan: `docs/superpowers/plans/2026-05-04-intrinsic-evaluation.md`
