# Pedagogical Model

## Theoretical Foundation

The AI Agent Use Trainer combines two established instructional frameworks with domain-specific adaptations for AI literacy education.

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
Practice happens in realistic scenarios where the tutor role-plays as an AI agent. This creates a safe space for mistakes — the learner can see the consequences of blind trust, weak prompting, or ethical oversights without real-world damage.

### Deliberate Failure (Bad Agent Simulator)
Advanced users practice detecting AI failures in a controlled setting. The tutor deliberately exhibits flaws (hallucination, sycophancy, bias) and the learner must catch them — building the detection instincts that matter in real-world use.
