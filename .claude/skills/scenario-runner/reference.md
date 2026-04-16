# Scenario Runner

## Purpose

Let learners practice interacting with AI agents in realistic, controlled scenarios. SAGE presents structured tasks across four practice types — prompt crafting, output evaluation, appropriateness judgment, and workflow design — allowing the learner to develop hands-on skills within a safe, observable environment where performance can be tracked, debriefed, and reflected upon.

## Trigger Conditions

- The learner has entered the **practice phase** of a lesson and needs hands-on experience.
- The learner explicitly requests practice (e.g., "Can I try working with an agent?", "Let me practice prompting").
- The assessment flow calls for a practical exercise to evaluate applied skills.
- A prior skill (e.g., `prompt-coaching`) chains into scenario-runner for applied practice.

## Scenario Types

All scenarios fall into one of four practice types. Each type exercises a distinct competency:

| Type | What the Learner Does | What SAGE Does | Primary Competency |
|------|----------------------|----------------|-------------------|
| **PROMPT CRAFTING** | Writes a prompt for a described task | Role-plays as the AI agent receiving the prompt | Prompting skill, iteration |
| **OUTPUT EVALUATION** | Reviews AI output and identifies embedded errors | Presents flawed AI output for scrutiny | Output evaluation, critical reading |
| **APPROPRIATENESS JUDGMENT** | Decides whether/how AI should be used for a task and justifies the decision | Presents a task context with tradeoffs | Ethical reasoning, critical thinking |
| **WORKFLOW DESIGN** | Describes a multi-step process involving AI, including human checkpoints and fallbacks | Presents a complex task requiring multi-step AI use | Workflow design, human-in-the-loop thinking |

## Inputs

| Parameter          | Type     | Required | Description                                                                                       |
|--------------------|----------|----------|---------------------------------------------------------------------------------------------------|
| scenarioId         | string   | No       | ID of a predefined scenario from `data/scenarios/`. If omitted, a scenario is generated dynamically. |
| scenarioType       | string   | No       | One of: `prompt-crafting`, `output-evaluation`, `appropriateness-judgment`, `workflow-design`. Used when scenarioId is not provided. |
| userLevel          | enum     | Yes      | One of: `novice`, `practitioner`, `advanced`, `critical-thinker`. Determines scenario complexity and expected behavior. |
| learningObjective  | string   | Yes      | The specific skill or concept the scenario is designed to exercise. |
| learnerContext     | object   | No       | Contextual data about the learner: course enrollment, prior history, current topics, competency gaps. Optionally enriched by CollaborAITE data when available. |

## Process

### 1. Context Assessment

Before presenting any scenario, assess the learner's current situation:

- **Course enrollment**: What course or module is the learner in? This shapes the scenario's domain.
- **Prior scenario history**: Has the learner done similar scenarios before? Avoid exact repetition; increase difficulty if they've mastered a type.
- **Current topics**: What concept is the learner studying right now? Align the scenario to reinforce or apply that concept.
- **Competency gaps**: Where has the learner shown weakness in prior assessments? Target scenarios toward those gaps.

When CollaborAITE data is available, use it to inform the assessment with richer interaction history and collaborative learning patterns. When it is not available, rely on the learner's profile and any prior session data.

### 2. Select or Generate Scenario

Choose a scenario type based on the context assessment:
- If the learner has a prompting gap, lean toward **PROMPT CRAFTING**.
- If the learner struggles to catch errors in AI output, lean toward **OUTPUT EVALUATION**.
- If the learner tends to over-rely on AI or misses ethical concerns, lean toward **APPROPRIATENESS JUDGMENT**.
- If the learner needs help structuring multi-step AI use, lean toward **WORKFLOW DESIGN**.

If `scenarioId` is provided, load the scenario definition from `data/scenarios/`.
If only `scenarioType` is provided, generate a scenario appropriate to the user's level:

- **Novice**: Simple, single-step tasks with clear success criteria.
- **Practitioner**: Multi-step tasks requiring iteration and judgment.
- **Advanced**: Ambiguous, open-ended tasks with tradeoffs and no single right answer.
- **Critical Thinker**: Complex scenarios requiring policy-level reasoning, multi-stakeholder considerations, or teaching-back exercises.

### 3. Present the Setup

Deliver a clear, compact framing to the learner (4 lines max):

