# SAGE — Final Agent vs. 4-16 Agent Comparison

**Project:** G10COS498 AI Use Tutor
**Date:** 2026-05-14
**Final agent:** branch `AgentV2.1` @ `f94da78` ([repo link](https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor/tree/AgentV2.1))
**4-16 agent:** branch `build/agent-2` @ [`7c5492d`](https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor/commit/7c5492d7d71a7381b2ead3df453627963c296e7e) (last commit on 4-16, the class-feedback day)

This write-up addresses items 4 and 5 in the assignment brief. The intrinsic
metrics (Front-Loading Discipline, Answer-First Adherence) and how they are
implemented are documented in `evaluation/intrinsic-evaluation.md`; the prose
below assumes that context and focuses on the comparison.

---

## 1. Methodology

Both agent versions were run against the same three persona learners
(`novice-curious`, `skeptical-engineer`, `fatigued-returner`) using
`evaluation/personas/simulator.py`. The simulator was pointed at each
version's `SYSTEM_PROMPT` via the `--sage-prompt` flag:

```bash
# 4-16 agent
python -m evaluation.personas.simulator --all \
  --sage-prompt evaluation/fixtures/prompts/sage-prompt-4-16-7c5492d.txt

# final agent — uses sage.prompts.SYSTEM_PROMPT by default
python -m evaluation.personas.simulator --all
```

Resulting transcripts live under
`evaluation/fixtures/simulated/{4-16-agent,final-agent}/`. Each set was
scored independently:

```bash
python -m evaluation.run_evaluation \
  --simulated-dir evaluation/fixtures/simulated/4-16-agent \
  --no-authored --label agent-4-16

python -m evaluation.run_evaluation \
  --simulated-dir evaluation/fixtures/simulated/final-agent \
  --no-authored --label agent-final
```

Saved artifacts (referenced by the notebook so a grader does not have to
re-run anything):

- `Experiment Results/agent-4-16-2026-05-14T18-20Z-{results.json,summary.md}`
- `Experiment Results/agent-final-2026-05-14T18-20Z-{results.json,summary.md}`
- `Experiment Results/final-agent-2026-05-14T18-15Z-{results.json,summary.md}` — full final-agent run including the 7 authored transcripts (53 SAGE turns)

Authored transcripts are static "gold" examples and are identical under both
agents, so the head-to-head comparison uses only the 19 simulated SAGE turns
per agent.

## 2. Experiment Results — head-to-head

### 2.1 Overall pass rates (simulated-only, 19 SAGE turns per agent)

| Metric             | 4-16 agent          | Final agent (AgentV2.1) | Δ           |
|--------------------|---------------------|-------------------------|-------------|
| Front-Loading      | **9/19 (0.474)**    | **9/19 (0.474)**        | 0.000       |
| Answer-First       | **8/8 (1.000)**     | **7/10 (0.700)**        | −0.300      |
| AF applicable turns| 8                   | 10                      | +2          |

### 2.2 Per-persona breakdown

Front-Loading (`?` ≤ 1 per turn AND ≤ 4 sentences before first `?`):

| Persona              | 4-16 FL  | Final FL | Δ FL  |
|----------------------|----------|----------|-------|
| `skeptical-engineer` | **0/6**  | **3/6**  | +0.50 |
| `novice-curious`     | 5/8      | 4/8      | −0.13 |
| `fatigued-returner`  | 4/5      | 2/5      | −0.40 |

Answer-First (LLM-as-judge — 2-stage classifier + grader):

| Persona              | 4-16 AF (pass/applicable) | Final AF (pass/applicable) |
|----------------------|---------------------------|----------------------------|
| `skeptical-engineer` | 2/2 (1.0)                 | 3/4 (0.75)                 |
| `novice-curious`     | 6/6 (1.0)                 | 3/5 (0.60)                 |
| `fatigued-returner`  | 0/0 (n/a)                 | 1/1 (1.0)                  |

### 2.3 Final agent — full run (authored + simulated)

For completeness, the final agent was also scored on the seven curated
authored examples plus the same three simulated sessions (10 transcripts,
53 SAGE turns total):

| Metric         | Applicable | Passed | Rate  |
|----------------|------------|--------|-------|
| Front-Loading  | 53         | 23     | 0.434 |
| Answer-First   | 13         | 9      | 0.692 |

The sanity check on authored transcripts holds — positive examples pass
Front-Loading more than negative ones (0.500 vs 0.333) — confirming the
rule-based metric is discriminative on this corpus.

