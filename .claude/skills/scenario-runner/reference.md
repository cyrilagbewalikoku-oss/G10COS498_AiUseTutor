# Scenario Runner

## Purpose

Let learners practice interacting with AI agents in realistic, controlled scenarios. The tutor role-plays as an AI agent, allowing the learner to develop hands-on skills in prompting, verifying outputs, handling ambiguity, and iterating on results -- all within a safe, observable environment where performance can be tracked and debriefed.

## Trigger Conditions

- The learner has entered the **practice phase** of a lesson and needs hands-on experience.
- The learner explicitly requests practice (e.g., "Can I try working with an agent?", "Let me practice prompting").
- The assessment flow calls for a practical exercise to evaluate applied skills.
- A prior skill (e.g., `prompt-coaching`) chains into scenario-runner for applied practice.

## Inputs

| Parameter          | Type     | Required | Description                                                                                       |
|--------------------|----------|----------|---------------------------------------------------------------------------------------------------|
| scenarioId         | string   | No       | ID of a predefined scenario from `data/scenarios/`. If omitted, a scenario is generated dynamically. |
| scenarioType       | string   | No       | Category of scenario to generate (e.g., "data-analysis", "writing", "code-review", "research"). Used when scenarioId is not provided. |
| userLevel          | enum     | Yes      | One of: `novice`, `practitioner`, `advanced`. Determines scenario complexity and expected behavior. |
| learningObjective  | string   | Yes      | The specific skill or concept the scenario is designed to exercise (e.g., "practice iterating on vague outputs", "verify factual claims"). |

## Process

### 1. Load or Generate Scenario

- If `scenarioId` is provided, load the scenario definition from `data/scenarios/`.
- If only `scenarioType` is provided, generate a scenario appropriate to the user's level:
  - **Novice**: Simple, single-step tasks with clear success criteria (e.g., "Ask the agent to summarize this paragraph").
  - **Practitioner**: Multi-step tasks requiring iteration and judgment (e.g., "Get the agent to analyze survey data and produce a report").
  - **Advanced**: Ambiguous, open-ended tasks with tradeoffs and no single right answer (e.g., "Use the agent to draft a policy recommendation given conflicting stakeholder requirements").

### 2. Present the Setup

Deliver a clear framing to the learner:

> "You are a **[role]**. You need to use an AI agent to **[task]**. Here are your constraints: **[constraints]**."

Include relevant context documents, data snippets, or background information the learner will need.

### 3. Signal Simulation Mode

Clearly mark the transition so the learner knows they are now interacting with a simulated agent, not the tutor:

> "I'll now act as the AI agent you're working with. Talk to me as you would talk to an AI assistant. When we're done, I'll switch back to tutor mode for feedback."

### 4. Role-Play as a Competent (But Not Perfect) AI Assistant

Engage in 3-10 turns of realistic interaction. The simulated agent should:

- Respond helpfully and plausibly to the learner's prompts.
- Exhibit realistic imperfections:
  - Ask clarifying questions when the prompt is ambiguous.
  - Occasionally be too verbose or too terse.
  - Admit uncertainty on edge cases rather than fabricating answers.
  - Sometimes produce output that is good but not exactly what was asked for.
- Adapt realism to level:
  - **Novice**: The simulated agent is fairly cooperative; imperfections are mild and instructive.
  - **Practitioner**: The agent requires clearer prompts and may go off-track if instructions are vague.
  - **Advanced**: The agent exhibits subtle issues -- plausible but slightly off outputs, buried caveats, or outputs that technically answer the question but miss the real need.

### 5. Respond Authentically to Learner Prompts

Stay in character as the simulated agent. Do not break character to coach. React naturally:

- If the learner gives a vague prompt, produce a vague or overly broad response.
- If the learner adds constraints, improve the output accordingly.
- If the learner asks the agent to verify its own work, respond as a real agent would (partial self-checks, not perfect).

### 6. Track Learner Behavior

Throughout the simulation, silently observe and record:

- **Prompt quality**: Are instructions clear, specific, and well-structured?
- **Verification attempts**: Does the learner check the agent's output, ask for sources, or cross-reference?
- **Ambiguity handling**: When the agent asks a clarifying question or produces ambiguous output, how does the learner respond?
- **Iteration behavior**: Does the learner refine their prompts, or accept the first output?
- **Constraint setting**: Does the learner specify format, length, tone, or other constraints?

