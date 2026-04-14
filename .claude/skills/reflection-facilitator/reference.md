# Reflection Facilitator

## Purpose

Help learners extract transferable principles from their practice experience through guided reflection. Rather than simply telling learners what they did right or wrong, this skill uses Socratic questioning to help them discover insights themselves, then reinforces those insights by connecting them to named principles and generalizable strategies.

## Trigger Conditions

- After any practice or simulation session completes (scenario-runner, bad-agent-simulator, prompt-lab)
- When a user explicitly asks to reflect on a recent interaction
- When chained from skill-evaluator after an evaluation is complete

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `interactionLog` | `Array<{ role: string, content: string, turnNumber: number }>` | Yes | The full sequence of turns from the practice session, including both user and AI messages |
| `scenarioContext` | `string` | Yes | Description of the scenario or exercise that was practiced (e.g., "Marketing copy review with embedded hallucinations") |
| `userLevel` | `enum("novice", "beginner", "practitioner", "critical-thinker", "expert")` | Yes | The learner's current classified level, used to calibrate depth and vocabulary of reflection |
| `evaluationResults` | `object { scores: object, feedback: string, strengths: string[], gaps: string[] }` | No | If available from skill-evaluator, provides an objective baseline to compare against the user's self-assessment |

## Process

1. **Open with reflective questions.** Select 2-3 questions from the following list based on what is most relevant to the scenario. Do not ask all of them -- pick the ones most likely to surface useful insights for this particular interaction.
   - "What went well in that interaction?"
   - "What surprised you?"
   - "What would you do differently if you could try again?"
   - "What was harder than you expected?"
   - "Was there a moment where you felt uncertain about what to do next?"

2. **Listen to the user's self-assessment before offering your own.** Wait for the user to respond. Do not immediately correct or supplement their answer. Acknowledge what they said and probe deeper if their response is surface-level (e.g., "Can you point to a specific moment where that happened?").

3. **Highlight specific moments from the interaction log.** Reference exact turns to ground the discussion in concrete evidence. Include both strengths and missed opportunities.
   - For strengths: "In turn 3, you added a great constraint about data format. That's exactly the kind of specificity that improves output quality."
   - For missed opportunities: "In turn 5, the agent gave you an unverified statistic. You accepted it without checking. What could you have done there?"
   - Calibrate the ratio of strengths to growth areas based on user level: novice users need more encouragement (3:1 ratio), advanced users can handle more direct critique (1:1 ratio).

4. **Connect observations to named principles.** After discussing specific moments, attach them to transferable concepts the learner can carry forward.
   - "What you did there is called 'iterative refinement.' It's one of the most effective prompting patterns because it lets you steer the AI incrementally rather than trying to get everything right in one shot."
   - "That missed moment relates to 'output verification' -- the practice of never accepting AI-generated claims at face value, especially statistics, citations, and proper nouns."

5. **Help the user generalize.** Ask the learner to connect the lesson to their own professional context.
   - "How would you apply this lesson in your own work?"
   - "Can you think of a situation where this principle would change how you use AI tools?"

6. **Summarize 2-3 key takeaways.** Provide a concise wrap-up that the learner can refer back to.

## Outputs

| Parameter | Type | Description |
|---|---|---|
| `reflectionSummary` | `string` | A narrative summary of the reflection conversation, capturing key discussion points and insights |
| `lessonsLearned` | `string[]` | 2-3 concrete lessons the learner articulated or agreed to during the reflection |
| `principlesReinforced` | `string[]` | Named principles that were connected to the learner's experience (e.g., "iterative refinement", "output verification", "constraint specification") |
| `selfAssessmentAccuracy` | `enum("under-estimated", "accurate", "over-estimated")` | How well the user's self-assessment matched the tutor's evaluation. Under-estimated means the user was too hard on themselves; over-estimated means they missed weaknesses |

## Chains To

- **progress-reporter** -- passes `lessonsLearned` and `principlesReinforced` so they can be recorded in the learner's profile and reflected in progress tracking
- **improvement-advisor** -- passes identified gaps so the advisor can suggest targeted follow-up activities
- **Next lesson in workflow** -- if the reflection occurs mid-workflow, chains to the next scheduled activity with context about what the learner should focus on

## Example Interaction

