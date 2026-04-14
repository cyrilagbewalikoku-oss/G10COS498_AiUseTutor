# Workflow: Assessment Flow

**Purpose**: Comprehensive evaluation to determine if a learner is ready to advance to the next skill level.

## Flow Diagram

```
User completes sufficient modules OR requests level-up check
  │
  ▼
session-router (routes to assessment flow)
  │
  ▼
knowledge-check (comprehensive: 5-8 questions)
  ├─ Covers all 5 dimensions
  ├─ Level-appropriate question types
  └─ Immediate feedback per question
       │
       ▼
scenario-runner (practical assessment scenario)
  ├─ Higher-stakes scenario than normal practice
  ├─ Designed to test multiple dimensions simultaneously
  └─ Full interaction log captured
       │
       ▼
skill-evaluator (evaluate both knowledge and practice)
  ├─ Combine knowledge-check scores with scenario performance
  ├─ Score all 5 dimensions
  └─ Generate comprehensive evaluation
       │
       ▼
level-classifier
  │
  ├─ Level-up warranted ──► 
  │     ├─ Congratulations + new level explanation
  │     ├─ progress-reporter (full summary with achievement)
  │     └─ Present updated learning path for new level
  │
  └─ Not ready yet ──►
        ├─ improvement-advisor (specific gap analysis)
        ├─ Suggest 2-3 targeted practice activities
        └─ Encourage: "You're close — here's what's left"
```

## Skills Used (in order)

1. **session-router** — Routes to assessment flow
2. **knowledge-check** — Comprehensive knowledge assessment (5-8 questions)
3. **scenario-runner** — Practical skills assessment scenario
4. **skill-evaluator** — Combined evaluation across all dimensions
5. **level-classifier** — Level determination
6. **progress-reporter** — Full progress summary
7. **improvement-advisor** (if gaps found) — Targeted improvement plan

## Duration

- Typical: 25-40 minutes
- Knowledge check: 10-15 minutes
- Practical scenario: 10-15 minutes
- Results + debrief: 5-10 minutes

## Assessment Scenario Selection

Each level-up assessment uses a scenario designed to test ALL dimensions:

| Advancing To | Scenario Type | Tests |
|-------------|---------------|-------|
| Practitioner | Professional task with ethical wrinkle | Basic prompting + output verification + simple ethics |
| Advanced | Multi-step task with subtle AI errors | Sophisticated prompting + hallucination detection + professional ethics |
| Critical Thinker | High-stakes ambiguous scenario | Expert prompting + system-level evaluation + complex ethical reasoning |

## Passing Criteria

All 5 dimensions must meet the target level's threshold:
- Practitioner: all >= 2.5
- Advanced: all >= 3.5
- Critical Thinker: all >= 4.5

No compensation across dimensions — a 5.0 in prompting cannot offset a 2.0 in ethics.

## Retake Policy

- Users can retake after completing recommended improvement activities
- Minimum 2 sessions between assessment attempts
- Different scenario and questions used for retake (no memorization advantage)

## Success Criteria

- Assessment covers all 5 dimensions with both knowledge and practical components
- User receives clear, specific feedback regardless of outcome
- Level-up feels earned and meaningful
- Non-advancement feels encouraging, not discouraging
