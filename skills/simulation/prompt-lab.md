# Prompt Lab

## Purpose

Provide an open sandbox where learners can experiment with prompts, see simulated AI output, and receive detailed analysis of the relationship between their prompt choices and the resulting output. The lab emphasizes iterative refinement -- learners write, observe, revise, and compare -- building an intuitive understanding of what makes prompts effective through direct experimentation rather than abstract instruction.

## Trigger Conditions

- The learner has completed a `prompt-coaching` session and wants to apply what they learned.
- The learner explicitly requests to test or experiment with a prompt (e.g., "Let me try writing a prompt," "I want to test something").
- A lesson plan calls for free experimentation as a learning activity.
- The learner wants to compare different prompt strategies side by side.

## Inputs

| Parameter       | Type   | Required | Description                                                                                         |
|-----------------|--------|----------|-----------------------------------------------------------------------------------------------------|
| taskDescription | string | No       | Optional description of the task the learner is trying to accomplish. Provides context for analysis.  |
| userPrompt      | string | Yes      | The prompt the learner wants to test.                                                                |
| userLevel       | enum   | Yes      | One of: `novice`, `practitioner`, `advanced`. Determines the depth and technicality of the analysis. |

## Process

### 1. Accept the User's Prompt

Receive the learner's prompt without modification. If a `taskDescription` is provided, use it to contextualize the analysis. If not, infer the likely intent from the prompt itself.

Acknowledge receipt briefly:

> "Got it. Let me show you what an AI agent would likely produce from this prompt."

### 2. Simulate AI Output

Generate a realistic response that an AI agent would produce given the learner's exact prompt. The simulation should:

- Reflect the actual quality level that the prompt would elicit -- vague prompts get vague outputs, specific prompts get specific outputs.
- Include realistic artifacts of prompt quality:
  - Missing constraints lead to arbitrary choices by the agent (e.g., defaulting to a length, format, or tone the learner did not specify).
  - Ambiguous wording leads to the agent interpreting the prompt one way when the learner may have meant another.
  - Well-structured prompts produce focused, on-target output.
- Adapt the realism to the learner's level:
  - **Novice**: The gap between prompt and output should be clearly visible and instructive.
  - **Practitioner**: The output should reveal moderate-subtlety issues that require closer reading to notice.
  - **Advanced**: The output should highlight edge cases -- technically correct but missing nuance, or following instructions literally rather than capturing intent.

Present the simulated output in a clearly labeled block:

> **Simulated Output:**
> [output here]

### 3. Provide Prompt-Output Analysis

Deliver a structured analysis alongside the output. Adapt depth to level.

**What Worked**:
Identify specific parts of the prompt that led to good output. Quote the prompt fragment and connect it to the result.

> "Because you wrote '[exact phrase]', the output correctly [specific quality]."

**What Was Ambiguous**:
Flag places where the simulated agent had to make assumptions because the prompt was unclear.

> "You said '[phrase]' -- this could mean [interpretation A] or [interpretation B]. The agent went with [A]. If you meant [B], consider rephrasing to '[suggestion]'."

**What Was Missing**:
Identify information, constraints, or framing that would have improved the output.

> "The output defaulted to [format/tone/length] because you didn't specify. Adding '[suggested constraint]' would give you more control."

**Prompt-Output Connection**:
Draw explicit causal lines between prompt choices and output characteristics, making the relationship visible.

> "Because you said X, the output did Y. If you had said X', the output would likely do Y' instead."

Adjust analysis depth by level:
- **Novice**: Focus on 1-2 high-impact observations. Keep language simple and actionable.
- **Practitioner**: Cover 3-4 observations including subtler issues like tone, framing, and structural choices.
- **Advanced**: Provide detailed analysis including prompt architecture, edge case handling, and tradeoffs between different prompt strategies.

### 4. Invite Revision

Prompt the learner to iterate:

> "Want to modify your prompt and compare? Try changing one thing at a time so you can see what each change does."

If the learner is a novice and seems unsure, offer a specific suggestion:

> "One thing to try: add a constraint about [format/length/audience]. For example, you could add '[specific addition]' to your prompt."

### 5. Show Side-by-Side Comparison (On Revision)

When the learner submits a revised prompt, present both versions for comparison:

> **Version 1 Prompt**: [original]
> **Version 1 Output**: [original output]
>
> **Version 2 Prompt**: [revised]
> **Version 2 Output**: [new output]
>
> **What Changed**: [specific differences in the output and why they occurred]

