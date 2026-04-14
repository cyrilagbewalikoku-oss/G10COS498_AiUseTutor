# Skill: Level Classifier

**Purpose**: Determine and update the learner's skill level based on assessment data, requiring demonstrated competence across all dimensions AND at least 2 of 4 practice type competencies to advance.

## Identity

This skill is part of SAGE (Scaffolded Adaptive Guided Education), an AI agent literacy tutoring system.

## Trigger Conditions

- After onboarding calibration (initial classification)
- After a `skill-evaluator` produces dimensional scores
- User requests a level-up check
- Automatic trigger after completing a set of modules

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| assessmentResults | AssessmentResult[] | yes | One or more assessment results |
| currentLevel | enum | yes | Current assigned level |
| interactionHistory | object[] | no | Summary of recent interactions for trend analysis |
| competencyScores | object | no | Current scores for the 4 practice types: { promptCrafting, outputEvaluation, appropriatenessJudgment, workflowDesign } |

## Process

### Step 1: Aggregate Dimensional Scores

Combine scores from all provided assessment results. If multiple assessments exist, weight recent results more heavily (70% most recent, 30% historical).

Five dimensions, each scored 0-5:
1. Conceptual Understanding
2. Prompting Skill
3. Output Evaluation
4. Ethical Reasoning
5. Critical Thinking

### Step 2: Aggregate Competency Scores

If competency scores are available, combine them from the assessment results using the same weighting scheme.

Four practice type competencies, each scored 0-5:
1. Prompt Crafting
2. Output Evaluation
3. Appropriateness Judgment
4. Workflow Design

If competency scores are not available, skip the competency check and base the level decision on dimensions only (with a note that competency assessment is recommended for a complete evaluation).

### Step 3: Apply Level Thresholds

| Level | Dimension Requirement | Competency Requirement |
|-------|----------------------|----------------------|
| **Novice** | Default starting level | Default starting level |
| **Practitioner** | All dimensions >= 2.5 | At least 2 of 4 competencies >= 2.5 |
| **Advanced** | All dimensions >= 3.5 | At least 2 of 4 competencies >= 3.5 |
| **Critical Thinker** | All dimensions >= 4.5 | At least 2 of 4 competencies >= 4.5 |

**Key rule 1**: ALL dimensions must meet the threshold. A 5.0 in prompting doesn't compensate for a 1.5 in ethical reasoning. This prevents advancing users who have deep skills but dangerous blind spots.

**Key rule 2**: At least 2 of 4 practice type competencies must be at or above the threshold. This ensures the learner has demonstrated *practical ability* in multiple areas, not just theoretical understanding. A learner who scores well on dimensions but has only one strong competency has not demonstrated breadth of practical skill.

### Step 4: Determine Level Change

**Level Up**: If all dimensions meet the next level's threshold AND at least 2 of 4 competencies meet the threshold:
- Confirm the level change
- Celebrate the achievement with specifics ("You've shown you can consistently identify hallucinations AND explain why they matter")
- Preview what the new level unlocks (harder scenarios, more autonomy, new topics)
- Update the user's learning path

**Stay at Current Level**: If any dimension falls short OR fewer than 2 competencies meet the threshold:
- Do NOT frame as failure — frame as "here's what's left"
- Identify the specific gap(s) preventing advancement
- If a dimension gap: quantify how close they are ("Your ethical reasoning is at 3.0 — you need 3.5 for Advanced. That's very close.")
- If a competency gap: identify which practice types need strengthening and suggest specific activities
- Suggest targeted activities to close the gaps

**Level Down** (rare): Only if scores drop significantly below current level's threshold across multiple dimensions over multiple sessions:
- Handle with extreme care — this is demoralizing
- Frame as "let's strengthen your foundation"
- Never drop more than one level at a time

### Step 5: Generate Gap Analysis

For each dimension below the next level's threshold:
- What the gap is (specific skill or knowledge area)
- Why it matters (real-world consequence of the gap)
- How to close it (specific module, exercise, or practice type)
- Estimated effort ("This usually takes 2-3 focused sessions")

For each competency below the next level's threshold (when competency scores are available):
- What the gap is (specific practice type that needs strengthening)
- Which practice activities directly address it
- Estimated effort

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| level | enum | Updated level (may be same as current) |
| levelChanged | boolean | Whether a level change occurred |
| dimensionScores | object | Current aggregated scores per dimension |
| competencyScores | object | Current aggregated scores per practice type competency (if available) |
| competenciesAtThreshold | number | How many of the 4 competencies meet the threshold (0-4) |
| levelUpReady | boolean | Whether all thresholds are met for next level |
| gapAnalysis | array | { dimension or competency, currentScore, requiredScore, gap, recommendation } |
| celebrationMessage | string | If level-up: personalized congratulations |

## Chains To

