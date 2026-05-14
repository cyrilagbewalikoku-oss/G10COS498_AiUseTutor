# Intrinsic Evaluation Results — final-agent-2026-05-14T18-15Z

- **SAGE version:** `f94da786fdc72187b5d4c2e7d51085b31175cdea`
- **Transcripts evaluated:** 10

## Overall pass rates

| Metric | Applicable turns | Passed | Pass rate |
|---|---|---|---|
| front_loading | 53 | 23 | 0.434 |
| answer_first | 13 | 9 | 0.692 |

## Pass rates by source label

| Label | Front-Loading | Answer-First |
|---|---|---|
| negative | 6/18 (0.333) | 2/2 (1.0) |
| positive | 8/16 (0.5) | 0/1 (0.0) |
| simulated | 9/19 (0.474) | 7/10 (0.7) |

## Per-transcript breakdown

- **positive/01-novice-learns-prompting** (authored, 3 SAGE turns): front-loading 1/3, answer-first 0/1
- **positive/02-practitioner-evaluates-output** (authored, 3 SAGE turns): front-loading 2/3, answer-first 0/0
- **positive/03-ethical-dilemma-discussion** (authored, 7 SAGE turns): front-loading 4/7, answer-first 0/0
- **positive/04-appropriateness-judgment** (authored, 3 SAGE turns): front-loading 1/3, answer-first 0/0
- **negative/01-blind-trust-in-output** (authored, 7 SAGE turns): front-loading 2/7, answer-first 2/2
- **negative/02-over-reliance-full-delegation** (authored, 5 SAGE turns): front-loading 1/5, answer-first 0/0
- **negative/03-sharing-sensitive-data** (authored, 6 SAGE turns): front-loading 3/6, answer-first 0/0
- **simulated/fatigued-returner** (simulated, 5 SAGE turns): front-loading 2/5, answer-first 1/1
- **simulated/novice-curious** (simulated, 8 SAGE turns): front-loading 4/8, answer-first 3/5
- **simulated/skeptical-engineer** (simulated, 6 SAGE turns): front-loading 3/6, answer-first 3/4

## Sanity check

Negative authored transcripts should fail more often than positive ones. Front-loading pass rate: positive=0.5, negative=0.333. Answer-first pass rate: positive=0.0, negative=1.0.
