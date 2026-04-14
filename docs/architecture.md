# System Architecture

## Overview

SAGE is a skill-based tutoring system that teaches people how to use AI agents effectively, ethically, and critically. It is built as a collection of modular **skills** orchestrated by **workflows** and personalized through **user profiles**. SAGE can operate standalone or integrate with the CollaborAITE platform for additional data sources and context.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                    USER MESSAGE                       │
│         (CLI or @SAGE on CollaborAITE)               │
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
              └────────┬────────┘
                       │
                       ▼
         ┌──────────────────────────────┐
         │  CollaborAITE Platform       │ ◄── Optional integration layer
         │  (when available)            │
         │  - Course context data       │
         │  - Assignment data           │
         │  - Peer interaction data     │
         │  - Channel conversations      │
         │  - Course slides/prior work  │
         └──────────────────────────────┘
```

## SAGE Interaction Cycle

Every teaching/practice session follows this 6-step cycle:

1. **Learner initiates** — asks a question, chooses a scenario, or continues a module
2. **SAGE assesses context** — reviews profile, course enrollment, competency gaps, and available CollaborAITE data sources
3. **Learner attempts practice task** — one of 4 practice types (Prompt Crafting, Output Evaluation, Appropriateness Judgment, Workflow Design)
4. **SAGE scaffolds feedback** — ACKNOWLEDGE what they did -> NUDGE with a reflective question -> EXPLAIN the principle (never explain before the learner reflects)
5. **Closing reflection** — a single brief question guiding the learner to notice a pattern or connect practice to their coursework
6. **SAGE updates progress** — competency scores, dimensional scores, difficulty level

## Technical Architecture Components

### Scenario Engine
Generates and manages practice scenarios for the 4 practice types. Scenarios can be drawn from SAGE's built-in library or contextualized using data from the CollaborAITE platform when available. The engine selects scenarios based on the learner's level, recent performance, and (when available) their actual course context.

### Feedback Generator
Implements the ACKNOWLEDGE -> NUDGE -> EXPLAIN scaffolding pattern. The Feedback Generator ensures that SAGE never explains before the learner has a chance to reflect. It structures all teaching feedback in three phases:
1. **ACKNOWLEDGE**: Validate what the learner did well or correctly noticed
2. **NUDGE**: Ask a question or prompt reflection that leads the learner toward the insight
3. **EXPLAIN**: Provide the full explanation, principle, or corrected approach after the learner has engaged

### Reflection Prompter
Delivers a single closing reflection question at the end of each practice session. Unlike multi-step debriefs, the Reflection Prompter asks one targeted question designed to connect the session's learning to the learner's own context or habits.

### Progress Tracker
Maintains dimensional scores (0-5 scale) and competency labels for each of the 5 assessment dimensions. Updates scores after every interaction and tracks improvement trajectories across sessions.

### Data Access Layer
Provides a unified interface for accessing user profiles, scenario libraries, and (when available) CollaborAITE platform data sources including course context, assignment data, and peer interaction patterns. All data access flows through a privacy layer that enforces data minimization and ensures no sensitive learner data is exposed beyond what is needed for the current interaction. SAGE never accesses other learners' data, even when CollaborAITE data sources are available.

### Conversation Manager
Handles turn-by-turn conversation state, skill chaining, and context window management. Ensures smooth transitions between skills and maintains conversation coherence across multi-skill workflows.

## Skill Categories

| Category | Skills | Purpose |
|----------|--------|---------|
| **Meta** | session-router, difficulty-adapter | Routing and calibration |
| **Teaching** | onboarding, concept-explainer, prompt-coaching, ethical-guidance | Content delivery |
| **Assessment** | knowledge-check, skill-evaluator, level-classifier | Evaluation |
| **Simulation** | scenario-runner, bad-agent-simulator, prompt-lab | Practice |
| **Feedback** | reflection-facilitator, progress-reporter, improvement-advisor | Reflection and growth |

### Practice Types

Simulation skills support 4 distinct practice types:

| Practice Type | Description | Skills Involved |
|---------------|-------------|-----------------|
| **Prompt Crafting** | Learner writes prompts and receives scaffolded feedback | scenario-runner (prompt-crafting type), prompt-lab |
| **Output Evaluation** | Learner evaluates AI-generated output for accuracy, bias, and framing | scenario-runner (output-evaluation type) |
| **Appropriateness Judgment** | Learner decides whether using AI is appropriate for a given task | scenario-runner (appropriateness type), ethical-guidance |
| **Workflow Design** | Learner designs human-AI collaboration workflows | scenario-runner (workflow-design type) |

## Data Flow

```
User Message → session-router → Selected Skill
    ↓
difficulty-adapter (called internally by skill)
    ↓
Skill executes (may chain to other skills)
    ↓
Feedback Generator applies ACKNOWLEDGE → NUDGE → EXPLAIN pattern
    ↓
Reflection Prompter delivers single closing reflection question
    ↓
Interaction logged → User profile updated → Progress Tracker updated
    ↓
Data Access Layer (with privacy layer) stores/retrieves as needed
    ↓
CollaborAITE data sources consulted (when available)
    ↓
Feedback skill (progress) → Response to user
```

## Key Design Principles

1. **Skills are modular and composable** — each skill does one thing well and can be combined into different workflows
2. **Workflows are the orchestration layer** — they define the sequence of skills for common patterns (onboarding, lessons, practice, assessment)
3. **User profiles are the personalization layer** — every skill reads from and writes to the profile, enabling adaptive behavior
4. **The difficulty adapter is invisible** — users experience natural adaptation without seeing explicit difficulty changes
5. **Assessment is multi-dimensional** — 5 dimensions (conceptual, prompting, evaluation, ethics, critical thinking) prevent blind-spot advancement
6. **ACKNOWLEDGE before NUDGE before EXPLAIN** — SAGE never explains before the learner reflects
7. **Single closing reflection** — one question at session end, not multi-step debriefs
8. **Privacy-by-Design** — the Data Access Layer enforces data minimization; CollaborAITE integration is optional and privacy-preserving; SAGE never accesses other learners' data

## Skill Interaction Rules

- **session-router** is always the entry point (except for internal calls between skills)
- **difficulty-adapter** is never called directly by users — only internally by other skills
- **Skills can chain** to any other skill via their "Chains To" specification
- **Feedback skills** typically terminate a workflow sequence
- **Assessment skills** can trigger level changes which reconfigure the learning path
- **Feedback Generator** applies the ACKNOWLEDGE -> NUDGE -> EXPLAIN pattern to all teaching interactions
- **Reflection Prompter** delivers a single closing question rather than a multi-step debrief