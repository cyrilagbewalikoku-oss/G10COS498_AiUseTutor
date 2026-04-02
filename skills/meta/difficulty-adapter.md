# Skill: Difficulty Adapter

**Purpose**: Dynamically adjust content complexity and scaffolding based on the learner's recent performance within a session.

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

## Process

### Step 1: Calculate Rolling Performance
Look at the last 5 scored interactions:
- Calculate success rate (fraction of scores >= 0.7)
- Identify streaks (consecutive successes or failures)
- Weight recent interactions more heavily (last 2 count double)

### Step 2: Detect Trend and Adjust

| Pattern | Signal | Adjustment |
|---------|--------|------------|
| 3+ successes in a row | Learner is ready for more challenge | Increase complexity (+0.5) |
| 2+ failures in a row | Learner is struggling | Decrease complexity (-0.5), add scaffolding |
| Mixed results | Learner is at appropriate level | No change (0) |
| First interaction (no history) | Unknown | Default to level baseline |

### Step 3: Apply Level-Specific Guidelines

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

### Step 4: Generate Scaffolding Hints
If complexity was decreased, generate 1-2 hints for the calling skill:
- "Remind the user of the CRAFT framework before asking them to write a prompt"
- "Reference the hallucination example from the previous lesson"
- "Break the task into two smaller steps"

### Step 5: Set Vocabulary Guidelines
Based on adjusted level, specify:
- **canUse**: Terms the user has demonstrated understanding of
- **introduce**: Terms to use with brief definitions
- **avoid**: Terms too advanced for current adjusted level

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| adjustedLevel | string | May differ from base level by +-0.5 |
| complexityModifier | number | -1 to +1, applied to content generation |
| scaffoldingHints | string[] | Hints for the calling skill if decreasing |
| vocabularyGuidelines | object | { canUse: [], introduce: [], avoid: [] } |

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

Output:
  adjustedLevel: "practitioner+0.5"
  complexityModifier: 0.5
  scaffoldingHints: []
  vocabularyGuidelines: {
    canUse: ["hallucination", "prompt engineering", "chain-of-thought", "few-shot"],
    introduce: ["task decomposition", "self-consistency", "constitutional AI"],
    avoid: ["RLHF specifics", "attention mechanism", "transformer architecture"]
  }

Effect: Next question will be multi-part analysis rather than 
straightforward application, using slightly more advanced vocabulary.
```

## Design Notes

- This skill should be invisible to the user — they should feel the tutor naturally adapting, not see explicit difficulty changes
- Never drop difficulty too aggressively — one failure might be a bad question, not a competence issue
- The 3-success-streak threshold prevents premature difficulty increase from lucky guesses
- Vocabulary guidelines prevent the tutor from either talking down to or over the head of the learner
- Track difficulty adjustments over time: if a user consistently needs -0.5 at their current level, consider whether their level classification is wrong
