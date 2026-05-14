# SAGE Intrinsic Evaluation

Two metrics that score SAGE against its own pedagogical contract:

- **Front-Loading Discipline** (rule-based): does SAGE keep responses short and ask one question at a time?
- **Answer-First Adherence** (LLM-as-judge): when the learner asks SAGE a direct question, does SAGE answer before redirecting?

Three transcript sources feed the metrics: 7 authored examples, 3 persona-simulated sessions, and any chats you export from the deployed Streamlit app.

---

## One-time setup

```bash
# from the repo root
python3 -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

Activate the venv (`source venv/bin/activate`) at the start of every new terminal session.

---

## Running an evaluation — five cases

Pick the case that matches what you want to do. Cases 1–3 spend no API tokens; cases 4–5 do.

### Case 1 — Verify the harness (unit tests, no API spend)

**When:** You just cloned, or you want to confirm nothing's broken before running anything else.

```bash
pytest evaluation/tests -v
```

Expected: **53 tests pass** in <1 second. Covers parser, both metrics, judge cache, JSON extraction.

---

### Case 2 — Rule-based scoring on authored transcripts (no API spend)

**When:** You want to see Metric 1 (Front-Loading) discriminate the 7 authored transcripts. Sanity-check the harness without spending tokens.

```bash
python -m evaluation.run_evaluation --no-judge
```

Produces a dated `<run-id>-results.json` and `<run-id>-summary.md` in `Experiment Results/`. The summary shows positive vs negative front-loading pass rates (expect roughly 50% vs 33%).

---

### Case 3 — Score a chat you exported from the SAGE app

**When:** You ran a real SAGE conversation in the Streamlit app and want to grade *just that conversation*.

#### Step 1 — Get the export

In the SAGE Streamlit app:

1. Open the left sidebar.
2. Scroll to the **Export chat** panel (above the chat input box).
3. Pick **`.md`** (recommended — preserves formatting) or **`.txt`**.
4. Click **Download**. The file lands in your Downloads folder, named `sage-chat-<your-name>-<timestamp>.md`.

#### Step 2 — Drop it into the exports folder

```bash
mv ~/Downloads/sage-chat-*.md evaluation/fixtures/exports/
```

You can drop in as many exports as you like — they're all picked up automatically. Files are gitignored by default since real chats may contain personal data.

#### Step 3 — Run the evaluation

**Just your chat (no API spend, fastest):**

```bash
python -m evaluation.run_evaluation --exports-only --no-judge
```

**Just your chat with the LLM judge (spends ~$0.05):**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python -m evaluation.run_evaluation --exports-only
```

