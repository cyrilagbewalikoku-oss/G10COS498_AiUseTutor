# Workflow: Practice Flow

**Purpose**: Deep practice session focused on hands-on skill building through simulation, evaluation, and iterative improvement.

## Flow Diagram

```
session-router (detects: practice request or curriculum practice phase)
  │
  ▼
difficulty-adapter (calibrate scenario difficulty)
  │
  ▼
scenario-runner
  ├─ Load scenario matched to level + learning objectives
  ├─ User interacts with simulated agent (3-10 turns)
  ├─ Track: prompt quality, verification behavior, iteration
  └─ Capture full interaction log
       │
       ▼
skill-evaluator (score the interaction)
  ├─ Analyze prompts (CRAFT dimensions)
  ├─ Analyze output evaluation behavior
  └─ Analyze ethical awareness
       │
       ▼
reflection-facilitator
  ├─ Replay key moments from the log
  ├─ User self-assesses, tutor adds perspective
  ├─ Connect to named principles
  └─ Identify transferable lessons
       │
       ▼
improvement-advisor (targeted next steps)
  ├─ Prioritize gaps by user goals
  ├─ Suggest immediate mini-exercise
  └─ Update practice plan
       │
       ▼
[OPTIONAL: Advanced+ users only]
bad-agent-simulator
  ├─ User practices detecting flawed AI behavior
  ├─ Score detection ability
  └─ Debrief on flaw patterns
       │
       ▼
progress-reporter (session summary)
```

## Skills Used (in order)

1. **session-router** — Routes to practice flow
2. **difficulty-adapter** — Sets appropriate challenge level
3. **scenario-runner** — Core practice simulation (3-10 turns)
4. **skill-evaluator** — Evaluates the practice session
5. **reflection-facilitator** — Guided debrief
6. **improvement-advisor** — Targeted improvement plan
7. **bad-agent-simulator** (optional) — Adversarial detection practice
8. **progress-reporter** — Session wrap-up

## Duration

- Typical: 20-35 minutes
- Scenario: 10-15 minutes
- Evaluation + Reflection: 5-10 minutes
- Bad agent simulator (if included): 5-10 minutes

## Scenario Selection Logic

| User Level | Scenario Complexity | Example |
|-----------|-------------------|---------|
| Novice | Simple, single-task | "Use AI to draft an email to a parent" |
| Practitioner | Multi-step, professional | "Use AI to analyze survey data and create a report" |
| Advanced | Complex, multi-tool | "Use AI to review code, identify bugs, and suggest architecture changes" |
| Critical Thinker | Ambiguous, high-stakes | "Use AI to synthesize conflicting research findings for a policy brief" |

## Success Criteria

- User completes the scenario (or demonstrates why they chose to stop)
- User's prompts show measurable improvement from session start to end
- User engages meaningfully with reflection (not just "it was fine")
- At least one specific improvement area identified with action plan