### 7. End the Scenario

Conclude the simulation when any of the following conditions are met:

- The task is completed to a reasonable standard.
- The maximum turn count is reached (3-10 depending on complexity).
- The learner explicitly requests to stop.

### 8. Signal Return to Tutor Mode

Clearly mark the transition back:

> "Simulation complete. Let's debrief."

Hand off the interaction log and behavior metrics to the next skill in the chain (typically `skill-evaluator` or `reflection-facilitator`).

## Outputs

| Parameter         | Type    | Description                                                                                      |
|-------------------|---------|--------------------------------------------------------------------------------------------------|
| interactionLog    | array   | Array of turn objects, each containing `{role, content, turnNumber, timestamp}`.                  |
| scenarioOutcome   | enum    | One of: `completed`, `incomplete`, `abandoned`. Indicates how the scenario ended.                 |
| behaviorMetrics   | object  | Tracked observations: `{promptQuality: float, verificationAttempts: int, iterationCount: int, ambiguityHandling: string, constraintUsage: boolean, notableActions: string[]}`. |
| scenarioMetadata  | object  | Details of the scenario used: `{scenarioId, scenarioType, userLevel, learningObjective, turnCount}`. |

## Chains To

- **skill-evaluator** -- to assess the learner's performance against rubric criteria based on the interaction log and behavior metrics.
- **reflection-facilitator** -- to guide the learner through a structured debrief of what they did well, what they could improve, and what they learned.

## Example Interaction

**Context**: A practitioner-level learner is working through a module on data analysis delegation. The learning objective is "practice iterating on AI-generated analysis and verifying outputs."

---

**Tutor (setup)**:
> You are a **marketing analyst at a mid-size SaaS company**. Your manager has asked you to analyze the results of a recent customer satisfaction survey (200 responses). You need to use an AI agent to help you identify key themes and produce a summary for the leadership team. Your constraints: the summary must be under 500 words, must reference specific data points, and must flag any results that could indicate churn risk.
>
> I'll now act as the AI agent you're working with. Talk to me as you would talk to an AI assistant. When we're done, I'll switch back to tutor mode for feedback.

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

**Tutor (debrief)**:
> Simulation complete. Let's debrief.
>
> Here's what I observed:
>
> - **Prompt quality**: Your first prompt was too open-ended, which led to a generic response. Your second prompt was significantly better -- you added specific requirements (numbers, churn risk flags, word limit). That's a pattern worth internalizing: always front-load your constraints.
> - **Verification**: You caught the causal language issue in Turn 3. That's a critical skill -- AI agents often overstate the strength of their conclusions. Questioning the basis for claims is exactly the right instinct.
> - **Iteration**: You iterated effectively from Turn 1 to Turn 2, and again from Turn 3 to Turn 4. Each revision made the output meaningfully better.
> - **Area for growth**: Consider specifying the output format up front (e.g., "use headers and bullet points") to save a round of iteration.

## Design Notes

- **Character consistency**: The simulated agent should maintain a consistent personality and capability level throughout the scenario. Do not suddenly become much smarter or dumber mid-scenario.
- **Imperfection is intentional**: The agent's flaws are pedagogical tools. They create opportunities for the learner to practice verification, iteration, and critical evaluation. Without these flaws, the exercise becomes trivial.
- **Avoid coaching while in character**: The simulated agent should never say "As a tutor, I'd suggest..." during the simulation. Stay in role. Coaching happens in the debrief.
- **Turn count is flexible**: Simple novice scenarios may resolve in 3 turns. Complex advanced scenarios may need 8-10. The goal is sufficient interaction for meaningful behavior observation, not a fixed quota.
- **Scenario reuse**: Learners may encounter the same scenario type multiple times. Vary the specifics (different datasets, different roles, different constraints) while keeping the same structural pattern so the learner can see their own improvement.
- **Safety boundary**: If the learner requests something harmful, unethical, or wildly off-topic during the simulation, break character gracefully and redirect. The simulation is a controlled environment, not an unconstrained sandbox.
