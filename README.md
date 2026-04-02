# AI Agent Use Trainer/Tutor

An AI agent prototype that teaches people how to use AI agents effectively, ethically, and critically — through adaptive instruction, interactive practice simulations, and guided reflection.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Claude Code](https://claude.ai/code) — CLI, VS Code extension, or Desktop app with an active account

## Quick Start

```bash
git clone https://github.com/Elorm-K/498_Agents.git
cd 498_Agents
git checkout prototype/v1
```

Then launch Claude Code in one of these ways:

| Method | Command |
|--------|---------|
| **CLI** | Run `claude` in the project directory |
| **VS Code** | Open the folder in VS Code with the Claude Code extension installed |
| **Desktop App** | Open the project folder in the Claude Code desktop app |

The tutor activates automatically — just start talking to it.

## Things to Try

| What to test | Say something like |
|--------------|--------------------|
| Onboarding | "I'm new to AI agents" |
| Prompt coaching | "Help me write a better prompt" |
| Practice scenario | "I want to practice using AI" |
| Ethical guidance | "Is it okay to paste customer data into ChatGPT?" |
| Detect a flawed AI | "Can I practice spotting bad AI?" |
| Check your progress | "How am I doing?" |

Feel free to explore — the tutor adapts to your level and interests.

## How to Give Feedback

Open a [GitHub Issue](https://github.com/Elorm-K/498_Agents/issues) and include:

- **What you tried** — the message or scenario you tested
- **What happened** — the tutor's response or behavior
- **What you expected** — how you think it should have responded

## Current Limitations

- This is a **prototype** — not all features are fully polished
- User profiles do not persist between sessions
- Requires Claude Code access (not a standalone app)

---

## What This Is

This is a prototype design for an AI tutoring system that helps people at all skill levels develop **AI agent literacy**. It teaches:

- **What AI agents are** — capabilities, limitations, how they work
- **How to use them well** — prompting with the CRAFT framework, iterative improvement
- **How to evaluate output** — hallucination detection, fact verification, bias recognition
- **What to avoid** — blind trust, data leakage, over-reliance, unethical use
- **Critical and ethical thinking** — transparency, privacy, fairness, accountability

## Project Structure

```
├── CLAUDE.md                  # System prompt for the tutor agent
├── skills/                    # 14 modular skill definitions
│   ├── teaching/              # Onboarding, concepts, prompting, ethics
│   ├── assessment/            # Knowledge checks, evaluation, level classification
│   ├── simulation/            # Practice scenarios, flawed AI detection, prompt lab
│   ├── feedback/              # Reflection, progress reporting, improvement advice
│   └── meta/                  # Session routing, difficulty adaptation
├── workflows/                 # 5 orchestrated multi-skill sequences
├── data/
│   ├── schemas/               # JSON schemas for all data types
│   ├── users/                 # 5 example user profiles (novice → expert)
│   ├── scenarios/             # 5 practice simulation scenarios
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
4. Simulated scenarios provide hands-on application with feedback
5. Guided reflection connects practice to the learner's own context

## Skill Levels

| Level | Who | Focus |
|-------|-----|-------|
| **Novice** | First-time AI users | Build a mental model, learn basics |
| **Practitioner** | Regular users | Systematic prompting and evaluation |
| **Advanced** | Power users / builders | Failure modes, system design, auditing |
| **Critical Thinker** | Experts / policy makers | Frameworks, teaching others, institutional policy |

Advancement requires demonstrated competence across **all 5 dimensions**: conceptual understanding, prompting skill, output evaluation, ethical reasoning, and critical thinking. No blind spots allowed.

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
- Novice learns prompting through iterative before/after comparison
- Practitioner detects "authoritative fabrication" in marketing copy
- Advanced user navigates AI ethics under realistic organizational pressure

### Negative (what the tutor catches and corrects)
- Blind trust: accepting AI statistics as fact without verification
- Over-reliance: attempting to fully delegate creative work to AI
- Data leakage: about to paste production customer data into an AI tool

## Branch

This prototype lives on the `prototype/v1` branch.
