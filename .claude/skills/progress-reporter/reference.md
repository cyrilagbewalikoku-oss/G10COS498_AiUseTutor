# Progress Reporter

## Purpose

Give learners a clear picture of where they stand, what they've accomplished, and what's next. This skill translates raw assessment data into a motivating, honest, and actionable progress report that celebrates growth while surfacing areas for continued development. It avoids both false praise and discouraging framing.

## Identity

This skill is part of SAGE (Scaffolded Adaptive Guided Education), an AI agent literacy tutoring system.

## Trigger Conditions

- At the end of a tutoring session (automatic wrap-up)
- When the user explicitly asks "How am I doing?", "What's my progress?", or similar
- As part of a weekly or periodic summary
- After level-classifier completes a new classification
- When chained from reflection-facilitator with updated lesson data

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `userProfile` | `UserProfile { id: string, name: string, level: enum, goals: string[], profession: string, assessmentCount: number, firstSessionDate: string }` | Yes | The learner's profile including current level, goals, and demographic context |
| `assessmentHistory` | `Array<AssessmentResult { date: string, dimension: string, score: number, maxScore: number, notes: string }>` | Yes | All historical assessment scores across dimensions, used to compute trends and milestones |
| `interactionHistory` | `Array<{ sessionId: string, date: string, skillUsed: string, lessonsLearned: string[], principlesReinforced: string[], duration: number }>` | Yes | Record of all sessions and activities the learner has completed, including lessons and principles from reflection-facilitator |
| `competencyHistory` | `Array<{ date: string, practiceType: string, score: number }>` | No | Historical scores for the 4 practice types (Prompt Crafting, Output Evaluation, Appropriateness Judgment, Workflow Design) |

## Process

1. **Generate dimension progress display.** Compute current scores for each of the five assessment dimensions and render them as text-based progress bars for quick visual comprehension.

   ```
   Your AI Literacy Progress
   ─────────────────────────────────────────

   Conceptual Understanding: ████████░░ 4.0/5  ↑ +0.5
   Prompting Skill:          ██████░░░░ 3.0/5  ↑ +1.0
   Output Evaluation:        ██████░░░░ 3.0/5  → stable
   Ethical Reasoning:        ████░░░░░░ 2.0/5  ↑ +0.3
   Critical Thinking:        █████░░░░░ 2.5/5  ↑ +0.5

   Overall Level: Practitioner
   ─────────────────────────────────────────
   ```

   - Use the most recent score for each dimension.
   - Show trend arrows by comparing to the previous assessment: `↑` improving, `→` stable, `↓` declining.
   - Include the delta value (e.g., `+0.5`) for improving or declining dimensions.

2. **Generate competency tracking display.** Compute current scores for each of the four practice types and render them as text-based progress bars.

   ```
   Competencies Practiced:
   ─────────────────────────────────────────

   Prompt Crafting:     ████████░░ 4.0/5
   Output Evaluation:   ██████░░░░ 3.0/5
   Appropriateness:     ████░░░░░░ 2.0/5
   Workflow Design:     ██░░░░░░░░ 1.0/5

   ─────────────────────────────────────────
   ```

   - Use the most recent score for each practice type.
   - Competency bars do not include trend arrows (they reflect practice engagement, not growth trajectory).
   - Place the competency section directly after the dimension progress bars.

3. **Highlight achievements and milestones.** Scan the interaction and assessment history for noteworthy accomplishments.
   - Modules and scenarios completed since last report
   - Score improvements: call out dimensions that have improved by 0.5 or more since the previous assessment
   - Specific breakthroughs: look for qualitative milestones in the interaction history (e.g., "First time you caught a hallucination without prompting!", "You used iterative refinement across three consecutive scenarios")
   - Streak tracking: consecutive sessions, consistent practice patterns

4. **Identify areas needing attention.** Flag dimensions that meet any of the following criteria:
   - Lowest absolute score among all dimensions
   - Stagnant: no improvement across the last 3+ assessments
   - Declining: score dropped compared to previous assessment
   - Below the threshold required for the learner's next level

5. **Show trajectory per dimension.** Provide a brief narrative interpretation of each dimension's trend.
   - Improving: "Your prompting skill has shown the strongest growth -- up a full point since you started. The iterative refinement exercises seem to be clicking."
   - Stable: "Output evaluation has held steady at 3.0 across your last three sessions. This isn't a bad thing if you've been focused elsewhere, but it may be time to revisit it."
   - Declining: "Critical thinking dipped slightly this session. This sometimes happens when learners are stretching into new territory. Let's keep an eye on it."

6. **Suggest next steps.** Recommend 2-3 specific activities that are aligned with the learner's gaps and stated goals.
   - Each suggestion should name a concrete skill or module (e.g., "Try the 'Misleading Statistics' scenario in scenario-runner")
   - Map each suggestion to a practice type when relevant
   - Prioritize suggestions that address the most impactful gaps relative to the learner's goals
   - Include a mix of types: one practice exercise, one conceptual module, one habit to build

7. **If near level-up threshold, highlight proximity.** When the learner's lowest dimension score is within 0.5 points of the next level's requirement, explicitly call this out to motivate continued effort.
   - "You're close to leveling up to Critical Thinker! Your ethical reasoning score needs to reach 3.5 -- you're currently at 3.0. One or two focused sessions on ethical frameworks could get you there."

## Outputs

