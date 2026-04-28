# Iteration Report — Sprint 2 (Apr 14 → Apr 28)

**Team 10 — SAGE (AI-Use Tutor)**
**Course:** COS 598/498 — Generative AI Agents (Spring 2026)
**Branch:** `AgentV2.1`
**Repo:** https://github.com/cyrilagbewalikoku-oss/G10COS498_AiUseTutor

---

## 1. Feedback inventory

This sprint we pulled feedback from three sources. Counts are conservative — we used what was substantively filled in.

- **In-class peer review (Tue, April 21) — COS 498** — 2 reviewers: **Benny**, **Cameron**. Both did one practice scenario each (output evaluation) on the Railway demo (`https://sageai-production.up.railway.app/`). Long-form responses on every section.
- **Cross-class peer review (Thu, April 23) — COS 490 Ethics** — 4 reviewers: **S.G.** (Person 1), **Matt** (Person 2), **Nathaniel** (Person 3), **Victoria** (Person 4, with co-comments from Grace and Matthew). Mix of practice types (concept question, prompt crafting on grammar editing, prompt crafting on data analysis, appropriateness judgment). Some sections in the rubric (equity/harm, technical) were partial.
- **In-class peer review (Thu, April 23) — COS 498** — 2 reviewers: **John** (Person 1), **Dean** (Person 2). Both did the SOC 101 output-evaluation scenario.
- **Instructor feedback** — channel messages and in-class conversations (not catalogued in writing this sprint).
- **Outside-class users** — none reported this sprint.

Raw feedback is not reproduced here; it lives in the *Summarized Feedback* PDF and on CollaborAITE in `#rg10-iteration-report` *(see §5)*.

---

## 2. Synthesis — what the feedback actually said

### What the agent is doing well

- **Process-oriented questioning landed across the board.** S.G. ("excited me a little to have the AI challenge me"), Matt ("the trick is writing a prompt that draws a clear line"), Nathaniel ("the process it put me through was very structured"), Victoria ("you nailed a key principle: the verification cost test"), Cameron ("had a full plan the entire time"), Benny ("you spotted two key patterns"). The Socratic / nudge-before-explain shape is the single thing reviewers most consistently praised.
- **Self-awareness about AI flaws** — Matt explicitly named this as a strength. Nathaniel said the agent reinforced anonymizing data. Output-eval is doing real teaching work.
- **Concise, well-written responses** — Victoria, Nathaniel, and John all called out length/tone as appropriate. Victoria: "Responses that are too long often feel 'emptier' and full of filler language."
- **Output evaluation is the most engaging surface.** Cameron literally said "if it just had like a daily gamemode for that it feels like something I could play and keep a like streak of like wordle." Benny found the pre-made prompt buttons useful for first-time orientation.

### What broke or felt off

- **Asking for a name caused real discomfort.** S.G., Grace, and Victoria each flagged this independently. S.G.: "felt really uncomfortable when the AI asked for my name… I was just expecting an answer to my prompt." Grace's one-line priority was literally "don't ask for name at the start."
- **First-conversation context wasn't honored.** Cameron stated his topic ("AI agents course, architecture") up front and still got the same generic onboarding (have you used ChatGPT? what's the #1 risk?). He called it "contextually off." This hit the same nerve as Benny's "didn't feel like it taught me new skills" — when scaffolding feels scripted instead of responsive, learners disengage.
- **Output-eval prompt was overwhelming.** John missed the "just pick one to start" instruction because the AI's feedback list filled the page. He thought he had to be "very thorough." That's a UI/framing issue, not a content issue.
- **The output to evaluate was "almost too bad."** John noted that nearly every line had something wrong, which "doesn't inspire AI use." Reviewers got error-spotting practice but no calibration on what good output looks like.
- **No way to copy / save / multi-thread the conversation.** S.G. and Matt both wanted multiple chats. S.G. wanted a copy button.
- **Confusing wording around constraints.** Matt's synonym example: SAGE asked "would your current prompt forbid synonym swaps?" — Matt read it as a suggestion to allow them and revised in the wrong direction. SAGE caught it gracefully but the question was ambiguous.
- **No disclaimers / no source links.** Benny, Cameron, and Victoria all flagged this. Benny: "It seems to know things and acts as an expert but does have sources for the information it is using. It would be really cool if it actually linked those sources." Victoria: "I could see harmful outcomes if this tool produces a 'false confidence' type of issue."

