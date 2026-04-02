# Content Map

## Curriculum Overview

The curriculum is organized into modules grouped by skill level. Users progress through modules based on their learning path, which is personalized during onboarding.

## Module Map by Level

### Novice Modules (100-series)

| Module ID | Title | Skills Used | Topics | Prerequisites |
|-----------|-------|-------------|--------|---------------|
| m-101 | What Are AI Agents? | concept-explainer, knowledge-check | Agent vs chatbot, capabilities, limitations, how they work at a high level | None |
| m-102 | Your First Prompt | prompt-coaching, prompt-lab | CRAFT framework (Context + Action only), before/after comparison, iteration basics | m-101 |
| m-103 | Can You Trust the Output? | concept-explainer, scenario-runner, knowledge-check | Hallucination basics, why AI sounds confident when wrong, simple verification strategies | m-101 |
| m-104 | AI in the Classroom | concept-explainer, ethical-guidance | Domain-specific: using AI for teaching, setting student expectations, detecting AI-generated work | m-101 (teacher track) |
| m-105 | Setting AI Policies | ethical-guidance, reflection-facilitator | Creating guidelines for AI use in your context, transparency principles | m-103 |

### Practitioner Modules (200-300 series)

| Module ID | Title | Skills Used | Topics | Prerequisites |
|-----------|-------|-------------|--------|---------------|
| m-201 | AI and Academic Integrity | ethical-guidance, scenario-runner | Domain-specific: responsible AI use in academics, citation, attribution, plagiarism line | m-101 (student track) |
| m-301 | Advanced Prompting Patterns | prompt-coaching, prompt-lab | Full CRAFT framework, constraint specification, anti-hallucination techniques, task decomposition | m-102 |
| m-302 | Evaluating AI Output Quality | concept-explainer, scenario-runner, skill-evaluator | Systematic evaluation: fact verification, error detection, bias recognition, completeness checking | m-103 |
| m-303 | AI for Content Workflows | scenario-runner, prompt-coaching | Brief → Draft → Review cycle, brand voice maintenance, disclosure practices | m-301 (marketer track) |
| m-401 | Ethics of AI-Generated Content | ethical-guidance, reflection-facilitator | FTC guidelines, disclosure obligations, transparency, accountability for AI output | m-302 |

### Advanced Modules (500-series)

| Module ID | Title | Skills Used | Topics | Prerequisites |
|-----------|-------|-------------|--------|---------------|
| m-501 | Agent Failure Mode Taxonomy | concept-explainer, bad-agent-simulator | Hallucination types, sycophancy, overconfidence, prompt injection, context window limits, tool use failures | m-302 |
| m-502 | Designing Human-in-the-Loop Systems | concept-explainer, scenario-runner | When to automate vs. involve humans, approval workflows, escalation patterns, kill switches | m-501 |
| m-503 | Red-Teaming AI Agents | bad-agent-simulator, scenario-runner, skill-evaluator | Adversarial testing, edge case discovery, robustness evaluation, safety boundaries | m-501 |
| m-504 | AI Governance Frameworks | concept-explainer, ethical-guidance | EU AI Act, NIST AI RMF, organizational AI policies, compliance requirements | m-401 |

### Critical Thinker Modules (600-series)

| Module ID | Title | Skills Used | Topics | Prerequisites |
|-----------|-------|-------------|--------|---------------|
| m-601 | Teaching Others AI Literacy | concept-explainer, scenario-runner, reflection-facilitator | Designing AI literacy curricula, mentoring strategies, common misconceptions to address | m-504 |
| m-602 | Institutional AI Policy Design | ethical-guidance, scenario-runner | Drafting organizational AI use policies, stakeholder engagement, implementation strategies, monitoring | m-504 |

## Concept Dependency Graph

```
What AI Agents Are (m-101)
├── Your First Prompt (m-102)
│   └── Advanced Prompting (m-301)
│       ├── Content Workflows (m-303)
│       └── Task Decomposition (within m-301)
├── Can You Trust the Output? (m-103)
│   └── Evaluating AI Output (m-302)
│       ├── Failure Mode Taxonomy (m-501)
│       │   ├── Human-in-the-Loop (m-502)
│       │   └── Red-Teaming (m-503)
│       └── Ethics of AI Content (m-401)
│           └── AI Governance (m-504)
│               ├── Teaching AI Literacy (m-601)
│               └── Institutional Policy (m-602)
└── Domain-Specific Entry Points
    ├── AI in the Classroom (m-104) [teacher track]
    ├── AI and Academic Integrity (m-201) [student track]
    └── Setting AI Policies (m-105) [any track]
```

## Cross-Cutting Themes

These themes appear across multiple modules at increasing depth:

| Theme | Novice | Practitioner | Advanced | Critical Thinker |
|-------|--------|-------------|----------|-----------------|
| **Hallucination** | "AI makes things up" | Detection patterns, verification | Failure mode taxonomy, subtle fabrication | Systemic analysis, research methodology |
| **Prompting** | Context + Action | Full CRAFT, constraints | Task decomposition, chains | Meta-prompting, prompt reliability |
| **Ethics** | "Should I?" basics | Professional obligations | Organizational governance | Policy design, institutional change |
| **Verification** | "Check your facts" | Systematic checking | Source-claim connection | Methodology evaluation |
| **Bias** | "AI can be biased" | Detection in output | Training data analysis | Systemic bias, fairness frameworks |
