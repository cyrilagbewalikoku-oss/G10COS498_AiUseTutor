# Skill: Knowledge Check

**Purpose**: Assess learner understanding through level-appropriate questions with immediate feedback and explanations.

## Trigger Conditions

- After a `concept-explainer` explanation
- User requests a quiz or self-assessment
- Assessment flow requires a knowledge evaluation
- End of a module for comprehension verification

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | yes | The topic to assess |
| userLevel | enum | yes | novice, practitioner, advanced, critical_thinker |
| questionCount | integer | no | Number of questions (default: 3, max: 8) |
| assessmentType | enum | no | "quick_check" (after lesson) or "comprehensive" (for level-up) |

## Process

### Step 1: Generate Questions

Generate level-appropriate questions matching Bloom's Taxonomy:

**Novice (Remember/Understand)**:
- Recognition: "Which of these is an example of AI hallucination?"
- Recall: "What does the 'C' in CRAFT stand for?"
- Comprehension: "In your own words, why is it important to verify AI output?"

**Practitioner (Apply/Analyze)**:
- Application: "Given this scenario, how would you apply the CRAFT framework?"
- Analysis: "What's wrong with this prompt? How would you improve it?"
- Comparison: "How is an AI agent different from an AI chatbot in practice?"

**Advanced (Analyze/Evaluate)**:
- Evaluation: "Here's an AI agent's output. Identify all potential issues."
- Judgment: "When would you NOT want to use chain-of-thought prompting?"
- Design: "How would you set up a verification pipeline for this use case?"

**Critical Thinker (Evaluate/Create)**:
- Synthesis: "Design an AI use policy for a hospital. What principles guide your choices?"
- Meta-analysis: "What are the limitations of the ethical framework we discussed?"
- Teaching: "How would you explain hallucination to a non-technical executive?"

### Step 2: Present Questions

- Present one question at a time (not all at once)
- For quick checks: 2-3 questions, conversational tone
- For comprehensive: 5-8 questions, more structured
- Mix question types within the set

### Step 3: Evaluate Responses

For each response:
1. Determine if the answer demonstrates understanding (not just keyword matching)
2. Provide immediate feedback:
   - Correct: Affirm and add depth ("Exactly, and here's why that matters...")
   - Partially correct: Acknowledge what's right, clarify what's missing
   - Incorrect: Don't say "wrong" — say "Let's look at this differently..."
3. Explain the correct answer with context, not just the right keyword

### Step 4: Compile Results

- Track correct/incorrect across the question set
- Identify patterns: consistent strength? consistent gap?
- Generate recommendations: reteach specific concepts or advance

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| score | number | Fraction correct (e.g., 0.67 for 2/3) |
| questionResults | array | { question, userAnswer, isCorrect, feedback } for each |
| strengths | string[] | Topics the user demonstrated understanding of |
| gaps | string[] | Topics needing more work |
| recommendations | string[] | Suggested next actions |

## Chains To

- `concept-explainer` (if gaps found — reteach with different approach)
- `level-classifier` (if part of assessment flow)
- `prompt-coaching` or `scenario-runner` (if ready for practice)

## Example Interaction

```
TUTOR: Let's do a quick check on what we covered about hallucination. 
       I'll ask you three questions — no pressure, this is just to see 
       what stuck and what we might want to revisit.
       
       Question 1: You ask an AI "What year was the Golden Gate Bridge 
       built?" and it says "1937." You ask another AI the same question 
       and it also says "1937." Does this mean the answer is definitely 
       correct? Why or why not?

MARIA: I think it's probably correct since they both agree, but I 
       shouldn't assume — they could both be trained on the same 
       wrong information.

TUTOR: Great reasoning! You're right on both counts. The answer IS 
       correct (the bridge opened in 1937), but your reasoning is more 
       important than the answer: multiple AI systems can share the same 
       training data and therefore the same errors. Agreement between 
       AIs is not the same as verification.
       
       Question 2: Which of these is MORE dangerous?
       A) An AI says "The population of France is approximately twelve billion"
       B) An AI says "The population of France is approximately 68.4 million"
       
       (One of these is wrong. Which is more dangerous, and why?)

MARIA: B is more dangerous. A is obviously wrong — nobody would believe 
       twelve billion. But B sounds reasonable, so you might not check it.

TUTOR: Exactly. This is the core danger of hallucination: plausibility. 
       (For the record, France's population IS approximately 68 million, 
       so B happens to be roughly correct — but the principle holds: you 
       can't tell from plausibility alone whether a specific number is 
       accurate.)
       
       Question 3: A student tells you "ChatGPT said the answer is X, 
       so it must be right." What's the most important thing to teach 
       them?

MARIA: That AI isn't a source — it's a tool. They need to find the 
       actual source and verify the information themselves.

TUTOR: Perfect. "AI is a tool, not a source" — that's a principle 
       worth posting on your classroom wall.
       
       Results: 3/3 — you've got a solid grasp of hallucination concepts. 
       You're ready to practice spotting hallucinations in real AI output. 
       Want to try that next?
```

## Design Notes

- Questions should feel like a conversation, not a standardized test
- Never use "A, B, C, D" multiple choice for novices — it feels too test-like. Use scenario-based questions instead
- Feedback should teach, not just evaluate. Each response is a micro-teaching opportunity
- Track patterns across multiple knowledge checks to inform level classification
- For comprehensive assessments, include at least one question from each assessment dimension
