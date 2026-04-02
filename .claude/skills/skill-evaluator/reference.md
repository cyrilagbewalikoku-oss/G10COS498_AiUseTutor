# Skill: Skill Evaluator

**Purpose**: Evaluate a learner's practical ability by analyzing their interaction logs from practice sessions across multiple competency dimensions.

## Trigger Conditions

- Practice scenario completed (after `scenario-runner`)
- Level-up assessment flow
- User requests a skills evaluation

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| interactionLog | InteractionLog | yes | The full interaction transcript from practice |
| rubric | string | no | Specific rubric to apply (default: general) |
| userLevel | enum | yes | Current level for calibration |
| focusDimensions | string[] | no | Specific dimensions to prioritize |

## Process

### Step 1: Analyze Prompt Quality (CRAFT Dimensions)

Review every prompt the user wrote during the interaction:

| Criterion | Score 1 | Score 3 | Score 5 |
|-----------|---------|---------|---------|
| Context | No context provided | Some background given | Rich, relevant context that shapes the response |
| Specificity | Vague request | Moderately specific | Precise constraints, clear success criteria |
| Iteration | Accepted first output | Some revision | Systematic iteration with targeted improvements |
| Constraint handling | No constraints | Some constraints | Explicit handling of edge cases and missing data |

### Step 2: Analyze Output Evaluation Behavior

Examine how the user responded to AI-generated content:

| Criterion | Score 1 | Score 3 | Score 5 |
|-----------|---------|---------|---------|
| Verification | Accepted everything at face value | Questioned some claims | Systematically verified factual claims |
| Error detection | Missed obvious errors | Caught some issues | Identified subtle errors and fabrications |
| Critical assessment | No evaluation of quality | Some quality judgment | Assessed accuracy, completeness, and appropriateness |
| Source awareness | Treated AI as authoritative source | Some awareness of limitations | Clear understanding that AI output requires verification |

### Step 3: Analyze Ethical Awareness

Evaluate whether the user considered ethical dimensions during practice:

| Criterion | Score 1 | Score 3 | Score 5 |
|-----------|---------|---------|---------|
| Data sensitivity | Shared sensitive data freely | Some awareness of data risks | Proactively protected sensitive information |
| Disclosure | No consideration of transparency | Mentioned disclosure | Actively planned for AI use disclosure |
| Bias awareness | No bias consideration | Recognized obvious bias | Proactively checked for and addressed bias |
| Accountability | Deferred entirely to AI | Some human oversight | Clear human accountability for all outputs |

### Step 4: Generate Dimensional Scores

Aggregate scores across the three analysis areas into five dimensions:

1. **Conceptual Understanding** (derived from how they described their thinking)
2. **Prompting Skill** (from Step 1 analysis)
3. **Output Evaluation** (from Step 2 analysis)
4. **Ethical Reasoning** (from Step 3 analysis)
5. **Critical Thinking** (composite of Steps 2 and 3)

### Step 5: Produce Evaluation Report

Structure the report as:
1. Overall assessment (1-2 sentences)
2. Strengths with specific evidence from the interaction
3. Growth areas with specific evidence and recommendations
4. Comparison to previous evaluation (if available)

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| dimensionScores | object | { conceptualUnderstanding, promptingSkill, outputEvaluation, ethicalReasoning, criticalThinking } each 0-5 |
| overallAssessment | string | 1-2 sentence summary |
| strengths | array | { dimension, evidence, score } |
| growthAreas | array | { dimension, evidence, score, recommendation } |
| levelRecommendation | string | Whether level change is suggested |

## Chains To

- `level-classifier` (to determine if level change is warranted)
- `reflection-facilitator` (to discuss the evaluation with the learner)
- `improvement-advisor` (if growth areas identified)

## Example Evaluation Output

```
EVALUATION SUMMARY: Priya demonstrates strong prompting skills and good 
instincts for output evaluation, but consistently overlooks ethical 
implications of AI-generated content in professional contexts.

STRENGTHS:
- Prompting (4.0/5): Used CRAFT framework consistently. Added constraints 
  for ambiguous data. Iterated twice with targeted improvements.
  Evidence: Turn 3 — revised prompt added brand voice guidelines and 
  formatting constraints.

- Output Evaluation (3.5/5): Caught the fabricated statistic in the 
  marketing copy. Questioned the source attribution.
  Evidence: Turn 5 — "Wait, did we actually get that Consumer Reports 
  rating? I should verify that."

GROWTH AREAS:
- Ethical Reasoning (2.0/5): Did not consider disclosure to clients 
  about AI-generated content. Did not flag potential FTC issues with 
  unverified claims.
  Evidence: Turns 6-8 — proceeded to finalize copy with fabricated 
  endorsement without raising transparency concerns.
  Recommendation: Complete "Ethics of AI-Generated Content" module.

- Critical Thinking (2.5/5): Good at catching factual errors but did 
  not consider systemic implications (what if all marketing teams do this?).
  Recommendation: Practice with ethical-reasoning scenarios.
```

## Design Notes

- Always ground evaluations in specific evidence from the interaction log
- Never surprise the user with a low score — the `reflection-facilitator` should help them see it first
- Evaluations should feel like coaching, not grading
- Weight dimensions differently based on the user's goals (a developer cares more about prompting; a manager cares more about evaluation)
- Track evaluations over time to show improvement trajectories
