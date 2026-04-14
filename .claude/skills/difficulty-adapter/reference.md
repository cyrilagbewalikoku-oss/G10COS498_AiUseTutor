# Skill: Difficulty Adapter

**Purpose**: Dynamically adjust content complexity and scaffolding based on the learner's recent performance within a session, their response to scaffolding nudges, and (optionally) course context from CollaborAITE.

## Identity

This skill is part of SAGE (Scaffolded Adaptive Guided Education), an AI agent literacy tutoring system.

## Trigger Conditions

- Called internally by other skills when generating content, questions, or scenarios
- Not directly triggered by user messages

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userLevel | enum | yes | novice, practitioner, advanced, critical_thinker |
| recentPerformance | array | yes | Last 5 interactions: { score (0-1), skill, timestamp } |
| contentType | enum | yes | explanation, question, scenario, feedback |
| currentModuleId | string | no | Current module for context |
| scaffoldingResponse | object | no | { avgSelfReflection: 0-5, avgSelfCorrection: 0-5, trend: enum } from skill-evaluator |
| collaborAITEContext | object | no | { courseLevel: string, upcomingAssignments: string[], timePressure: boolean, enrollmentDetails: object } |

## Process

### Step 1: Calculate Rolling Performance
Look at the last 5 scored interactions:
- Calculate success rate (fraction of scores >= 0.7)
- Identify streaks (consecutive successes or failures)
- Weight recent interactions more heavily (last 2 count double)

### Step 2: Assess Scaffolding Response

If scaffolding response data is available from skill-evaluator:
- **avgSelfReflection < 2.5**: Learner is not engaging with reflective nudges. Increase scaffolding: add analogies, break into smaller steps, make guidance more explicit.
- **avgSelfCorrection < 2.5**: Learner is not adjusting approach when nudged. Increase scaffolding: make the gap more visible, provide worked examples of what adjustment looks like.
- **Both >= 3.0**: Learner is responding well to scaffolding. Maintain or slightly reduce scaffolding level.

Key signals from the interaction:
| Signal | Interpretation | Adjustment |
|--------|---------------|-----------|
| Short, surface answers to reflective prompts | Nudge not landing | Increase scaffolding: more analogies, smaller steps |
| No self-correction when nudged toward a gap | Gap not visible enough | Increase scaffolding: make connection explicit |
| Reflective, thoughtful responses to nudges | Scaffolding effective | Maintain current level |
| Learner asks clarifying questions after a nudge | Engagement present | Maintain — engagement is positive |

### Step 3: Detect Trend and Adjust

| Pattern | Signal | Adjustment |
|---------|--------|------------|
| 3+ successes in a row | Learner is ready for more challenge | Increase complexity (+0.5) |
| 2+ failures in a row | Learner is struggling | Decrease complexity (-0.5), add scaffolding |
| Mixed results | Learner is at appropriate level | No change (0) |
| First interaction (no history) | Unknown | Default to level baseline |
| Low scaffolding response (self-reflection < 2.5) | Nudges not working | Increase scaffolding (add analogies, smaller steps, more explicit guidance) |

### Step 4: Apply CollaborAITE Context (Optional)

If CollaborAITE data is available, consider:

| Context Signal | Adjustment |
|---|---|
| Introductory course | Lean toward simpler examples even at higher levels |
| Advanced seminar | Lean toward more challenging scenarios |
| Upcoming assignment on a specific topic | Adjust toward that topic's skill requirements |
| Time pressure (midterms, deadlines) | Reduce cognitive load, focus on essentials |
| Learner new to course | More scaffolding, slower pace |
| Learner near course end | Consolidate and integrate, slightly more challenge |

CollaborAITE context supplements performance data but never overrides it. If the learner is clearly struggling based on performance, increase scaffolding regardless of course context.

If no CollaborAITE data is available, skip this step entirely.

### Step 5: Apply Level-Specific Guidelines

**Novice** (complexityModifier applied):
| Content Type | Baseline | If +0.5 | If -0.5 |
|-------------|----------|---------|---------|
| Explanation | Analogy-first, no jargon | Introduce one technical term | Add more analogies, slower pace |
| Question | Recognition/recall | Simple application | Yes/no with explanation |
| Scenario | Single-step, everyday task | Two-step task | Guided walkthrough with hints |
| Feedback | Specific praise + one improvement | Two improvements | Only praise, save improvements for next time |

**Practitioner**:
| Content Type | Baseline | If +0.5 | If -0.5 |
|-------------|----------|---------|---------|
| Explanation | Technical terms with brief definitions | Terms without definitions | Add definitions and analogies |
| Question | Application/analysis | Multi-part analysis | Straightforward application |
| Scenario | Professional, multi-step | Add ethical wrinkle | Reduce steps, add hints |
| Feedback | Strengths + growth areas | Focus on growth areas | Focus on strengths |

**Advanced**:
| Content Type | Baseline | If +0.5 | If -0.5 |
|-------------|----------|---------|---------|
| Explanation | Full technical vocabulary | Edge cases and exceptions | Add more examples |
| Question | Evaluation/judgment | Novel scenario, no hints | Standard scenario with context |
| Scenario | Complex, multi-tool | Ambiguous constraints | Clearer constraints |
| Feedback | Peer-level critique | Challenge assumptions | More supportive tone |

