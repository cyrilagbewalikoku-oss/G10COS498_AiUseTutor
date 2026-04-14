# Workflow: Lesson Flow

**Purpose**: Deliver a standard lesson cycle: teach a concept, check understanding, apply through practice, and reflect.

## Platform Context

SAGE operates within the CollaborAITE platform. When a user @mentions SAGE on CollaborAITE, optional data sources (course context, peer activity, shared resources) may be available to enrich lesson content. SAGE uses CollaborAITE data only when present; all functionality works without it.

## Flow Diagram

```
session-router (detects: lesson intent or curriculum next-step)
  │
  ▼
difficulty-adapter (calibrate for this session)
  │
  ▼
concept-explainer
  ├─ Definition + analogy
  ├─ Concrete example
  ├─ Common misconception
  └─ Comprehension check (ACKNOWLEDGE → NUDGE → EXPLAIN scaffolding)
       │
       ├─ Gaps found ──► concept-explainer (reteach with different approach)
       │                       │
       │                       ▼
       │                  knowledge-check (verify again)
       │
       └─ Understood ──► continue
                           │
                           ▼
                    practice type selection (based on concept type)
                           │
                    ┌──────┼──────┬──────┐
                    │      │      │      │
              Prompt     Scenario  Ethical  Conceptual
              Crafting   Simulation Reasoning Application
                    │      │      │      │
                    └──────┴──────┴──────┘
                           │
                    practice with ACKNOWLEDGE → NUDGE → EXPLAIN feedback
                           │
                           ▼
                  Single closing reflection question
                    └─ "What is one thing you'll take from this into your own AI use?"
                           │
                           ▼
                  progress-reporter (end-of-lesson summary)
                    ├─ Module marked complete
                    ├─ Scores updated
                    ├─ Competencies practiced updated
                    └─ Next step suggested
```

## Skills Used (in order)

1. **session-router** — Routes to lesson flow
2. **difficulty-adapter** — Calibrates complexity for this session
3. **concept-explainer** — Teaches the concept (with ACKNOWLEDGE → NUDGE → EXPLAIN scaffolding)
4. **knowledge-check** — Verifies understanding (2-3 questions)
5. **Practice skill** (selected by concept type) — Apply the concept (with ACKNOWLEDGE → NUDGE → EXPLAIN feedback)
6. **Single closing reflection** — One reflection question
7. **progress-reporter** — Session summary

## Practice Type Selection

| Concept Type | Practice Activity |
|-------------|-------------------|
| Prompting-related | prompt-coaching → prompt-lab (Prompt Crafting) |
| Evaluation-related | scenario-runner with outputs to evaluate (Scenario Simulation) |
| Ethics-related | ethical-guidance case study (Ethical Reasoning) |
| Conceptual | knowledge-check (deeper) then scenario-runner (Conceptual Application) |

## Scaffolding Pattern

SAGE uses **ACKNOWLEDGE → NUDGE → EXPLAIN** at two points in this flow:

**In concept-explainer (comprehension check):**
1. **ACKNOWLEDGE**: Validate the learner's response
2. **NUDGE**: Ask a brief guiding question or offer a hint
3. Learner responds
4. **EXPLAIN**: Provide the principle or explanation

**In practice steps (feedback on learner attempts):**
1. **ACKNOWLEDGE**: Note what the learner did well or attempted
2. **NUDGE**: Point toward an improvement with a question or suggestion
3. Learner responds or revises
4. **EXPLAIN**: Reveal the principle or improved approach

## Duration

- Typical: 15-25 minutes
- Teach phase: 5-8 minutes
- Practice phase: 5-10 minutes
- Reflection: 1 question (~1-2 minutes)

## Branching Logic

| After knowledge-check | Next Step |
|----------------------|-----------|
| 3/3 correct | Proceed to practice with reduced scaffolding |
| 2/3 correct | Proceed to practice with extra hints |
| 1/3 or 0/3 correct | Reteach with different approach, then re-check |

## Success Criteria

- User can explain the concept in their own words
- User successfully applies the concept in at least one practice exercise
- User answers the closing reflection question substantively
- Module marked as completed in learning path