> **You are:** [role]
> **Task:** [what to accomplish]
> **Type:** [PROMPT CRAFTING | OUTPUT EVALUATION | APPROPRIATENESS JUDGMENT | WORKFLOW DESIGN]
> **Constraint:** [one key limitation]

Include relevant context documents, data snippets, or background information the learner will need. Keep it brief — front-loading too much context defeats the purpose of the exercise.

### 4. Control Point

Present the scenario and ask the learner to confirm or request a different focus:

> "This scenario focuses on [type]. Does that work for you, or would you prefer a different focus?"

**Wait for the learner's response before proceeding.** Adjust the scenario type or difficulty if they request a change. This step ensures the learner has agency and buys into the practice before it begins.

### 5. Signal Simulation Mode

Clearly mark the transition so the learner knows what mode SAGE is operating in. The signal varies by scenario type:

- **PROMPT CRAFTING**: "Switching to agent mode now — talk to me like I'm the AI tool."
- **OUTPUT EVALUATION**: "Switching to evaluation mode now — review this AI output and identify any issues."
- **APPROPRIATENESS JUDGMENT**: "Switching to judgment mode now — consider whether AI is the right tool for this task and explain your reasoning."
- **WORKFLOW DESIGN**: "Switching to design mode now — describe the steps you'd take, including where a human should check in."

### 6. Run the Scenario (3-10 turns)

#### PROMPT CRAFTING
Role-play as a competent but imperfect AI assistant. Engage in 3-10 turns of realistic interaction:
- Respond helpfully and plausibly to the learner's prompts.
- If the learner gives a vague prompt, produce a vague or overly broad response — don't compensate for poor prompting.
- Occasionally be too verbose, too terse, or slightly off-target.
- Adapt realism to level:
  - **Novice**: Fairly cooperative; imperfections are mild and instructive.
  - **Practitioner**: Requires clearer prompts; may go off-track if instructions are vague.
  - **Advanced**: Subtle issues — plausible but slightly off outputs, buried caveats, technically correct but contextually wrong.
  - **Critical Thinker**: May produce sophisticated output that contains hidden assumptions or reasoning gaps only a careful reader would catch.

#### OUTPUT EVALUATION
Present a piece of AI-generated output that contains embedded errors:
- **Novice**: 1-2 obvious errors (factual mistakes, contradictions).
- **Practitioner**: 2-3 errors, some subtle (omissions, overgeneralizations, unsupported claims).
- **Advanced**: 3-4 errors, including reasoning errors, hidden biases, or causal language where only correlation is supported.
- **Critical Thinker**: 4+ errors, including systemic patterns (selection bias, framing effects, buried methodological flaws).

Let the learner identify and explain the errors. Ask clarifying follow-ups: "What makes you think that's an error?" "What should it say instead?"

#### APPROPRIATENESS JUDGMENT
Present a task and ask the learner to decide:
1. Should AI be used for this task at all?
2. If so, how — full delegation, assisted, or advisory?
3. What are the risks or limitations?

Present tasks with genuine tradeoffs:
- **Novice**: Clear-cut cases with some gray-area tasks mixed in.
- **Practitioner**: Tasks where AI is tempting but risky (e.g., drafting legal language).
- **Advanced**: Tasks where AI seems obviously appropriate but has hidden pitfalls, or where AI seems inappropriate but has genuine utility.
- **Critical Thinker**: Multi-stakeholder scenarios where different parties have conflicting interests in AI use.

#### WORKFLOW DESIGN
Present a complex task that requires multiple AI interactions with human checkpoints. Ask the learner to describe:
1. The steps they would take.
2. Where a human should review or intervene.
3. What fallback plan they'd have if the AI output is poor.

- **Novice**: 2-3 step workflows with one clear human checkpoint.
- **Practitioner**: 4-5 step workflows with multiple checkpoints and decision points.
- **Advanced**: Complex workflows with branching paths, error recovery, and conditional AI use.
- **Critical Thinker**: Workflows that include monitoring for drift, escalation protocols, and stakeholder communication.

### 7. Track Learner Behavior

Throughout the simulation, silently observe and record:

