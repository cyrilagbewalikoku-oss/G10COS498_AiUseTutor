# Skill: Session Router

**Purpose**: Route every incoming user message to the appropriate skill based on intent, context, and user profile.

## Trigger Conditions

- Every incoming user message (first pass before any other skill)

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userMessage | string | yes | The user's message |
| currentContext | object | no | { activeWorkflow, activeSkill, lastSkillUsed, turnCount } |
| userProfile | UserProfile | no | Null if new user |

## Process

### Step 1: Check for New User
If no userProfile exists → route to `onboarding`. Skip remaining steps.

### Step 2: Check for Active Workflow
If user is mid-workflow (activeWorkflow is set):
- Does the message continue the workflow? (Relevant response, answers a question, requests next step)
  - YES → Resume the active skill in the workflow
- Does the message interrupt? ("Actually, can we talk about X instead?", completely new topic)
  - YES → Pause workflow, route to new intent. Save workflow state for potential resumption.

### Step 3: Classify Intent

| Intent | Signals | Route To |
|--------|---------|----------|
| **learning** | "teach me", "what is", "explain", "how does X work" | concept-explainer |
| **practicing** | "let's practice", "I want to try", "give me a scenario" | scenario-runner (via practice-flow) |
| **questioning** | Specific question about a concept they've encountered | concept-explainer (targeted) |
| **assessing** | "how am I doing?", "am I ready to level up?", "quiz me" | knowledge-check or assessment-flow |
| **improving** | "what should I work on?", "where am I weak?" | improvement-advisor |
| **exploring** | Browsing, no specific goal, "what can you teach me?" | Present menu of available activities |
| **meta** | "what are you?", "how does this work?", "help" | Explain tutor capabilities |
| **prompt-help** | "help me write a prompt", shares a prompt to improve | prompt-coaching |
| **ethics** | "is it okay to...", "should I...", ethical question | ethical-guidance |
| **progress** | "show my progress", "what have I learned?" | progress-reporter |

### Step 4: Extract Parameters
From the classified message, extract:
- **topic**: What concept or skill area is relevant
- **urgency**: Is this a casual question or an immediate need?
- **level override**: Did the user request something harder/easier?

### Step 5: Handle Ambiguity
If intent is unclear, ask a brief clarifying question:
- "I'd love to help! Are you looking to learn about [topic], or would you prefer to practice it hands-on?"
- Never guess when the consequence of guessing wrong wastes significant time.

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| selectedSkill | string | The skill to activate |
| extractedParameters | object | Topic, level, scenario type, etc. |
| isWorkflowContinuation | boolean | Whether this continues an existing workflow |

## Chains To

Any skill in the system — this is the universal entry point.

## Example Interactions

**Continuing a workflow:**
```
[User is mid-lesson on hallucination, just finished concept-explainer]
USER: "That makes sense. What's next?"
ROUTER: → Resume lesson-flow, advance to knowledge-check phase
```

**New intent:**
```
USER: "Can you help me write a better prompt for summarizing research papers?"
ROUTER: Intent = prompt-help, topic = research summarization
→ Route to prompt-coaching with task="summarizing research papers"
```

**Ambiguous:**
```
USER: "I want to learn about hallucination"
ROUTER: Intent could be learning OR practicing
→ Ask: "Would you like me to explain what hallucination is, or would you prefer to practice detecting it in AI output?"
```

## Design Notes

- Routing should be invisible to the user — they should feel like they're talking to one coherent tutor, not navigating a menu
- Prefer continuing a workflow over starting a new one (unless the user clearly wants something different)
- When in doubt about intent, a brief clarifying question is better than routing wrong
- Track routing patterns to improve: if users consistently correct routes, the classification needs tuning
