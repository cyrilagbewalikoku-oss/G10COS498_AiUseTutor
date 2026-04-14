# Workflow: Lesson Flow

**Purpose**: Deliver a standard lesson cycle: teach a concept, check understanding, apply through practice, and reflect.

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
  └─ Comprehension check
       │
       ├─ Gaps found ──► concept-explainer (reteach with different approach)
       │                       │
       │                       ▼
       │                  knowledge-check (verify again)
       │
       └─ Understood ──► continue
                           │
                           ▼
                    ┌──────┴──────┐
                    │             │
              prompt-coaching   scenario-runner
              (if prompting     (if concept is
               concept)          best learned
                    │            by doing)
                    │             │
                    └──────┬──────┘
                           │
                           ▼
                  reflection-facilitator
                    ├─ "What went well?"
                    ├─ Highlight key moments
                    └─ Connect to principles
                           │
                           ▼
                  progress-reporter (end-of-lesson summary)
                    ├─ Module marked complete
                    ├─ Scores updated
                    └─ Next step suggested
```

## Skills Used (in order)

1. **session-router** — Routes to lesson flow
2. **difficulty-adapter** — Calibrates complexity for this session
3. **concept-explainer** — Teaches the concept
4. **knowledge-check** — Verifies understanding (2-3 questions)
5. **prompt-coaching** OR **scenario-runner** — Apply the concept
6. **reflection-facilitator** — Guided reflection
7. **progress-reporter** — Session summary

## Duration

- Typical: 15-25 minutes
- Teach phase: 5-8 minutes
- Practice phase: 5-10 minutes
- Reflection: 3-5 minutes

## Branching Logic

| After knowledge-check | Next Step |
|----------------------|-----------|
| 3/3 correct | Proceed to practice with reduced scaffolding |
| 2/3 correct | Proceed to practice with extra hints |
| 1/3 or 0/3 correct | Reteach with different approach, then re-check |

| Concept Type | Practice Activity |
|-------------|-------------------|
| Prompting-related | prompt-coaching → prompt-lab |
| Evaluation-related | scenario-runner (with outputs to evaluate) |
| Ethics-related | ethical-guidance (case study) |
| Conceptual | knowledge-check (deeper) then scenario-runner |

## Success Criteria

- User can explain the concept in their own words
- User successfully applies the concept in at least one practice exercise
- User identifies at least one key takeaway during reflection
- Module marked as completed in learning path