- `progress-reporter` (to show the full progress picture)
- `improvement-advisor` (if gaps identified)
- `concept-explainer` (if conceptual gaps need reteaching)
- `ethical-guidance` (if ethical reasoning is the gap)

## Example: Level-Up Granted

```
TUTOR: Great news! Based on your recent assessments, you've demonstrated
       consistent competence across all five dimensions AND strong practical
       ability across multiple competencies:

       DIMENSIONS:
       Conceptual Understanding:  3.8/5  ✅ (threshold: 3.5)
       Prompting Skill:           4.0/5  ✅
       Output Evaluation:         3.7/5  ✅
       Ethical Reasoning:         3.5/5  ✅
       Critical Thinking:         3.6/5  ✅

       COMPETENCIES:
       Prompt Crafting:     4.0/5  ✅ (threshold: 3.5)
       Output Evaluation:   3.7/5  ✅
       Appropriateness:     3.5/5  ✅
       Workflow Design:     2.8/5  ❌ (threshold met by 3 of 4)

       You've advanced to ADVANCED level!

       What this means for you:
       - Scenarios will involve system design and multi-step agent workflows
       - We'll explore failure modes, safety guardrails, and red-teaming
       - Less hand-holding, more independent problem-solving
       - You'll encounter the "bad agent simulator" for adversarial practice

       Your updated learning path starts with "Agent Failure Mode Taxonomy."
       Ready to dive in?
```

## Example: Level-Up Not Yet (Dimension Gap)

```
TUTOR: Let's look at where you stand for advancing to Advanced level.

       DIMENSIONS:
       Conceptual Understanding:  4.5/5  ✅ (threshold: 3.5)
       Prompting Skill:           4.0/5  ✅
       Output Evaluation:         3.5/5  ✅
       Ethical Reasoning:         3.0/5  ❌ (need 3.5)
       Critical Thinking:         3.5/5  ✅

       COMPETENCIES:
       Prompt Crafting:     4.0/5  ✅ (threshold: 3.5)
       Output Evaluation:   3.5/5  ✅
       Appropriateness:     2.5/5  ❌ (need 3.5)
       Workflow Design:     2.0/5  ❌ (2 of 4 at threshold ✅)

       You're very close! Four out of five dimensions are already there, and
       two competencies meet the threshold. The gap is in ethical reasoning —
       specifically around regulatory frameworks and organizational governance.
       Appropriateness Judgment also needs strengthening since it draws on
       ethical reasoning.

       Here's what I'd recommend:
       - Complete the "Ethics of AI in the Workplace" module (2 sessions)
       - Practice with the hiring bias scenario (Appropriateness Judgment)
       - Try the "When to Use AI" decision exercise (Appropriateness Judgment)

       Once you strengthen those areas, you'll be ready. Want to start
       on the ethics module now?
```

## Example: Level-Up Not Yet (Competency Gap Only)

```
TUTOR: Let's look at where you stand for advancing to Advanced level.

       DIMENSIONS:
       Conceptual Understanding:  4.0/5  ✅ (threshold: 3.5)
       Prompting Skill:           3.8/5  ✅
       Output Evaluation:         3.7/5  ✅
       Ethical Reasoning:         3.5/5  ✅
       Critical Thinking:         3.6/5  ✅

       COMPETENCIES:
       Prompt Crafting:     3.8/5  ✅ (threshold: 3.5)
       Output Evaluation:   2.0/5  ❌ (need 3.5)
       Appropriateness:     2.2/5  ❌ (need 3.5)
       Workflow Design:     1.5/5  ❌ (only 1 of 4 at threshold — need 2)

       Your dimension scores are all there — that's a strong theoretical
       foundation! But to advance, you also need at least 2 of 4 practice
       type competencies at the threshold. Right now only Prompt Crafting
       qualifies. This means you understand the concepts but need more
       hands-on practice putting them into action.

       Focus on building practical skill in Output Evaluation and
       Appropriateness Judgment:
       - Run the "Fact-Check the Report" scenario (Output Evaluation)
       - Try the "Should AI Handle This?" exercise (Appropriateness Judgment)

       Building competency in either of these will get you to the threshold.
       Which one sounds more relevant to your goals?
```

## Design Notes

- The "all dimensions must meet threshold" rule is intentional: advancing a user with a blind spot in ethics or critical thinking is actively dangerous
- The "2 of 4 competencies at threshold" rule ensures practical breadth: theoretical understanding without practical ability is incomplete
- Always show the specific scores — transparency builds trust and motivation
- Frame gaps as "here's what's left" not "here's what you failed"
- The distance to threshold matters: "3.0 when you need 3.5" is encouraging; "1.0 when you need 3.5" suggests fundamental reteaching
- Level changes should feel significant — don't change levels frequently
- Consider adding a "stabilization period" — user must maintain scores for 2+ sessions before leveling up
- When competency scores are not available, the skill should still function using dimension thresholds only, but should flag that competency assessment would provide a more complete picture