Highlight:
- Which changes in the prompt had the most impact on the output.
- Whether the revision fixed the issues identified in the previous analysis.
- Any new issues introduced by the revision (over-constraining, conflicting instructions, etc.).

### 6. Track Iteration History

Maintain a running record of all prompt versions:

| Version | Prompt Summary        | Key Change               | Output Quality | Notable Effect                     |
|---------|-----------------------|--------------------------|----------------|------------------------------------|
| V1      | [brief summary]       | (initial)                | [rating]       | [what happened]                    |
| V2      | [brief summary]       | Added format constraint  | [rating]       | Output became more structured      |
| V3      | [brief summary]       | Added audience context   | Output improved tone targeting     |

Present this table to the learner after each revision so they can see their trajectory.

### 7. Summarize Key Insight (After 2-3 Iterations)

After the learner has gone through 2-3 revision cycles, synthesize the learning:

> "Looking across your iterations, here's the key insight: **[single most impactful change and why it worked]**."

Frame this as a transferable principle, not just feedback on this specific prompt:

> "This is a pattern you can apply broadly: [general principle]. Whenever you're writing prompts for [type of task], [actionable rule of thumb]."

If the learner wants to continue beyond 3 iterations, allow it, but offer a periodic summary every 2-3 additional versions.

## Outputs

| Parameter        | Type    | Description                                                                                              |
|------------------|---------|----------------------------------------------------------------------------------------------------------|
| simulatedOutput  | string  | The AI output generated in response to the learner's prompt.                                              |
| promptAnalysis   | object  | `{whatWorked: string[], whatWasAmbiguous: string[], whatWasMissing: string[], promptOutputConnections: string[]}`. |
| iterationHistory | array   | Array of `{version: int, prompt: string, output: string, changes: string, qualityDelta: string}`.         |
| keyInsight       | string  | The synthesized takeaway after multiple iterations: the single change that had the most impact.            |

## Chains To

- **prompt-coaching** -- if the analysis reveals the learner needs more structured guidance on a specific prompting technique before continuing to experiment.
- **reflection-facilitator** -- to consolidate what the learner discovered through experimentation into durable knowledge.

## Example Interaction

**Context**: A novice-level learner wants to test a prompt for getting an AI to write a professional email. No task description provided.

---

**Learner (V1)**:
> Write me an email to my boss about the project.

**Tutor**:
> Got it. Let me show you what an AI agent would likely produce from this prompt.
>
> **Simulated Output:**
>
> Subject: Project Update
>
> Hi,
>
> I wanted to give you a quick update on the project. Things are going well and we're making good progress. There are a few things I'd like to discuss with you when you have a chance.
>
> Let me know if you'd like to set up a meeting to go over the details.
>
> Best regards,
> [Your Name]
>
> ---
>
> **Analysis:**
>
> **What worked**: You specified the format (email) and the recipient (your boss). That's why the output has an appropriate professional-but-not-overly-formal tone and a standard email structure.
>
> **What was ambiguous**: "About the project" -- which project? What aspect? The agent had to guess and defaulted to a generic "things are going well" update because it had no specifics to work with.
>
> **What was missing**:
> - What the email is actually about: Is this a status update? A request? An escalation? A celebration?
> - Key details: deadlines, milestones, blockers, requests.
> - Tone guidance: Are you on good terms with your boss? Is this a formal or casual workplace?
>
> **Prompt-output connection**: Because you said "about the project" without specifics, the output is vague and could apply to literally any project in any company. The agent filled the gap with generic filler.
>
> Want to modify your prompt and compare? One thing to try: add what specifically you want to communicate -- for example, what happened on the project this week and what you need from your boss.

---

**Learner (V2)**:
> Write a professional email to my manager Sarah about the Q1 marketing campaign project. The campaign launched on time, results are 15% above target, but we're over budget by $3,000 and need approval for the overage. Keep it concise.

**Tutor**:
> **Simulated Output:**
>
> Subject: Q1 Marketing Campaign -- Results and Budget Update
>
> Hi Sarah,
>
> Quick update on the Q1 marketing campaign: we launched on schedule and early results are strong -- 15% above our target metrics.
>
> One item that needs your attention: we came in $3,000 over budget, primarily due to [additional spend area]. I'd like to request your approval for the overage. Happy to walk through the breakdown if that would be helpful.
>
> Thanks,
> [Your Name]
>
> ---
>
> **Comparison:**
>
> | Aspect       | V1                                    | V2                                        |
> |--------------|---------------------------------------|-------------------------------------------|
> | Specificity  | "the project" -- generic              | Named project, named recipient, real data |
> | Purpose      | Unclear -- vague "update"             | Clear: report results, request approval   |
> | Data         | None                                  | 15% above target, $3,000 over budget      |
> | Actionability| "Let me know if you'd like to meet"   | Specific ask: approve the overage         |
> | Tone         | Generic professional                  | Appropriate for a direct report to manager |
>
> **What changed**: The output went from a throwaway placeholder to something you could actually send. The biggest driver was adding **concrete data and a specific ask**. The agent now knows what the email needs to accomplish.
>
> **What still could improve**: The output has a placeholder -- "[additional spend area]" -- because you mentioned the overage but not the reason. If you add why you went over budget, the agent won't need to guess. Also, you said "concise" which helped, but you could specify an approximate length ("3-5 sentences") for even tighter control.
>
> Want to try one more revision?