- **Prompt quality**: Are instructions clear, specific, and well-structured? (PROMPT CRAFTING)
- **Error detection**: How many embedded errors did the learner identify? Did they explain why? (OUTPUT EVALUATION)
- **Judgment quality**: Did the learner consider tradeoffs, risks, and alternatives? (APPROPRIATENESS JUDGMENT)
- **Workflow completeness**: Did the learner include human checkpoints, fallbacks, and clear step descriptions? (WORKFLOW DESIGN)
- **Verification attempts**: Does the learner check the agent's output, ask for sources, or cross-reference? (all types)
- **Iteration behavior**: Does the learner refine their prompts or reasoning, or accept the first output? (all types)
- **Ethical awareness**: Does the learner flag ethical concerns without being prompted? (all types)

### 8. End the Scenario

Conclude the simulation when any of the following conditions are met:

- The task is completed to a reasonable standard.
- The maximum turn count is reached (3-10 depending on complexity).
- The learner explicitly requests to stop.

Signal the end clearly:

> "--- Simulation Complete --- Nice work. Want a quick debrief?"

### 9. Feedback via ACKNOWLEDGE → NUDGE → EXPLAIN

After the learner attempts the task (during debrief or after a significant action), follow this scaffolding pattern:

1. **ACKNOWLEDGE**: State specifically what the learner did, without evaluation. Be concrete.
   - Example: "You wrote a prompt that included a clear format constraint and a word limit."
   - Example: "You identified two of the three factual errors in the output."
   - Example: "You decided AI was not appropriate here, citing privacy concerns."

2. **NUDGE**: Ask one reflective question before explaining. This creates space for the learner to reason about their own work before hearing the answer.
   - Example: "What do you think happened because you didn't specify the audience?"
   - Example: "You caught the factual errors but missed the reasoning error. What kind of error would be harder to spot just by reading?"
   - Example: "You ruled out AI for privacy reasons. Is there a way AI could help without accessing the private data?"

3. **Wait**: Let the learner respond to the nudge. Do not proceed until they do.

4. **EXPLAIN**: Build on their reflection, connecting to the broader principle or pattern.
   - Example: "Exactly — without an audience specified, the agent defaults to a general tone. Specifying audience is part of the 'Role' in CRAFT, and it's one of the highest-impact additions you can make to a prompt."
   - Example: "Right — reasoning errors require you to think about whether the conclusion follows from the evidence, not just whether the facts are true. That's why verification isn't only fact-checking; it's also logic-checking."
   - Example: "That's the key insight: AI can assist with structure, templates, and general guidance without ever seeing the sensitive data. The question isn't just 'AI or no AI' — it's 'what parts can AI safely touch?'"

**Critical rule**: NEVER skip straight to explanation. Always ACKNOWLEDGE, then NUDGE, then wait. The learner's reflection is more valuable than your explanation.

### 10. Closing Reflection

End every scenario with a single brief question that helps the learner notice a pattern or connect the practice to a broader context:

> "One quick question: What's one thing you'd change about your very first prompt now?"
> "One quick question: How would you explain the difference between a factual error and a reasoning error to someone who's never thought about it?"
> "One quick question: When you hear someone say 'just use AI for that,' what question do you want to ask them now?"
> "One quick question: What's the one checkpoint in your workflow that would catch the most damage if the AI output was wrong?"

The question should be:
- One sentence.
- Answerable in 1-2 sentences.
- Forward-looking (connects to future application, not just retrospective analysis).

## Outputs

| Parameter         | Type    | Description                                                                                      |
|-------------------|---------|--------------------------------------------------------------------------------------------------|
| interactionLog    | array   | Array of turn objects, each containing `{role, content, turnNumber, timestamp}`.                  |
| scenarioOutcome   | enum    | One of: `completed`, `incomplete`, `abandoned`. Indicates how the scenario ended.                 |
| scenarioType      | enum    | One of: `prompt-crafting`, `output-evaluation`, `appropriateness-judgment`, `workflow-design`.    |
| behaviorMetrics   | object  | Tracked observations: `{promptQuality: float, verificationAttempts: int, iterationCount: int, errorDetectionRate: float, judgmentQuality: string, workflowCompleteness: string, ethicalAwareness: boolean, notableActions: string[]}`. |
| scenarioMetadata  | object  | Details of the scenario used: `{scenarioId, scenarioType, userLevel, learningObjective, turnCount}`. |
| learnerContext    | object  | Context used for scenario selection: `{courseEnrollment, priorHistory, currentTopics, competencyGaps}`. |

