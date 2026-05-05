# SAGE Intrinsic Evaluation

Two metrics that score SAGE against its own pedagogical contract.

## Metrics

### Metric 1 — Front-Loading Discipline (rule-based)
Per SAGE turn, two sub-checks:
- **Question Discipline** — count of `?` must be ≤ 1 (catches stacked questions in one turn).
- **Pre-Pause Length** — number of sentences before the first `?` must be ≤ 4 (catches walls of text before SAGE invites the learner in). If the turn has no `?`, the whole turn is measured.

A turn passes when both sub-checks pass.

### Metric 2 — Answer-First Adherence (LLM-as-judge)
Two-stage judge applied to SAGE turns whose immediately preceding learner turn is a direct question.
- **Stage 1 (Haiku 4.5):** classify the prior learner message — `yes_no`, `factual`, `open`, or `not_a_question`. Only `yes_no` and `factual` qualify for grading.
- **Stage 2 (Sonnet 4.6):** grade SAGE's reply — `answered_first`, `answered_and_followed_up`, `redirected_without_answer`, or `non_answer`.

A turn passes when behavior is `answered_first` or `answered_and_followed_up`.

> **Note on `answered_first`:** the metric only checks the *order* of answer vs. redirection, not whether SAGE asked a follow-up question. SAGE can pass by answering and stopping. CLAUDE.md's "answer, then deepen with a question" pattern is a stricter pedagogical norm; this metric is deliberately more permissive.

## Test data

The runner combines three sources, all turned into the same `Transcript` shape:

- **Authored** (7 transcripts): `examples/interactions/{positive,negative}/*.md` — 4 positive + 3 negative. Markers may be `**LEARNER**:` or named-learner like `**JAKE**:`, `**PRIYA**:`, `**CHEN**:`.
- **Simulated** (3 sessions): `evaluation/fixtures/simulated/*.json` — produced by `evaluation.personas.simulator`. Personas: `novice-curious` (yes/no questions), `skeptical-engineer` (factual questions), `fatigued-returner` (terse, asks to wrap up). Gitignored.
- **Exported** (any number): `evaluation/fixtures/exports/*.{md,txt}` — chats downloaded from the SAGE Streamlit app's "Export chat" button (see `sage/export.py`). The parser auto-detects markdown (`### You` / `### SAGE`) vs plain text (`You:` / `SAGE:`) format. Drop a file in, re-run the runner — it gets scored automatically. Gitignored by default since exports may contain real learner data.

### Scoring an exported chat

```bash
# In the Streamlit app: open the sidebar's "Export chat" panel, pick .md or .txt, click Download.
mv ~/Downloads/sage-chat-*.md evaluation/fixtures/exports/
python -m evaluation.run_evaluation
```

The new transcript shows up in the summary under the `exported` label alongside `authored` and `simulated`.

## Running it

```bash
# install dev deps once
pip install -e ".[dev]"

# run unit tests (no API tokens)
pytest evaluation/tests -v

# rule-based metric only (no API tokens)
python -m evaluation.run_evaluation --no-judge

# generate persona transcripts (spends API tokens)
export ANTHROPIC_API_KEY="<your-key>"
python -m evaluation.personas.simulator --all

# both metrics (uses cache after first run)
python -m evaluation.run_evaluation
```

## Output

- `evaluation/results/<run-id>-results.json` — raw per-turn scores with full judge reasoning
- `evaluation/results/<run-id>-summary.md` — human-readable aggregates + per-transcript breakdown + sanity check
- `evaluation/results/.judge-cache.json` — gitignored hash-keyed judge cache (re-runs against unchanged transcripts cost zero tokens)

## Architecture

```
evaluation/
  metrics/
    transcript.py      # authored markdown + simulated JSON + exported-chat parser
    front_loading.py   # Metric 1 (rule-based)
    judge.py           # Anthropic SDK wrapper + cache + balanced JSON extractor
    answer_first.py    # Metric 2 (two-stage LLM-as-judge)
  personas/
    personas.json      # 3 persona definitions
    simulator.py       # persona-LLM ↔ SAGE conversation driver
  tests/               # 53 unit tests
  fixtures/simulated/  # simulator output (gitignored)
  fixtures/exports/    # drop-zone for chats exported from the Streamlit app (gitignored)
  results/             # dated runs (gitignored except .gitkeep)
  run_evaluation.py    # entry point — loads transcripts, runs metrics, writes results
```

## Design

See `docs/superpowers/specs/2026-05-04-intrinsic-evaluation-design.md` for the full design rationale and `docs/superpowers/plans/2026-05-04-intrinsic-evaluation.md` for the implementation plan.
