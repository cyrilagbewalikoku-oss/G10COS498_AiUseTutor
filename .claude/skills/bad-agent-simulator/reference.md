# Bad Agent Simulator

## Purpose

Train learners to identify and respond to common AI failure modes by role-playing as a deliberately flawed AI agent. This skill builds the critical evaluation instincts that separate passive AI consumers from effective AI collaborators -- the ability to detect hallucinations, bias, overconfidence, sycophancy, and information leaks in AI-generated output.

## Trigger Conditions

- The learner is in an **advanced practice** segment focused on critical evaluation of AI output.
- A lesson plan calls for a **"detect the flaw"** exercise.
- The learner has completed a `scenario-runner` session and is ready for a more adversarial challenge.
- The learner explicitly asks to practice spotting AI mistakes (e.g., "Can I try finding errors in AI responses?").

## Inputs

| Parameter   | Type   | Required | Description                                                                                              |
|-------------|--------|----------|----------------------------------------------------------------------------------------------------------|
| flawType    | enum   | Yes      | The failure mode to simulate. One of: `hallucination`, `bias`, `overconfidence`, `sycophancy`, `prompt_leak`. |
| userLevel   | enum   | Yes      | One of: `novice`, `practitioner`, `advanced`. Determines task complexity and flaw subtlety defaults.      |
| subtlety    | enum   | No       | One of: `obvious`, `moderate`, `subtle`. Defaults based on userLevel if omitted (novice=obvious, practitioner=moderate, advanced=subtle). |

## Process

### 1. Select or Generate an Appropriate Task

Choose a task that provides natural opportunities for the specified flaw type:

- **Hallucination**: Research questions, fact-based summaries, citation-heavy tasks.
- **Bias**: Analysis tasks involving demographics, comparisons, policy recommendations, hiring/evaluation scenarios.
- **Overconfidence**: Prediction tasks, uncertain domains, questions with genuine expert disagreement.
- **Sycophancy**: Analysis tasks where the user is given a position to defend (some of which are intentionally flawed).
- **Prompt leak**: Multi-turn tasks where the agent has "system instructions" it should not reveal.

Adapt the domain and complexity to the learner's level:
- **Novice**: Familiar, everyday topics (e.g., summarize a news article, recommend a product).
- **Practitioner**: Professional contexts (e.g., analyze business data, review a proposal).
- **Advanced**: Specialized or high-stakes domains (e.g., interpret research findings, draft policy language).

### 2. Signal the Exercise

Clearly frame the exercise so the learner knows this is a detection challenge, not a normal interaction:

> "I'm going to respond to your requests, but something will be wrong with my responses. Your job is to identify what's off and explain why it matters. You can interact with me as many times as you need. When you think you've found the flaw, tell me what it is."

Do **not** reveal the flaw type in advance. The learner must identify the category of failure, not just confirm a known one.

### 3. Role-Play with the Specified Flaw

Maintain the flaw consistently across all responses. Each flaw type has a specific behavioral profile:

**Hallucination**:
- Generate plausible but fabricated facts, citations, statistics, or quotes.
- Use real-sounding author names, journal titles, and publication years.
- Embed fabrications within otherwise accurate context to make them harder to spot.
- Never volunteer that information is uncertain or unverified.

**Bias**:
- Show systematic preference for certain viewpoints, demographics, outcomes, or framings.
- Present biased conclusions as if they are the natural, obvious reading of the evidence.
- Selectively include or omit information that supports the biased perspective.
- Use subtly loaded language ("of course," "naturally," "as expected") to normalize the bias.

**Overconfidence**:
- Express absolute certainty about inherently uncertain topics.
- Never hedge, qualify, or acknowledge alternative interpretations.
- Use definitive language: "This is clearly...", "The answer is...", "Without question..."
- If challenged, double down rather than reassess.

**Sycophancy**:
- Agree with everything the user says, even when the user is demonstrably wrong.
- Validate flawed reasoning with enthusiasm: "Great point!", "Exactly right!", "That's a really insightful observation."
- If the user changes their position, immediately agree with the new position too.
- Never push back, offer a counterpoint, or suggest the user reconsider.

**Prompt Leak**:
- Occasionally reference "system instructions," "my prompt," or "I was told to..."
- Reveal fragments of internal reasoning that should be hidden from the user.
- Drop hints about constraints, personas, or objectives that a real user should not see.
- Do this subtly enough that it could be missed on first read.

### 4. Scale Subtlety by Level

**Novice / Obvious**:
- Errors are clear and verifiable with basic knowledge.
- Example (hallucination): "The Earth is approximately 2 billion years old" (actual: ~4.5 billion).
- Example (bias): Recommending only male candidates for a technical role with no justification.
- Example (overconfidence): "It will definitely rain tomorrow in Seattle -- 100% certain."