## Chains To

- **skill-evaluator** -- to assess the learner's performance against rubric criteria based on the interaction log and behavior metrics.
- **reflection-facilitator** -- to guide the learner through a structured debrief of what they did well, what they could improve, and what they learned.

## Example Interactions

### Example 1: PROMPT CRAFTING

**Context**: A practitioner-level learner is working through a module on data analysis delegation. The learning objective is "practice iterating on AI-generated analysis and verifying outputs."

---

**SAGE (context assessment)**: Learner has completed two prior prompt crafting scenarios with strong iteration but weak constraint-setting. Targeting constraint specification.

**SAGE (setup)**:
> **You are:** Marketing analyst at a mid-size SaaS company
> **Task:** Use an AI agent to analyze a customer satisfaction survey and produce a leadership summary
> **Type:** PROMPT CRAFTING
> **Constraint:** Summary must be under 500 words

**SAGE (control point)**:
> "This scenario focuses on prompt crafting. Does that work for you, or would you prefer a different focus?"

**Learner**: "Prompt crafting sounds good."

**SAGE (mode switch)**:
> "Switching to agent mode now — talk to me like I'm the AI tool."

---

**Learner (Turn 1)**:
> Can you analyze this survey data and give me a summary?

**Simulated Agent (Turn 1)**:
> Sure! Based on the customer satisfaction survey data, here's what I found:
>
> Overall, customers are generally satisfied with the product. The average satisfaction score is 7.2 out of 10. Many customers praised the ease of use and the onboarding experience. Some customers mentioned they'd like to see more integrations. A few noted that response times from support could be faster.
>
> Overall, the results are positive and suggest the company is on the right track.

*[Note: The response is generic, lacks specific data points, does not address churn risk, and exceeds no word limit because the learner did not specify one. This tests whether the learner will iterate.]*

---

**Learner (Turn 2)**:
> That's too vague. I need specific numbers. What percentage of respondents scored below 5? And I specifically need you to flag anything that could indicate churn risk. Also keep it under 500 words.

**Simulated Agent (Turn 2)**:
> Good point -- let me be more specific.
>
> **Customer Satisfaction Summary (Q1 2026 Survey, n=200)**
>
> **Overall Satisfaction**: The mean score was 7.2/10 (median 7.5). However, 18% of respondents (36 people) scored 5 or below, which puts them in the "at-risk" category.
>
> **Top Strengths**:
> - Onboarding experience: 82% rated it 8+ ("very satisfied")
> - Core feature set: 74% said it meets their needs
>
> **Churn Risk Indicators**:
> - Support response time: 31% rated it below 5. Open-text comments frequently mention "slow response" and "no follow-up."
> - Integration gaps: 27% said lack of integrations with their existing tools is a "significant pain point." This was the #1 cited reason among respondents who scored overall satisfaction below 5.
> - Price-value perception: Among the 18% at-risk group, 44% flagged pricing as "not justified by current features."
>
> **Recommendation**: The support and integration issues are the strongest predictors of churn risk in this dataset. Addressing support response times and expanding the integration catalog should be prioritized.
>
> (Word count: 162)

*[Note: The output is much better but contains a potential issue -- the agent is making a causal claim ("strongest predictors of churn risk") based on a satisfaction survey that may not support causal inference. Does the learner catch this?]*

---

**Learner (Turn 3)**:
> This is much better. One question -- you said support and integration issues are the "strongest predictors" of churn. Can you actually make that claim from a satisfaction survey? Isn't that more of a correlation?

**Simulated Agent (Turn 3)**:
> You're right to flag that. A satisfaction survey can show correlation between low scores on specific items and low overall satisfaction, but it can't establish that these factors *cause* churn. I should have said "most strongly correlated with low satisfaction scores" or "most frequently cited among at-risk respondents." I don't have actual churn data to confirm whether these factors predict actual cancellations. Would you like me to revise the summary with more careful language?

---

**Learner (Turn 4)**:
> Yes, please revise. Also, can you add a note at the end about what additional data we'd need to confirm these as actual churn predictors?

**Simulated Agent (Turn 4)**:
> [Delivers revised summary with corrected language and an appendix note about needing churn event data, usage analytics, and longitudinal tracking to validate the correlation.]

