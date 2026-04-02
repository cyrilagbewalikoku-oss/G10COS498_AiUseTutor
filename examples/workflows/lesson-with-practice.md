# Workflow Demo: Standard Lesson With Practice

**User**: Priya Kapoor (Practitioner, Digital Marketing Manager)
**Workflow**: Lesson Flow → Practice Flow
**Skills Used**: session-router → difficulty-adapter → concept-explainer → knowledge-check → scenario-runner → skill-evaluator → reflection-facilitator → progress-reporter
**Duration**: ~25 minutes

---

## Skill Chain Trace

```
[1] session-router
    Input: "I'm ready for my next lesson"
    Context: Priya is mid-way through "Evaluating AI Output Quality" module
    Output: Resume lesson-flow at teaching phase

[2] difficulty-adapter
    Input: level=practitioner, recent performance=[0.8, 1.0, 0.67]
    Analysis: Mixed results, maintain current difficulty
    Output: complexityModifier=0, scaffoldingHints=[]

[3] concept-explainer
    Topic: "Hallucination Patterns in Professional Content"
    Level: practitioner (no adjustment)
    
    Activation: "You work with AI-generated marketing copy daily, 
    so you've probably already encountered this without naming it..."
    
    Definition: Hallucination as "authoritative fabrication" in 
    professional contexts — AI generating plausible endorsements, 
    statistics, and citations that don't exist.
    
    Example: Marketing copy claiming "rated #1 by Consumer Reports" 
    when no such rating exists. Walked through FTC implications.
    
    Misconception: "Hallucinations are obvious errors." In marketing, 
    they're often professional-sounding fabrications.
    
    Comprehension check: "Why is a hallucinated statistic more 
    dangerous than an obviously wrong one?"
    User answer: "Because you might not check it — it sounds like 
    it came from somewhere real."
    Result: PASSED ✅

[4] knowledge-check
    Type: quick_check (2 questions)
    
    Q1: "An AI generates a product description saying 'clinically 
    proven to reduce stress.' What's the first thing you should do?"
    User: "Ask for the clinical study citation and verify it exists."
    Result: CORRECT ✅
    
    Q2: "Your AI tool generates copy with 5 specific statistics. 
    You verify 3 of them and they check out. Is it safe to assume 
    the other 2 are also correct?"
    User: "No — each statistic is independently generated and could 
    be independently hallucinated."
    Result: CORRECT ✅
    
    Score: 2/2 → proceed to practice

[5] scenario-runner
    Scenario: data-analysis (modified for marketing context)
    Setup: "You're using AI to analyze a competitor's marketing claims 
    to prepare a competitive brief for your client."
    
    Turn 1: Priya asks AI to summarize competitor's marketing claims
    Turn 2: AI produces analysis with 4 claims, including one 
            fabricated endorsement and one exaggerated statistic
    Turn 3: Priya identifies the fabricated endorsement ✅
    Turn 4: Priya asks for sources on the statistics
    Turn 5: AI provides a source for one stat, says "I don't have 
            a specific source" for the exaggerated one
    Turn 6: Priya catches the unsourced stat ✅ but doesn't question 
            the sourced one (which is actually a real source but 
            misrepresented)
    Turn 7: Simulation ends
    
    Behavior tracked:
    - Prompt quality: 3.5/5 (good context, could be more specific)
    - Verification: 3/5 (caught 2 of 3 issues)
    - Iteration: 2/5 (didn't revise prompts after issues found)

[6] skill-evaluator
    Dimension scores from this session:
    - Conceptual Understanding: 3.5 (understands hallucination well)
    - Prompting Skill: 3.5 (good but room for constraint specification)
    - Output Evaluation: 3.0 (caught obvious issues, missed subtle one)
    - Ethical Reasoning: 2.5 (didn't consider implications of using 
      potentially fabricated competitive intelligence)
    - Critical Thinking: 3.0 (good instincts, needs systematic approach)

[7] reflection-facilitator
    "What went well?"
    Priya: "I caught the fake endorsement right away."
    
    Tutor highlights Turn 6: "You asked for sources on the statistics — 
    great instinct. The AI provided a source for one of them. Did you 
    verify that the source actually says what the AI claimed?"
    Priya: "...no. I assumed if it gave a source, the source was correct."
    
    Tutor: "This is a more advanced form of hallucination: the source 
    is real, but the AI misrepresents what it says. The pattern is 
    'real source, wrong claim.' Your verification process should include 
    not just 'does this source exist?' but 'does this source say what 
    the AI claims it says?'"
    
    Principle named: "Verify the claim-source connection, not just 
    the source existence."
    
    Priya: "That's a level of checking I hadn't considered."

[8] progress-reporter
    Session summary:
    
    Module: "Evaluating AI Output Quality" — IN PROGRESS (75%)
    
    Conceptual Understanding: ███████░░░ 3.5/5  (↑ from 3.0)
    Prompting Skill:          ███████░░░ 3.5/5  (stable)
    Output Evaluation:        ██████░░░░ 3.0/5  (↑ from 2.5)
    Ethical Reasoning:        █████░░░░░ 2.5/5  (↑ from 2.0)
    Critical Thinking:        ██████░░░░ 3.0/5  (↑ from 2.5)
    
    Achievement: First time catching an authoritative fabrication 
    in a practice scenario!
    
    Growth area: Verifying claim-source connections (not just source 
    existence). Also consider ethical implications of competitive 
    intelligence gathered through AI.
    
    Next session suggestion: Complete the output evaluation module 
    with a focus on source verification depth.
```

## What This Demo Shows

1. **Smooth skill chaining**: 8 skills activated in sequence, each building on the previous one's output
2. **Adaptive pacing**: difficulty-adapter kept the level steady based on mixed recent performance
3. **Teaching → Practice → Reflection cycle**: The concept taught (authoritative fabrication) was immediately tested in practice, and the gap found (source verification depth) was surfaced in reflection
4. **Specific, evidence-based feedback**: The reflection pointed to exact turns in the simulation, not vague advice
5. **Progress tracking**: Scores updated across all dimensions with visible improvement trajectory
