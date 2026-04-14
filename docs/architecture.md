# System Architecture

## Overview

The AI Agent Use Trainer is a skill-based tutoring system that teaches people how to use AI agents effectively, ethically, and critically. It is built as a collection of modular **skills** orchestrated by **workflows** and personalized through **user profiles**.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                    USER MESSAGE                       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  session-router  │ ◄── Classifies intent, routes to skill
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────────┐
        │              │                  │
        ▼              ▼                  ▼
   ┌─────────┐   ┌──────────┐   ┌────────────────┐
   │ Teaching │   │Assessment│   │   Simulation   │
   │  Skills  │   │  Skills  │   │    Skills      │
   ├─────────┤   ├──────────┤   ├────────────────┤
   │onboarding│   │knowledge │   │scenario-runner │
   │concept-  │   │ -check   │   │bad-agent-sim   │
   │explainer │   │skill-    │   │prompt-lab      │
   │prompt-   │   │evaluator │   └────────────────┘
   │coaching  │   │level-    │
   │ethical-  │   │classifier│
   │guidance  │   └──────────┘
   └─────────┘
        │              │                  │
        └──────────────┼──────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Feedback Skills  │
              ├─────────────────┤
              │reflection-facil. │
              │progress-reporter │
              │improvement-adv.  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  User Profile    │ ◄── Updated after every interaction
              └─────────────────┘
```

## Skill Categories

| Category | Skills | Purpose |
|----------|--------|---------|
| **Meta** | session-router, difficulty-adapter | Routing and calibration |
| **Teaching** | onboarding, concept-explainer, prompt-coaching, ethical-guidance | Content delivery |
| **Assessment** | knowledge-check, skill-evaluator, level-classifier | Evaluation |
| **Simulation** | scenario-runner, bad-agent-simulator, prompt-lab | Practice |
| **Feedback** | reflection-facilitator, progress-reporter, improvement-advisor | Reflection and growth |

## Data Flow

```
User Message → session-router → Selected Skill
    ↓
difficulty-adapter (called internally by skill)
    ↓
Skill executes (may chain to other skills)
    ↓
Interaction logged → User profile updated
    ↓
Feedback skill (reflection/progress) → Response to user
```

## Key Design Principles

1. **Skills are modular and composable** — each skill does one thing well and can be combined into different workflows
2. **Workflows are the orchestration layer** — they define the sequence of skills for common patterns (onboarding, lessons, practice, assessment)
3. **User profiles are the personalization layer** — every skill reads from and writes to the profile, enabling adaptive behavior
4. **The difficulty adapter is invisible** — users experience natural adaptation without seeing explicit difficulty changes
5. **Assessment is multi-dimensional** — 5 dimensions (conceptual, prompting, evaluation, ethics, critical thinking) prevent blind-spot advancement

## Skill Interaction Rules

- **session-router** is always the entry point (except for internal calls between skills)
- **difficulty-adapter** is never called directly by users — only internally by other skills
- **Skills can chain** to any other skill via their "Chains To" specification
- **Feedback skills** typically terminate a workflow sequence
- **Assessment skills** can trigger level changes which reconfigure the learning path
