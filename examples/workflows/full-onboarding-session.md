# Workflow Demo: Full Onboarding Session

**User**: Maria Santos (new user, no profile)
**Workflow**: Onboarding Flow
**Skills Used**: session-router → onboarding → level-classifier → concept-explainer
**Duration**: ~12 minutes

---

## Skill Chain Trace

```
[1] session-router
    Input: New user, no profile
    Output: Route to onboarding
    
[2] onboarding
    ├─ Welcome + explain tutor purpose
    ├─ Calibration Q1: AI experience → "ChatGPT a few times for newsletters"
    ├─ Calibration Q2: Chatbot vs agent → "Aren't they the same?"
    ├─ Calibration Q3: Risk awareness → "Students copying without thinking"
    ├─ Calibration Q4: Goals → "Guide students, set policies, lesson planning"
    └─ Calibration Q5: Self-rated → 2/10
    
[3] level-classifier
    Input: Calibration answers
    Analysis:
      - Has used AI but minimally (chatbot only)
      - Cannot distinguish agent from chatbot (key diagnostic)
      - Good instincts on risk (ethical reasoning baseline)
      - Clear, practical goals
    Output: level = "novice"
    Scores: concept=1.5, prompting=1.0, output_eval=1.0, ethics=2.0, critical=2.5
    
[4] onboarding (continued)
    Present learning path:
      1. "What Are AI Agents?" → concept-explainer
      2. "Your First Prompt" → prompt-coaching
      3. "Can You Trust the Output?" → scenario-runner + knowledge-check
      4. "AI in the Classroom" → concept-explainer (domain-specific)
      5. "Setting AI Policies" → ethical-guidance
    Ask: "Ready for Lesson 1?"
    User: "Yes"
    
[5] concept-explainer
    Topic: "What Are AI Agents?"
    Level: novice
    Activation: "You mentioned using ChatGPT for newsletters..."
    Definition: Plain language, intern analogy
    Example: ChatGPT (chatbot) vs a multi-step research agent
    Misconception: "They don't actually understand anything"
    Comprehension check: "What's one thing an agent can do that a chatbot can't?"
    User answer: "Use tools and take multiple steps?"
    Result: PASSED
    
[6] Profile saved
    New profile created with:
    - Level: novice
    - Goals: [guide students, set policies, lesson planning]
    - Learning path: 5 modules, first marked in_progress
    - Session count: 1
```

## Key Decisions Made by the System

1. **Routing**: session-router correctly identified new user (no profile) and routed to onboarding instead of any other skill
2. **Level assignment**: The chatbot-vs-agent question was diagnostic — Maria's answer ("same thing") confirmed novice level even though her ethical reasoning was above average for a novice
3. **Learning path personalization**: The path includes "AI in the Classroom" and "Setting AI Policies" specifically because of her teacher role and stated goals — a developer would get a different path
4. **First lesson selection**: Started with "What Are AI Agents?" because the calibration revealed she can't yet distinguish chatbots from agents — this is foundational

## What Would Be Different for Other Users

| User | Level Assignment | First Lesson | Path Customization |
|------|-----------------|--------------|-------------------|
| Jake (student) | Novice (knows "prompt" but not agents) | "What Are AI Agents?" | Includes "AI and Academic Integrity" early |
| Priya (marketer) | Practitioner (knows prompting, hallucination) | "Advanced Prompting Patterns" | Skips basics, focuses on evaluation + ethics |
| Chen (developer) | Advanced (knows RAG, tool use, agents) | "Agent Failure Mode Taxonomy" | Technical track: red-teaming, guardrails, HITL |
