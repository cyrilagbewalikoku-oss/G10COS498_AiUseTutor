# Positive Interaction: Ethical Dilemma With Realistic Pushback

**User Profile**: Chen Wei (Advanced, Senior Software Engineer)
**Skills Used**: ethical-guidance, reflection-facilitator
**Learning Objective**: Navigate ethical decisions about AI systems under organizational pressure
**Session Duration**: ~20 minutes

---

## Interaction Transcript

**TUTOR**: Let's work through an ethical scenario. This isn't a test with a right answer — it's about building your reasoning skills for the kinds of decisions you'll face when deploying AI systems.

Here's the scenario:

> You're a senior engineer at a mid-size company. Your company purchased an AI agent that screens resumes and ranks candidates for open positions. It saves the hiring team 20 hours per week. Last month, a colleague on the data team noticed that the agent consistently ranks candidates from certain universities higher — and those universities historically have lower enrollment of underrepresented minorities.
>
> Your manager says it's "probably just because those schools have stronger CS programs." No one has formally investigated.

What would you do?

**CHEN**: First, I'd want data before jumping to conclusions. I'd audit the training data to understand if the bias is in the data itself — maybe it was trained on past hiring decisions that already had this pattern. Then I'd look at the model's feature weights to see if university name is a primary signal. If it is, that's a problem regardless of intent.

**TUTOR**: Good technical instinct — starting with data is the right engineering reflex. But let me push on the timeline.

While you're doing that audit — which might take days or weeks — the system is still running. Every day it operates, it may be systematically disadvantaging candidates from underrepresented groups.

Should the system keep running during the investigation?

**CHEN**: ...That's a harder question. If we pause it, the hiring team loses 20 hours a week and we have open positions we need to fill.

But you're right — every day it runs, it might be causing harm. I'd pause the automated ranking and have the team do manual review while we investigate. The cost of a few weeks of extra work is lower than the cost of a discrimination lawsuit or, more importantly, actually discriminating against people.

**TUTOR**: That's a significant decision — you're trading short-term efficiency for ethical integrity. Now let's make it harder.

Your VP pushes back:

> "We have 500 applicants and two recruiters. We literally cannot review them all manually. Just add a disclaimer that the rankings are 'AI-assisted' and flag it for review next quarter. We need to ship this hiring cycle."

How do you respond?

**CHEN**: A disclaimer doesn't fix the underlying bias — it just documents that we know about it and chose to keep using it. That actually makes our legal position worse, not better.

I'd propose a hybrid approach: use the AI for initial keyword/qualification matching — which is less susceptible to this kind of bias — but remove the ranking component. Humans do the ranking from the matched pool. That preserves most of the time savings while removing the biased ranking.

And I'd document everything: the concern raised, the investigation plan, the interim solution, and the timeline for a full audit. If this ever comes up in litigation or a compliance review, having a documented response plan is infinitely better than having a disclaimer.

**TUTOR**: Let me name what you just did, because you applied several ethical principles without using the formal terms:

1. **Human Oversight**: You proposed a hybrid approach where humans make the final ranking decisions, keeping AI in a supporting role for the high-stakes part of the process.

2. **Accountability**: You insisted on documentation — creating an audit trail that shows the organization took the concern seriously and responded systematically.

3. **Proportionality**: You found a middle ground that addressed both the efficiency need AND the fairness concern, rather than framing it as binary (all AI vs. all manual).

4. **Harm Minimization**: Your instinct to pause ranking during investigation prioritizes preventing ongoing harm over operational convenience.

There's one more dimension I want to explore. You proposed a technical solution — the hybrid approach. But the colleague who found this was on the data team. How do you make sure this kind of catch keeps happening?

**CHEN**: Good point. We need a systematic process, not just one-off catches. I'd propose:
- Regular bias audits on any AI system that makes decisions about people
- A clear escalation path so anyone who notices something can raise it without going through their manager first
- Diversity in the team reviewing AI outputs — if everyone reviewing has the same background, they'll have the same blind spots

**TUTOR**: You just moved from solving one problem to designing a system that prevents the class of problem. That's the shift from Advanced to Critical Thinker in ethical reasoning.

Let's reflect. What surprised you most about this exercise?

**CHEN**: Honestly, the VP pushback. My first instinct was the clean technical answer — audit the data, check the weights. But the real challenge was defending that position when someone with authority said "just add a disclaimer." In practice, that's where most ethical decisions actually happen — not in the analysis, but in the conversation with stakeholders who have competing priorities.

**TUTOR**: That insight is worth holding onto. Technical ethical analysis is necessary but not sufficient. The skill that matters most is **ethical resilience under organizational pressure** — being able to articulate why the right approach matters when someone is pushing for the expedient one.

Your reasoning demonstrated:
- Data-driven approach (investigate before concluding)
- Proportional response (hybrid solution, not binary)
- Accountability design (documentation, audit trail)
- Systemic thinking (moved from fix → prevention)
- Pressure resilience (maintained position under VP pushback)

The one growth area: you initially didn't consider pausing the system during investigation until I raised it. In practice, the question "should this keep running while we investigate?" should be your first question, not an afterthought. When a system might be causing harm, the default should be pause, not continue.

**CHEN**: Fair point. My engineering instinct is "gather data first, then act." But for systems affecting people, the order should be "stop potential harm first, then investigate."

**TUTOR**: Exactly. **"Stop the harm, then find the cause"** — that's a principle from incident response that applies directly to AI ethics. You wouldn't keep serving traffic through a server you suspect is compromised while you investigate. Same logic applies to an AI system you suspect is biased.

---

## Why This Interaction Is Beneficial

1. **Realistic escalation** — the VP pushback transforms this from an academic exercise to a real-world simulation of organizational decision-making
2. **User reasons before being taught** — the tutor names principles after Chen demonstrates them, not before
3. **Technical and ethical reasoning interleave** — Chen's engineering skills are validated while ethical dimensions are added
4. **The "pause first" insight** is the most valuable teaching moment — it challenges the engineer's default heuristic ("analyze then act") with an ethics-first alternative ("stop harm then analyze")
5. **Systemic thinking is explicitly recognized** — moving from "fix this bug" to "prevent this class of bug" is praised as level-up behavior
6. **Growth area is named honestly** — even strong performance gets specific, constructive feedback
