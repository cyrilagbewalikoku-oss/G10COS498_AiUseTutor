# Workflow: Assessment Flow

**Purpose**: Comprehensive evaluation to determine if a learner is ready to advance to the next skill level.

## Platform Context

SAGE operates within the CollaborAITE platform. When a user @mentions SAGE on CollaborAITE, optional data sources (course progress, peer benchmarks, shared submissions) may be available to enrich assessment context. SAGE uses CollaborAITE data only when present; all functionality works without it.

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
  └─ Immediate feedback per question (ACKNOWLEDGE → NUDGE → EXPLAIN)
       │
       ▼
practice assessment (one or more of 4 practice types)
  ├─ Prompt Crafting: write and refine prompts under timed conditions
  ├─ Scenario Simulation: interact with simulated AI, demonstrate verification
  ├─ Ethical Reasoning: work through case study with Socratic pressure
  ├─ Conceptual Application: explain and apply framework to novel scenario
  └─ Full interaction log captured
       │
       ▼
skill-evaluator (evaluate both knowledge and practice)
  ├─ Combine knowledge-check scores with practice performance
  ├─ Score all 5 dimensions
  ├─ Generate competency-specific scores across 4 practice types
  └─ Generate comprehensive evaluation
       │
       ▼
single closing reflection question
  └─ "What area of AI agent use do you now feel most confident in?"
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
3. **Practice assessment** — At least 2 of 4 practice types assessed
4. **skill-evaluator** — Combined evaluation across all dimensions + competencies
5. **Single closing reflection** — One reflection question
6. **level-classifier** — Level determination
7. **progress-reporter** — Full progress summary
8. **improvement-advisor** (if gaps found) — Targeted improvement plan

## Duration

- Typical: 25-40 minutes
- Knowledge check: 10-15 minutes
- Practice assessment: 10-15 minutes
- Results + closing reflection: 5-10 minutes

## Assessment Practice Types

Each level-up assessment includes at least 2 of the 4 practice types:

| Practice Type | What It Tests | How Assessed |
|--------------|---------------|--------------|
| **Prompt Crafting** | CRAFT framework application, constraint specificity | Prompt quality score (CRAFT dimensions) |
| **Scenario Simulation** | Verification behavior, iteration, output evaluation | Interaction log analysis (verification moves, re-prompting) |
| **Ethical Reasoning** | Stakeholder awareness, principle application, pressure resilience | Socratic dialogue quality, position defense |
| **Conceptual Application** | Transfer of knowledge to novel contexts | Explanation accuracy, framework application |

## Competency-Specific Assessment

Alongside the 5 dimensional scores, SAGE tracks competency across the 4 practice types:

| Competency | Scored 0-5 | Description |
|-----------|-----------|-------------|
| Prompt Crafting | 0-5 | Can write clear, well-constrained prompts using CRAFT |
| Scenario Simulation | 0-5 | Can interact with AI agents critically and iteratively |
| Ethical Reasoning | 0-5 | Can identify ethical issues and reason through dilemmas |
| Conceptual Application | 0-5 | Can explain and apply AI concepts to new situations |

Advancement requires both dimensional thresholds AND minimum competency scores.

## Scaffolding Pattern

During knowledge-check feedback, SAGE uses **ACKNOWLEDGE → NUDGE → EXPLAIN**:

1. **ACKNOWLEDGE**: Note what the learner got right
2. **NUDGE**: Ask a guiding question about the gap
3. **EXPLAIN**: Provide the principle or correction after the learner responds

## Assessment Scenario Selection

Each level-up assessment uses scenarios designed to test ALL dimensions:

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

Competency minimums (in addition to dimensional thresholds):
- Practitioner: at least 2 competencies >= 2.5
- Advanced: at least 3 competencies >= 3.5
- Critical Thinker: all 4 competencies >= 4.0

## Retake Policy

- Users can retake after completing recommended improvement activities
- Minimum 2 sessions between assessment attempts
- Different scenario and questions used for retake (no memorization advantage)

## Success Criteria

- Assessment covers all 5 dimensions with both knowledge and practical components
- At least 2 practice types are assessed
- Competency-specific scores provided alongside dimensional scores
- User receives clear, specific feedback regardless of outcome
- Level-up feels earned and meaningful
- Non-advancement feels encouraging, not discouraging