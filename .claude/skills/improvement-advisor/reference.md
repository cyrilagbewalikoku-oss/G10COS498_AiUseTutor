# Improvement Advisor

## Purpose

Turn assessment gaps into actionable learning plans prioritized by the learner's goals. Instead of presenting a generic list of weaknesses, this skill analyzes which gaps matter most for what the learner is trying to accomplish and provides immediately actionable exercises alongside a longer-term development plan. The framing is always forward-looking: "here's how to get from good to great," not "here's what you're bad at."

## Trigger Conditions

- After an assessment reveals gaps between current scores and required scores for the next level
- After level-classifier identifies specific dimension gaps
- When the user explicitly asks "What should I work on?", "How do I improve?", or similar
- When chained from progress-reporter after areas needing attention are identified

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `gapAnalysis` | `Array<{ dimension: string, currentScore: number, requiredScore: number, gap: number }>` | Yes | The computed gaps between where the learner is and where they need to be, typically produced by level-classifier or skill-evaluator |
| `userLevel` | `enum("novice", "beginner", "practitioner", "critical-thinker", "expert")` | Yes | The learner's current classified level, used to calibrate exercise difficulty and language |
| `userGoals` | `string[]` | Yes | The learner's stated goals (e.g., "evaluate AI content for clients", "set classroom AI policies", "audit agent behavior in production") used to prioritize which gaps to address first |

## Process

1. **Prioritize gaps by impact on user's stated goals.** Not all gaps are equally important -- the one that most directly blocks the learner's goals should be addressed first. Apply the following prioritization logic:
   - Map each goal to the dimensions it depends on most heavily:
     - "evaluate AI content for clients" -> Output Evaluation, Critical Thinking
     - "set classroom AI policies" -> Ethical Reasoning, Conceptual Understanding
     - "audit agent behavior in production" -> Ethical Reasoning, Critical Thinking, Output Evaluation
     - "write better prompts for daily work" -> Prompting Skill, Conceptual Understanding
     - "teach others to use AI" -> Conceptual Understanding, Ethical Reasoning, Prompting Skill
   - Rank gaps by: (a) relevance to the user's primary goal, (b) size of the gap, (c) whether the dimension is stagnant or declining
   - Select the top 2-3 gaps for focused attention. Do not overwhelm the learner with more than three simultaneous improvement areas.

2. **For each prioritized gap (top 2-3), provide a structured improvement block:**

   a. **Explain WHY this gap matters for their specific goals.** Do not use abstract language. Connect the dimension directly to their stated objective.
      - Good: "As someone who wants to audit agent behavior in production, you need to recognize when an AI system is operating outside ethical boundaries. Right now, your ethical reasoning score suggests you may miss some of these situations."
      - Bad: "Ethical reasoning is an important skill for AI literacy."

   b. **Provide a targeted mini-exercise they can do RIGHT NOW (5-10 minutes).** The exercise should be:
      - Self-contained (no dependencies on other modules)
      - Directly relevant to the gap dimension
      - Calibrated to the user's current level (not too easy, not too hard)
      - Completable in a single sitting

   c. **Link to the relevant module or skill for deeper work.** Name the specific module, scenario, or skill that would provide sustained practice in this area.

   d. **Give an estimated timeline.** Set realistic expectations: "This usually takes 2-3 focused sessions to strengthen" or "Most learners see improvement in this area within a week of regular practice."

3. **Create a focused practice plan** with three time horizons:
   - **This session:** One mini-exercise from the highest-priority gap (the one provided in step 2b)
   - **Next 2-3 sessions:** Targeted modules and scenarios for the top gaps, with a suggested sequence
   - **Ongoing:** 1-2 habits to build into their regular AI use that will reinforce the improvement areas over time (e.g., "Always verify the first statistic in any AI output", "Before submitting a prompt, ask yourself: did I specify the format I want?")

4. **Frame everything positively.** The learner should leave this interaction feeling motivated and equipped, not demoralized.
   - Lead with what they're already doing well before addressing gaps
   - Use growth language: "strengthen", "build on", "develop", "sharpen"
   - Avoid deficit language: "weakness", "failure", "poor", "bad at"
   - Acknowledge that gaps are normal and expected at every level

## Outputs

| Parameter | Type | Description |
|---|---|---|
| `improvementPlan` | `Array<{ priority: number, dimension: string, gap: number, whyItMatters: string, miniExercise: string, linkedModule: string, estimatedSessions: number }>` | Ordered list of improvement areas with full context for each |
| `immediateAction` | `string` | The single most impactful thing the learner can do right now, described in 1-2 sentences |
| `habitSuggestions` | `string[]` | 1-2 ongoing practices the learner can adopt to reinforce improvement in their gap areas |

## Chains To

- **concept-explainer** -- for gaps rooted in conceptual misunderstanding, chains to deliver targeted conceptual content
- **prompt-coaching** -- for gaps in prompting skill, chains to provide guided prompting practice with real-time feedback
- **ethical-guidance** -- for gaps in ethical reasoning, chains to explore ethical frameworks and case studies
- **scenario-runner** -- for gaps that benefit from hands-on practice, chains to launch a targeted scenario

## Example Interaction

> **Context:** Chen is an advanced developer currently classified at the Practitioner level. His goal is "audit agent behavior in production." Level-classifier has identified that his ethical reasoning score is 3.0 but needs to reach 3.5 for Critical Thinker. His output evaluation is at 3.8 (strong) and his prompting is at 4.0 (strong). His critical thinking is at 3.2 (needs 3.5).

