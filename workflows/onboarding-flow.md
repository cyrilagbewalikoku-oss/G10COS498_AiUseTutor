# Workflow: Onboarding Flow

**Purpose**: Guide a new user from first contact through level assessment to their first lesson.

## Flow Diagram

```
User arrives
  │
  ▼
session-router (detects: new user, no profile)
  │
  ▼
onboarding
  ├─ 1. Welcome + explain tutor's purpose
  ├─ 2. Ask 3-5 calibration questions
  ├─ 3. ──► level-classifier (assign initial level)
  ├─ 4. Present personalized learning path
  └─ 5. Ask: "Ready for your first lesson, or explore on your own?"
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
2. **onboarding** — Runs the welcome and calibration sequence
3. **level-classifier** — Assigns initial level based on calibration answers
4. **concept-explainer** OR **session-router** — First lesson or free exploration

## Data Flow

```
[No profile] → onboarding creates UserProfile
  → level-classifier sets level + dimensionScores
  → onboarding generates learningPath
  → Profile saved for all future sessions
```

## Duration

- Typical: 5-10 minutes
- Should feel like a conversation, not a registration form

## Success Criteria

- User has a complete profile with level, goals, and prior knowledge
- User understands what the tutor does and how sessions work
- User has a visible learning path with 3-5 modules
- User has started their first activity (lesson or exploration)

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User skips calibration questions | Assign Novice by default, adapt based on subsequent interactions |
| User claims expert level but calibration suggests otherwise | Trust the calibration, not self-report. Frame diplomatically: "Let's start here and we can move quickly if this is too easy" |
| User wants to jump to a specific topic | Allow it — mark skipped modules as "skipped" not "completed", revisit if gaps emerge later |
| User returns after long absence | Offer abbreviated re-calibration: "Welcome back! Want a quick refresher, or pick up where you left off?" |