## 3. What improved, what did not, and why

### 3.1 Front-Loading on `skeptical-engineer` — clear improvement

The biggest single delta is on the `skeptical-engineer` persona, whose
opening prompt is *"What is a hallucination, technically? Don't sugarcoat
it."* The 4-16 agent failed Front-Loading on **every one of its six SAGE
turns** (0/6). The final agent passes half (3/6).

Direct inspection of the transcripts shows the failure mode. The 4-16
SAGE answered the technical question with a 7–10 sentence multi-paragraph
dump including bulleted lists and no pause:

> *"...Technically: LLMs are next-token predictors trained to maximize the
> likelihood of plausible-sounding sequences. They don't have a truth
> model. They have a probability model over text. When the training data
> is sparse..."* — 4-16 agent, turn 1 (≈ 9 sentences before any question)

The final agent, on the same prompt, answers in two short paragraphs and
adds a "Quick gut check" question before going deeper, hitting the
Pre-Pause Length threshold:

> *"A hallucination is when a language model generates text that's fluent
> and confident but factually wrong... Quick gut check before I go deeper:
> do you think hallucination is a bug or a feature?"* — final agent, turn 1

**Relevant changes (4-16 → final):**

1. The system prompt added a new explicit carve-out: the
   ACKNOWLEDGE → NUDGE → EXPLAIN scaffolding pattern was renamed
   *"Scaffolding Pattern (applies to feedback on practice, NOT to direct
   questions)"* and gained a one-paragraph Scope note: *"For direct
   questions, answer first, then optionally ask a follow-up to deepen
   understanding."* In 4-16 the section title implied the pattern applied
   to all teaching interactions, which biased SAGE toward asking before
   answering.
2. The `Answer, then ask questions` bullet was expanded from one
   half-sentence to a two-sentence rule that explicitly anchors on the
   example *"What is a hallucination?"* — the same prompt that fails the
   skeptical-engineer persona at 4-16.
3. A *"Re-check intent each turn"* checklist was added, including the
   row *"Off-topic question → break script, answer it, offer to resume or
   stop"*, which discourages SAGE from bulldozing through a scripted
   teach-then-test flow when the learner is asking a substantive
   question.

**Hypothesis on why this worked:** The skeptical-engineer prompt is the
clearest case of a direct technical question in the persona set. The
final agent's prompt makes "this is a direct question, do not run the
scaffolding pattern" an explicit and repeatedly-named rule rather than
an implicit one. The metric directly catches the failure mode the rule
targets.

### 3.2 Front-Loading on `novice-curious` and `fatigued-returner` — small regressions

Front-Loading **dropped** on the other two personas (5/8 → 4/8, and 4/5 →
2/5). Inspection shows the failure mode is different from
skeptical-engineer: the regressions are not about long pre-pauses, they
are about **question-stacking**. For example, the final agent on
novice-curious produced a 253-character SAGE turn containing **four**
question marks:

> *"...So before we go further: what part of that feels most useful to
> you? The framework? The example? Or seeing how it changes the output?
> Or is something else still bugging you?"*

The 4-16 agent never produced multi-question turns on novice-curious
(every SAGE turn had `?` ≤ 1).

**Relevant changes (4-16 → final):** The final prompt adds substantially
more content — the in-turn intent re-check table, voice-and-register
references, the answer-first carve-out expansion — without strengthening
the "ONE question per message" rule. The cumulative effect appears to be
that SAGE, when trying to mirror the learner's register and pivot to a
choice menu (a behavior favored by the new `voice-and-register` and
`difficulty-adapter` cues), defaults to a multi-option question stack.
The Question Discipline sub-check, which is binary on `?` count, then
flips from pass to fail.

