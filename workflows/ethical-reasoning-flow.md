# Workflow: Ethical Reasoning Flow

**Purpose**: Dedicated ethics module that builds ethical reasoning skills through case study analysis, Socratic dialogue, and reflective practice.

## Platform Context

SAGE operates within the CollaborAITE platform. When a user @mentions SAGE on CollaborAITE, optional data sources (course ethics requirements, peer discussions, institutional policies) may be available to enrich ethical context. SAGE uses CollaborAITE data only when present; all functionality works without it.

## Flow Diagram

```
session-router (detects: ethics topic or scheduled ethics module)
  │
  ▼
ethical-guidance
  ├─ 1. Present case study with realistic context and pressure
  ├─ 2. Socratic questioning sequence (ACKNOWLEDGE → NUDGE → EXPLAIN pattern)
  │     ├─ ACKNOWLEDGE learner's initial stance
  │     ├─ NUDGE: "What could go wrong?"
  │     ├─ Learner responds
  │     ├─ EXPLAIN: Name the principle the learner touched on
  │     ├─ NUDGE: "Who is affected?"
  │     ├─ Learner responds
  │     ├─ EXPLAIN: Surface the stakeholder framework
  │     ├─ NUDGE: "What would you do differently?"
  │     └─ Learner responds → EXPLAIN: Connect to ethical framework principles
  ├─ 3. User articulates their position
  ├─ 4. Escalate with realistic pushback
  │     └─ "Your boss says just add a disclaimer..."
  ├─ 5. User revises or defends position
  ├─ 6. Introduce ethical framework principles
  │     └─ Name the principles the user applied
  ├─ 7. User commits to a specific behavior change
  │
  ├─ [OPTIONAL: Advanced+ learners]
  │   "Challenge the Agent" exercise
  │     ├─ Learner picks a stance SAGE defended and argues against it
  │     ├─ SAGE defends its reasoning; learner practices finding weaknesses
  │     ├─ SAGE reveals any genuine gaps in its own position
  │     └─ Debrief: even AI agents have blind spots — what were SAGE's?
  │
  ▼
single closing reflection question
  └─ "What is one way your own AI use will change after this?"
       │
       ▼
knowledge-check (ethical reasoning questions: 2-3)
  ├─ Scenario-based questions testing ethical reasoning
  ├─ No "right answer" format — evaluate reasoning quality
  └─ Feedback focuses on reasoning process, not conclusions
       │
       ▼
progress-reporter
  └─ Update ethical reasoning dimension score + Ethical Reasoning competency
```

## Skills Used (in order)

1. **session-router** — Routes to ethics flow
2. **ethical-guidance** — Core Socratic exploration (15-20 minutes)
3. **Single closing reflection** — One reflection question
4. **knowledge-check** — Ethical reasoning assessment (5 minutes)
5. **progress-reporter** — Update scores and suggest next steps

## Duration

- Typical: 20-30 minutes
- Case study + Socratic dialogue: 15-20 minutes
- Closing reflection + assessment: 5-10 minutes
- Challenge the agent (if included): adds 5-10 minutes

## Case Study Selection by Level

| Level | Case Complexity | Example |
|-------|----------------|---------|
| Novice | Clear stakeholders, personal impact | "Should you submit an AI-written essay as your own?" |
| Practitioner | Professional context, competing pressures | "Should you disclose AI use in client marketing content?" |
| Advanced | System-level, organizational impact | "Your company's AI hiring tool shows demographic bias. What do you do?" |
| Critical Thinker | Institutional/policy, no clear right answer | "Design an AI use policy for a research institution. What principles guide you?" |

## Scaffolding Pattern: Socratic Dialogue as ACKNOWLEDGE → NUDGE → EXPLAIN

The Socratic questioning sequence in ethical-guidance is structured as repeated ACKNOWLEDGE → NUDGE → EXPLAIN cycles:

1. **ACKNOWLEDGE**: Validate the learner's current position or reasoning ("That's a reasonable starting point" / "You're thinking about impact on the user")
2. **NUDGE**: Pose a Socratic question that extends or challenges their thinking ("But what about...?" / "Who else might be affected?")
3. **EXPLAIN**: After the learner responds, name the ethical principle or framework they touched on ("That's actually the principle of transparency" / "You've identified a stakeholder conflict")

This pattern ensures the learner does the reasoning work before SAGE names the concept.

## Challenge the Agent (Advanced+ Learners Only)

When a learner is at Advanced or Critical Thinker level, SAGE offers the "Challenge the Agent" exercise:

- **Setup**: SAGE summarizes its own position on an ethical question from the session
- **Challenge**: The learner argues against SAGE's position
- **Defense**: SAGE defends its reasoning; the learner probes for weaknesses
- **Reveal**: SAGE identifies genuine gaps or limitations in its own position
- **Debrief**: "Even AI agents have blind spots. What were mine in this case?"

This exercise teaches that:
- AI agents (including SAGE) have training-based biases and blind spots
- Ethical reasoning requires challenging authority, not just accepting it
- The best defense of a position comes from surviving challenges

## What Makes This Flow Different

Unlike other flows, ethical reasoning has no "correct answer." The assessment evaluates:
- **Reasoning quality**: Did the user consider multiple stakeholders?
- **Principle application**: Did they apply ethical frameworks (even implicitly)?
- **Pressure resilience**: Did they maintain their position under pushback, or revise thoughtfully?
- **Action orientation**: Did they commit to a specific behavior change?

## Success Criteria

- User engaged with at least 2 Socratic questions substantively (not one-word answers)
- User articulated a position and defended or thoughtfully revised it under pressure
- User identified at least one ethical principle by name or description
- User committed to a specific, actionable behavior change
- User answered the closing reflection question substantively
- Ethical reasoning dimension score and competency updated in profile