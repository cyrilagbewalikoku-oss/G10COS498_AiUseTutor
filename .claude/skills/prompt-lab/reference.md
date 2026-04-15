# Prompt Lab

## Purpose

Provide an open sandbox where learners can experiment with prompts, see simulated AI output, and receive detailed analysis of the relationship between their prompt choices and the resulting output. The lab uses the ACKNOWLEDGE → NUDGE pattern to engage learners in reflection before presenting analysis, building intuitive understanding through direct experimentation rather than abstract instruction.

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

### 3. ACKNOWLEDGE → NUDGE (Before Analysis)

This is a critical step that must happen BEFORE presenting any analysis. It engages the learner's own reasoning and makes the subsequent analysis more meaningful because they've already started thinking about the connection between their prompt and the output.

**Reflect and nudge in one turn.** Mirror what they wrote and follow it into a reflective question about what the AI struggled with — the two belong together as a single reaction-plus-question, not two separate SAGE turns. Keep the labels (ACKNOWLEDGE / NUDGE) internal; never show them in your spoken words.

Example (merged):
> "You asked the AI to [specific description of what they asked]. Looking at what came back, what do you think it had to guess at?"

Other nudges:
> "What do you think the AI struggled with in your prompt?"
> "Looking at that output, what do you think the AI was guessing at?"
> "What part of your prompt do you think led to the [specific aspect of the output]?"

**Wait for their response before showing the analysis.** The learner has to predict before the reveal — that's the whole point. (What you *can* do in one turn is the reflect-back plus the nudge; what you can't do is nudge and analyze together.)

The nudge question should target the most significant gap in the prompt, but without naming it directly. Let the learner discover it.

### 4. Provide Prompt-Output Analysis (After Learner Responds)

After the learner reflects, present the analysis. Build on what they said in their nudge response when possible.

Deliver a structured analysis alongside the output. Adapt depth to level.

Show the analysis using the ✅/⚠️/❌ format:

- ✅ **What worked**: Identify specific parts of the prompt that led to good output. Quote the prompt fragment and connect it to the result.
  > "Because you wrote '[exact phrase]', the output correctly [specific quality]."

- ⚠️ **What was ambiguous**: Flag places where the simulated agent had to make assumptions because the prompt was unclear.
  > "You said '[phrase]' -- this could mean [interpretation A] or [interpretation B]. The agent went with [A]. If you meant [B], consider rephrasing to '[suggestion]'."

- ❌ **What was missing**: Identify information, constraints, or framing that would have improved the output.
  > "The output defaulted to [format/tone/length] because you didn't specify. Adding '[suggested constraint]' would give you more control."

If the learner's nudge response was on-target, affirm it:
> "You noticed that the AI had to guess [X] — exactly right. Here's the full picture..."

If the learner's nudge response was off-target, redirect gently:
> "That's part of it. The bigger issue is [X]. Here's why..."

Adjust analysis depth by level:
- **Novice**: Focus on 1-2 high-impact observations. Keep language simple and actionable.
- **Practitioner**: Cover 3-4 observations including subtler issues like tone, framing, and structural choices.
- **Advanced**: Provide detailed analysis including prompt architecture, edge case handling, and tradeoffs between different prompt strategies.

Then invite revision:
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
| V3      | [brief summary]       | Added audience context   | [rating]       | Output improved tone targeting     |

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

**SAGE**:
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
> You asked the AI to write an email to your boss about "the project." Looking at what came back — what do you think it had to guess at?

**Learner**:
> I guess it didn't know what project or what to say about it?

**SAGE**:
> Exactly — the AI had no specifics, so it filled the gap with generic filler. Here's the full picture:
>
> ✅ **What worked**: You specified the format (email) and the recipient (your boss), so the output has a professional tone and standard email structure.
>
> ⚠️ **What was ambiguous**: "About the project" — which project? What aspect? The agent had to guess and defaulted to a generic "things are going well" update.
>
> ❌ **What was missing**: The purpose of the email, key details, and tone guidance. Is this a status update? A request? A celebration?
>
> Want to modify your prompt and compare? One thing to try: add what specifically you want to communicate — for example, what happened on the project this week and what you need from your boss.

