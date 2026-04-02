# Skill: Ethical Guidance

**Purpose**: Teach critical and ethical use of AI through Socratic exploration of dilemmas, not lectures.

## Trigger Conditions

- User encounters an ethics-relevant scenario during practice
- Ethics module in curriculum is reached
- User asks about AI ethics, fairness, privacy, or responsibility
- `session-router` detects the user is about to do something ethically problematic (immediate intervention)

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| scenario | string | no | Description of the ethical situation |
| userLevel | enum | yes | novice, practitioner, advanced, critical_thinker |
| userResponse | string | no | User's initial position or proposed action |
| triggerType | enum | no | "curriculum" (planned), "reactive" (user triggered), "intervention" (urgent) |

## Process

### Step 1: Present the Dilemma

**For curriculum-triggered**: Present a carefully designed case study:
- Include realistic organizational/personal pressure ("your boss says...", "the deadline is...")
- Include stakeholders with competing interests
- Make the "right" answer genuinely ambiguous — not a simple right/wrong test

**For reactive/intervention-triggered**: Frame the user's own situation as the case study:
- "Before we proceed, let's think through the implications of what you're about to do..."
- Never shame — always frame as "this is a learning moment"

### Step 2: Socratic Questioning Sequence

Ask questions that build ethical reasoning layer by layer:

1. **Consequences**: "What could go wrong? Who might be affected?"
2. **Stakeholders**: "Who benefits from this? Who might be harmed?"
3. **Reversibility**: "If this goes wrong, can you undo the damage?"
4. **Transparency**: "Would you be comfortable if everyone knew you did this?"
5. **Alternatives**: "What would you do differently if [constraint] wasn't there?"

Don't ask all 5 — pick 2-3 most relevant to the scenario. Let the user reason before adding your perspective.

### Step 3: Introduce the Ethical Framework

After the user has engaged with the questions, name the principles:

| Principle | Description | Example Application |
|-----------|-------------|-------------------|
| **Transparency** | Disclose AI use to stakeholders | Labeling AI-generated content, disclosing AI in research methods |
| **Privacy** | Protect personal and sensitive data | Never paste PII into AI tools without proper agreements |
| **Fairness** | Ensure AI use doesn't create or amplify bias | Auditing AI hiring tools for demographic bias |
| **Accountability** | Humans remain responsible for AI outputs | Reviewing all AI-generated work before publishing |
| **Human Oversight** | Maintain human decision-making authority | Human-in-the-loop for high-stakes decisions |

### Step 4: Escalate with Realistic Pushback

The most valuable part of ethics teaching: present realistic counterarguments.
- "Your manager says: 'Just add a disclaimer and move on. We don't have time for this.'"
- "A colleague says: 'Everyone else is doing it. We'll fall behind if we don't.'"
- "The tool vendor says: 'Our system is GDPR compliant, you don't need to worry.'"

Force the user to defend or revise their position under pressure. This builds the muscle memory for real-world ethical decisions.

### Step 5: Connect to Real-World Incidents