**Critical Thinker**:
| Content Type | Baseline | If +0.5 | If -0.5 |
|-------------|----------|---------|---------|
| Explanation | Research-level, nuanced | Invite debate | Provide more structure |
| Question | Create/design | Open-ended, no scaffolding | Provide framework to apply |
| Scenario | High-stakes, ambiguous | Add time pressure | Remove one constraint |
| Feedback | Socratic, minimal | Only questions, no answers | Balance questions with observations |

### Step 6: Generate Scaffolding Hints
If complexity was decreased OR scaffolding response was low, generate 1-3 hints for the calling skill:
- "Remind the user of the CRAFT framework before asking them to write a prompt"
- "Reference the hallucination example from the previous lesson"
- "Break the task into two smaller steps"
- "Add an analogy: compare the concept to something from their everyday experience"
- "Instead of asking an open question, provide a partially completed example and ask them to finish it"
- "Make the connection to the gap more explicit: 'This is similar to the issue you noticed earlier about...'"

### Step 7: Set Vocabulary Guidelines
Based on adjusted level, specify:
- **canUse**: Terms the user has demonstrated understanding of
- **introduce**: Terms to use with brief definitions
- **avoid**: Terms too advanced for current adjusted level

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| adjustedLevel | string | May differ from base level by +-0.5 |
| complexityModifier | number | -1 to +1, applied to content generation |
| scaffoldingLevel | enum | "standard", "increased", "high" — how much scaffolding the calling skill should provide |
| scaffoldingHints | string[] | Hints for the calling skill if decreasing or if scaffolding response was low |
| vocabularyGuidelines | object | { canUse: [], introduce: [], avoid: [] } |
| contextAdjustment | string | Description of any CollaborAITE-informed adjustment (empty string if none) |

## Chains To

Returns to the calling skill (not standalone).

## Example

```
Input:
  userLevel: "practitioner"
  recentPerformance: [
    { score: 1.0, skill: "knowledge-check" },
    { score: 1.0, skill: "knowledge-check" },
    { score: 0.8, skill: "scenario-runner" }
  ]
  contentType: "question"
  scaffoldingResponse: { avgSelfReflection: 3.5, avgSelfCorrection: 3.0, trend: "stable" }
  collaborAITEContext: null

Output:
  adjustedLevel: "practitioner+0.5"
  complexityModifier: 0.5
  scaffoldingLevel: "standard"
  scaffoldingHints: []
  contextAdjustment: ""
  vocabularyGuidelines: {
    canUse: ["hallucination", "prompt engineering", "chain-of-thought", "few-shot"],
    introduce: ["task decomposition", "self-consistency", "constitutional AI"],
    avoid: ["RLHF specifics", "attention mechanism", "transformer architecture"]
  }

Effect: Next question will be multi-part analysis rather than
straightforward application, using slightly more advanced vocabulary.
Scaffolding remains at standard level since learner is engaging well.
```

## Example: Low Scaffolding Response

```
Input:
  userLevel: "practitioner"
  recentPerformance: [
    { score: 0.6, skill: "scenario-runner" },
    { score: 0.5, skill: "scenario-runner" },
    { score: 0.7, skill: "knowledge-check" }
  ]
  contentType: "scenario"
  scaffoldingResponse: { avgSelfReflection: 1.5, avgSelfCorrection: 2.0, trend: "declining" }
  collaborAITEContext: { courseLevel: "introductory", timePressure: false }

Output:
  adjustedLevel: "practitioner-0.5"
  complexityModifier: -0.5
  scaffoldingLevel: "high"
  scaffoldingHints: [
    "Break the scenario into two smaller steps with a checkpoint between them",
    "Add an analogy comparing the ethical decision to a familiar everyday situation",
    "Provide a partially completed analysis example and ask them to finish it",
    "Make the gap more explicit: 'Notice how this connects to the verification step you skipped earlier'"
  ]
  contextAdjustment: "Introductory course — lean toward simpler, more relatable examples"
  vocabularyGuidelines: {
    canUse: ["hallucination", "prompt engineering"],
    introduce: ["chain-of-thought", "few-shot"],
    avoid: ["task decomposition", "constitutional AI", "self-consistency"]
  }

Effect: Next scenario will be simplified with more hints. Scaffolding is
increased because the learner is giving surface responses to nudges.
Course context indicates introductory level, so examples should be
more everyday and relatable.
```

## Design Notes

- This skill should be invisible to the user — they should feel the tutor naturally adapting, not see explicit difficulty changes
- Never drop difficulty too aggressively — one failure might be a bad question, not a competence issue
- The 3-success-streak threshold prevents premature difficulty increase from lucky guesses
- Vocabulary guidelines prevent the tutor from either talking down to or over the head of the learner
- Track difficulty adjustments over time: if a user consistently needs -0.5 at their current level, consider whether their level classification is wrong
- **Scaffolding pattern awareness prevents the "nudge loop."** If a learner is not responding to nudges, repeating the same nudge harder doesn't help. Instead, change the scaffolding approach: switch from abstract to concrete, add analogies, break into smaller steps.
- **Surface answers are a signal, not a failure.** When a learner gives short answers to reflective prompts, it usually means the nudge wasn't concrete enough, not that the learner is resistant. Adjust the approach, not the learner.
- **CollaborAITE context is always optional.** The skill must work fully without it. When available, it supplements performance data — it never overrides it. A learner who is clearly struggling based on interaction data needs more scaffolding regardless of what the course context suggests.
- **Time pressure reduces cognitive load.** During high-stress periods (midterms, deadlines), simplify even if the learner's level would normally support more complexity. Focus on essentials and consolidation.