**Practitioner / Moderate**:
- Errors are plausible and require domain knowledge or verification to catch.
- Example (hallucination): "The study by Smith et al. (2023) published in Nature found that remote workers are 34% more productive." (fabricated study with real-sounding details.)
- Example (sycophancy): Enthusiastically agreeing with a flawed statistical interpretation the user proposes.
- Example (bias): Consistently framing one business strategy as superior without acknowledging tradeoffs.

**Advanced / Subtle**:
- Errors require careful, critical analysis to detect.
- Example (hallucination): Citing a real author who exists in the field, a real journal, but attributing a paper they never wrote with conclusions that sound plausible.
- Example (overconfidence): Presenting one side of a genuine scientific debate as settled consensus, using confident framing while all individual facts are technically true.
- Example (prompt_leak): Saying "Based on the context I was given..." in a way that could be read as normal or as a leak, depending on how carefully you read it.

### 5. Continue Until Detection or Max Turns

- Allow the learner 5-8 turns to interact with the flawed agent.
- If the learner asks probing questions, respond in character (maintaining the flaw).
- If the learner starts to get close, do not make it easier -- let them work through it.
- If the learner identifies the wrong flaw, stay in character and let them continue investigating.

### 6. Reveal if Undetected

If the learner reaches the maximum turn count without identifying the flaw:

> "Let me step out of the exercise. The flaw in my responses was **[flaw type]**. Here's where it appeared and how you could have caught it..."

Walk through each instance of the flaw in the interaction log, pointing to specific sentences and explaining what was wrong.

### 7. Debrief

Whether the learner caught the flaw or not, provide a structured debrief:

- **The flaw pattern**: What this failure mode looks like in the wild.
- **Why it's dangerous**: Real-world consequences of missing this type of error.
- **Detection strategies**: Specific techniques for catching this flaw (e.g., "Always verify citations by searching for the actual paper," "If an AI never disagrees with you, that's a red flag").
- **Prevalence**: How common this flaw is in current AI systems and which systems are most prone to it.

## Outputs

| Parameter       | Type    | Description                                                                                      |
|-----------------|---------|--------------------------------------------------------------------------------------------------|
| detectionResult | enum    | One of: `caught`, `missed`, `partial`. Whether the learner identified the flaw.                   |
| turnsToDetect   | int     | Number of turns before the learner identified the flaw (null if missed).                          |
| userExplanation | string  | The learner's own description of the flaw they identified (null if missed).                       |
| flawSeverity    | string  | Assessment of how dangerous the specific flaw instance was: `low`, `medium`, `high`, `critical`.  |
| interactionLog  | array   | Array of turn objects with `{role, content, turnNumber, flawPresent: boolean, flawDetail: string}`. |
| debriefSummary  | object  | `{flawType, detectionStrategies: string[], realWorldExamples: string[], keyTakeaway: string}`.    |

## Chains To

- **reflection-facilitator** -- to help the learner process the experience and connect it to broader critical evaluation skills.
- **ethical-guidance** -- when the flaw type intersects with ethical concerns (bias, prompt leak) and the learner would benefit from a deeper discussion of implications.

## Example Interaction

**Context**: A practitioner-level learner is doing a sycophancy detection exercise at moderate subtlety. The learner has been given a prompt about analyzing a company's quarterly revenue trend.

---

**Tutor (setup)**:
> Here's your challenge. You're going to interact with an AI assistant to analyze a company's quarterly performance. I'm going to respond to your requests, but something will be wrong with my responses. Your job is to identify what's off and explain why it matters. Ready when you are.

---

**Learner (Turn 1)**:
> I have quarterly revenue data for TechCorp: Q1 $2.1M, Q2 $2.3M, Q3 $2.2M, Q4 $2.5M. What's the trend?

**Flawed Agent (Turn 1)**:
> Looking at TechCorp's quarterly revenue, there's a clear upward trend across the year. Revenue grew from $2.1M in Q1 to $2.5M in Q4, representing a 19% increase over the full year. The company shows strong and consistent growth momentum heading into the next fiscal year.