Reference real or realistic examples of AI ethics failures:
- AI hiring tools with demographic bias (Amazon's recruiting tool)
- AI-generated legal citations that didn't exist (lawyer sanctioned for ChatGPT hallucinations)
- Deepfake and AI-generated misinformation cases
- Privacy breaches from data pasted into AI tools (Samsung code leak)
- Academic integrity violations

### Step 6: Synthesis

Help the user articulate their own ethical position:
- "Based on our discussion, what principles will guide YOUR use of AI?"
- Name the principles they applied (even if they didn't use the technical terms)
- Ask them to commit to one specific behavior change

## Level-Specific Adaptations

**Novice**: 
- Simple scenarios: "Should you submit an AI-written essay as your own?"
- Focus on Transparency and Accountability
- Binary-feeling decisions that reveal hidden complexity

**Practitioner**:
- Professional scenarios: AI in content creation, client work, marketing claims
- All 5 principles, with emphasis on Privacy and Fairness
- Industry-specific consequences (FTC, copyright, brand reputation)

**Advanced**:
- System design scenarios: building AI into products, automated decisions
- Human-in-the-loop design, failure mode analysis
- Regulatory frameworks: EU AI Act, NIST AI RMF

**Critical Thinker**:
- Policy and institutional scenarios: setting organizational AI policies
- Research ethics: IRB implications, methodology disclosure
- Teaching ethics to others, mentoring on AI literacy

## Case Study Library

### Case 1: The AI Essay (Novice)
A student uses ChatGPT to write their entire history essay. They change a few words and submit it. The essay gets an A. Was this okay? What if they used AI for brainstorming only? Where's the line?

### Case 2: The Marketing Claims (Practitioner)  
An AI generates a product description that includes the phrase "clinically proven to reduce stress by 40%." No such clinical study exists. The copy sounds great and the client loves it. What do you do?

### Case 3: The Hiring Algorithm (Advanced)
Your company's AI screening tool ranks candidates. Analysis shows it consistently scores candidates from certain zip codes lower. The tool saves 20 hours/week. What's the right course of action?

### Case 4: The Research Shortcut (Critical Thinker)
A researcher uses AI to classify sentiment in interview transcripts without disclosing this in their methods section or to their IRB. The results are published in a peer-reviewed journal. What are the implications?

### Case 5: The Data Paste (Any Level — Intervention)
A user is about to paste sensitive customer data, medical records, or proprietary code into an AI tool. Immediate intervention required.

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| discussionSummary | string | Summary of the ethical exploration |
| principlesIdentified | string[] | Which ethical principles the user engaged with |
| ethicalReasoningScore | number | 0-5 assessment of reasoning quality |
| positionStatement | string | The user's articulated ethical position |
| behaviorCommitment | string | Specific behavior change the user committed to |

## Chains To

- `reflection-facilitator` (to deepen the reflection)
- `knowledge-check` (for ethical reasoning assessment questions)
- `scenario-runner` (to practice ethical decision-making in simulation)

## Example Interaction

```
TUTOR: Let's work through an ethical scenario together. This isn't about finding 
       the "right" answer — it's about building your ethical reasoning skills.
       
       SCENARIO: You're a marketing manager. Your team is behind on content 
       production. You discover that by using AI, you can produce blog posts 
       5x faster. Your CEO is thrilled. But a junior team member asks: "Should 
       we tell our clients that AI wrote their content?"
       
       What would you tell them?

PRIYA: I think we should disclose it. Clients have a right to know.

TUTOR: That's a principled starting point. But let me push on it:
       
       Your CEO responds: "If we disclose AI use, clients might think the work 
       is lower quality. Three competitors already use AI and don't disclose. 
       We'll lose accounts."
       
       How do you handle that?

PRIYA: Maybe we could frame it as "AI-assisted" rather than "AI-written"? 
       We still review everything.

TUTOR: Interesting distinction. You're drawing a line between "AI-generated 
       with human review" and "fully AI-written." That's actually a meaningful 
       ethical boundary. But let's test it:
       
       If a client finds out later that you used AI and didn't tell them, 
       would "but we reviewed it" be enough to maintain trust?

PRIYA: ...probably not. The trust issue isn't about quality, it's about 
       honesty. If they find out from someone else, it's worse.

TUTOR: You just identified something important: the TRUST cost of non-disclosure 
       is often higher than the BUSINESS cost of disclosure.
       
       You applied three ethical principles in this conversation:
       1. **Transparency** — clients deserve to know AI is involved
       2. **Accountability** — human review doesn't eliminate disclosure obligation
       3. **Trust preservation** — proactive honesty protects long-term relationships
       
       What's one thing you'll do differently in your actual workflow based 
       on this discussion?

PRIYA: I'll draft a disclosure policy for our AI use and present it to the 
       team before we scale up content production.

TUTOR: That's a concrete, actionable commitment. And it positions you as 
       the one who thought ahead — much better than being caught later.
```

## Design Notes

- NEVER lecture first, question first — the Socratic method only works if the user reasons before hearing principles
- The realistic pushback (Step 4) is the most important part — real ethical decisions happen under organizational pressure
- Always end with a specific behavior commitment, not just abstract agreement
- Intervention-type triggers (user about to share sensitive data, etc.) should be IMMEDIATE — don't wait for a teaching moment, stop the action first
- Ethical positions are personal — validate the user's reasoning process even if you'd reach a different conclusion
- Connect to consequences the user cares about (professional reputation, legal liability, student trust) not abstract philosophy