**Tutor:** You've built a strong foundation, Chen. Your prompting and output evaluation skills are well above the threshold for your current level -- that's real expertise showing through. Let's talk about how to close the remaining gaps so you can reach Critical Thinker level.

Based on your goal of auditing agent behavior in production, I've prioritized two areas for you:

---

**Priority 1: Ethical Reasoning (3.0 -> 3.5 needed)**

**Why this matters for you:** When you're auditing AI agents in production, technical correctness is only part of the picture. You also need to recognize when an agent is operating in ways that create regulatory risk, violate user privacy, or produce outcomes that are fair in aggregate but harmful to specific groups. Your current ethical reasoning score suggests you're solid on the obvious cases -- you can spot clearly biased output -- but may miss more subtle issues like differential impact across user segments or tension between business objectives and user welfare.

**Try this now (5-10 minutes):**

> *Mini-Exercise: GDPR Implications Audit*
>
> Imagine you're reviewing an AI customer service agent deployed in the EU. The agent has access to the following user data to personalize responses: purchase history, support ticket history, user's stated age, and browsing behavior on the company website.
>
> The agent uses this data to prioritize support tickets -- users who browse premium products get faster response times.
>
> Identify at least three ethical or regulatory concerns with this setup. For each one, explain: (a) what the concern is, (b) which principle or regulation it relates to, and (c) what you would recommend changing.

When you're ready, share your analysis and I'll walk through it with you.

**For deeper work:** The "AI Governance Frameworks" module covers GDPR, the EU AI Act, and fairness frameworks in detail. It includes case studies specifically about production AI systems. I'd recommend completing it across your next two sessions.

**Estimated timeline:** Most developers at your level strengthen ethical reasoning to 3.5 within 2-3 focused sessions, especially since your critical thinking skills help you reason through ethical scenarios once you have the right frameworks.

---

**Priority 2: Critical Thinking (3.2 -> 3.5 needed)**

**Why this matters for you:** In production auditing, you'll encounter situations where an AI agent's behavior is technically correct but strategically problematic -- or where multiple stakeholders have conflicting definitions of "correct." Critical thinking at the 3.5 level means you can hold multiple perspectives simultaneously and evaluate trade-offs without defaulting to a single stakeholder's view.

**Try this now (5-10 minutes):**

> *Mini-Exercise: Stakeholder Trade-off Analysis*
>
> A content moderation AI agent is flagging 15% of legitimate product reviews as potentially harmful. Reducing the false positive rate to 5% would require loosening the filters, which would also let through approximately 2% more genuinely harmful content.
>
> Write a brief analysis (3-5 paragraphs) addressing: Who are the stakeholders? What does each stakeholder value? What would you recommend, and what is the strongest argument against your recommendation?

**For deeper work:** The "Trade-off Analysis" scenario in scenario-runner presents increasingly complex multi-stakeholder situations. Completing 2-3 of these scenarios would directly build this skill.

**Estimated timeline:** 2-3 sessions, running in parallel with your ethical reasoning work since the two dimensions reinforce each other.

---

**Your practice plan:**

| Timeframe | Activity |
|---|---|
| **This session** | Complete the GDPR Implications Audit mini-exercise above |
| **Next session** | Start the "AI Governance Frameworks" module (Part 1: Regulatory Landscape) |
| **Session after that** | Complete the "AI Governance Frameworks" module (Part 2: Fairness Frameworks) and run one "Trade-off Analysis" scenario |
| **Ongoing habit** | When reviewing any AI system, add a standing question to your audit checklist: "Who could be disproportionately harmed by this system's behavior, and would they have recourse?" |

You're closer to Critical Thinker than you might think -- your strong technical skills mean you just need to layer in the ethical and multi-perspective reasoning. Two to three focused sessions should get you there.

## Design Notes

- **Goal-driven prioritization is essential.** Learners are more motivated to work on gaps they can see are relevant to their objectives. A developer who wants to audit production systems will engage with ethical reasoning when framed as "regulatory risk detection" far more readily than when framed as "ethical reasoning."
- **Mini-exercises must be immediately doable.** If the exercise requires setup, background reading, or external tools, the learner is unlikely to do it. The best mini-exercises are thought experiments or short analysis tasks that can be completed in the chat interface.
- **Estimate timelines honestly.** Over-promising ("You'll master this in one session!") erodes trust. Under-promising ("This takes months") kills motivation. Base estimates on observed patterns across learners at similar levels.
- **Limit to 2-3 priorities.** Research on goal-setting consistently shows that more than three simultaneous improvement areas leads to diffusion of effort. Even if there are five gaps, focus the learner on the top two or three.
- **Connect dimensions that reinforce each other.** Ethical reasoning and critical thinking often develop in tandem. Prompting skill and output evaluation are similarly linked. When two prioritized gaps are synergistic, point this out -- it makes the work feel more efficient.
- **The habit suggestion is the highest-leverage output.** A mini-exercise happens once. A habit compounds over time. Invest effort in crafting habit suggestions that are specific, easy to remember, and naturally fit into the learner's existing workflow.
- **Revisit and update.** If the learner returns after working on the plan, acknowledge their effort before running a new assessment. Don't just regenerate the plan from scratch -- show continuity.