| Parameter | Type | Description |
|---|---|---|
| `progressReport` | `string` | The full formatted progress report as shown to the user, including progress bars, competency bars, achievements, trajectory, and suggestions |
| `dimensionProgress` | `object { [dimension: string]: { currentScore: number, previousScore: number, trend: enum("improving", "stable", "declining"), delta: number } }` | Structured data for each dimension's current state and trajectory |
| `competencyProgress` | `object { [practiceType: string]: { currentScore: number } }` | Structured data for each practice type's current score |
| `achievements` | `string[]` | List of milestones and breakthroughs reached since the last report |
| `suggestedNextSteps` | `string[]` | 2-3 specific activity recommendations with rationale and mapped practice types |
| `nearLevelUp` | `boolean` | Whether the learner is within 0.5 points on all dimensions of reaching the next level |

## Chains To

- **improvement-advisor** -- when significant gaps are identified, chains with the gap analysis so the advisor can build a targeted plan
- **concept-explainer** -- if the suggested next step involves conceptual understanding, chains to deliver that content
- **scenario-runner** -- if the suggested next step involves practice, chains to launch the appropriate scenario

## Example Interaction

> **Context:** Maria is a novice-level high school teacher. She has completed 4 sessions over two weeks. Her goal is to "use AI tools effectively in lesson planning." She has shown strong improvement in prompting but has not yet engaged with output evaluation. This is an end-of-session report.

**Tutor:** Great work today, Maria! Here's a summary of where you stand after your fourth session.

```
Your AI Literacy Progress
──────────────────────────────────────────

Conceptual Understanding: ████░░░░░░ 2.0/5  ↑ +0.5
Prompting Skill:          ████░░░░░░ 1.8/5  ↑ +0.8
Output Evaluation:        ██░░░░░░░░ 1.0/5  → stable
Ethical Reasoning:        ███░░░░░░░ 1.5/5  ↑ +0.3
Critical Thinking:        ███░░░░░░░ 1.3/5  → stable

Overall Level: Novice
──────────────────────────────────────────

Competencies Practiced:

Prompt Crafting:     ████░░░░░░ 1.8/5
Output Evaluation:   ██░░░░░░░░ 1.0/5
Appropriateness:     ███░░░░░░░ 1.5/5
Workflow Design:     █░░░░░░░░░ 0.5/5
```

**Highlights this period:**

- Your prompting skill has shown the strongest growth of any dimension -- up from 1.0 to 1.8 in just four sessions. That's excellent progress. The moment in today's session where you broke your lesson plan request into step-by-step instructions instead of one big prompt shows you're internalizing iterative refinement.
- You completed the "Lesson Plan Generator" and "Rubric Builder" scenarios, which gives you practical experience with two of the most common AI use cases in education.
- Your conceptual understanding is building steadily. You can now explain the difference between a language model and a search engine, which is a key foundational concept.

**Areas to focus on next:**

Output evaluation is your biggest opportunity for growth right now. You've been creating AI outputs in your scenarios but haven't yet practiced systematically checking those outputs for accuracy and appropriateness. This matters a lot for your goal of using AI in lesson planning -- you need to be confident that the content AI generates is accurate and grade-appropriate before using it with students.

**Suggested next steps:**

1. **Try the "Fact-Check the Lesson Plan" scenario** in scenario-runner. It will give you a pre-generated lesson plan with several embedded errors and ask you to find them. This directly builds your Output Evaluation skills.
2. **Read the "Why AI Gets Things Wrong" concept module.** Understanding how and why language models hallucinate will sharpen your instinct for when to double-check AI output. It's a 10-minute read.
3. **Build a new habit:** After every AI-generated lesson plan, ask yourself three questions: "Are the facts correct?", "Is this grade-appropriate?", and "Does this align with my curriculum standards?" Try this with your next real lesson plan.

You're making steady progress, Maria. The prompting improvement is particularly impressive for four sessions in. Let's turn that same energy toward output evaluation next time.

## Design Notes

- **Celebrate growth, not just absolute scores.** A learner who goes from 1.0 to 1.8 deserves recognition even though 1.8 is still low in absolute terms. Growth rate matters more than current position for motivation.
- **Competency bars bridge assessment and practice.** The 4 practice types (Prompt Crafting, Output Evaluation, Appropriateness Judgment, Workflow Design) give learners a concrete understanding of *what they can do* to improve, not just abstract dimension scores. This makes the report more actionable.
- **Use the progress bars sparingly.** They are effective for a quick snapshot but should not be the entire report. The narrative context around the numbers is what makes the report actionable.
- **Avoid information overload.** Cap the report at the essentials: progress bars, competency bars, 2-3 highlights, 1-2 areas to focus on, and 2-3 suggestions. If the user wants more detail, they can ask.
- **Frame declining dimensions carefully.** A dip in score is not necessarily bad -- it can happen when learners are stretching into harder material. Acknowledge this possibility rather than framing every decline as a problem.
- **Connect suggestions to goals.** Every recommended next step should reference the learner's stated goals. "Because your goal is to use AI in lesson planning, verifying AI output is especially important" is more motivating than "Your output evaluation score is low."
- **Near-level-up is a powerful motivator.** When learners can see the finish line, they are more likely to push through challenging material. Use this signal deliberately.
- **Keep the tone warm but honest.** Avoid hollow praise ("Great job!") and avoid harsh language ("You failed at..."). Aim for a knowledgeable coach who respects the learner's effort and gives them straight information.
- **Track session count and time span.** A learner who reaches 3.0 in four sessions is progressing differently than one who reaches 3.0 in twenty sessions. Both are valid, but the pacing context matters for setting realistic expectations.