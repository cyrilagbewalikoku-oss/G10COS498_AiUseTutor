# Learner Predicts and Cognitive Conflict

## What it is

The "Learner Predicts" pattern is the pedagogical move inside SAGE's NUDGE step. Before the tutor explains a correct or stronger approach, the learner is asked to predict, reason about, or commit to a position. The act of committing creates a small, productive gap between the learner's expectation and what they are about to see — a gap the explanation then fills.

This is a specific application of **cognitive conflict** (Piaget; Posner et al., 1982): a new concept is more likely to be retained when it resolves a felt tension, rather than arriving unannounced as a piece of information.

## Why it matters for AI literacy specifically

Learners using AI tools typically *receive* — AI output arrives, they read, they move on. The habit SAGE is trying to build is the opposite: an anticipatory, predictive relationship with the tool. "What do I expect this to say? Where is it likely to fail?" A NUDGE that demands a prediction is the same cognitive move the learner needs to use in the wild: form a hypothesis, watch what the AI does, compare.

Skipping the NUDGE (explaining first, asking questions after) teaches the opposite habit: AI as oracle, learner as receiver.

## How to recognize a good Learner Predicts nudge

- It asks the learner to *commit to an answer*, not just "any thoughts?"
- The answer could be wrong — the learner has something to lose by guessing
- The resolution (the EXPLAIN step) gets its force from whatever gap the prediction exposed

Weak nudges look like: "Does that make sense?" / "What do you think?" / "Any questions?"
Strong nudges look like: "Before I react — what do you predict the AI got wrong?" / "Commit to a number: on a scale of 0–10, was AI the right tool here?"

## Selected grounding

- Posner, Strike, Hewson & Gertzog (1982) — accommodation of scientific conceptions; cognitive conflict as a condition for conceptual change.
- Chi (2009) — ICAP framework: Interactive > Constructive > Active > Passive engagement in learning outcomes.
- Hattie & Timperley (2007) — feedback is most effective when it addresses a gap the learner has already recognized.
- Bjork & Bjork (2011) — "desirable difficulties" improve retention; prediction is one such difficulty.

## How SAGE applies it

Every skill that gives feedback on a learner attempt (prompt-coaching, scenario-runner, knowledge-check, improve-interaction, bad-agent-simulator) must use a Learner Predicts nudge before explaining. The explicit naming is in [CLAUDE.md §Scaffolding Pattern](../../CLAUDE.md).
