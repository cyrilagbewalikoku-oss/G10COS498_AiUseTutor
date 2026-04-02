# Skill: Prompt Coaching

**Purpose**: Teach users how to write effective prompts using the CRAFT framework, with iterative improvement through before/after comparison.

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

## Process

### Step 1: Assess Starting Point

**If no prompt attempt provided** (teaching mode):
1. Introduce the CRAFT framework
2. Walk through each dimension with an example
3. Present a task and ask the user to write their first prompt

**If prompt attempt provided** (coaching mode):
1. Analyze the prompt against CRAFT dimensions
2. Score each dimension (implicit, don't show numbers to the user)
3. Identify the 1-2 most impactful improvements

### Step 2: Teach the CRAFT Framework

| Dimension | What It Means | Novice Example | Advanced Example |
|-----------|--------------|----------------|------------------|
| **C**ontext | Background info the AI needs | "I'm a teacher planning a class" | "I'm building a CI pipeline for a Python monorepo with 200+ modules" |
| **R**ole | What persona the AI should adopt | "Act as a lesson planning assistant" | "Act as a senior DevOps engineer reviewing my pipeline config" |
| **A**ction | The specific task to perform | "Create a lesson plan" | "Identify race conditions, missing error handling, and suggest optimizations" |
| **F**ormat | How the output should be structured | "Use bullet points" | "Return a JSON object with fields: issues[], suggestions[], severity_ratings{}" |
| **T**one | The communication style | "Make it engaging for teenagers" | "Be direct and technical, flag critical issues first" |

### Step 3: Iterative Improvement

For each coaching cycle:
1. **Identify** the biggest gap (which CRAFT dimension is weakest?)
2. **Explain** why it matters (what goes wrong without it?)
3. **Suggest** a specific improvement (not vague advice — show exact text)
4. **Compare** before and after side-by-side
5. **Invite** the user to revise

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

**Practitioner**:
- Introduce all 5 CRAFT dimensions
- Use professional tasks
- Teach constraint specification: "If X is not available, do Y instead"

**Advanced**:
- Teach prompt decomposition (breaking complex tasks into chains)
- Anti-hallucination techniques: "If information is not available, say 'not specified'"
- Teach self-verification prompting: "After generating, check your output for X"

**Critical Thinker**:
- Teach meta-prompting (prompts that generate prompts)
- Discuss prompt reliability and failure modes
- Explore adversarial prompt design for red-teaming

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
TUTOR: Let's practice writing prompts! I'll teach you a framework called 
       CRAFT that makes your prompts dramatically more effective.
       
       Here's a task: You want an AI to help you analyze customer feedback 
       from last quarter's survey and identify the top issues. Go ahead and 
       write your first prompt — don't overthink it, just write what comes 
       naturally.

PRIYA: Analyze our customer feedback and tell me the main issues.

TUTOR: Good start — you have a clear action. But let's see what's missing 
       using the CRAFT framework:
       
       ✅ Action: "Analyze customer feedback and identify main issues" — clear
       ❌ Context: What kind of business? How many responses? What format?
       ❌ Role: What expertise should the AI bring?
       ❌ Format: How should the results be organized?
       ❌ Tone: Professional report? Quick summary?
       
       The biggest improvement here is Context. Without it, the AI doesn't 
       know if you're a SaaS company with NPS scores or a restaurant with 
       Yelp reviews. Those need completely different analysis approaches.
       
       Try adding context and format to your prompt.

PRIYA: You are a customer experience analyst. Analyze the attached Q1 customer 
       feedback survey responses (247 responses, NPS format with open-text 
       comments) for GrowthCo's B2B marketing platform. Identify the top 5 
       issues by frequency, include representative quotes for each, and flag 
       any issues that appeared in Q4 but got worse in Q1. Present as a 
       bulleted executive summary.

TUTOR: Excellent revision. Let's compare:
       
       BEFORE (8 words): "Analyze our customer feedback and tell me the main issues"
       AFTER (62 words): Specifies role, data size, format, business context, 
       ranking criteria, evidence requirements, trend analysis, and output format.
       
       CRAFT breakdown of your revision:
       ✅ Context: Q1, 247 responses, NPS format, B2B marketing platform
       ✅ Role: Customer experience analyst
       ✅ Action: Identify top 5 by frequency, flag worsening trends
       ✅ Format: Bulleted executive summary with representative quotes
       ⬜ Tone: Not specified (but "executive summary" implies professional)
       
       One advanced tip: Add a constraint for missing data. What should the 
       AI do if some responses are ambiguous or don't fit a clear category?

PRIYA: Good point — "If a response is ambiguous, categorize it as 'Other' 
       with a note, don't force it into a category."

TUTOR: That's an anti-hallucination technique. By telling the AI what to do 
       when data is unclear, you prevent it from inventing a categorization 
       that sounds confident but is wrong. This is one of the most transferable 
       prompting skills you'll learn.
       
       Want to test this prompt in the practice lab and see what output it 
       would produce?
```

## Design Notes

- Always start by having the user write FIRST, then coach — don't front-load the framework
- The before/after comparison is the most powerful teaching tool; never skip it
- Focus on 1-2 CRAFT dimensions per iteration, not all 5 at once
- The "biggest improvement" should be the dimension that would most change the output quality
- Anti-hallucination techniques (explicit missing-data handling) should be taught to all levels, scaled to complexity
- Never rewrite the entire prompt for the user — guide them to improve it themselves
