# Common Learner Misconceptions About AI Agents

A catalog of misconceptions SAGE frequently encounters, what each signals about the learner's mental model, and where to intervene. Skills should use this as a diagnostic — if a learner says one of these things, the linked remediation is the right move.

## 1. "The AI searches the internet / looks things up"

What they believe: the model retrieves facts from a live index.
What's actually happening (for most chatbot interactions): the model generates plausible tokens from its training distribution, which may or may not reflect real sources.

**Signal:** learner asks the AI to "find sources" and expects retrieval.
**Intervention:** `improve-interaction` or `concept-explainer` — teach the distinction between generation and retrieval, and the specific case of tool-augmented models that *do* search.

## 2. "If the AI sounds confident, it's probably right"

What they believe: fluency and authority correlate with accuracy.
What's actually happening: LLMs are trained to be fluent; hallucinations are often *more* confident than correct answers because the model's distribution is smoother in fabricated regions.

**Signal:** learner accepts outputs uncritically, especially technical content.
**Intervention:** `bad-agent-simulator` — role-play a confidently-wrong agent and make them spot it.

## 3. "The AI remembers me between conversations"

What they believe: persistent memory across sessions.
What's actually happening (by default for most chat interfaces): no memory beyond the current context window; any "memory" is a retrieval step they may not be aware of.

**Signal:** learner references something they "told it before" and expects continuity.
**Intervention:** `concept-explainer` — context window + session boundary, and when memory *is* enabled (custom GPTs, projects, etc.).

## 4. "If I phrase it nicely, it works better"

What they believe: politeness or magical incantations ("you are an expert...") dominate output quality.
What's actually happening: specificity, constraints, and examples dominate; politeness is largely noise.

**Signal:** learner writes elaborate role-play preambles with no concrete task description.
**Intervention:** `prompt-coaching` — teach CRAFT, de-emphasize Role until C and A are solid.

## 5. "AI is a better writer / coder / researcher than me"

What they believe: AI output is the ceiling, their own work is the floor.
What's actually happening: AI output is an average — helpful starting material, rarely the best version of the work, and never a substitute for the learner's judgment on what matters.

**Signal:** learner asks SAGE to "rewrite this prompt for me" or accepts a first draft wholesale.
**Intervention:** `ethical-guidance` + `reflection-facilitator` — agency and over-reliance. Never do the work for them.

## 6. "The AI understands what I mean"

What they believe: the model shares their context, goals, and constraints.
What's actually happening: the model has exactly what is in the prompt, nothing more.

**Signal:** short prompts with heavy implicit assumptions.
**Intervention:** `prompt-coaching` NUDGE — "if you were the AI reading this cold, what would you have to guess?"

## 7. "More capable model = always better answer"

What they believe: upgrading the model solves prompt problems.
What's actually happening: a weak prompt on a strong model is still a weak prompt; the biggest lever at a given model tier is prompt quality and verification pipeline.

**Signal:** learner frustrated with results, asks about model selection instead of examining the prompt.
**Intervention:** `prompt-lab` — let them see the same bad prompt fail across models; redirect to CRAFT.

## 8. "AI is objective / unbiased"

What they believe: math + code = neutral.
What's actually happening: training data, reinforcement preferences, and safety tuning all encode viewpoints. AI outputs reflect their origin.

**Signal:** learner treats AI output as an authoritative reference for contested topics.
**Intervention:** `ethical-guidance` + `scenario-runner` output-evaluation type — bias recognition, framing analysis.

## How SAGE uses this catalog

Skills can reference this list to (a) recognize which misconception is showing up in a learner's attempt, and (b) route to the appropriate remediation. The catalog is deliberately short — 8 entries is more than enough for the practice scenarios SAGE runs. Additions should be earned by real, repeated observations across learners.
