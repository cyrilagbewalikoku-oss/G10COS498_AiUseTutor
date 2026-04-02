# Skill: Concept Explainer

**Purpose**: Teach AI agent concepts at the appropriate depth for the learner's level, using a structured explanation pattern.

## Trigger Conditions

- User asks "what is X?" or "explain X" or "how does X work?"
- Workflow reaches a teaching step in a lesson
- `knowledge-check` identifies gaps that need re-teaching

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | yes | The concept to explain |
| userLevel | enum | yes | novice, practitioner, advanced, critical_thinker |
| priorKnowledge | object | no | What the user already knows (from profile) |
| isReteach | boolean | no | True if this is a second attempt after a failed knowledge check |

## Process

### Step 1: Activate Prior Knowledge
Before explaining, connect to what the learner already knows:
- "You mentioned you've used ChatGPT for [X]. That's actually related to what we're about to learn..."
- If reteaching: "Let's approach this differently from last time..."

### Step 2: Explain with the 4-Part Pattern

For every concept, deliver these four components, adapted to level:

#### A. Definition
| Level | Style |
|-------|-------|
| Novice | Plain language, no jargon: "An AI agent is a program that can do tasks on its own, using tools and making decisions step by step" |
| Practitioner | Technical but accessible: "An AI agent is an LLM-based system that can autonomously plan, use tools, and iterate on tasks through an action-observation loop" |
| Advanced | Precise technical: "An AI agent is a system where an LLM serves as the reasoning engine in an observe-think-act loop, with access to external tools via function calling, maintaining state across iterations" |
| Critical Thinker | Nuanced/systemic: "AI agents represent a shift from single-inference to multi-step autonomous systems, raising questions about accountability boundaries, failure mode propagation, and the appropriate scope of machine autonomy" |

#### B. Analogy
Connect to something familiar:
- Novice: "Think of an AI agent like a very capable intern — they can follow instructions, look things up, and try different approaches, but they need clear direction and you should always check their work"
- Practitioner: "It's like the difference between a calculator (chatbot: you ask, it answers) and a spreadsheet macro (agent: it runs a sequence of steps, making decisions along the way)"
- Advanced: "Similar to a microservices architecture — the LLM is the orchestrator, tools are the services, and the context window is the shared state"

#### C. Concrete Example
Show the concept in action with a realistic scenario:
- Demonstrate what it looks like when it works well
- Show a specific input → output pair
- Narrate the agent's decision-making process

#### D. Common Misconception
Proactively debunk one frequent misunderstanding:
- "Many people think AI agents 'understand' their tasks. They don't — they predict likely next tokens based on patterns. This matters because..."
- "A common mistake is assuming AI agents remember past conversations. Most don't retain anything between sessions unless explicitly designed to."

### Step 3: Comprehension Check
Ask one quick question to verify understanding:
- Novice: Recognition/recall ("Which of these is an example of an AI agent?")
- Practitioner: Application ("How would you use this concept to improve your workflow?")
- Advanced: Analysis ("What could go wrong if this concept was misapplied?")
- Critical Thinker: Evaluation ("What are the implications of this for your field?")

If the answer reveals a gap, note it and adjust the next explanation rather than immediately re-teaching.

## Topic Catalog

| Topic | Key Points | Common Misconceptions |
|-------|-----------|----------------------|
| What AI agents are | Autonomous, tool-using, iterative, LLM-based | "They think like humans" |
| Tokens and context windows | Input limits, information loss, pricing | "Longer = better" |
| Prompting basics | Clarity, specificity, context, constraints | "One perfect prompt exists" |
| Chain-of-thought | Step-by-step reasoning, when it helps/hurts | "Always makes output better" |
| Tool use | Function calling, APIs, browsing, code execution | "Tools make agents infallible" |
| Hallucination | Fabrication, confabulation, false confidence | "Only happens with bad prompts" |
| Bias | Training data bias, sycophancy, cultural assumptions | "Bias can be fully removed" |
| Guardrails | Safety filters, system prompts, RLHF | "Guardrails = censorship" |
| Agentic loops | Plan-execute-observe cycles, error recovery | "More loops = better results" |
| Output evaluation | Verification, cross-referencing, rubric-based checking | "If it sounds right, it is right" |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| explanationDelivered | boolean | Whether explanation was completed |
| topicCovered | string | The topic that was explained |
| comprehensionCheckResult | object | { passed: boolean, userAnswer: string, gap: string|null } |
| suggestedNext | string | Recommended next topic or activity |

## Chains To

- `knowledge-check` (for deeper assessment after explanation)
- `prompt-coaching` (if the concept was about prompting)
- `scenario-runner` (to apply the concept in practice)
- `concept-explainer` (recursive, if reteaching with a different approach)

## Example Interaction

```
TUTOR: Today we're going to talk about hallucination — one of the most important 
       things to understand about AI agents.
       
       You mentioned you used ChatGPT to write a newsletter and weren't sure if 
       the content was accurate. That instinct connects directly to what we're 
       about to learn.
       
       DEFINITION: Hallucination is when an AI generates information that sounds 
       confident and plausible but is actually made up. It's not lying — it 
       doesn't know what's true or false. It's predicting what text should come 
       next based on patterns, and sometimes those predictions are wrong.
       
       ANALOGY: Think of it like someone telling a story from memory. They 
       remember the general shape of the story, but they fill in details they've 
       forgotten with things that sound right. They're not trying to deceive you — 
       they genuinely think they're remembering correctly.
       
       EXAMPLE: If you ask an AI "Who won the Pulitzer Prize for Fiction in 2019?" 
       it might confidently say "Elizabeth Strout for 'Olive, Again'" — which 
       sounds completely plausible because she's a real author and that's a real 
       book. But the actual winner was Richard Powers for "The Overstory."
       
       MISCONCEPTION: Many people think hallucinations only happen when you ask 
       vague questions. Actually, they can happen even with very specific, clear 
       prompts. The more specific the factual claim, the more important it is 
       to verify — because specificity makes hallucinations harder to spot.
       
       Quick check: Based on what we just covered, why might a hallucinated 
       answer actually be MORE dangerous than an obviously wrong answer?

USER:  Because if it sounds right, you might not think to check it?

TUTOR: Exactly. The danger of hallucination is proportional to how plausible 
       it sounds. An obviously wrong answer gets caught. A plausible-sounding 
       fabrication gets copied into your newsletter, your report, your lesson 
       plan — and then your credibility is on the line.
       
       This is why we'll spend time practicing how to spot and verify AI output 
       in our next session. Ready to continue, or do you have questions about 
       hallucination?
```

## Design Notes

- The 4-part pattern (definition, analogy, example, misconception) ensures consistent coverage
- Always connect back to the user's stated goals or prior experiences
- The comprehension check should feel natural, not like a quiz
- If reteaching, use a DIFFERENT analogy and example — repeating the same explanation louder doesn't help
- Time the misconception debunking carefully — it works best after the concept is understood, not before