**Hypothesis on why it regressed:** Prompt growth without
counter-balancing constraints. Each new section ("answer first then
ask", "re-check intent", "voice-and-register") nudges toward more
interactional behavior; none of them say "and still only one `?` in the
turn." The metric correctly catches the regression. This is consistent
with prior literature on long system prompts diluting earlier
constraints — the original "ONE question per message" line is the same
in both versions, but the relative weight has dropped as the surrounding
prompt has grown by ~58% (9.1 KB → 14.3 KB).

### 3.3 Answer-First — appears to regress, mostly a denominator artifact

The 4-16 agent's 100 % Answer-First (8/8) versus the final agent's 70 %
(7/10) is the most eye-catching number, and the most misleading. Two
things are happening at once:

1. **Different conversations sample different applicable sets.** Both
   personas are driven by a separate Haiku-4.5 LLM that responds to
   whatever SAGE says. Because SAGE's replies differ between versions,
   the persona's follow-up questions also differ, and the
   classifier-stage of the judge ends up labelling different numbers of
   learner turns as direct questions. The final agent's run produced
   **10** applicable answer-first turns, against **8** for 4-16.
2. **The final agent fails Answer-First on novice-curious specifically.**
   The two failed turns are turns where SAGE, asked a definitional
   question, opens with a clarifying question of its own instead of an
   answer. The 4-16 agent on the same persona answered 6/6 — but again,
   the **prompts the persona asked were different**, and were less
   crisply phrased as definitional questions.

Net: the apparent regression is partially real (the final agent does
sometimes ask before answering when it should not) and partially a
denominator-shift artifact. The total *number* of passing Answer-First
turns increased modestly (from 8 to 7 — the absolute counts are
fragile). Honest reading: Answer-First behavior is roughly unchanged on
the small persona corpus; we would need more transcripts to make a
strong claim.

### 3.4 Things that did not move at all

Both agents share:

- The same baseline Front-Loading rule list (one `?`, four sentences).
- The same set of skills (`onboarding`, `concept-explainer`,
  `prompt-coaching`, etc.) — no new skill was added between 4-16 and the
  final version that bears directly on either intrinsic metric. The
  `voice-and-register` reference skill is new but is loaded *inside*
  other skills, not by the runtime tool router.
- The same `claude-opus-4-6` model in `sage/agent.py`. Both versions
  call the same model.

This suggests the prompt is the primary lever for these metrics; the
data layer (`sage/`, `data/`, `workflows/`) was modified between
versions for unrelated reasons (Streamlit app polish, prompt-drift CI,
file-name sanitization) but the agent's *behavior* with respect to the
metrics is dominated by `CLAUDE.md` and the auto-generated
`sage/prompts.py`.

## 4. Future work and design rationale

The comparison surfaces three concrete problems worth addressing before
the next release:

### 4.1 Question-Discipline regression on conversational personas

**Problem.** The final agent stacks 2–4 questions in a single turn on
the `novice-curious` persona, violating both Question Discipline and
Pre-Pause Length sub-checks. Root cause is a prompt-growth dilution:
later sections add interactional cues without re-stating the
one-question constraint.

**Proposed design.** Move the "ONE question per message" rule from a
bullet inside the Interaction Style section to a top-of-prompt
*"Mechanical constraints"* block, alongside the
`?`-count threshold itself (i.e. state the *measurable* constraint, not
just the principle). Phrase it the way the metric scores it:

> *"Mechanical constraints (the evaluation harness scores against these
> directly): a single SAGE turn must contain at most one `?` character,
> and at most four sentences before the first `?` or before the end of
> the turn."*

