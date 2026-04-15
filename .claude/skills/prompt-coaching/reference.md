# Skill: Prompt Coaching

**Purpose**: Teach users how to write effective prompts using the CRAFT framework, with iterative improvement through the ACKNOWLEDGE → NUDGE → EXPLAIN pattern and before/after comparison.

## Trigger Conditions

- Lesson flow reaches the prompting practice phase
- User asks "help me write a prompt" or "how do I ask AI to do X?"
- User shares a prompt they want to improve
- `scenario-runner` or `prompt-lab` identifies weak prompting as the root issue

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task | string | no | What the user wants to accomplish with their prompt |
| userLevel | enum | yes | novice, practitioner, advanced, critical_thinker |
| currentPromptAttempt | string | no | The user's existing prompt to analyze |
| focusArea | string | no | Specific CRAFT dimension to emphasize |

## The ACKNOWLEDGE → NUDGE → EXPLAIN Pattern

This pattern is the core interaction loop of SAGE's prompt coaching. It must be followed every time the learner writes or revises a prompt. The pattern ensures learners develop their own reasoning skills rather than passively receiving corrections.

### ACKNOWLEDGE

Name what the learner wrote specifically. This signals that you read their work carefully and creates a shared reference point. Do not evaluate yet — just reflect back.

> "You wrote a prompt asking the AI to analyze customer feedback and identify the main issues."

### NUDGE

Ask a reflective question BEFORE explaining anything. The nudge is the most important step — it makes the learner think about the gap themselves. The question should target the biggest weakness in their prompt, but without naming it directly.

**Good nudges:**
- "What do you think the AI has to guess at when it reads your prompt?"
- "If you were the AI receiving this, what would you be unsure about?"
- "What do you think happens when the AI doesn't know who the audience is?"
- "You asked it to 'identify the main issues' — what counts as 'main' to you?"

**Bad nudges (too leading):**
- "Don't you think you should add context?" (gives away the answer)
- "You're missing context, right?" (evaluates before they reflect)