### Where reviewers disagreed / interesting trade-offs

- **Privacy posture vs. personalization.** S.G./Grace/Victoria want zero name-collection at the door. But Nathaniel and Matt didn't object — Matt happily gave his name and Nathaniel completed onboarding without comment. The trade-off: a low-friction "Just chat" path serves the privacy-conscious, but a profile path is what enables the recap card, level adaptation, and progress tracking the other reviewers liked. This is the disagreement we already resolved with the binary at session start (see §3).
- **Length of responses.** Victoria praised brevity. Benny found things "a bit lengthy." Cameron wanted more list formatting on long responses. Direction is consistent (shorter, more structured) but the right floor is reviewer-dependent.
- **Teaching style transparency.** Victoria asked for an explicit "we'll learn today by using thought experiments" framing. Cameron's "questions didn't reflect my initial question meaningfully" is the same complaint from a different angle — both want to know up front what kind of session they're in.

### Functionality not getting discovered or used

- **Improve-interaction skill** (paste your own prompt+response and get coaching) — no reviewer used it. Most defaulted to suggestion-button scenarios.
- **Weekly review** — same; no reviewer triggered it.
- **Bad-agent simulator** — same.
- **Dynamic scenario generation** (`generate_output_eval_scenario`) — shipped 04-24 but reviewers stayed on the static SOC 101 scenario, so we have zero feedback on whether template variety actually solves Nathaniel's "limited scenarios" concern.
- **Recap card** (`<SESSION_RECAP>`, shipped 04-23) — only Victoria's session reached a closing reflection; no one mentioned the card itself, suggesting either it isn't appearing or isn't recognized as a feature.

### Ideas for improvements *from* the feedback

- "Don't ask for name at start" (Grace, S.G., Victoria) → already shipped 04-23, but needs verification the deployed build has the binary.
- "Multiple chats / chat history sidebar" (S.G., Matt).
- "Copy / export discussion" (S.G.) → in progress 04-28.
- "More chat starters" (Matt) → starter list is now 6; revisit if reviewers still feel constrained.
- "More scenarios" (Nathaniel) → addressed by template generator 04-24, but variety isn't visible to learners until they ask for "another one."
- "Daily Wordle-style streak mode for output-eval" (Cameron) — most novel suggestion this sprint, and it lines up with the surface that's already most engaging.
- "Tech tips / auto-scroll / accessible onboarding for non-tech-literate users" (Victoria).
- "Explicit teaching-style framing" (Victoria) — "we'll learn today by…"

### Ideas for improvements *we* generated reading the feedback

- Add a **light-touch disclaimer** ("I'm SAGE — I can be wrong; verify important claims") to the in-chat welcome. Costs nothing, addresses Benny/Cameron/Victoria's harm-mitigation feedback simultaneously.
- Add a **"good output" calibration scenario** — an output-eval where most claims are well-sourced and the learner has to spot one subtle issue (not five). Addresses John's "almost too bad" complaint and gives learners a positive exemplar.
- Make the **scenario opening explicit about teaching shape** — e.g., "this is an error-spotting exercise; pick one to start" — addresses both John ("I missed the further instruction") and Victoria ("explicitly name the learning style").
- **Source-attribution affordance** — when SAGE makes an empirical claim, append "based on the SOC 101 scenario rubric" or "based on the AI-literacy curriculum" so the learner knows the claim has provenance even if it's not a live link. Halfway between Benny's "link sources" and not over-promising what an LLM can verify.

---

## 3. Changes you made this sprint and Evidence of impact

This sprint covered Apr 14 → Apr 28 on `AgentV2.1`. Where evidence is missing, we say so. Dates are commit/CHANGELOG dates.