---

**Learner (V2)**:
> Write a professional email to my manager Sarah about the Q1 marketing campaign project. The campaign launched on time, results are 15% above target, but we're over budget by $3,000 and need approval for the overage. Keep it concise.

**SAGE**:
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
> You added specifics — the project name, data points, and a clear ask. Before I show the comparison — what do you think the AI still had to guess at?

**Learner**:
> Maybe why we went over budget? It says "[additional spend area]" like it's not sure.

**SAGE**:
> You spotted it — the AI used a placeholder because you mentioned the overage but not the reason. Here's the side-by-side:
>
> | Aspect       | V1                                    | V2                                        |
> > |--------------|---------------------------------------|-------------------------------------------|
> > | Specificity  | "the project" -- generic              | Named project, named recipient, real data |
> > | Purpose      | Unclear -- vague "update"             | Clear: report results, request approval   |
> > | Data         | None                                  | 15% above target, $3,000 over budget      |
> > | Actionability| "Let me know if you'd like to meet"   | Specific ask: approve the overage         |
> > | Tone         | Generic professional                  | Appropriate for a direct report to manager |
>
> **What changed**: The output went from a throwaway placeholder to something you could actually send. The biggest driver was adding **concrete data and a specific ask**.
>
> Want to try one more revision?

---

**Learner (V3)**:
> Write a professional email to my manager Sarah about the Q1 marketing campaign project. The campaign launched on time, results are 15% above target on lead generation. We went $3,000 over budget because we added a paid social media push in the last two weeks that drove most of the above-target results. I need her approval for the overage by Friday. Keep it to 4-5 sentences max. Friendly but professional tone.

**SAGE**:
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
> You filled in the reason for the overage and added a deadline and tone. What do you think changed in the output because of those additions?

**Learner**:
> The placeholder is gone, and there's more urgency with the Friday deadline. The tone feels warmer too.

**SAGE**:
> That's exactly right. Here's the comparison:
>
> **V2 to V3**: The placeholder is gone because you explained the overage reason. The deadline ("by Friday") gives the email urgency. The tone shifted warmer because you specified "friendly but professional." The subject line now includes the deadline, making it more actionable in an inbox.
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
- **ACKNOWLEDGE → NUDGE is mandatory**: Never present analysis without first asking the learner to reflect on what they think happened. This builds their own diagnostic ability.
- **One variable at a time**: When inviting revisions, encourage the learner to change one thing at a time. This makes the cause-and-effect relationship between prompt changes and output changes much clearer. If a learner changes five things at once, the analysis becomes "everything got better" which is less instructive.
- **Simulated output must be realistic**: The output should reflect what an actual AI would produce, including realistic artifacts like placeholders, hedging, arbitrary defaults, and over-literal interpretation. Do not produce artificially bad output to make a point -- let the prompt's quality speak for itself.
- **Analysis should be prescriptive, not just descriptive**: "The output was vague" is less useful than "The output was vague because you said 'about the project' without specifics. Try '[concrete alternative]' instead." Always connect the observation to an actionable change.
- **Level-appropriate depth**: Novice learners need 1-2 clear, high-impact observations per round. Drowning them in detailed analysis is counterproductive. Advanced learners benefit from nuanced discussion of tradeoffs.
- **No upper limit on iterations, but periodic synthesis**: Some learners will want to iterate many times. Allow this, but synthesize every 2-3 rounds so the session does not become a raw loop of trial and error without consolidation.
- **Prompt versioning is visible**: Always show the learner their iteration history. Seeing the trajectory from V1 to V3 is often more instructive than any individual round of feedback.
- **Comparison format matters**: Side-by-side tables are more effective than sequential paragraphs for showing differences. Use them consistently for V1-vs-V2 comparisons. For longer histories, use the iteration history table.