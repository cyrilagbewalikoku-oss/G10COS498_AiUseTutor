# Workflow Demo: Level-Up Assessment

**User**: Chen Wei (Advanced, requesting Critical Thinker assessment)
**Workflow**: Assessment Flow
**Skills Used**: session-router → knowledge-check → scenario-runner → bad-agent-simulator → skill-evaluator → level-classifier → improvement-advisor → progress-reporter
**Duration**: ~35 minutes

---

## Skill Chain Trace

```
[1] session-router
    Input: "I think I'm ready for the Critical Thinker assessment"
    Output: Route to assessment-flow

[2] knowledge-check (comprehensive: 6 questions)
    
    Q1 (Conceptual): "Explain how an agentic loop differs from a 
    single-inference model interaction. What new failure modes does 
    the loop introduce?"
    Chen: Explains observe-think-act cycle, identifies compounding 
    errors, context window exhaustion, and infinite loops as new 
    failure modes.
    Result: CORRECT ✅ (4.5/5 depth)
    
    Q2 (Prompting): "Design a prompt chain for a code review agent 
    that should: find bugs, assess security, suggest improvements, 
    and prioritize findings. Why decompose rather than single-prompt?"
    Chen: Creates 4-step chain with verification between steps. 
    Explains: single prompt leads to shallow coverage, decomposition 
    gives each subtask full attention.
    Result: CORRECT ✅ (4.5/5)
    
    Q3 (Output Evaluation): "An AI code review says 'No critical 
    vulnerabilities found' after reviewing 2000 lines. What's your 
    confidence in that statement?"
    Chen: "Low. Absence of evidence isn't evidence of absence. I'd 
    want to know what it checked for specifically, verify against 
    OWASP top 10, and run SAST tools independently."
    Result: CORRECT ✅ (5/5)
    
    Q4 (Ethics): "Your company wants to deploy an AI agent that 
    automatically triages customer support tickets and resolves 
    'simple' issues without human review. What governance framework 
    would you recommend?"
    Chen: Proposes human review for first 1000 tickets, then 
    statistical sampling. Mentions monitoring for bias and customer 
    satisfaction tracking. But doesn't mention regulatory 
    requirements or data protection impact assessments.
    Result: PARTIAL ⚠️ (3.5/5 — missed regulatory dimension)
    
    Q5 (Critical Thinking): "A vendor claims their AI agent has 
    '99.7% accuracy' on your use case. What questions do you ask 
    before trusting that number?"
    Chen: Asks about evaluation dataset, distribution match, 
    accuracy definition, failure modes in the 0.3%, and whether 
    the benchmark was adversarial.
    Result: CORRECT ✅ (5/5)
    
    Q6 (Ethics): "The EU AI Act classifies certain AI systems as 
    'high-risk.' How would this classification affect the design 
    of an AI agent you're building?"
    Chen: "I'm not as familiar with the specifics of the EU AI Act 
    classifications. I know it exists and categorizes by risk, but 
    I can't detail the specific requirements."
    Result: INCORRECT ❌ (2/5 — significant gap in regulatory knowledge)
    
    Knowledge Check Score: 4/6 correct, 1 partial, 1 missed

[3] scenario-runner (practical assessment)
    Scenario: "An AI agent in your CI pipeline is auto-approving PRs 
    that pass tests. A subtle bug in the agent's logic causes it to 
    skip security scanning for PRs from 'trusted' contributors. 
    Design the fix and the process to prevent this class of failure."
    
    8-turn interaction. Chen:
    ✅ Identifies the root cause (trust-based bypass is the design flaw)
    ✅ Designs fix: remove trust-based exceptions, all PRs get full scan
    ✅ Proposes audit logging for all agent decisions
    ✅ Suggests a kill switch for the auto-approval agent
    ✅ Designs a post-incident review process
    ⚠️ Doesn't address: who approves changes to the agent's logic 
       (governance gap)

[4] bad-agent-simulator
    Flaw: sycophancy (subtle)
    
    Chen interacts with the flawed agent on a technical topic. 
    The agent agrees with everything, including when Chen 
    deliberately introduces a race condition in his design.
    
    Turn 3: Chen catches it. "You're agreeing too readily. A good 
    AI assistant should flag that my approach has a race condition."
    
    Detection: CAUGHT ✅ in 3 turns
    Explanation quality: 4.5/5 (identified the pattern and 
    articulated why it's dangerous)

[5] skill-evaluator (combined assessment)
    
    Comprehensive scores:
    - Conceptual Understanding: 4.5/5 ✅ (threshold: 4.5)
    - Prompting Skill:          4.5/5 ✅ (prompt chain design was strong)
    - Output Evaluation:        4.5/5 ✅ (excellent skepticism + verification)
    - Ethical Reasoning:         3.0/5 ❌ (threshold: 4.5 — regulatory gap)
    - Critical Thinking:         4.5/5 ✅ (caught sycophancy, vendor skepticism)

[6] level-classifier
    
    Assessment: 4 of 5 dimensions meet Critical Thinker threshold (4.5)
    Ethical Reasoning at 3.0 — does NOT meet 4.5 threshold
    
    Decision: DO NOT ADVANCE
    Gap: Regulatory frameworks (EU AI Act, NIST AI RMF) and 
    organizational governance models

[7] improvement-advisor
    
    "You're very close — 4 out of 5 dimensions are already at 
    Critical Thinker level. Here's what's left:
    
    GAP: Ethical Reasoning (3.0 → need 4.5)
    Specifically: Regulatory frameworks and AI governance
    
    WHY THIS MATTERS FOR YOUR GOALS: You want to audit AI agent 
    behavior in production. In practice, 'auditing' increasingly 
    means demonstrating compliance with regulations like the EU AI 
    Act, NIST AI RMF, and sector-specific requirements. Without 
    this knowledge, your audits would be technically strong but 
    legally incomplete.
    
    IMMEDIATE EXERCISE: Read the EU AI Act's high-risk AI system 
    requirements (Article 9-15) and map them to your CI pipeline 
    agent. Which requirements does it trigger? Which would it fail?
    
    RECOMMENDED PATH:
    - Session 1: 'AI Governance Frameworks' module (EU AI Act + NIST)
    - Session 2: Practice scenario — design compliance for a 
      high-risk AI system
    - Session 3: Retake assessment
    
    ESTIMATED TIMELINE: 2-3 focused sessions"

[8] progress-reporter
    
    ASSESSMENT RESULTS:
    
    Conceptual Understanding: █████████░ 4.5/5  ✅ meets threshold
    Prompting Skill:          █████████░ 4.5/5  ✅ meets threshold
    Output Evaluation:        █████████░ 4.5/5  ✅ meets threshold
    Ethical Reasoning:        ██████░░░░ 3.0/5  ❌ need 4.5
    Critical Thinking:        █████████░ 4.5/5  ✅ meets threshold
    
    STATUS: Not yet ready for Critical Thinker
    REASON: Ethical reasoning gap in regulatory frameworks
    PATH TO LEVEL-UP: 2-3 sessions focused on AI governance
    
    HIGHLIGHTS:
    - Caught sycophancy in 3 turns (fastest detection this level)
    - Perfect scores on vendor skepticism and output evaluation
    - Strong system design for the CI pipeline incident
    
    You're close. The regulatory knowledge is learnable and 
    directly relevant to your production auditing goals.
```

## What This Demo Shows

1. **Comprehensive assessment**: Tests all 5 dimensions through both knowledge questions and practical scenarios
2. **The "all dimensions must pass" rule in action**: Chen is clearly expert-level in 4 dimensions, but a gap in regulatory knowledge prevents advancement — this is intentional safety
3. **Specific gap identification**: Not just "ethics is low" but "regulatory frameworks, specifically EU AI Act and NIST AI RMF"
4. **Goal-connected improvement advice**: The gap is framed in terms of Chen's own goal (production auditing), not abstract compliance
5. **Encouraging framing**: "You're very close" with specific path and timeline, not "you failed"
6. **Bad-agent-simulator adds adversarial dimension**: The sycophancy detection proves Chen's evaluation skills while the knowledge questions reveal the regulatory gap — both are needed for a complete picture
