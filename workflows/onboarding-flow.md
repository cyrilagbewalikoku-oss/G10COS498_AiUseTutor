# Workflow: Onboarding Flow

**Purpose**: Guide a new user from first contact through level assessment to their first lesson.

## Platform Context

SAGE operates within the CollaborAITE platform. When a user @mentions SAGE on CollaborAITE, optional data sources (course enrollment, peer activity, shared resources) may be available to enrich onboarding. SAGE uses CollaborAITE data only when present; all functionality works without it.

## Flow Diagram

```
User arrives
  │
  ▼
session-router (detects: new user, no profile)
  │
  ▼
onboarding
  ├─ 1. Welcome + explain SAGE's purpose
  ├─ 2. Low-stakes orientation (quick, no-pressure intro activity)
  ├─ 3. Ask 3-5 calibration questions
  ├─ 4. ──► level-classifier (assign initial level)
  ├─ 5. Agent assesses context (CollaborAITE data if available, stated goals, prior knowledge)
  ├─ 6. Present personalized learning path
  └─ 7. Ask: "Ready for your first lesson, or explore on your own?"
           │
           ├─ "Lesson" ──► concept-explainer (first module)
           │                    │
           │                    ▼
           │               lesson-flow (continues from here)
           │
           └─ "Explore" ──► session-router (free exploration mode)
```

## Trigger

- First interaction from a user with no existing profile
- User explicitly requests to start over

## Skills Used (in order)

1. **session-router** — Detects new user, routes to onboarding
2. **onboarding** — Runs the welcome, orientation, and calibration sequence
3. **level-classifier** — Assigns initial level based on calibration answers
4. **concept-explainer** OR **session-router** — First lesson or free exploration

## Data Flow

```
[No profile] → onboarding creates UserProfile
  → level-classifier sets level + dimensionScores
  → onboarding generates learningPath
  → Profile includes competency tracking across 4 practice types:
       ├─ Prompt Crafting
       ├─ Scenario Simulation
       ├─ Ethical Reasoning
       └─ Conceptual Application
  → [If on CollaborAITE] → merge available platform data (course context, peer activity)
  → Profile saved for all future sessions
```

## Scaffolding Pattern

When giving feedback during onboarding (e.g., on calibration answers), SAGE uses **ACKNOWLEDGE → NUDGE → EXPLAIN**:

1. **ACKNOWLEDGE**: Validate the user's input ("Good thought" / "Interesting perspective")
2. **NUDGE**: Pose a brief question or hint that guides toward deeper understanding
3. **EXPLAIN**: Provide the explanation or principle after the learner responds

## Duration

- Typical: 5-10 minutes
- Should feel like a conversation, not a registration form

## Success Criteria

- User has a complete profile with level, goals, prior knowledge, and competency baselines across 4 practice types
- User understands what SAGE does and how sessions work
- User has a visible learning path with 3-5 modules
- User has started their first activity (lesson or exploration)

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User skips calibration questions | Assign Novice by default, adapt based on subsequent interactions |
| User claims expert level but calibration suggests otherwise | Trust the calibration, not self-report. Frame diplomatically: "Let's start here and we can move quickly if this is too easy" |
| User wants to jump to a specific topic | Allow it — mark skipped modules as "skipped" not "completed", revisit if gaps emerge later |
| User returns after long absence | Offer abbreviated re-calibration: "Welcome back! Want a quick refresher, or pick up where you left off?" |
| CollaborAITE data unavailable | Proceed with self-reported data only; platform data is always optional |