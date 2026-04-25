# Motivational Scaffolding & Conversational Engagement

## What it is

The pedagogical research behind keeping a learner engaged across a conversation — neither bored (under-challenged, hand-holdy, repetitive) nor overwhelmed (jargon, walls of text, too many moves per turn). Sits underneath SAGE's voice, the dialogue-move taxonomy, and the difficulty adapter.

This file documents the lineage so the choices in `voice-and-register/SKILL.md`, the move tables in skill files, and the in-turn signals in `difficulty-adapter/SKILL.md` can be cited rather than re-derived.

## The four pillars

### 1. Self-Determination Theory (Deci & Ryan, 2000)

Intrinsic motivation needs three nutrients:

- **Autonomy** — the learner feels in charge of the path. Choice architecture, not forced sequence. (SAGE: opt-in retrieval warm-ups, three-paths menu, the "any of these feel wrong?" hook in `progress-reporter`.)
- **Competence** — the learner feels capable. Specific, process-oriented feedback; visible growth; winnable challenges. (SAGE: process-praise phrase bank in voice-and-register §2; feed-up framing in `scenario-runner` and `concept-explainer`.)
- **Relatedness** — the learner feels the tutor is *with* them, not grading them. Peer tone, shared language, genuine interest. (SAGE: register-matching cues in voice-and-register §5; peer tone in `weekly-review`.)

These three are why the rules around "no ability praise", "match the learner's register", and "let the learner challenge the score" are not stylistic preferences — they are how the learner stays motivated to come back next session.

### 2. Lepper's INSPIRE motivational scaffolding (Lepper & Woolverton, 2002)

Studied expert human tutors. The best ones do far more than explain — they hit a consistent set of motivational moves:

- **Indirect correction** — never say "wrong"; ask a question that exposes the issue.
- **Attribution to effort/strategy, not ability** — *"that didn't land because you didn't constrain the format"* not *"you're close"*.
- **Minimising the negative** — acknowledge what worked before probing what didn't.
- **Challenge framing** — name the difficulty before springing it.

Lepper's moves are the basis for the attribution templates and challenge-framing openers in voice-and-register §2 and §3. They are also why "great thinking!" and "perfect!" are banned — they're ability praise, which Dweck (2007) shows produces fragile learners. Process praise — naming the *move*, not the *person* — produces resilient ones.

### 3. AutoTutor dialogue moves (Graesser et al., 2001, 2014)

AutoTutor matched human-tutor learning gains by cycling through a rich set of **dialogue acts** rather than a single scaffolding pattern. The six SAGE imports:

| Move | Purpose |
|---|---|
| Pump | *"…and?"* — elicit more without revealing |
| Hint | Partial cue toward the answer |
| Prompt | Direct question about a specific element |
| Elaborate | Tutor adds correct info after learner gets partial |
| Verify | *"Does that make sense?"* — checks shaky understanding |
| Self-explain | *"Say that back in your own words."* — anchors transfer |

Variety itself sustains attention. Same nudge twice in a row reads as a script, even when each individual nudge is well-formed. The move tables now embedded in `prompt-coaching`, `scenario-runner`, `concept-explainer`, `knowledge-check`, `improve-interaction`, and `bad-agent-simulator` come from this lineage.

### 4. Flow + expertise reversal (Csikszentmihalyi 1990; Kalyuga 2007)

Engagement peaks when difficulty sits just above current skill. Below → boredom. Above → anxiety. **Expertise reversal**: scaffolds that help novices actively *harm* experts — worked examples feel patronising, step-by-step hints break concentration. Fade scaffolds as competence grows.

This is why `difficulty-adapter`'s in-turn engagement signals exist (the table added under "In-Turn Engagement Signals"). Boredom and overwhelm are signals that fire *inside* a session, not just between sessions, and they require the next message to change shape — not the next module.

## Connected ideas SAGE uses but doesn't necessarily cite to the learner

- **Feed-up / feed-back / feed-forward** (Hattie & Timperley, 2007). Effective feedback answers: where am I going? how am I going? what's next? The feed-up framing in `scenario-runner` Step 2 and `concept-explainer` is feed-up; the session-recap block is feed-back + feed-forward.
- **Process praise vs. ability praise** (Dweck, 2007). See voice-and-register §2.
- **Productive failure** (Kapur, 2008, 2016). Letting learners struggle *before* instruction improves transfer. The struggle-framing line in `prompt-coaching` and `scenario-runner` ("writing a prompt that doesn't land is how you learn which parts matter") is the explicit framing.
- **Self-explanation** (Chi et al., 1989; Dunlosky et al., 2013). Asking the learner to restate a principle in their own words after the EXPLAIN. Distinct from Learner Predicts (which happens *before* the answer); self-explain happens *after*, and it's the move that actually transfers the principle. The `self-explain` cell in every move table is this.
- **Open Learner Models** (Bull & Kay, 2007). When learners can see and challenge the tutor's model of them, engagement rises. The "any of these feel wrong?" hook in `progress-reporter` is this idea, scaled down.
- **Communication Accommodation Theory** (Giles et al., 1991). Mirroring register builds rapport. The register-matching cues in voice-and-register §5 are this.
- **Spaced retrieval** (Roediger & Karpicke, 2006; Bjork & Bjork, 2011). The optional warm-up in `session-router` Step 1b is this — one pulse on a stale-but-shaky dimension at session start.

## Deliberately not used

- **Gamification** (points, streaks, badges). Lepper's overjustification effect (1973) shows extrinsic rewards can erode intrinsic motivation in learning contexts. SAGE relies on competence-affirming feedback and meaningful progress visibility (the open learner model), not extrinsic rewards.

## Selected grounding

- Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry*, 11(4), 227–268.
- Lepper, M. R., & Woolverton, M. (2002). The wisdom of practice: Lessons learned from the study of highly effective tutors. In J. Aronson (Ed.), *Improving academic achievement: Impact of psychological factors on education*.
- Graesser, A. C., VanLehn, K., Rosé, C. P., Jordan, P. W., & Harter, D. (2001). Intelligent tutoring systems with conversational dialogue. *AI Magazine*, 22(4), 39–51.
- Csikszentmihalyi, M. (1990). *Flow: The psychology of optimal experience*.
- Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. *Educational Psychology Review*, 19(4), 509–539.
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81–112.
- Dweck, C. S. (2007). *Mindset: The new psychology of success*.
- Kapur, M. (2016). Examining productive failure, productive success, unproductive failure, and unproductive success in learning. *Educational Psychologist*, 51(2), 289–299.
- Chi, M. T. H., et al. (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science*, 13(2), 145–182.
- Bull, S., & Kay, J. (2007). Student models that invite the learner in: The SMILI:() open learner modelling framework. *International Journal of AI in Education*, 17(2), 89–120.
- Giles, H., Coupland, N., & Coupland, J. (1991). *Contexts of accommodation*.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249–255.

## How SAGE applies it

The synthesis is operationalized in four places — citing the research here so the implementation files don't have to:

1. **`voice-and-register/SKILL.md`** — register matching, process praise, attribution templates, challenge framing, struggle framing, banned phrases.
2. **`difficulty-adapter/SKILL.md` "In-Turn Engagement Signals" section** — Flow / expertise-reversal, applied per-turn.
3. **Skill move tables** in `prompt-coaching`, `scenario-runner`, `concept-explainer`, `improve-interaction`, `knowledge-check`, `bad-agent-simulator` — AutoTutor dialogue acts.
4. **The simulation-interior carve-out** in `scenario-runner` Step 5 and `bad-agent-simulator` Step 2 — protects the planted-error practice value from leaking via mid-simulation tutor moves.
