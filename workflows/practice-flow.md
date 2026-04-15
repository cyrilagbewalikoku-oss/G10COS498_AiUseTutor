# Workflow: Practice Flow

**Purpose**: Deep practice session built around the 6-step SAGE interaction cycle for hands-on skill building through feedback, iteration, and light reflection.

## Platform Context

SAGE operates within the CollaborAITE platform. When a user @mentions SAGE on CollaborAITE, optional data sources (course enrollment, peer activity, shared resources) may be available to enrich practice context. SAGE uses CollaborAITE data only when present; all functionality works without it.

## The 6-Step SAGE Interaction Cycle

```
Step 1: Learner Initiates
  │  User requests practice or curriculum reaches practice phase
  ▼
Step 2: Agent Assesses Context
  │  SAGE reviews: course context, interaction history, topic focus,
  │  competency levels, difficulty level
  │  [If on CollaborAITE] → incorporate available platform data
  ▼
Step 3: Learner Attempts Practice Task (one of 4 types)
  │  ┌─────────────┬──────────────────┬─────────────────┬──────────────────┐
  │  │ Prompt       │ Scenario         │ Ethical         │ Conceptual       │
  │  │ Crafting     │ Simulation       │ Reasoning       │ Application      │
  │  │ (write/      │ (interact with   │ (case study     │ (explain/apply   │
  │  │  refine      │  simulated AI    │  with Socratic  │  framework to    │
  │  │  prompts)    │  agent)          │  questions)     │  novel scenario) │
  │  └─────────────┴──────────────────┴─────────────────┴──────────────────┘
  ▼
Step 4: Agent Scaffolds Feedback with Embedded Reflection
  │  Internal shape: ACKNOWLEDGE → NUDGE → LEARNER RESPONDS → EXPLAIN
  │  1. ACKNOWLEDGE: Validate what the learner did well or attempted
  │  2. NUDGE: Ask the learner to predict/reason before you reveal
  │  3. LEARNER RESPONDS: Learner thinks and replies
  │  4. EXPLAIN: Name the principle — or skip if the learner already did
  │  (Execute as dialogue, not labeled stages. Merge ACK+NUDGE when
  │   natural; skip EXPLAIN when the learner has already articulated
  │   the principle. The one non-negotiable: nudge precedes explain.)
  ▼
Step 5: Light Closing Reflection (single question)
  │  One question: e.g., "What pattern did you notice in your prompts?"
  │  or "What would you do differently next time?"
  ▼
Step 6: Agent Updates Learner Progress
     ├─ Competencies practiced (which of the 4 types, how many attempts)
     ├─ Reflection responses logged
     ├─ Difficulty level adjusted if warranted
     └─ Progress saved to learner profile
```

## Skills Used (in order)

1. **session-router** — Routes to practice flow
2. **difficulty-adapter** — Sets appropriate challenge level based on assessed context
3. **Practice skill** (selected from 4 types based on concept and learner needs)
4. **skill-evaluator** — Evaluates the practice session
5. **Single closing reflection** — One reflection question
6. **progress-reporter** — Session wrap-up with competency tracking

## Practice Type Details

| Practice Type | Description | When Selected |
|--------------|-------------|---------------|
| **Prompt Crafting** | Write, test, and refine prompts using CRAFT framework; see simulated output | Prompting concepts, CRAFT dimensions |
| **Scenario Simulation** | Interact with SAGE role-playing as an AI agent; practice verification and iteration | Evaluation concepts, workflow skills |
| **Ethical Reasoning** | Work through case studies with Socratic dialogue; defend and revise positions | Ethics concepts, responsible use |
| **Conceptual Application** | Explain a framework in own words, then apply it to a novel scenario | Architecture, capabilities, limitations concepts |

## Scaffolding Pattern (Step 4 in detail)

The **ACKNOWLEDGE → NUDGE → LEARNER RESPONDS → EXPLAIN** cycle is the core feedback mechanism — but it's an internal shape, not a visible script. Execute it as natural dialogue. The steps may be compressed (ACK+NUDGE in one turn) or truncated (skip EXPLAIN when the learner has already named the principle). The underlying logic is: the learner predicts or reasons before SAGE names the principle.

**Example (Prompt Crafting)** — reads as a two-turn exchange, not a four-step script:

> **SAGE:** "Your prompt has clear audience context — that's strong. What format would help the AI give you exactly what you need?"
>
> **Learner:** "Maybe a bulleted list?"
>
> **SAGE:** "Right — that's the 'F' in CRAFT. Adding 'as a bulleted list of 5 items' locks it in."

**Example (Scenario Simulation)** — SAGE skips the EXPLAIN because the learner named the move:

> **SAGE:** "You caught that the AI's first answer was too vague — good instinct. How could you press it to show its reasoning?"
>
> **Learner:** "Ask it to explain its sources?"
>
> **SAGE:** "Exactly — that's a verification move. It forces the AI to surface its basis."

In both: the nudge came before anything was explained, ACK and NUDGE shared a single turn, and when the learner already named the principle the reply was brief affirmation + transferable label, not a paragraph.

## Duration

- Typical: 20-35 minutes
- Practice interaction: 10-20 minutes
- Closing reflection: 1-2 minutes
- Progress update: 1-2 minutes

## Scenario Selection Logic

| User Level | Scenario Complexity | Example |
|-----------|-------------------|---------|
| Novice | Simple, single-task | "Use AI to draft an email to a parent" |
| Practitioner | Multi-step, professional | "Use AI to analyze survey data and create a report" |
| Advanced | Complex, multi-tool | "Use AI to review code, identify bugs, and suggest architecture changes" |
| Critical Thinker | Ambiguous, high-stakes | "Use AI to synthesize conflicting research findings for a policy brief" |

## Success Criteria

- Learner completes the practice task (or demonstrates why they chose to stop)
- Learner's attempts show measurable improvement within the session
- Learner responds substantively to at least one NUDGE in the scaffolding cycle
- Closing reflection answer shows genuine insight, not just "it was fine"
- Progress updated with competencies practiced, reflection response, and difficulty level