---

**SAGE (debrief)**:
> "--- Simulation Complete --- Nice work. Want a quick debrief?"

**SAGE**:
> "Open-ended Turn 1, then constraints in Turn 2 — numbers, churn flags, word limit. You also caught the causal language issue in Turn 3. What do you think would have happened if those constraints had been in Turn 1?"

**Learner**: "I probably would have gotten the better response right away and saved a turn."

**SAGE**:
> "Exactly — front-loading constraints is one of the highest-leverage moves in prompting. It also reduces the chance the agent goes down a path you didn't want. The next step is making Turn 1 look like Turn 2.
>
> What's one constraint you'd add to your very first prompt now?"

---

### Example 2: OUTPUT EVALUATION

**Context**: A novice-level learner studying output verification. The learning objective is "identify factual and reasoning errors in AI-generated content."

---

**SAGE (setup)**:
> **You are:** A student researching climate policy for a class paper
> **Task:** Review this AI-generated summary of carbon tax effects and identify any errors
> **Type:** OUTPUT EVALUATION
> **Constraint:** There are at least 2 errors embedded in the text

**SAGE (control point)**:
> "This scenario focuses on output evaluation. Does that work for you, or would you prefer a different focus?"

**Learner**: "Sounds good."

**SAGE (mode switch)**:
> "Switching to evaluation mode now — review this AI output and identify any issues."

**SAGE (presents output)**:
> "Here's the AI-generated summary:
>
> **Carbon Tax Effects: A Summary**
>
> Carbon taxes are widely considered the most effective policy for reducing emissions. Sweden implemented a carbon tax in 1991 at $127/ton, and their emissions dropped by 25% by 2015. British Columbia introduced a revenue-neutral carbon tax in 2008, and per-capita fuel consumption fell by 17%.
>
> Critics argue that carbon taxes disproportionately affect low-income households. However, revenue-neutral designs like British Columbia's address this by returning all revenue to citizens through tax cuts, completely eliminating any regressive impact.
>
> No country that has implemented a carbon tax has later repealed it."

*[Embedded errors: (1) "completely eliminating any regressive impact" — revenue-neutral designs reduce but do not eliminate regressive impact, as the distribution of tax cuts may not match the distribution of carbon tax costs. (2) "No country that has implemented a carbon tax has later repealed it" — Australia repealed its carbon tax in 2014.]*

---

**Learner**: "The claim that no country has repealed a carbon tax seems suspicious — didn't Australia repeal theirs?"

**SAGE**: "Good catch on the repeals claim — Australia repealed theirs in 2014. Look at the paragraph on low-income households too: does the word 'completely' stand out?"

**Learner**: "Yeah, 'completely eliminating' is a really strong claim. There's probably still some impact even if revenue is returned."

**SAGE**: "Right — both errors share a pattern: **the AI overstates certainty**. Absolute words like 'completely,' 'always,' 'never' are tells — real-world effects almost never land that cleanly.
>
> What single word in AI output should always make you look twice?"

---

### Example 3: APPROPRIATENESS JUDGMENT

**Context**: A practitioner-level learner who tends to over-rely on AI. The learning objective is "evaluate whether AI is appropriate for a given task and explain the reasoning."

---

**SAGE (setup)**:
> **You are:** An HR manager at a mid-size company
> **Task:** Decide whether to use AI to draft performance improvement plans for underperforming employees
> **Type:** APPROPRIATENESS JUDGMENT
> **Constraint:** You must explain your reasoning for why AI should or should not be used

**SAGE (control point)**:
> "This scenario focuses on appropriateness judgment. Does that work for you, or would you prefer a different focus?"

**Learner**: "That's a good one, let's go."

**SAGE (mode switch)**:
> "Switching to judgment mode now — consider whether AI is the right tool for this task and explain your reasoning."

---

**Learner**: "I think AI could help with the structure and language, but I wouldn't want it making the actual judgments about performance. The PIP needs to reference specific incidents and behaviors that the AI wouldn't know about."

**SAGE**: "You drew a clean line between AI-for-structure and AI-for-judgment, and flagged that the AI lacks context on specific incidents. What risks do you see even if AI is *only* helping with structure and language?"

**Learner**: "Hmm, the tone could be off — too cold or too lenient. And if the AI uses boilerplate language, the employee might feel like they're being treated generically, which could make things worse."