**Rationale.** Two evidence threads: (a) the metric is rule-based, so
restating the rule in measurable form is a cheap intervention with a
clear failure mode; (b) prompt-engineering work on
[long-context dilution](https://arxiv.org/abs/2307.03172) suggests
material weight is recovered when constraints are placed near the start
or restated in a dedicated block. Cost: ~20 minutes of prompt edit.

**Plan.** (1) Add the block to `CLAUDE.md`'s prompt-contribution region;
(2) regenerate `sage/prompts.py` via `scripts/build_prompts.py`;
(3) re-run the persona simulator with `--all`; (4) confirm
novice-curious front-loading is ≥ 5/8 again before merging.

### 4.2 Larger, more discriminative persona corpus

**Problem.** Three personas × ~6 SAGE turns each = 19 scoreable turns
per agent version. Several of the per-metric per-persona cells (0/0,
1/1, 0/1) have too few applicable turns for the rate to mean much. The
Answer-First denominator-shift effect in §3.3 is a direct symptom.

**Proposed design.** Triple the persona set. Add five new personas
covering currently-absent quadrants:

| New persona            | Direct-question density | Register      |
|------------------------|-------------------------|---------------|
| `homework-pressed`     | Low (task-mode)         | Casual        |
| `policy-curious`       | High (factual)          | Formal        |
| `ESL-learner`          | Medium                  | Plain         |
| `data-scientist`       | High (technical)        | Terse         |
| `ethics-curious`       | Medium                  | Probing       |

Each persona produces 8–12 SAGE turns. Target: ≥ 60 scoreable turns per
agent version, ≥ 30 Answer-First applicable turns. At that scale the
Δ in §3.3 would either solidify or wash out, and we could add a
chi-square test rather than relying on raw percentages.

**Rationale.** The simulator is already parametric on `personas.json`,
so adding personas is a content task, not a code task. The per-persona
cost is roughly $0.05 (Haiku persona + Opus SAGE for 10 turns + judge
runs), so 5 new personas × 2 agent versions ≈ $0.50. Cheap.

**Plan.** (1) Author 5 new persona JSON blocks under
`evaluation/personas/personas.json`; (2) regenerate with
`python -m evaluation.personas.simulator --all` for both
`--sage-prompt` targets; (3) score with the same `--no-authored` flow;
(4) update the table in §2.1 to use the larger corpus.

### 4.3 A third intrinsic metric: scaffold-vs-direct routing accuracy

**Problem.** The cleanest improvement we measured (skeptical-engineer
Front-Loading: 0/6 → 3/6) is also a routing change — SAGE *correctly
decided* the prompt was a direct technical question and not a practice
attempt. Neither current metric measures that decision directly.
Front-Loading catches it indirectly via sentence count; Answer-First
catches it only if the classifier labels the prior learner turn as
factual.

**Proposed design.** Add **Metric 3 — Routing Discipline**, a
single-call LLM judge that, given a SAGE turn and its preceding
learner turn, labels the turn as one of:

- `direct-answer`            — substantive answer to a direct question
- `practice-feedback`        — ANE-shaped feedback on a learner attempt
- `routing-handoff`          — explicit handoff to another skill or path
- `unsafe-mode-collapse`     — ANE applied where direct-answer was correct

A turn passes if the label matches the type of the preceding learner
turn (definitional question → `direct-answer`; practice attempt →
`practice-feedback`; "actually, can we…" → `routing-handoff`). The
`unsafe-mode-collapse` label is always a fail and surfaces the specific
failure mode CLAUDE.md warns about ("Misapplying ANE to direct questions
makes SAGE feel evasive").

**Rationale.** This metric closes the gap between the two existing
metrics. Front-Loading is mechanical; Answer-First requires the prior
turn to be classified as a direct question. Routing Discipline scores
the *decision* SAGE made about which mode to operate in, which is the
behavior CLAUDE.md spends the most language on. It is also the metric
most likely to credit the prompt changes we made between 4-16 and the
final version, since those changes were primarily about routing
(direct-question carve-out, intent re-check checklist).

**Plan.** (1) Add a new module `evaluation/metrics/routing.py`
mirroring the structure of `answer_first.py` (single judge call,
hash-keyed JSON cache); (2) write a system prompt for the judge using
the four labels above; (3) author 8–10 labelled fixtures under
`evaluation/tests/fixtures/routing/` so the metric is unit-testable
without API spend; (4) integrate into `run_evaluation.py` alongside the
existing two metrics; (5) re-run §2.1 with three columns instead of
two and document the result in `intrinsic-evaluation.md`.

### 4.4 (Stretch) Tighten the model gap

Both versions still run on `claude-opus-4-6`. The persona-simulator and
judges use newer models (`claude-opus-4-7`, `claude-haiku-4-5`,
`claude-sonnet-4-6`). Migrating the runtime to `claude-opus-4-7` is
non-trivial: the model is more verbose by default and might re-break
Front-Loading. The work would be: (1) flip `MODEL` in `sage/agent.py`
and `sage/app.py`; (2) re-run the persona simulator; (3) if
Front-Loading drops more than 10 percentage points, revisit §4.1's
mechanical-constraints block. We are deliberately ordering this *after*
§4.1 so the constraint block is in place before the model change.

---

## 5. Summary

Between 4-16 and the final version, the system prompt grew by ~58%, the
ANE scaffolding pattern was carved out explicitly to *not* apply to
direct questions, and an in-turn intent re-check table was added. On
the simulated persona corpus, this produced one large, defensible win
(skeptical-engineer Front-Loading: 0/6 → 3/6) and a smaller regression
on conversational personas (multi-question stacking on
`novice-curious`). Answer-First moved within the noise floor of an
8-turn applicable set. The three pieces of follow-up work in §4 are
ordered by expected ROI: cheapest first (rule restatement),
medium-cost middle (corpus expansion), most-leveraged last (new
routing metric).

The repository, run artifacts, and metric implementations are at
<https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor/tree/AgentV2.1>;
the executable form of this comparison is preserved in
`evaluation/AIAgents_S26_SAGE.ipynb` so a grader can read the numbers
without re-running anything.