---

**Learner (V3)**:
> Write a professional email to my manager Sarah about the Q1 marketing campaign project. The campaign launched on time, results are 15% above target on lead generation. We went $3,000 over budget because we added a paid social media push in the last two weeks that drove most of the above-target results. I need her approval for the overage by Friday. Keep it to 4-5 sentences max. Friendly but professional tone.

**Tutor**:
> **Simulated Output:**
>
> Subject: Q1 Campaign Results + Budget Approval Needed by Friday
>
> Hi Sarah,
>
> Great news on the Q1 marketing campaign -- we launched on time and lead generation came in 15% above target. The boost was largely driven by a paid social push we added in the final two weeks, which also put us $3,000 over budget. Given the strong ROI, I'd like to request your approval for the overage. Could you let me know by Friday? Happy to share the full breakdown anytime.
>
> Thanks!
>
> ---
>
> **What changed from V2 to V3**: The placeholder is gone because you explained the overage reason. The deadline ("by Friday") gives the email urgency. The tone shifted slightly warmer because you specified "friendly but professional." The subject line now includes the deadline, making it more actionable in an inbox.
>
> ---
>
> **Iteration History:**
>
> | Version | Key Change                           | Effect                                              |
> |---------|--------------------------------------|-----------------------------------------------------|
> | V1      | (initial -- minimal prompt)          | Generic, unusable output                            |
> | V2      | Added specifics, data, and purpose   | Output became sendable; still had a placeholder gap |
> | V3      | Added reason for overage, deadline, tone, length | Output is complete and ready to send       |
>
> **Key Insight**: Looking across your three versions, the single change that had the most impact was **moving from "about the project" to stating the specific purpose and data points** (V1 to V2). That one change transformed the output from filler to substance. The refinements in V3 polished the result, but V2 was where the real jump happened.
>
> **Transferable principle**: Whenever you're asking an AI to write communication for you, always include three things upfront: (1) the specific purpose of the message, (2) the key facts or data points, and (3) what you need the recipient to do. Those three elements do more work than any amount of style or formatting instructions.

## Design Notes

- **The sandbox is judgment-free**: The lab should never make the learner feel bad about a weak prompt. The V1 prompt is not a "failure" -- it is the starting point that makes the learning visible. Frame every version as progress.
- **One variable at a time**: When inviting revisions, encourage the learner to change one thing at a time. This makes the cause-and-effect relationship between prompt changes and output changes much clearer. If a learner changes five things at once, the analysis becomes "everything got better" which is less instructive.
- **Simulated output must be realistic**: The output should reflect what an actual AI would produce, including realistic artifacts like placeholders, hedging, arbitrary defaults, and over-literal interpretation. Do not produce artificially bad output to make a point -- let the prompt's quality speak for itself.
- **Analysis should be prescriptive, not just descriptive**: "The output was vague" is less useful than "The output was vague because you said 'about the project' without specifics. Try '[concrete alternative]' instead." Always connect the observation to an actionable change.
- **Level-appropriate depth**: Novice learners need 1-2 clear, high-impact observations per round. Drowning them in detailed analysis is counterproductive. Advanced learners benefit from nuanced discussion of tradeoffs (e.g., "Adding more constraints improves precision but can reduce creativity -- here's how to balance that").
- **No upper limit on iterations, but periodic synthesis**: Some learners will want to iterate many times. Allow this, but synthesize every 2-3 rounds so the session does not become a raw loop of trial and error without consolidation.
- **Prompt versioning is visible**: Always show the learner their iteration history. Seeing the trajectory from V1 to V3 is often more instructive than any individual round of feedback. It makes improvement tangible and builds confidence.
- **Comparison format matters**: Side-by-side tables are more effective than sequential paragraphs for showing differences. Use them consistently for V1-vs-V2 comparisons. For longer histories, use the iteration history table.
