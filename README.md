# SAGE — Scaffolded AI Guidance for Engagement

An AI agent that tutors learners in the critical, effective, and ethical use of AI tools — through interactive practice, scaffolded feedback, and guided reflection.

## Quick Start (Web UI)

The fastest way to use SAGE. Opens a chat interface in your browser.

**Prerequisites:** Python 3.10+, [Anthropic API key](https://console.anthropic.com/)

### 1. Clone and set up the virtual environment

```bash
git clone https://github.com/Elorm-K/498_Agents.git
cd 498_Agents

# Create a virtual environment (keeps SAGE's dependencies isolated)
python3 -m venv venv

# Activate it
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install SAGE and all dependencies into the venv
pip install .
```

### 2. Launch the Web UI

```bash
sage-ui
```

Opens `http://localhost:8501` in your browser. Enter your Anthropic API key in the sidebar and start chatting. Quick-start buttons let you jump into any practice type with one click.

To stop the server, press `Ctrl+C` in the terminal.

### 3. Next time you return

```bash
cd 498_Agents
source venv/bin/activate        # re-activate the venv
sage-ui                         # launch
```

You only need to run `pip install .` once (or again after pulling new changes).

## All Ways to Run SAGE

| Method | Command | Best for |
|--------|---------|----------|
| **Web UI** | `sage-ui` | Evaluators, demos, anyone who prefers a browser |
| **Terminal CLI** | `sage` | Terminal users, scripting |
| **Claude Code Skills** | `claude` in project dir | Development, skill editing |

### Terminal CLI

```bash
source venv/bin/activate               # activate the venv (if not already active)
export ANTHROPIC_API_KEY="your-key"    # required for terminal mode
sage
```

### Claude Code Skills (original prototype)

Runs inside Claude Code with skill-based routing. Requires [Claude Code](https://claude.ai/code).

```bash
claude    # from the project directory
```

SAGE activates automatically. On CollaborAITE, mention `@SAGE` in any channel.

To force Claude Code to respond only through skills (simulates production):

```
Using only the skills available to you (YOU MUST USE THE SKILLS), use the
session-start skill to respond to the following prompt:

"<your message here>"
```

## Things to Try

| What to test | Say something like |
|--------------|--------------------|
| Onboarding | "I'm new to AI agents" |
| Prompt practice | "I want to practice writing prompts" |
| Output evaluation | "Give me an AI output to evaluate" |
| Appropriateness judgment | "Should I use AI for this task?" |
| Workflow design | "Help me design an AI workflow" |
| Coach a real prompt | "Help me improve this prompt: [paste yours]" |
| Weekly reflection | "Let's do a weekly review" |
| Ethical guidance | "Is it okay to paste customer data into ChatGPT?" |
| Detect a flawed AI | "Can I practice spotting bad AI?" |
| Check progress | "How am I doing?" |

## Deployment Modes

| Feature | Web UI / CLI | Claude Code Skills | CollaborAITE (target) |
|---|---|---|---|
| Onboarding + assessment | Automatic | `/onboarding` | On first @mention |
| Four practice types | Automatic | `/scenario-runner` | Automatic |
| Coach your AI interactions | Paste in chat | `/improve-interaction` | Sidebar nudge |
| Weekly reflection | Ask in chat | `/weekly-review` | Scheduled |
| Learner profile | `data/users/*.json` | `data/users/*.json` | Platform data layer |
| Course-material context | Describe or attach | Describe or attach | Automatic retrieval |
| Peer-pattern retrieval | Deferred | Deferred | Anonymized |

The pedagogy is identical across all modes. See [docs/roadmap.md](docs/roadmap.md) for the full CollaborAITE vision.

## Project Structure

```
sage/                          # Python agent (Claude Agent SDK)
  agent.py                     # Terminal conversation loop
  app.py                       # Streamlit web UI
  ui.py                        # Web UI launcher
  tools.py                     # Tool definitions (profile, scenario, rubric I/O)
  prompts.py                   # System prompt
pyproject.toml                 # Package config, dependencies, entry points
CLAUDE.md                      # System instructions (Claude Code skills mode)
.claude/skills/                # 20 modular skill definitions
workflows/                     # 5 orchestrated multi-skill sequences
data/
  schemas/                     # JSON schemas for all data types
  users/                       # Learner profiles (5 examples included)
  scenarios/                   # 8 practice scenarios
  rubrics/                     # 3 evaluation rubrics
examples/
  interactions/                # 6 example transcripts (3 positive, 3 negative)
  workflows/                   # 3 end-to-end workflow demos
docs/                          # Architecture, pedagogical model, content map
```

## How It Works

### Scaffolding Pattern

Every teaching interaction follows this internal shape:

1. **ACKNOWLEDGE** — Name what the learner did, specifically
2. **NUDGE** — Ask a question that makes them predict or reason *before* hearing the explanation
3. **LEARNER RESPONDS** — They think through their own logic
4. **EXPLAIN** — Build on their reflection to name the transferable principle

The learner experiences a conversation, not a template. See [data/research/learner-predicts.md](data/research/learner-predicts.md) for the research grounding.

### Four Practice Types

| Type | What the learner does |
|------|----------------------|
| **Prompt Crafting** | Writes a prompt for a described task |
| **Output Evaluation** | Identifies errors in AI-generated output |
| **Appropriateness Judgment** | Decides whether/how AI should be used |
| **Workflow Design** | Designs a multi-step process involving AI |

### Skill Levels

| Level | Who | Focus |
|-------|-----|-------|
| **Novice** | First-time AI users | Build a mental model, learn basics |
| **Practitioner** | Regular users | Systematic prompting and evaluation |
| **Advanced** | Power users / builders | Failure modes, system design, auditing |
| **Critical Thinker** | Experts / policy makers | Frameworks, teaching others, policy |

Advancement requires demonstrated competence across **all 5 dimensions**: conceptual understanding, prompting skill, output evaluation, ethical reasoning, and critical thinking.

### Pedagogical Approach

Built on **Merrill's First Principles** and **Bloom's Revised Taxonomy**:

1. Lessons anchor on real tasks the learner cares about
2. The tutor surfaces existing knowledge before teaching
3. Worked examples (good and bad) precede practice
4. Simulated scenarios provide hands-on application with scaffolded feedback
5. A single closing reflection question connects practice to broader context

## Current Limitations

- This is a **prototype** for April 2026 evaluation
- The Web UI and Terminal CLI require an Anthropic API key
- The Claude Code skills version requires a Claude Code subscription
- CollaborAITE features (sidebar nudges, scheduled reflections, peer patterns) are deferred

## Feedback

Open a [GitHub Issue](https://github.com/Elorm-K/498_Agents/issues) with what you tried, what happened, and what you expected.
