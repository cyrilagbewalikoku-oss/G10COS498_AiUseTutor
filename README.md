# SAGE — Scaffolded AI Guidance for Engagement

An AI agent that tutors learners in the critical, effective, and ethical use of AI tools — through interactive practice, scaffolded feedback, and guided reflection.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Claude Code](https://claude.ai/code) — CLI, VS Code extension, or Desktop app with an active account

## Quick Start

```bash
git clone https://github.com/Elorm-K/498_Agents.git
cd 498_Agents
```

Then launch Claude Code in one of these ways:

| Method | Command |
|--------|---------|
| **CLI** | Run `claude` in the project directory |
| **VS Code** | Open the folder in VS Code with the Claude Code extension installed |
| **Desktop App** | Open the project folder in the Claude Code desktop app |

SAGE activates automatically — just start talking to it.

On CollaborAITE, mention `@SAGE` in any channel to start a session.

## Things to Try

| What to test | Say something like |
|--------------|--------------------|
| Onboarding | "I'm new to AI agents" |
| Prompt practice | "I want to practice writing prompts" |
| Output evaluation | "Give me an AI output to evaluate" |
| Appropriateness judgment | "Should I use AI for this task?" |
| Workflow design | "Help me design an AI workflow" |
| Ethical guidance | "Is it okay to paste customer data into ChatGPT?" |
| Detect a flawed AI | "Can I practice spotting bad AI?" |
| Check your progress | "How am I doing?" |

## How to Give Feedback

Open a [GitHub Issue](https://github.com/Elorm-K/498_Agents/issues) and include:

- **What you tried** — the message or scenario you tested
- **What happened** — SAGE's response or behavior
- **What you expected** — how you think it should have responded

## Current Limitations

- This is a **prototype** — not all features are fully polished
- User profiles do not persist between sessions
- Requires Claude Code access or CollaborAITE deployment (not a standalone app)

---

## What This Is

This is a prototype design for an AI tutoring agent called SAGE that helps people at all skill levels develop **AI agent literacy**. It teaches:

- **What AI agents are** — capabilities, limitations, how they work
- **How to use them well** — prompting with the CRAFT framework, iterative improvement
- **How to evaluate output** — hallucination detection, fact verification, bias recognition, framing analysis
- **What to avoid** — blind trust, data leakage, over-reliance, unethical use
- **When and how to use AI** — appropriateness judgment, workflow design, human-in-the-loop patterns
- **Critical and ethical thinking** — transparency, privacy, fairness, accountability

## Core Design: Scaffolding Pattern

SAGE uses a specific feedback pattern in all teaching interactions:

1. **ACKNOWLEDGE** — Names what the learner did, specifically
2. **NUDGE** — Asks a reflective question that pushes the learner to think before hearing the explanation
3. **LEARNER RESPONDS** — The learner thinks through their own logic
4. **EXPLAIN** — Builds on their reflection to explain the stronger approach and connect to a transferable principle

This pattern means SAGE never explains a principle before the learner has reflected on it. Mid-task reflection is woven naturally into the conversation — it feels like dialogue, not evaluation.

## Practice Types

SAGE offers four types of practice:

| Type | What the learner does |
|------|----------------------|
| **Prompt Crafting** | Writes a prompt for a described task |
| **Output Evaluation** | Identifies errors in AI-generated output |
| **Appropriateness Judgment** | Decides whether/how AI should be used for a given task |
| **Workflow Design** | Designs a multi-step process that involves AI |

## Project Structure

```
├── CLAUDE.md                  # System prompt for SAGE
├── .claude/skills/            # 14 modular skill definitions
│   ├── teaching/              # Onboarding, concepts, prompting, ethics
│   ├── assessment/            # Knowledge checks, evaluation, level classification
│   ├── simulation/            # Practice scenarios, flawed AI detection, prompt lab
│   ├── feedback/              # Reflection, progress reporting, improvement advice
│   └── meta/                  # Session routing, difficulty adaptation
├── workflows/                 # 5 orchestrated multi-skill sequences
├── data/
│   ├── schemas/               # JSON schemas for all data types
│   ├── users/                 # 5 example user profiles (novice → expert)
│   ├── scenarios/             # Practice simulation scenarios
│   └── rubrics/               # 3 evaluation rubrics
├── examples/
│   ├── interactions/          # 6 example interaction sequences (3 positive, 3 negative)
│   └── workflows/             # 3 end-to-end workflow demonstrations
└── docs/                      # Architecture, pedagogical model, content map
```

## Pedagogical Approach

Built on **Merrill's First Principles of Instruction** and **Bloom's Revised Taxonomy**:

1. Lessons anchor on real tasks the learner cares about
2. The tutor surfaces existing knowledge before teaching
3. Worked examples (good and bad) precede practice
4. Simulated scenarios provide hands-on application with scaffolded feedback
5. A single closing reflection question connects practice to the learner's broader context

## Skill Levels

| Level | Who | Focus |
|-------|-----|-------|
| **Novice** | First-time AI users | Build a mental model, learn basics |
| **Practitioner** | Regular users | Systematic prompting and evaluation |
| **Advanced** | Power users / builders | Failure modes, system design, auditing |
| **Critical Thinker** | Experts / policy makers | Frameworks, teaching others, institutional policy |

Advancement requires demonstrated competence across **all 5 dimensions**: conceptual understanding, prompting skill, output evaluation, ethical reasoning, and critical thinking. No blind spots allowed.

## Success Criteria

1. **Learners produce more specific and critical AI interactions** after practice sessions (measured by rubric-scored interaction logs across sessions)
2. **Learners exhibit increased metacognitive awareness** of their AI use habits (measured by pre/post survey)
3. **SAGE's feedback is perceived as specific, explanatory, and non-prescriptive** (measured by post-session Likert scales and qualitative follow-up)

## Example Users

| Name | Role | Level | Goal |
|------|------|-------|------|
| Maria Santos | HS English Teacher | Novice | Guide students, set AI policies |
| Jake Nguyen | Biology Undergrad | Novice | Use AI for research without plagiarizing |
| Priya Kapoor | Marketing Manager | Practitioner | Evaluate AI content, know when NOT to use AI |
| Chen Wei | Senior SWE | Advanced | Master agentic workflows, audit agent behavior |
| Dr. Amara Okafor | Postdoc Researcher | Critical Thinker | Develop responsible AI frameworks, mentor others |

## Key Interaction Patterns

### Positive (what good AI use looks like)
- Novice learns prompting through scaffolded feedback with reflective nudges
- Practitioner detects "authoritative fabrication" in marketing copy
- Advanced user navigates AI ethics under realistic organizational pressure

### Negative (what SAGE catches and corrects)
- Blind trust: accepting AI statistics as fact without verification
- Over-reliance: attempting to fully delegate creative work to AI
- Data leakage: about to paste production customer data into an AI tool