# CRAFT Framework

## What it is

CRAFT is a five-part scaffold for writing effective prompts to large language models: **C**ontext, **R**ole, **A**ction, **F**ormat, **T**one. SAGE teaches it piece by piece in the `prompt-coaching` skill.

## Why SAGE teaches *this* framework specifically

There are many prompt frameworks in circulation (CLEAR, RISEN, ICIO, the "five P's", etc.). SAGE chose CRAFT because:

1. It maps cleanly to what LLMs actually condition on: background information, implied viewpoint, task verb, output shape, register.
2. It is small enough to teach Novices in two elements (C + A), then extend to full five-part use for Practitioners and above — avoiding the "complete framework up front" front-loading that novices struggle with.
3. Every element maps to a testable failure mode: missing Context produces generic output, missing Role produces wrong-audience output, missing Action produces meandering output, missing Format produces unparseable output, missing Tone produces off-register output. This gives SAGE distinct remediation levers.

## Teaching order

| Level | Taught | Rationale |
|---|---|---|
| Novice | Context + Action | Without these, no other element matters |
| Practitioner | Add Format | Once the output is *about* the right thing, make it *shaped* right |
| Advanced | Add Role + Tone | Advanced learners recognize register and POV as part of quality |
| Critical Thinker | All five, plus when to break the framework | Masters know when rules help and when they constrain |

## When CRAFT is *not* the right tool

- **Multi-turn conversational tasks** — CRAFT is optimized for single-shot prompts. For agent workflows, teach task decomposition instead (see `scenario-runner` WORKFLOW DESIGN type).
- **Tool-calling / function-calling** — the structure matters more than the prose. Teach schema specification, not CRAFT.
- **Classification or extraction** — a well-formed schema plus few-shot examples beats a CRAFT prompt.

## How SAGE teaches it

The `prompt-coaching` skill:
- Asks the learner to write a prompt first, without teaching CRAFT
- Diagnoses which CRAFT element is weakest in what they wrote
- Teaches that one element (ACKNOWLEDGE → NUDGE → EXPLAIN)
- Asks the learner to rewrite
- Repeats for one more element at most in a single session

## Selected grounding

- Liu et al. (2023) — "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods" — taxonomy of prompt structure.
- White et al. (2023) — "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT" — named patterns that CRAFT generalizes.
- Schulhoff et al. (2024) — "The Prompt Report" — empirical survey of which prompt elements most affect output quality.