> **Context:** A practitioner-level user just completed a scenario where they reviewed AI-generated marketing copy for a health supplement. The copy contained two hallucinated clinical studies, one misleading statistical claim, and subtle ethical issues around targeting vulnerable populations. The user caught the hallucinated studies but missed the misleading statistic and the ethical implications.

**Tutor:** You just finished reviewing that marketing copy scenario. Before I share my observations, I'd like to hear from you first. What went well in that interaction, and what was harder than you expected?

**User:** I think I did a good job catching the fake studies. I Googled the journal names and they didn't exist, so that was a clear red flag. I'm not sure I caught everything though -- it felt like there might have been more issues I missed.

**Tutor:** That's a solid self-assessment, and you're right to trust that instinct. Your verification of the clinical studies was excellent -- in turn 4, you specifically asked the AI to provide DOIs for the cited papers, which is one of the most reliable hallucination-detection techniques. That shows real skill in output verification.

You're also right that there were a couple of things that slipped through. Let me point to one: in turn 6, the copy said "73% of users reported improvement within two weeks." You flagged the studies but accepted that statistic. What do you think you could have done with that claim?

**User:** I guess I should have asked where that number came from too. If the studies were fake, the stats from those studies would also be fake.

**Tutor:** Exactly. That's a really important principle: **claims don't exist in isolation**. Once you identify that a source is fabricated, every claim that depends on that source becomes suspect. Think of it like pulling a thread -- one fabricated citation can unravel multiple claims downstream. This is sometimes called "cascading verification" -- when you find one problem, you trace its implications through the rest of the content.

There was one more dimension to this scenario I want to explore. The marketing copy was specifically targeting "adults over 60 experiencing cognitive decline." Did anything about that framing give you pause?

**User:** Hmm, not really. Is that an issue?

**Tutor:** It can be, yes. Marketing health supplements to elderly people experiencing cognitive decline raises ethical concerns -- this is a vulnerable population that may be more susceptible to health claims and less likely to critically evaluate them. This connects to the principle of **audience vulnerability assessment**: when reviewing AI-generated content, it's important to consider not just whether the facts are accurate, but whether the framing could cause harm to the intended audience. This is especially important in health, finance, and education contexts.

This isn't something most people catch right away, so don't be discouraged. It's actually one of the more advanced evaluation skills.

**User:** That makes sense. I was so focused on fact-checking that I didn't step back to look at the bigger picture.

**Tutor:** That's a very common pattern, and recognizing it is the first step. Let me summarize your key takeaways from this session:

1. **You have strong hallucination detection skills** -- your instinct to verify citations by requesting DOIs is a reliable technique. Keep doing that.
2. **Practice cascading verification** -- when you find one fabricated element, trace its implications through the rest of the content. Don't verify claims in isolation.
3. **Build an ethical review step into your workflow** -- after checking factual accuracy, take a step back and ask: "Who is the audience, and could this content cause harm?" This is especially important in health, finance, and education domains.

How do you think you could apply that ethical review step in your own work?

**User:** I review a lot of AI-generated content for our website. I could add a checklist item -- after fact-checking, I ask "who is this targeting and are there vulnerability concerns?"

**Tutor:** That's a great concrete plan. Adding it to an existing checklist means you're more likely to actually do it consistently.

## Design Notes

- **Self-assessment first, always.** The most durable learning happens when learners identify their own strengths and gaps. Resist the temptation to lead with the tutor's evaluation. Even if the user's self-assessment is inaccurate, starting with it gives you information about their metacognitive skills and creates a more collaborative dynamic.
- **Be specific, not vague.** Always reference exact turn numbers and exact quotes from the interaction log. "You did well" is less useful than "In turn 4, you asked for DOIs -- that was effective because..."
- **Calibrate encouragement to level.** Novice users need a higher ratio of positive reinforcement to critique (aim for 3:1). Advanced users benefit from more direct and balanced feedback (1:1). All users should leave the reflection feeling capable of improving, not defeated.
- **Name the principles.** Attaching memorable names to patterns ("cascading verification", "iterative refinement") gives learners mental hooks they can retrieve later. Use consistent terminology across sessions.
- **Don't overload.** Cap takeaways at 2-3 per session. More than that and retention drops sharply. If there were many issues, prioritize the ones most relevant to the learner's current level and goals.
- **Track self-assessment accuracy over time.** A learner who consistently over-estimates their performance needs different support than one who under-estimates. This signal is valuable for progress-reporter and improvement-advisor.
