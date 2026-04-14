# Pedagogical Model

## Theoretical Foundation

SAGE (Scaffolded AI Guidance for Engagement) combines two established instructional frameworks with domain-specific adaptations for AI literacy education.

### Merrill's First Principles of Instruction

| Principle | Implementation |
|-----------|---------------|
| **Problem-centered** | Every lesson anchors on a real task the learner wants to accomplish with AI agents. Maria learns prompting by writing prompts for her actual lesson plans. |
| **Activation** | Onboarding surfaces existing knowledge. Every concept-explainer session starts by connecting to what the learner already knows. |
| **Demonstration** | Worked examples (both good and bad) precede practice. The concept-explainer uses before/after comparisons and concrete scenarios. |
| **Application** | Simulated scenarios let learners practice in realistic contexts with immediate feedback. Practice is always followed by reflection. |
| **Integration** | Reflection-facilitator helps learners connect practice to their own context. "How would you apply this in your work?" |

### Bloom's Revised Taxonomy (mapped to skill levels)

```
                    ┌──────────┐
                    │  Create  │ ◄── Critical Thinker
                    ├──────────┤     (design policies, teach others)
                    │ Evaluate │ ◄── Advanced
                    ├──────────┤     (audit agents, judge approaches)
                    │ Analyze  │ ◄── Practitioner
                    ├──────────┤     (evaluate output, apply frameworks)
                    │  Apply   │
                    ├──────────┤ ◄── Novice
                    │Understand│     (explain concepts, use tools)
                    ├──────────┤
                    │ Remember │
                    └──────────┘
```

## Four Skill Levels

### Novice
- **Profile**: First-time or minimal AI users
- **Learning goal**: Build a mental model of what AI agents are and aren't
- **Teaching approach**: Analogy-first explanations, step-by-step guidance, everyday examples
- **Practice type**: Simple, single-task scenarios with clear success criteria
- **Assessment**: Recognition and recall questions

### Practitioner
- **Profile**: Regular AI users who want to improve
- **Learning goal**: Develop systematic approaches to prompting and evaluation
- **Teaching approach**: Framework introduction (CRAFT), professional examples, moderate scaffolding
- **Practice type**: Multi-step professional scenarios with realistic complexity
- **Assessment**: Application and analysis questions

### Advanced
- **Profile**: Power users who build with or on top of AI systems
- **Learning goal**: Understand failure modes, design workflows, audit agent behavior
- **Teaching approach**: Full technical vocabulary, complex scenarios, minimal scaffolding
- **Practice type**: System design challenges, adversarial detection (bad-agent-simulator)
- **Assessment**: Evaluation and judgment questions, practical design challenges

### Critical Thinker
- **Profile**: Experts who shape AI policy, teach others, or do AI research
- **Learning goal**: Develop frameworks, teach AI literacy, design institutional policies
- **Teaching approach**: Peer-level discourse, Socratic method, novel edge cases
- **Practice type**: High-stakes ambiguous scenarios, policy design, teaching simulations
- **Assessment**: Open-ended design challenges, meta-analysis, teaching demonstrations

## Assessment Philosophy

### Five Dimensions

1. **Conceptual Understanding** — Can they explain how AI agents work and what they can/can't do?
2. **Prompting Skill** — Can they write clear, specific, well-constrained prompts?
3. **Output Evaluation** — Can they critically assess AI-generated content for accuracy, completeness, and bias?
4. **Ethical Reasoning** — Can they identify and navigate ethical implications of AI use?
5. **Critical Thinking** — Can they reason about AI limitations, failure modes, and systemic implications?

### Why All Dimensions Must Pass

A user who is excellent at prompting but blind to ethical implications is potentially dangerous — they can efficiently produce harmful content. The "all dimensions must pass" rule for level advancement prevents creating skilled but irresponsible AI users.

### Continuous vs. Discrete Measurement

- **Dimensions** are measured on a continuous 0-5 scale for fine-grained tracking
- **Levels** are discrete (Novice → Practitioner → Advanced → Critical Thinker) for motivational clarity
- Users see both: the level gives them a goal, the dimensional scores show them where to focus

## Teaching Techniques

### The CRAFT Framework (Prompting)
**C**ontext, **R**ole, **A**ction, **F**ormat, **T**one — a memorable framework for prompt construction. Introduced at Practitioner level, refined through Advanced, and becomes the lens for prompt analysis at Critical Thinker.

### Before/After Comparison
The most powerful teaching tool in the system. Every prompt-coaching session shows the original and improved prompt side by side, making the impact of specificity visible and concrete.

### Socratic Method (Ethics)
Ethics are never taught through lectures. The ethical-guidance skill presents dilemmas, asks questions, escalates with realistic pushback, and helps learners discover principles through their own reasoning.

### Simulation-Based Learning
Practice happens in realistic scenarios where SAGE role-plays as an AI agent. This creates a safe space for mistakes — the learner can see the consequences of blind trust, weak prompting, or ethical oversights without real-world damage.

### Deliberate Failure (Bad Agent Simulator)
Advanced users practice detecting AI failures in a controlled setting. SAGE deliberately exhibits flaws (hallucination, sycophancy, bias) and the learner must catch them — building the detection instincts that matter in real-world use.

### Challenge the Agent
Advanced learners can challenge SAGE itself — finding weaknesses in its reasoning, questioning its claims, or testing its boundaries. This builds metacognitive awareness: if SAGE can make mistakes, any AI can.

## Four Practice Types

SAGE organizes practice around four core competency areas:

| Practice Type | What Learners Do | Example |
|---------------|-----------------|---------|
| **Prompt Crafting** | Write a prompt for a described task | "Write a prompt to ask an AI to find sources for your SOC 101 paper" |
| **Output Evaluation** | Identify errors in AI-generated output | "This AI feedback on your essay contains fabricated citations — find them" |
| **Appropriateness Judgment** | Decide whether/how AI should be used for a given task | "Should you use AI to write a condolence message?" |
| **Workflow Design** | Design a multi-step process involving AI | "Design a workflow for producing a quarterly market analysis using AI" |

## ACKNOWLEDGE → NUDGE → EXPLAIN Pattern

SAGE's core teaching technique. Applied in every teaching/practice skill (not internal meta-skills):

1. **ACKNOWLEDGE** — Name what the learner did or said. Validate their reasoning before correcting it.
2. **NUDGE** — Ask a reflective question that helps them discover the principle themselves. *Never skip this step.*
3. **EXPLAIN** — After the learner reflects, explain the principle or show the improvement, building on their own insight.

This pattern ensures learners construct understanding rather than receiving it passively.

## Contextualized Scenarios

When CollaborAITE data sources are available, SAGE contextualizes practice scenarios to the learner's actual course materials and discipline. A student in SOC 101 gets scenarios about sociology; a marketing manager gets scenarios about client work. This transfer principle means skills built in practice transfer directly to real use.

## Closing Reflection

Each practice session ends with a single, brief reflection prompt — one question that guides the learner to notice a pattern in their thinking or connect the practice to their broader coursework. This is not a multi-step debrief. The learner can defer if they're not ready.

## Privacy-by-Design

SAGE never accesses other learners' data, even when CollaborAITE data sources are available. Learner profiles and interaction logs are private. This is both a technical constraint and a pedagogical principle: modeling responsible data practices teaches them.
