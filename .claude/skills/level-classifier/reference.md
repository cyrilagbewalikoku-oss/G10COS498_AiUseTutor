# Skill: Level Classifier

**Purpose**: Determine and update the learner's skill level based on assessment data, requiring demonstrated competence across all dimensions to advance.

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

## Process

### Step 1: Aggregate Dimensional Scores

Combine scores from all provided assessment results. If multiple assessments exist, weight recent results more heavily (70% most recent, 30% historical).

Five dimensions, each scored 0-5:
1. Conceptual Understanding
2. Prompting Skill
3. Output Evaluation
4. Ethical Reasoning
5. Critical Thinking

### Step 2: Apply Level Thresholds

| Level | Requirement | Description |
|-------|-------------|-------------|
| **Novice** | Default starting level | Any score distribution |
| **Practitioner** | All dimensions >= 2.5 | Consistent baseline competence across all areas |
| **Advanced** | All dimensions >= 3.5 | Strong skills with no major blind spots |
| **Critical Thinker** | All dimensions >= 4.5 | Expert-level across all dimensions |

**Key rule**: ALL dimensions must meet the threshold. A 5.0 in prompting doesn't compensate for a 1.5 in ethical reasoning. This prevents advancing users who have deep skills but dangerous blind spots.

### Step 3: Determine Level Change

**Level Up**: If all dimensions meet the next level's threshold:
- Confirm the level change
- Celebrate the achievement with specifics ("You've shown you can consistently identify hallucinations AND explain why they matter")
- Preview what the new level unlocks (harder scenarios, more autonomy, new topics)
- Update the user's learning path

**Stay at Current Level**: If any dimension falls short:
- Do NOT frame as failure — frame as "here's what's left"
- Identify the specific gap(s) preventing advancement
- Quantify how close they are ("Your ethical reasoning is at 3.0 — you need 3.5 for Advanced. That's very close.")
- Suggest targeted activities to close the gap

**Level Down** (rare): Only if scores drop significantly below current level's threshold across multiple dimensions over multiple sessions:
- Handle with extreme care — this is demoralizing
- Frame as "let's strengthen your foundation"
- Never drop more than one level at a time

### Step 4: Generate Gap Analysis

For each dimension below the next level's threshold:
- What the gap is (specific skill or knowledge area)
- Why it matters (real-world consequence of the gap)
- How to close it (specific module, exercise, or practice type)
- Estimated effort ("This usually takes 2-3 focused sessions")

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| level | enum | Updated level (may be same as current) |
| levelChanged | boolean | Whether a level change occurred |
| dimensionScores | object | Current aggregated scores per dimension |
| levelUpReady | boolean | Whether all thresholds are met for next level |
| gapAnalysis | array | { dimension, currentScore, requiredScore, gap, recommendation } |
| celebrationMessage | string | If level-up: personalized congratulations |

## Chains To

- `progress-reporter` (to show the full progress picture)
- `improvement-advisor` (if gaps identified)
- `concept-explainer` (if conceptual gaps need reteaching)
- `ethical-guidance` (if ethical reasoning is the gap)

## Example: Level-Up Granted

```
TUTOR: Great news! Based on your recent assessments, you've demonstrated 
       consistent competence across all five dimensions:
       
       Conceptual Understanding:  3.8/5  ✅ (threshold: 3.5)
       Prompting Skill:           4.0/5  ✅
       Output Evaluation:         3.7/5  ✅
       Ethical Reasoning:         3.5/5  ✅
       Critical Thinking:         3.6/5  ✅
       
       You've advanced to ADVANCED level!
       
       What this means for you:
       - Scenarios will involve system design and multi-step agent workflows
       - We'll explore failure modes, safety guardrails, and red-teaming
       - Less hand-holding, more independent problem-solving
       - You'll encounter the "bad agent simulator" for adversarial practice
       
       Your updated learning path starts with "Agent Failure Mode Taxonomy."
       Ready to dive in?
```

## Example: Level-Up Not Yet

```
TUTOR: Let's look at where you stand for advancing to Advanced level.
       
       Conceptual Understanding:  4.5/5  ✅ (threshold: 3.5)
       Prompting Skill:           4.0/5  ✅
       Output Evaluation:         3.5/5  ✅
       Ethical Reasoning:         3.0/5  ❌ (need 3.5)
       Critical Thinking:         3.5/5  ✅
       
       You're very close! Four out of five dimensions are already there. 
       The gap is in ethical reasoning — specifically around regulatory 
       frameworks and organizational governance.
       
       Here's what I'd recommend:
       - Complete the "Ethics of AI in the Workplace" module (2 sessions)
       - Practice with the hiring bias scenario (applies ethical frameworks 
         under realistic pressure)
       
       Once you strengthen that area, you'll be ready. Want to start 
       on the ethics module now?
```

## Design Notes

- The "all dimensions must meet threshold" rule is intentional: advancing a user with a blind spot in ethics or critical thinking is actively dangerous
- Always show the specific scores — transparency builds trust and motivation
- Frame gaps as "here's what's left" not "here's what you failed"
- The distance to threshold matters: "3.0 when you need 3.5" is encouraging; "1.0 when you need 3.5" suggests fundamental reteaching
- Level changes should feel significant — don't change levels frequently
- Consider adding a "stabilization period" — user must maintain scores for 2+ sessions before leveling up