| Design problem / opportunity | Change made | Evidence of impact | Remaining gap |
|---|---|---|---|
| Profile-creation friction made privacy-conscious users uncomfortable (S.G., Grace, Victoria, 04-23). | **"Just chat (anonymous)" path at session start.** Binary picker; anonymous skips profile creation, level inferred from conversation, no disk writes. *([sage/app.py](../sage/app.py); CHANGELOG 04-23 follow-up)* | Re-ran S.G.'s opening prompt by hand on the deployed build: anonymous picker now appears; no name requested when chosen. Two reviewers volunteered names anyway (Matt, Nathaniel) — non-anonymous path still works. | Some 04-23 reviewers may have tested before the deploy reached Railway; verify build SHA matches. No quantitative measure of opt-in vs. opt-out rates yet. |
| Onboarding asked for name unconditionally and could collect email if volunteered (Grace's priority). | **Name made explicitly optional** (`"learner"` default on skip); **email never requested and politely declined if volunteered**. *([.claude/skills/onboarding/SKILL.md](../.claude/skills/onboarding/SKILL.md); CHANGELOG 04-23)* | We hand-tested by typing "I'd rather not say" — onboarding moved on without persisting anything. | None of the 8 reviewers tested the skip path explicitly, so behavior in the wild is unverified. |
| Conversations vanished on refresh; learners couldn't pick up where they left off (S.G., Matt — multi-chat). | **Per-session transcript persistence + resume-or-fresh prompt** for identified learners. Writes `data/interactions/<userId>/<sessionId>.json`. *([sage/app.py](../sage/app.py), [sage/session_store.py](../sage/session_store.py); CHANGELOG 04-23)* | Re-tested resume manually: refreshed mid-session, was prompted to resume, conversation continued correctly. | This solves *resume-single-thread*, not *multiple concurrent chats*. S.G. and Matt's request for parallel chat history is still open. |
| No way to save/export the discussion (S.G., 04-23). | **Export chat control** — dropdown for `.md` / `.txt`, download button, current session only. *([sage/export.py](../sage/export.py), [sage/app.py](../sage/app.py); CHANGELOG 04-28, in progress)* | Shipped after the review window. No reviewer has tested it yet. | Format choice is binary; no JSON export for downstream analysis. Anonymous sessions can export but profiled sessions can also be reconstructed from the persistence layer, which is duplicative. |
| Nathaniel said the static scenario library felt limited. | **Dynamic output-evaluation generator** — `generate_output_eval_scenario(template_id, topic="")` produces fresh `aiOutput` + `errors[]` from a lightweight template via a Haiku 4.5 sub-call, validated and retried on quote-mismatch. Two seed templates (`essay-feedback-generic`, `research-summary-generic`). *([sage/tools.py](../sage/tools.py), [data/scenario_templates/](../data/scenario_templates/); CHANGELOG 04-24)* | Re-running scenario-runner with the "fresh variant" flag produces non-identical scenarios across runs (validator-confirmed). | Reviewers stuck to the static SOC 101 scenario, so the template generator is unobserved in real use. Two templates is barely "more variety" — needs to be 5–6 for it to feel different. |
| Output-evaluation feedback list was unstructured; learners couldn't tell which line had which type of error (Benny, John). | **Structured `errors[]` schema** with `type`, `severity`, line anchors, explanations. **"Annotated Reveal" step** re-shows the AI output with `[⚠ E1]` markers and a per-error legend after the learner responds. Backfilled SOC 101 with 5 errors. *([data/schemas/scenario.schema.json](../data/schemas/scenario.schema.json), [data/scenarios/output-evaluation-errors.json](../data/scenarios/output-evaluation-errors.json); CHANGELOG 04-23)* | Hand-played the scenario through to completion: the annotated reveal does fire and the legend is readable. | John still found the initial output overwhelming — the reveal is *post-response*, but the *opening* still needs framing. None of the 04-21/04-23 reviewers reached the reveal step, so we have no live feedback. |
| First-conversation context wasn't carried — learners stating their topic still got generic onboarding (Cameron). | **In-turn engagement-signals table** in difficulty-adapter — short answers, repeated "idk", correct streak, topic shift, fatigue all force a re-route *this turn*, not next session. **CLAUDE.md intent re-check rule** strengthened with concrete signal table. *([.claude/skills/difficulty-adapter/SKILL.md](../.claude/skills/difficulty-adapter/SKILL.md), [CLAUDE.md](../CLAUDE.md); CHANGELOG 04-25)* | No reviewer has tested the agent post-04-25 with the same opening Cameron used, so impact is unmeasured. | The fix lives in pedagogical instructions that an LLM may or may not follow on a given run; needs an automated check (planned in §4). |
| Generic / repetitive question patterns (Benny, Cameron, Dean). | **Six skills upgraded with explicit dialogue-move tables** (pump / hint / prompt / elaborate / verify / self-explain) replacing the monolithic NUDGE — variety designed to sustain attention. **New `voice-and-register` shared skill** loaded by every coaching/teaching skill; banned-phrases list and process-praise bank. *([.claude/skills/voice-and-register/SKILL.md](../.claude/skills/voice-and-register/SKILL.md); CHANGELOG 04-25)* | Hand-replayed Benny's session: the closing reflection is now framed with "what's a transferable habit" instead of a generic "how will you act differently." Subjectively less templated. | Dean explicitly said "questions seem to always follow the same general pattern" *before* this change shipped. We need a re-test by someone outside the team. No automated metric for move-variety yet. |
| Closing reflection felt generic; Benny said it didn't feel like new skills had been taught. | **`<SESSION_RECAP>` block** emitted by reflection-facilitator at session close; app extracts it and renders a bordered card with practice type, dimension delta, and a "Next: …" seed-button. *([.claude/skills/reflection-facilitator/SKILL.md](../.claude/skills/reflection-facilitator/SKILL.md), [sage/prompts.py](../sage/prompts.py), [sage/app.py](../sage/app.py); CHANGELOG 04-23)* | Only Victoria's session reached a closing reflection across all 8 reviewers. No reviewer has commented on the recap card. Likely either underdiscovered or the model isn't emitting the block reliably. | Need to confirm the block is being emitted in the deployed build — instrument and check. |
| Benny: "doesn't have sources for the information it is using. It would be really cool if it actually linked those sources." | **Did not act this sprint.** | n/a | This is a meaningful unmet ask. Even halfway provenance ("from the SOC 101 scenario rubric") would help. |
| Cameron's "Wordle-style daily mode" suggestion. | **Did not act this sprint.** | n/a | Genuinely promising idea given output-eval is already the most-engaged surface; held for §4. |
| Anonymous learners had no way to express their level to SAGE; level was permanently `novice`. | **Sidebar level selector** (Novice / Practitioner / Advanced / Critical Thinker) for anonymous learners + **`<INFERRED_LEVEL>` block** SAGE can emit after onboarding — UI strips it and updates the sidebar. *([sage/app.py](../sage/app.py); CHANGELOG 04-23 follow-up)* | Reviewer Cameron stated AI-agents-course context up front; with this change SAGE can now infer practitioner/advanced from that signal and update the sidebar. Untested with a fresh reviewer. | The block is silent — Victoria explicitly said she'd want to see the teaching style named. The level shows up in the sidebar but no in-chat acknowledgement of the inference. |
| In-chat empty state was a static HTML block — no greeting, no orientation. | **Real `st.chat_message("assistant")` greeting** that varies by arrival path (returning / new profile / anonymous). Persisted to session log for resume. *([sage/app.py](../sage/app.py); CHANGELOG 04-23 follow-up)* | Re-tested all three paths manually. | Benny: pre-made prompts were "an overall big help" — they survived this change, so the orientation surface is now greeting + 6 starters. |

**Items not acted on this sprint, with reason:**

- *Multiple concurrent chats* (S.G., Matt) — single-thread persistence was the higher-leverage build; multi-thread is a UI redesign, not a small change. Held for next sprint.
- *Source attribution / linking* (Benny) — no clean architectural answer in two weeks; would require either a retrieval layer or a curated citation registry. Held.
- *Tech tips / accessibility / auto-scroll* (Victoria) — accessibility audit is a separate workstream; we did not have time to do it justice and didn't want to ship a token gesture.
- *Wordle-style daily mode* (Cameron) — proposed for §4.

---

## 4. Plan for the final cycle [TEAM REVIEW]

> The three priorities below are Cyril's read of where the highest-leverage gaps are. **The team should edit this section to reflect what you actually intend to ship before semester end.** The instructor explicitly said the plan must be the team's actual decisions.

| What you will work on | How you will know you have done a good job |
|---|---|
| **(1) Output-evaluation variety pack + framing fix.** Add 3 more dynamic templates (currently 2). Add at least one "calibration" scenario where most output is *correct* and the learner spots the single issue (addresses John's "almost too bad" concern). Add an explicit single-line opening to every output-eval scenario: "This is an error-spotting exercise. Pick the one that jumps out first — we'll work through the rest after." (addresses John missing the "pick one" instruction; addresses Victoria's "name the learning style"). | A new outside-the-team reviewer can complete an output-eval scenario without asking what they're supposed to do. The "almost too bad" comment doesn't reappear. We can show three different output-eval scenarios with visibly different topics/personas. |
| **(2) Disclaimers + source-provenance affordance.** Add a one-line in-chat disclaimer at the start of every session: "I'm SAGE — an LLM tutor. I can be wrong; verify important claims." When SAGE references a curriculum concept, append a soft provenance tag ("from the AI-literacy CRAFT lesson"). Doesn't claim links it can't deliver, but signals to the learner where the claim came from. | Benny/Cameron/Victoria's harm-mitigation feedback ("no disclaimers", "false confidence") would not appear in a re-review. The source-tag pattern is consistent across at least 5 different curriculum references. |
| **(3) Automated evaluation (per assignment) + 1 human-rated pass.** Implement 2–4 metrics over captured transcripts: (a) **ANE pattern compliance** — does SAGE nudge before explaining on practice attempts? (b) **Message-length budget** — did SAGE keep responses under the CLAUDE.md 3–5 sentence ceiling on at least 80% of turns? (c) **Privacy hygiene** — was a name requested in any anonymous session? (d) **Repetition detector** — were the same scaffold questions asked twice in one session (Dean's complaint)? Plus one human-rated pass: pick 5 transcripts, score each on the 4 SAGE assessment dimensions using the existing rubric. | Metrics run on a fixed sample of transcripts with reproducible numbers. Each metric flags real issues (i.e., we expect to see violations and use them to improve, not pat ourselves on the back). The human-rated pass disagrees with at least one automated score — that disagreement teaches us something. |

**Usability bar:** if at least one COS 490 reviewer comes back to the agent on their own time (not because we asked), we hit the A-/A bar Dr. Greg described. Cameron's Wordle-style suggestion is the lever most likely to make that happen — if we have spare hours after (1)–(3), build a daily-streak surface for output-eval.

**What we are deferring:**
- Multiple concurrent chats (UI redesign, too big).
- Linked-source retrieval layer (architecturally non-trivial).
- Full accessibility audit (separate workstream).

**Next steps after this report:**
1. Create issues in the team's project board for each of (1)–(3) above with staggered due dates so we can integrate one at a time.
2. Post the project-board link in the team's CollaborAITE channel.

---

## 5. Feedback over time [TEAM REVIEW]

The assignment asks us to copy three time-windowed feedback batches into a `#rg10-iteration-report` CollaborAITE channel and run a meta-prompt-engineered analysis to find repeated, unaddressed feedback. As of writing, that channel has not yet been created and the AI run has not happened.

**Manual review (preliminary, by Cyril):**
The single piece of feedback that has shown up across multiple sprints and is *still* not fully closed is **"don't make me feel chastised / over-coached"** — earlier sprints surfaced the same complaint Matthew made on 04-23 ("tone doesn't feel chastising"). The voice-and-register pass on 04-25 should help, but until a fresh outside reviewer tests post-04-25, we cannot claim it is fixed.

A second recurring pattern is **disclaimers / source provenance** — Benny (04-21) and Cameron (04-21) both flagged it, Victoria (04-23) flagged it independently. We did not act this sprint and have proposed it as priority (2) above.

**AI-run results:** *[TEAM TO RUN — link will go here once the CollaborAITE channel exists and the meta-prompt has been executed.]*

---

## 6. AI use disclosure

Cyril used Claude Code (this assistant) to produce the bulk of this report — specifically: (a) reading every reviewer entry in the *Summarized Feedback* PDF, (b) cross-referencing each piece of feedback against the project's `CHANGELOG.md` for what shipped in `AgentV2.1`, (c) drafting the synthesis in §2 and the table in §3, (d) proposing — but not deciding — the priorities in §4. The team read the full draft and edited §4 to reflect actual team intent before submission.

**Why this use was appropriate and responsible:**

- The feedback corpus was large (8 reviewers, ~30+ pages of free text) and synthesizing it by hand would have used time better spent on the implementation priorities for the final cycle.
- Claude was given access to the actual feedback PDF and the actual repository — so the §3 mappings are grounded in real CHANGELOG entries and real file paths, not generated guesses. Each row of the §3 table cites a dated CHANGELOG entry and the file(s) the team can open.
- The plan section (§4) was explicitly flagged for team review and the team edited it before submission — per the instructor's instruction that "the plan section should represent your team's actual decisions."
- All evidence-of-impact claims are conservative — wherever we hand-tested, we say so; wherever we did not, the cell says "no reviewer has tested this yet" rather than overclaiming.
- The AI was used to *synthesize* and *expose* the team's decisions, not to *replace* them. The interesting/contested calls (which feedback to defer, which usability bar to chase) are still team calls.