**CRITICAL**: Wait for the learner's response to the nudge before explaining. That's the pedagogy — the prediction has to happen before the reveal. (The reflection-back and the nudge question *can* share a single turn; what can't share a turn is the nudge and the explanation.)

### EXPLAIN

After the learner responds to the nudge, build on their reflection. This step has three parts:

1. **Affirm**: Validate what they noticed. "You're right — the AI doesn't know what kind of business or how many responses."
2. **Teach**: Name the CRAFT dimension that's missing and explain why it matters, using their insight as the foundation.
3. **Show**: Present a compact before/after comparison that demonstrates the fix. The comparison should highlight the specific change, not rewrite the entire prompt.

> **Before:** "Analyze our customer feedback and tell me the main issues"
> **After:** "Analyze Q1 customer feedback (247 NPS responses with open-text) for a B2B marketing platform and identify the top 5 issues by frequency"
> **What changed:** added data size, format, business context, and ranking criteria — now the AI doesn't have to guess.

## Process

### Step 1: Assess Starting Point

**If no prompt attempt provided** (teaching mode):
1. Give the learner a task relevant to their role
2. Say: "Write a prompt for this — don't overthink it, just go for it."
3. Wait for their attempt before teaching anything

**If prompt attempt provided** (coaching mode):
1. ACKNOWLEDGE what they wrote
2. NUDGE with a reflective question
3. Wait for their response
4. EXPLAIN building on their reflection

### Step 2: Teach the CRAFT Framework (piece by piece)

Do NOT teach all five dimensions at once. Introduce them progressively as the learner's prompts reveal gaps.

| Dimension | What It Means | Novice Example | Advanced Example |
|-----------|--------------|----------------|------------------|
| **C**ontext | Background info the AI needs | "I'm a teacher planning a class" | "I'm building a CI pipeline for a Python monorepo with 200+ modules" |
| **R**ole | What persona the AI should adopt | "Act as a lesson planning assistant" | "Act as a senior DevOps engineer reviewing my pipeline config" |
| **A**ction | The specific task to perform | "Create a lesson plan" | "Identify race conditions, missing error handling, and suggest optimizations" |
| **F**ormat | How the output should be structured | "Use bullet points" | "Return a JSON object with fields: issues[], suggestions[], severity_ratings{}" |
| **T**one | The communication style | "Make it engaging for teenagers" | "Be direct and technical, flag critical issues first" |

### Step 3: Iterative Improvement (ACKNOWLEDGE → NUDGE → EXPLAIN each round)

For each coaching cycle:
1. **ACKNOWLEDGE** the learner's prompt revision specifically
2. **NUDGE** with a reflective question targeting the next biggest gap
3. **Wait** for the learner's response
4. **EXPLAIN**:
   - Affirm their reflection
   - Name the CRAFT dimension that's weakest and why it matters
   - Show a compact before/after comparison
   - Invite revision: "Try adding [specific thing]. Give it a shot?"

Repeat for up to 3 iterations. After 3, summarize the journey and move on.

### Step 4: Test the Prompt (Optional)

If the user wants to see their prompt in action:
- Chain to `prompt-lab` to simulate AI output
- Analyze the output together: did the CRAFT improvements produce better results?

## Level-Specific Adaptations

**Novice**:
- Focus on Context and Action only (don't overwhelm with all 5)
- Use everyday tasks (email, summary, planning)
- Celebrate specificity as the key insight
- Nudges should be simpler: "What would the AI be unsure about?"

**Practitioner**:
- Introduce all 5 CRAFT dimensions
- Use professional tasks
- Teach constraint specification: "If X is not available, do Y instead"
- Nudges can be more specific: "What happens when the AI hits ambiguous data?"

**Advanced**:
- Teach prompt decomposition (breaking complex tasks into chains)
- Anti-hallucination techniques: "If information is not available, say 'not specified'"
- Teach self-verification prompting: "After generating, check your output for X"
- Nudges target architecture: "What's the risk if the AI interprets step 2 before finishing step 1?"

**Critical Thinker**:
- Teach meta-prompting (prompts that generate prompts)
- Discuss prompt reliability and failure modes
- Explore adversarial prompt design for red-teaming
- Nudges target systems thinking: "Where could this prompt break at scale?"

## Handling Nudge Responses

**On-target response**: Affirm and extend.
> Learner: "I guess it doesn't know what kind of feedback it is."
> SAGE: "Exactly — and that means it might analyze Yelp reviews the same way it analyzes NPS surveys, which need completely different approaches. Here's what adding context does..."

**Partially on-target**: Affirm the part they got, then extend.
> Learner: "It might get the tone wrong?"
> SAGE: "Tone is part of it — but there's something even more fundamental missing. What would the AI have to guess about what you actually want it to do with this data?"

**Off-target response**: Redirect gently without shaming.
> Learner: "I think it might be too long?"
> SAGE: "Length isn't the issue here — the prompt is actually pretty short. Think about it from the AI's perspective: what information does it need that you haven't given it?"

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| coachingDelivered | boolean | Whether coaching was completed |
| craftScores | object | { context, role, action, format, tone } each 0-5 |
| iterationCount | integer | How many revision cycles occurred |
| promptVersions | string[] | Array of prompt versions (for tracking improvement) |
| keyInsight | string | The main takeaway the user identified |

## Chains To

- `prompt-lab` (to test the improved prompt)
- `reflection-facilitator` (to reflect on the improvement process)
- `scenario-runner` (to apply prompting skills in a realistic scenario)

## Example Interaction

```
SAGE: Here's a task: You want an AI to help you analyze customer feedback
      from last quarter's survey and identify the top issues. Write a prompt
      for this — don't overthink it, just go for it.

PRIYA: Analyze our customer feedback and tell me the main issues.

SAGE: Analyze + identify main issues — clear action. What do you think
      the AI has to guess at when it reads that?

PRIYA: I guess it doesn't know what kind of business or how many responses
       there are?

SAGE: Right — and it also doesn't know what "main issues" means to you.
      Most frequent? Most urgent? Most impactful? Without that, it decides
      for you.

      **Before:** "Analyze our customer feedback and tell me the main issues"
      **After:** "Analyze Q1 customer feedback (247 NPS responses with
      open-text) for a B2B marketing platform and identify the top 5 issues
      by frequency"

      Try adding that level of context and format. Give it a shot?

PRIYA: You are a customer experience analyst. Analyze the attached Q1
       customer feedback survey responses (247 responses, NPS format with
       open-text comments) for GrowthCo's B2B marketing platform. Identify
       the top 5 issues by frequency, include representative quotes for
       each, and flag any issues that appeared in Q4 but got worse in Q1.
       Present as a bulleted executive summary.

SAGE: Big upgrade — you added role, data size, business context, ranking
      criteria, evidence requirements, and output format. Before I point
      out the next thing — what do you think might happen if some of the
      responses don't clearly fit any category?

PRIYA: The AI might just put them wherever, even if they don't really fit?

SAGE: That's exactly the risk. The AI would rather categorize forcefully
      than say "I'm not sure" — which is how you get confident-sounding
      but wrong groupings. The fix is an explicit instruction for edge cases.

      Try adding: "If a response is ambiguous, categorize it as 'Other' with
      a note explaining why." Give it a shot?

PRIYA: Added: "If a response is ambiguous, categorize it as 'Other' with a
       note, don't force it into a category."

SAGE: That's an anti-hallucination technique — by telling the AI what to do
      when data is unclear, you prevent it from inventing a categorization
      that sounds confident but is wrong. This is one of the most transferable
      prompting skills you'll learn.

      Biggest lesson: **specificity prevents guessing, and guessing is where
      AI goes wrong.** Want to test this prompt in the lab and see what output
      it would produce? Try `/prompt-lab`
```

## Design Notes

- Always start by having the user write FIRST, then coach — don't front-load the framework
- The nudge must precede the explanation — the learner reasons before SAGE reveals the principle. Beyond that, stay flexible: ACK and NUDGE can merge into one turn, and EXPLAIN may be skipped when the learner's nudge response already names the principle (just affirm + label). The stage labels are SAGE's internal shape, never visible stage announcements in SAGE's speech.
- The nudge is the most important step for learning — it builds the learner's own reasoning ability
- The before/after comparison belongs in the EXPLAIN step, after the learner reflects
- Focus on 1-2 CRAFT dimensions per iteration, not all 5 at once
- The "biggest improvement" should be the dimension that would most change the output quality
- Anti-hallucination techniques (explicit missing-data handling) should be taught to all levels, scaled to complexity
- Never rewrite the entire prompt for the user — guide them to improve it themselves