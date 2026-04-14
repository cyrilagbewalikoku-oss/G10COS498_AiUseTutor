# Skill: Skill Evaluator

**Purpose**: Evaluate a learner's practical ability by analyzing their interaction logs from practice sessions across multiple competency dimensions and practice types, including assessment of how well the learner responds to scaffolding.

## Identity

This skill is part of SAGE (Scaffolded Adaptive Guided Education), an AI agent literacy tutoring system.

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
| scaffoldingLog | Array<{ nudge: string, learnerResponse: string, responseType: enum("reflective", "surface", "none") }> | no | Record of scaffolding nudges and how the learner responded |

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

### Step 4: Evaluate Practice Type Competencies

Score the learner across the 4 practice types, drawing evidence from Steps 1-3:

| Practice Type | Score 1 | Score 3 | Score 5 |
|---|---------|---------|---------|
| **Prompt Crafting** | Wrote vague, context-free prompts; accepted first output | Added some context and constraints; iterated once | Used CRAFT consistently; iterated with targeted improvements; handled edge cases |
| **Output Evaluation** | Accepted all AI output without question | Checked some claims for accuracy | Systematically verified facts, detected errors, assessed quality and completeness |
| **Appropriateness Judgment** | Used AI for every task without considering suitability | Paused on some clearly inappropriate use cases | Proactively evaluated when AI is suitable, considered ethical and practical trade-offs |
| **Workflow Design** | No verification or human-in-the-loop steps | Added basic verification steps | Designed reliable human-AI patterns with checkpoints, fallbacks, and oversight |

### Step 5: Evaluate Scaffolding Effectiveness

Assess how the learner responded to scaffolding nudges during the session:

| Criterion | Score 1 | Score 3 | Score 5 |
|-----------|---------|---------|---------|
| Self-reflection | Gave short answers with no insight when nudged | Reflected briefly before responding | Nudges prompted genuine reflection and new insight |
| Self-correction | Did not adjust approach when nudged toward a gap | Partially adjusted approach | Actively changed approach based on scaffolding feedback |

This evaluation informs the difficulty-adapter: if the learner is not responding to nudges, the calling skill should increase scaffolding (more analogies, smaller steps, more explicit guidance).

### Step 6: Generate Dimensional Scores

Aggregate scores across the analysis areas into five dimensions:

1. **Conceptual Understanding** (derived from how they described their thinking)
2. **Prompting Skill** (from Step 1 analysis)
3. **Output Evaluation** (from Step 2 analysis)
4. **Ethical Reasoning** (from Step 3 analysis)
5. **Critical Thinking** (composite of Steps 2 and 3)

### Step 7: Produce Evaluation Report

Structure the report as:
1. Overall assessment (1-2 sentences)
2. Dimensional scores
3. Competency scores (4 practice types)
4. Scaffolding response assessment
5. Strengths with specific evidence from the interaction
6. Growth areas with specific evidence and recommendations
7. Comparison to previous evaluation (if available)

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| dimensionScores | object | { conceptualUnderstanding, promptingSkill, outputEvaluation, ethicalReasoning, criticalThinking } each 0-5 |
| competencyScores | object | { promptCrafting, outputEvaluation, appropriatenessJudgment, workflowDesign } each 0-5 |
| scaffoldingResponse | object | { selfReflection: 0-5, selfCorrection: 0-5, summary: string } |
| overallAssessment | string | 1-2 sentence summary |
| strengths | array | { dimension or competency, evidence, score } |
| growthAreas | array | { dimension or competency, evidence, score, recommendation } |
| levelRecommendation | string | Whether level change is suggested |

## Chains To

- `level-classifier` (to determine if level change is warranted)
- `reflection-facilitator` (to discuss the evaluation with the learner)
- `improvement-advisor` (if growth areas identified)
- `difficulty-adapter` (to inform scaffolding adjustments based on learner response)

## Example Evaluation Output

```
EVALUATION SUMMARY: Priya demonstrates strong prompting skills and good 
instincts for output evaluation, but consistently overlooks ethical 
implications of AI-generated content in professional contexts. She 
responded to scaffolding nudges with reflection on prompting but gave 
surface responses on ethics-related nudges.

DIMENSIONAL SCORES:
- Conceptual Understanding: 3.5/5
- Prompting Skill: 4.0/5
- Output Evaluation: 3.5/5
- Ethical Reasoning: 2.0/5
- Critical Thinking: 2.5/5

COMPETENCY SCORES:
- Prompt Crafting: 4.0/5
- Output Evaluation: 3.5/5
- Appropriateness Judgment: 2.0/5
- Workflow Design: 2.0/5

SCAFFOLDING RESPONSE:
- Self-reflection: 3.0/5 [engaged with prompting nudges, surface on ethics]
- Self-correction: 2.0/5 [adjusted prompts but did not address ethical gaps]

STRENGTHS:
- Prompt Crafting (4.0/5): Used CRAFT framework consistently. Added constraints 
  for ambiguous data. Iterated twice with targeted improvements.
  Evidence: Turn 3 — revised prompt added brand voice guidelines and 
  formatting constraints.

- Output Evaluation (3.5/5): Caught the fabricated statistic in the 
  marketing copy. Questioned the source attribution.
  Evidence: Turn 5 — "Wait, did we actually get that Consumer Reports 
  rating? I should verify that."

GROWTH AREAS:
- Appropriateness Judgment (2.0/5): Did not consider disclosure to clients 
  about AI-generated content. Did not flag potential FTC issues with 
  unverified claims.
  Evidence: Turns 6-8 — proceeded to finalize copy with fabricated 
  endorsement without raising transparency concerns.
  Recommendation: Complete "Ethics of AI-Generated Content" module.

- Workflow Design (2.0/5): No verification checkpoints or fallback steps 
  in the content creation workflow.
  Recommendation: Practice with workflow design scenarios that require 
  human-in-the-loop patterns.

SCAFFOLDING NOTE: Learner responds well to technical nudges but gives 
surface responses to ethical ones. Consider increasing scaffolding for 
ethics-related topics: add more analogies, break into smaller steps, 
use relatable real-world examples.
```

## Design Notes

- Always ground evaluations in specific evidence from the interaction log
- Never surprise the user with a low score — the `reflection-facilitator` should help them see it first
- Evaluations should feel like coaching, not grading
- Weight dimensions differently based on the user's goals (a developer cares more about prompting; a manager cares more about evaluation)
- Track evaluations over time to show improvement trajectories
- Practice type competencies make evaluation actionable: they tell the learner *what kind of practice* they need, not just which abstract dimension is weak
- Scaffolding effectiveness data feeds directly to difficulty-adapter: if the learner is not reflecting, the system needs to increase scaffolding, not just repeat the same nudge
- Surface responses to nudges are a signal, not a failure — they indicate the scaffolding approach needs adjustment, not that the learner is resistant