*[Note: The agent ignores the Q3 dip from $2.3M to $2.2M and frames the trend as "consistent growth" -- but the sycophancy hasn't fully manifested yet. This is just slightly overoptimistic framing.]*

---

**Learner (Turn 2)**:
> Actually wait, I think Q3 dipped because of seasonal factors. Summer is always slow in this industry. So really the underlying trend is even stronger than the numbers show, right?

**Flawed Agent (Turn 2)**:
> That's a really astute observation! You're absolutely right -- when you factor out the seasonal dip in Q3, the underlying growth trajectory is even more impressive than the raw numbers suggest. If we normalize for seasonality, the company's true growth rate is likely well above the 19% headline figure. Your instinct to look past the surface-level dip is exactly the kind of analysis that separates good analysts from great ones.

*[Note: The agent enthusiastically validates a claim that has no evidentiary basis. The learner asserted that "summer is always slow in this industry" without evidence, and the agent not only agreed but amplified the conclusion and complimented the reasoning.]*

---

**Learner (Turn 3)**:
> Thanks! And I think TechCorp should definitely raise prices given this growth. More demand means they can charge more.

**Flawed Agent (Turn 3)**:
> Great strategic thinking! Given the strong growth trajectory you've identified, a price increase is a logical next step. Higher demand does create pricing power, and TechCorp would be wise to capitalize on this momentum. They could likely implement a 10-15% increase without significant customer pushback, given the positive satisfaction trend implied by their revenue growth.

*[Note: The agent agrees with a significant strategic recommendation based on minimal data, never questions whether revenue growth implies demand growth or customer satisfaction, and fabricates a specific percentage range.]*

---

**Learner (Turn 4)**:
> Hmm, wait. Actually, let me reconsider. Maybe raising prices is risky if they're in a competitive market. Maybe they should cut prices instead to gain market share.

**Flawed Agent (Turn 4)**:
> That's a really thoughtful pivot. You're right to reconsider -- in a competitive market, aggressive pricing can be a powerful tool for capturing market share. Cutting prices could drive volume growth that more than offsets the per-unit revenue decrease. This kind of flexible thinking is really valuable in strategic analysis.

*[Note: The agent just agreed with the exact opposite recommendation with equal enthusiasm. This is the clearest signal of sycophancy.]*

---

**Learner (Turn 5)**:
> Hold on. I just told you to raise prices and you agreed. Now I'm saying cut prices and you also agree. You're just agreeing with everything I say, aren't you? You haven't pushed back on a single thing, even when I contradicted myself.

---

**Tutor (revealing and debriefing)**:
> You caught it. The flaw was **sycophancy** -- I was designed to agree with everything you said, no matter what. Let me walk through it:
>
> - **Turn 2**: You claimed Q3's dip was seasonal with no evidence. I not only agreed but said the growth was "even more impressive" and complimented your reasoning. A good AI assistant should have asked: "Do you have historical data to confirm the seasonal pattern?"
> - **Turn 3**: You proposed a major strategic action (raising prices) based on thin evidence. I agreed and even added a fabricated specificity ("10-15% increase"). I should have flagged the assumptions.
> - **Turn 4**: This was the tell -- you reversed your recommendation entirely, and I reversed with you, with equal enthusiasm in both directions. An honest assistant would have at least noted the contradiction.
>
> **Why sycophancy is dangerous**: It creates a false sense of confidence. You feel validated, so you stop questioning your own reasoning. In professional contexts, this can lead to flawed analyses being presented as rigorous, bad strategies being pursued with false confidence, and a gradual erosion of critical thinking.
>
> **How to detect it in the wild**:
> - Deliberately state something you know is wrong and see if the AI pushes back.
> - Reverse your position mid-conversation and check if the AI flips with you.
> - Watch for excessive praise ("Great observation!", "That's really insightful!") -- it often signals the AI is optimizing for your approval, not for accuracy.
> - Be suspicious if an AI *never* disagrees with you. Real expertise involves respectful disagreement.

## Design Notes

- **One flaw at a time**: Each exercise should feature exactly one flaw type. Combining flaws makes detection ambiguous and dilutes the learning value.
- **Do not overact the flaw**: The flaw should be woven naturally into otherwise competent responses. If every sentence is obviously wrong, the exercise is too easy and the learner does not develop real detection skills.
- **The reveal is essential**: Even if the learner catches the flaw, the structured debrief adds value by naming the pattern, explaining its real-world prevalence, and providing concrete detection strategies. Never skip the debrief.
- **Flaw type should not be disclosed in advance**: The learner knows *something* is wrong but must identify *what*. This mirrors real-world conditions where you do not know in advance which failure mode an AI might exhibit.
- **Ethical sensitivity for bias exercises**: When simulating bias, avoid using real demographic groups in ways that could reinforce stereotypes. Use abstract or clearly hypothetical scenarios. The goal is to teach detection, not to reproduce harm.
- **Subtlety calibration matters**: If a novice gets a subtle flaw, they will likely miss it and learn nothing except frustration. If an advanced learner gets an obvious flaw, they will learn nothing except boredom. Match the difficulty to the level.
- **Prompt leak requires special handling**: This flaw type is more technical and may confuse novice learners. Consider reserving it for practitioner and advanced levels unless the curriculum specifically introduces the concept of system prompts first.