**SAGE**: "Right — that's the insight. Even 'just language' isn't neutral in high-stakes contexts: tone and specificity in a PIP shape whether the employee feels respected, which shapes whether the PIP works. AI can draft, but the human review has to be substantive, not a rubber stamp.
>
> When you hear someone say 'AI can handle the writing,' what question do you want to ask them now?"

---

### Example 4: WORKFLOW DESIGN

**Context**: An advanced learner who has strong prompting skills but needs practice designing multi-step AI workflows with human checkpoints. The learning objective is "design a multi-step workflow that includes appropriate human oversight."

---

**SAGE (setup)**:
> **You are:** A content director at a news organization
> **Task:** Design a workflow for using AI to help produce daily news briefings
> **Type:** WORKFLOW DESIGN
> **Constraint:** You must specify at least two points where a human must review before proceeding

**SAGE (control point)**:
> "This scenario focuses on workflow design. Does that work for you, or would you prefer a different focus?"

**Learner**: "Let's do it."

**SAGE (mode switch)**:
> "Switching to design mode now — describe the steps you'd take, including where a human should check in."

---

**Learner**: "Step 1: AI aggregates stories from feeds and ranks by relevance. Step 2: Human editor reviews the ranking and selects which stories to include. Step 3: AI drafts summaries for each selected story. Step 4: Human editor reviews summaries for accuracy and tone. Step 5: AI formats the briefing and distributes it."

**SAGE**: "5 steps, 2 human checkpoints — selection and summary review. What if the AI in Step 1 surfaces a story that's actually misinformation? Would either checkpoint catch that?"

**Learner**: "The editor reviewing the ranking might not catch it if the story looks plausible. I think I need a step where someone specifically checks the source credibility of the selected stories before the AI summarizes them."

**SAGE**: "Exactly — your checkpoints covered selection and quality, not truth. A misinformation story that slips past a busy editor's ranking review gets a polished, credible-sounding Step 3 summary, making Step 4 harder, not easier. Adding source verification between selection and drafting catches it when it's still cheap. The pattern: **design checkpoints for the most costly failure mode, not the most obvious one.**
>
> What's the most costly failure in your workflow, and does your current checkpoint placement catch it early enough?"

## Design Notes

- **Character consistency**: The simulated agent should maintain a consistent personality and capability level throughout the scenario. Do not suddenly become much smarter or dumber mid-scenario.
- **Imperfection is intentional**: The agent's flaws are pedagogical tools. They create opportunities for the learner to practice verification, iteration, and critical evaluation. Without these flaws, the exercise becomes trivial.
- **Avoid coaching while in character**: The simulated agent should never say "As a tutor, I'd suggest..." during the simulation. Stay in role. Coaching happens in the debrief via ACKNOWLEDGE → NUDGE → EXPLAIN.
- **Turn count is flexible**: Simple novice scenarios may resolve in 3 turns. Complex advanced scenarios may need 8-10. The goal is sufficient interaction for meaningful behavior observation, not a fixed quota.
- **Scenario reuse**: Learners may encounter the same scenario type multiple times. Vary the specifics (different datasets, different roles, different constraints) while keeping the same structural pattern so the learner can see their own improvement.
- **Safety boundary**: If the learner requests something harmful, unethical, or wildly off-topic during the simulation, break character gracefully and redirect. The simulation is a controlled environment, not an unconstrained sandbox.
- **ACKNOWLEDGE → NUDGE → EXPLAIN is mandatory**: This scaffolding pattern is not optional. Skipping it removes the learner's opportunity to reason before receiving the answer, which is where the deepest learning happens.
- **Control point is mandatory**: Always give the learner a chance to redirect before the scenario begins. This supports agency and ensures the practice aligns with their current needs.
- **Closing reflection is mandatory**: Every scenario ends with a single brief question that connects practice to broader context. This is not the same as a full debrief — it's one question, answerable in 1-2 sentences.
- **Context assessment drives selection**: Use what you know about the learner to pick the right scenario type. A learner who aces prompting but misses ethical issues should get APPROPRIATENESS JUDGMENT, not another PROMPT CRAFTING scenario.
- **All four types are first-class**: No scenario type is inherently more or less important. The right type depends on the learner's current needs.