**Your chat *plus* the authored examples and any simulated sessions** (so you can compare against baseline corpora):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # only needed without --no-judge
python -m evaluation.run_evaluation
```

#### Step 4 — Read the summary

The runner prints two paths. Open the `*-summary.md` one:

```bash
ls -t Experiment Results/*-summary.md | head -n 1 | xargs cat
```

In `--exports-only` mode you'll see something like:

```
# Intrinsic Evaluation Results — 2026-05-05T15-36Z

- **SAGE version:** `ad6e0e8...`
- **Transcripts evaluated:** 1

## Overall pass rates
| Metric         | Applicable turns | Passed | Pass rate |
|---             |---               |---     |---        |
| front_loading  | 12               | 9      | 0.75      |
| answer_first   | 3                | 2      | 0.667     |

## Per-transcript breakdown
- **exported/sage-chat-elvis-2026-05-05-1422** (exported, 12 SAGE turns): front-loading 9/12, answer-first 2/3
```

The full per-turn details — including the LLM judge's reasoning for each Metric 2 turn — live in the matching `*-results.json` file.

#### Tips

- **Multiple chats at once:** drop several files; each appears as its own row in the per-transcript breakdown.
- **Iterating on a single chat:** delete the old file before dropping the new one, or keep both — timestamps in the filenames disambiguate.
- **Cleanup:** when you're done, `rm evaluation/fixtures/exports/*.md evaluation/fixtures/exports/*.txt` clears the drop-zone.

---

### Case 4 — Generate fresh persona-simulated SAGE conversations (spends API tokens)

**When:** You want new transcripts where Claude (running as SAGE) is driven by simulated learner personas. Useful for stress-testing the metrics on realistic dialogue.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python -m evaluation.personas.simulator --all     # all 3 personas
# or
python -m evaluation.personas.simulator --persona novice-curious   # one at a time
```

Writes timestamped JSON files to `evaluation/fixtures/simulated/`. Each persona produces ~6–11 turns. Cost: well under $0.10 per persona. Personas defined in `evaluation/personas/personas.json`:

- `novice-curious` — first-year student, short yes/no questions
- `skeptical-engineer` — pointed factual questions, low patience
- `fatigued-returner` — terse, asks to wrap up

To re-score after generating new simulated transcripts, run Case 2 or Case 5.

---

### Case 5 — Full evaluation: both metrics, all sources (spends API tokens)

**When:** You want the canonical assignment-submission run.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
./evaluation/run_all.sh
```

`run_all.sh` does five things in order:

1. Sanity checks (API key set, anthropic SDK importable)
2. Runs the 53 unit tests
3. Generates 3 fresh persona-simulated transcripts
4. Runs both metrics over all available transcripts (authored + simulated + any exports you've dropped in)
5. Prints the summary and shows the exact `git add -f` command to commit the canonical run

If you want the steps separately:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
pytest evaluation/tests -q                              # 1
python -m evaluation.personas.simulator --all           # 3
python -m evaluation.run_evaluation                     # 4
```

The judge cache lives at `Experiment Results/.judge-cache.json` — re-runs against unchanged transcripts cost zero tokens.

---

## What an evaluation produces

Two files per run, dated by UTC timestamp:

| File | Contents |
|---|---|
| `Experiment Results/<run-id>-results.json` | Raw per-turn scores, including full judge reasoning for every applicable Metric 2 turn |
| `Experiment Results/<run-id>-summary.md` | Markdown summary: overall pass rates, by-label table, per-transcript breakdown, sanity-check paragraph |

Side artifacts:

- `Experiment Results/.judge-cache.json` — hash-keyed cache (gitignored)
- `evaluation/fixtures/simulated/*.json` — simulator outputs (gitignored)
- `evaluation/fixtures/exports/*.{md,txt}` — chats you dropped in (gitignored)

---

## Metrics, in detail

### Metric 1 — Front-Loading Discipline (rule-based)

Per SAGE turn, two sub-checks:

- **Question Discipline** — count of `?` characters must be ≤ 1. Catches stacked questions like `"What did you mean? And why?"`.
- **Pre-Pause Length** — sentences before the first `?` (or whole turn if no `?`) must be ≤ 4. Catches walls of text before SAGE invites the learner in.

A turn passes when both sub-checks pass.

### Metric 2 — Answer-First Adherence (LLM-as-judge)

Two-stage judge, applied only to SAGE turns whose immediately preceding learner turn is a direct question.

- **Stage 1 — Classifier (Haiku 4.5):** labels the prior learner message as `yes_no`, `factual`, `open`, or `not_a_question`. Only `yes_no` and `factual` qualify for grading.
- **Stage 2 — Grader (Sonnet 4.6):** labels SAGE's reply as `answered_first`, `answered_and_followed_up`, `redirected_without_answer`, or `non_answer`.

A turn passes when behavior is `answered_first` or `answered_and_followed_up`.

> **Note on `answered_first`:** the metric only checks the *order* of answer vs. redirection, not whether SAGE asked a follow-up question. SAGE can pass by answering and stopping. CLAUDE.md's "answer, then deepen with a question" pattern is a stricter pedagogical norm; this metric is deliberately more permissive.

---

## Transcript sources

The runner combines three sources, all turned into the same `Transcript` shape:

| Source | Path | Format | Origin tag | Committed? |
|---|---|---|---|---|
| Authored | `examples/interactions/{positive,negative}/*.md` | `**LEARNER**:` / `**SAGE**:` markers (or named-learner: `**JAKE**:`, `**PRIYA**:`, `**CHEN**:`) | `authored` | yes |
| Simulated | `evaluation/fixtures/simulated/*.json` | Canonical `{source_id, origin, turns}` JSON | `simulated` | no |
| Exported | `evaluation/fixtures/exports/*.{md,txt}` | `### You` / `### SAGE` (markdown) or `You:` / `SAGE:` (text) — auto-detected | `exported` | no |

---

## Architecture

```
evaluation/
  metrics/
    transcript.py        # authored markdown + simulated JSON + exported-chat parser
    front_loading.py     # Metric 1 (rule-based)
    judge.py             # Anthropic SDK wrapper + cache + balanced JSON extractor
    answer_first.py      # Metric 2 (two-stage LLM-as-judge)
  personas/
    personas.json        # 3 persona definitions
    simulator.py         # persona-LLM ↔ SAGE conversation driver
  tests/                 # 53 unit tests
  fixtures/simulated/    # simulator output (gitignored)
  fixtures/exports/      # drop-zone for exported chats (gitignored)
  results/               # dated runs (gitignored except .gitkeep)
  run_evaluation.py      # entry point — loads transcripts, runs metrics, writes results
  run_all.sh             # one-shot: sanity + tests + simulator + full eval
```

---

## Troubleshooting

- **`ANTHROPIC_API_KEY not set`** — export it (`export ANTHROPIC_API_KEY=sk-ant-...`) or add `--no-judge` to skip Metric 2.
- **`No transcripts found`** — `examples/interactions/` is missing. Either you're not in the repo root or the assignment's seed transcripts have been removed.
- **`Cannot import sage.prompts`** — run `pip install -e .` from the repo root so SAGE's package is importable.
- **A bad simulated JSON aborted my run** — fixed in `0eda5d9`: malformed files are now skipped with a warning rather than crashing the run.
- **My exported chat shows zero turns in the summary** — the file got skipped because no markers were detected. Make sure it's the actual download from the app's Export panel, not e.g. a screenshot or copy-paste of the rendered chat.

---

## Reusing this harness for a different agent

The `evaluation/` directory is **self-contained** — no module-level imports from `sage.*`, no hardcoded paths to project-specific corpora at the boundaries. To evaluate a different Anthropic-based agent:

1. **Provide the agent's system prompt** to the simulator via either:
   ```bash
   python -m evaluation.personas.simulator --all --sage-prompt my-agent.txt
   # or
   export SAGE_SYSTEM_PROMPT_FILE=my-agent.txt
   python -m evaluation.personas.simulator --all
   ```
   If `sage.prompts.SYSTEM_PROMPT` is importable, it's used as a fallback when neither override is set.

2. **Point at your authored corpus** (optional) via:
   ```bash
   python -m evaluation.run_evaluation --authored-dir path/to/transcripts
   ```
   The directory must contain `positive/*.md` and `negative/*.md` subdirectories using `**LEARNER**:` / `**SAGE**:` markers (or any consistent named markers — the parser auto-detects). Default points at this project's `examples/interactions/`.

3. **The metric definitions and judge prompts** in `evaluation/metrics/` are agent-agnostic — they grade any conversation that follows the SAGE-style learner/agent turn structure.

The only project-specific dependency that remains is the persona system prompts in `evaluation/personas/personas.json`, which are general enough to drive most coaching agents but can be edited freely.

## Design

- Spec: `docs/superpowers/specs/2026-05-04-intrinsic-evaluation-design.md`
- Implementation plan: `docs/superpowers/plans/2026-05-04-intrinsic-evaluation.md`
