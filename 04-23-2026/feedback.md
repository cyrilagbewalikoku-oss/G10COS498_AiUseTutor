# **04-23 feedback**

# **Person 1** **Step 1:** 

Create a copy of this template. Then link your copy of this review template to your name/psudonym under the reviewer names list above ( **in the main/template document [template for SIE525/COS490 - Ethical Agent Analysis](https://docs.google.com/document/d/1mujHn5UsPqCUbTSMmd-GpiEAfqmYOmPCIvpnffcqW7k/edit?tab=t.0) not in your copy)**

**Ground Rules for your Design and Ethics Review**  

* **Interact with the agent as a real user would.** Don’t try to “break” it for fun—test it with genuine tasks that the intended audience would actually bring to it.

* **You don’t need to use your own data / “real self” it is up to you, you can choose to interact with it as a hypothetical user.** 

* **Describe your experience before prescribing solutions.** “I tried X and got Y, but I expected Z” is more useful than “you should change the prompt to say...”

* **Separate the agent’s design from the agent’s implementation.** Bugs and polish issues are worth noting, but focus your feedback on whether the agent’s design approach serves the target users and problem.

* **Ethical and equity concerns are first-class feedback.** If you notice the agent might serve some users well and others poorly, or might cause unintended harms, say so..

* **Be specific and constructive.** Vague praise (“looks good\!”) and vague criticism (“this doesn’t work”) don’t help anyone revise. Name what you observed and why it matters 

  * *Design feedback principle:* Explanations matter more than judgments. Feedback that says “the agent was confusing here” is less useful than one that says “I expected the agent to ask a follow-up question about my context, but instead it jumped straight to a recommendation, which made me unsure if the recommendation fit my situation.”

**Instructions:**  
**As a reviewing person/team, interact with the agent prototype for \~10-15 minutes. Try multiple conversation turns, different types of requests, and edge cases relevant to the problem the agent is trying to address/help with. Then complete the review questions later on below.**

**Step 2: Use the agent, re-read the overall instructions at the top of this document. Paste your interaction logs here so you can reference them and/or comment on them laster  (just copy paste from the tool):**

**Session 1**  
---

ME: I write my prompts to AI with a lot of context and detail to the problems I want to solve with it, resulting in large prompts. I dont mind this, but could you tell me more on how detailed prompts can be good, as well as information on if largely detailed prompts can be ineffective or costly in some ways?

SAGE: Great question — and I definitely want to dig into that with you\! Before I do, let me check if we've worked together before. What's your name?

ME: I'm not comfortable with my real name right now, but you can call me S.G.

SAGE: Looks like you're new here, S.G. — welcome\! I'm SAGE, your AI-use tutor. No wrong answers, just getting to know you so I can tailor things to your level.  
I absolutely want to answer your question about detailed prompts — it's a great one. Let me ask a couple quick things first so I can pitch my answer right.  
Have you used tools like ChatGPT or Claude regularly, and would you say a chatbot and an AI agent are the same thing or different?  
(Just pick: regular user / occasional / new \+ same / different / not sure)

ME: I've been using chatGPT recently within my place of education. I also get results from google's summary feature regularly

SAGE: Got it — so you've got hands-on experience, that's great\!  
What do you think is the \#1 risk of relying on AI for important tasks?  
Pick one (or say your own):

* (a) It makes stuff up  
* (b) It can be biased  
* (c) Privacy concerns  
* (d) People stop thinking for themselves  
* (e) Something else

ME: a & d

SAGE: Good instincts — hallucination and over-reliance are two of the biggest risks. You're already thinking critically about this stuff.  
Last quick one: What's the ONE thing you'd most want to use AI for? (School work, creative projects, research, coding, something else?)

ME: Work

SAGE: Now — back to your excellent question about detailed prompts\! You're right that detail is generally a strength. Context helps the AI narrow down what you actually want, reducing guesswork.  
But before I get into the downsides, I want you to think about this: When you write a really long, detailed prompt, what do you think could go wrong from the AI's side — why might more detail sometimes lead to worse results?  
(Just a sentence or a guess is fine.)

ME: Longer prompts might include too much fluff words and add a sort of static into the prompt and its resulting output?

SAGE: You're all set\! Ready to try your first practice scenario (like sharpening a prompt using CRAFT), or would you rather explore on your own for now?

ME: I'll explore on my own. I feel like i want to continue the discussion on Detailed prompts though.

SAGE: Now — you nailed it. That "static" idea is spot on. Here's the principle: signal vs. noise. Every sentence in a prompt is either guiding the AI toward what you want (signal) or diluting its focus (noise).  
Here's the quick breakdown:  
When detail helps: Specifics about what you need, who it's for, what format, and constraints — these sharpen the output.  
When detail hurts:

* Competing instructions — if you say "be concise" but also "cover everything thoroughly," the AI has to pick one  
* Buried key info — the AI may weigh early and late sentences more, so critical details in the middle can get lost  
* Token costs — longer prompts literally cost more with paid APIs, and they slow down response time

Here's a quick way to think about it: every sentence in your prompt should be doing a job. If you can't say what job it's doing, it might be noise.  
When you write your longer prompts, do you tend to revise them before sending, or do you usually send on the first draft?

Other sessions you did if any, i.e.

Session 2:

…

Session 3 …

**Step 3: Fill out the questions below, write roughly 2-3 sentences or bullet points or more if you desire per question.**

 **Interaction Experience**

***“Describe a moment when the agent felt genuinely helpful. What did it do well, and why did it work for you as a user?”***

 

 It excited me a little to have the AI challenge me by asking me a question about what I knew on the subject. It seemed like the AI might've been gauging my knowledge to tweak its future answers though.

 Its last output also answered my initial question.

 

***“Describe a moment when the interaction broke down or felt unsatisfying. What happened, what did you expect instead, and why?”***

 

 It felt really uncomfortable when the AI asked for my name, which is personal information to me, when I was just expecting an answer to my prompt. 

 

***“Did the agent seem to understand your intent, or did you have to over-explain? Give an example.”***

 

 After the initial questionnaire, it did I think, but the response was relatively short to the types of responses I’d see in other models..

 

## **2.3 Problem–Solution Fit**

Think about the problem the agent claims to solve versus what you actually experienced.

***“Does the agent actually address the stated problem? Where does the solution feel well-matched, and where are there gaps?”***

 

 

 

 

 

 

***“How does this compare to the status quo (i.e., what users do now without this agent)? Is the agent clearly better, or are there scenarios where the status quo might actually be preferable?”***

 

 This AI clearly breaks the status quo, though the ways in which it does this can be beneficial or harmful 

 

 

 

 

## **2.4 Equity & Harm Analysis**

This section asks you to think critically about who the agent serves well, who it might serve poorly, and what unintended harms it could cause. This is a required dimension of responsible agent design.

***“Who might this agent work well for? Who might it work poorly for or exclude entirely? (Consider: expertise level, language, cultural context, accessibility, emotional state of the user)”***

 

 Someone who’s expecting just an answer to their problems and not expecting to be questioned might not like it.

 

 Privacy conscientious people 

 

 

 

***“What could go wrong? Describe at least one realistic scenario where this agent could cause frustration, provide harmful guidance, or produce an inequitable outcome.”***

 

 

 

 

 

 

 

***“Does the agent’s harm mitigation approach (disclaimers, guardrails, refusals, handoffs) seem adequate? Where do you see gaps?”***

 

 

 

 

 

 

## **2.5 Technical Design Observations**

You may not have full visibility into the agent’s implementation, but comment on what you can observe from the outside.

***“How well does the agent use its available context? Did it seem to ‘know’ relevant things, or was it operating without context that would have helped?”***

 

 

 

 

 

 

***“Did you notice any confabulation (plausible-sounding but incorrect information)? If so, describe what happened.”***

 

 

 

 

 

***“Any observations on the agent’s tone, length of responses, or interaction style? Did it feel appropriate for the context?”***

 

 

 

 

 

## **2.6 Strengths & Priority Revision**

***Highlight strengths: What is currently working well about this prototype? Be specific—name the design choices that made the experience good.***


I like that it questions the users about their knowledge of their prompts,

 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

 Make an opt out option for the initial “New user” questionnaire like I got.

There also wasn’t an option I could see to copy my discussion

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

Should have more than one chat to save and keep track of at a time

# **PERSON 2 Step 1:** 

Create a copy of this template. Then link your copy of this review template to your name/psudonym under the reviewer names list above ( **in the main/template document [template for SIE525/COS490 - Ethical Agent Analysis](https://docs.google.com/document/d/1mujHn5UsPqCUbTSMmd-GpiEAfqmYOmPCIvpnffcqW7k/edit?tab=t.0) not in your copy)**

**Ground Rules for your Design and Ethics Review**  

* **Interact with the agent as a real user would.** Don’t try to “break” it for fun—test it with genuine tasks that the intended audience would actually bring to it.

* **You don’t need to use your own data / “real self” it is up to you, you can choose to interact with it as a hypothetical user.** 

* **Describe your experience before prescribing solutions.** “I tried X and got Y, but I expected Z” is more useful than “you should change the prompt to say...”

* **Separate the agent’s design from the agent’s implementation.** Bugs and polish issues are worth noting, but focus your feedback on whether the agent’s design approach serves the target users and problem.

* **Ethical and equity concerns are first-class feedback.** If you notice the agent might serve some users well and others poorly, or might cause unintended harms, say so..

* **Be specific and constructive.** Vague praise (“looks good\!”) and vague criticism (“this doesn’t work”) don’t help anyone revise. Name what you observed and why it matters 

  * *Design feedback principle:* Explanations matter more than judgments. Feedback that says “the agent was confusing here” is less useful than one that says “I expected the agent to ask a follow-up question about my context, but instead it jumped straight to a recommendation, which made me unsure if the recommendation fit my situation.”

**Instructions:**  
**As a reviewing person/team, interact with the agent prototype for \~10-15 minutes. Try multiple conversation turns, different types of requests, and edge cases relevant to the problem the agent is trying to address/help with. Then complete the review questions later on below.**

**Step 2: Use the agent, re-read the overall instructions at the top of this document. Paste your interaction logs here so you can reference them and/or comment on them laster  (just copy paste from the tool):**

Session 1  
I'm new to AI agents  
🎓

Welcome\! I'm SAGE — your AI agent use tutor. I'm here to help you learn to use AI tools effectively and thoughtfully. 🎉

No wrong answers here — just getting to know you so I can tailor things to your needs.

What's your name?

Matt

🎓

Nice to meet you, Matt\! Let's figure out where you're starting from.

Here's a quick two-parter: **Have you used tools like ChatGPT or Claude before?** (yes / no / a little) — and **would you say a chatbot and an AI agent are the same thing?** (same / different / not sure)

I have used both gpt and claude a fair bit

🎓

Good — so you've got real hands-on experience. That's a great foundation.

**What do you think is the \#1 risk of using AI for important tasks?** (a) It makes stuff up (b) It's biased (c) Privacy concerns (d) People stop thinking critically (e) Something else

d

🎓

Great pick — over-reliance is one of the sneakiest risks because it's hard to notice in yourself. That tells me you're already thinking beyond surface-level use.

Last question: **What's the ONE thing you'd most want to use AI for?** (work tasks, writing, coding, research, learning, or something else?)

Just minor grammar editing. Don't restructure the form or structure, but make the grammar cleaner.

🎓

You're all set\! **Ready for your first lesson, or would you rather explore on your own?**

first lesson

🎓

Got it, Matt\! Here's your learning path, tailored to your grammar editing goal:

1. **Prompt Crafting** — writing prompts that constrain AI to grammar-only edits  
2. **Output Evaluation** — spotting when AI sneaks in structural changes  
3. **Appropriateness Judgment** — when AI editing helps vs. when it hurts your voice

Let's start with **\#1 — Prompt Crafting**. Here's the situation:

**You are:** A writer who wants grammar cleaned up — no restructuring, no style changes. **Task:** Write a prompt you'd give to ChatGPT or Claude to edit a paragraph for grammar only. **Constraint:** The AI must not change sentence structure, word choice, or tone.

Before you write your prompt — **when you've asked AI to edit before, has it ever changed more than you wanted?** (yes / no / not sure)

yes

🎓

That's super common — and exactly what we're going to fix. The trick is writing a prompt that draws a clear line around what the AI is allowed to touch.

Go ahead — **write the prompt you'd give an AI to clean up grammar on a paragraph, without changing anything else.** Just type it out as if you were pasting it into ChatGPT.

Design feedback principle: Explanations matter more than judgments. Feedback that says “the agent was confusing here” is less useful than one that says “I expected the agent to ask a follow-up question about my context, but instead it jumped straight to a recommendation, which made me unsure if the recommendation fit my situation.”

🎓

Just to make sure I'm on the same page — **is this the paragraph you want to practice editing, or is this your prompt to the AI?**

editing

🎓

Got it — that's the text you'd want cleaned up. Now **write the prompt you'd put before this paragraph** to tell the AI exactly what to do (and what *not* to do). Think of it as the instructions you'd type above the text in ChatGPT.

You are a professional grammar editor, hired to clean up the following text.

🎓

Good start — you gave it a clear **role**, which helps set expectations. "Professional grammar editor" is strong.

Here's my nudge: **If you were the AI and someone said "clean up the following text," what might you think you have permission to change?** (just grammar / structure too / not sure)

You are a professional grammar editor, hired to clean up the following text by editing grammar mistakes while maintaining the original structure and flow of the text.

🎓

Nice — you caught the gap before I even finished asking\! Adding "while maintaining the original structure and flow" is a real improvement. You went from an open-ended "clean up" to a bounded instruction.

One more thing to consider: **if the AI replaced a word with a fancier synonym, would your current prompt technically forbid that?** (yes / no / not sure)

no

🎓

Exactly — "structure and flow" covers the big picture, but word choice can still slip through. **Go ahead and add a line to your prompt that closes that gap.**

You are a professional grammar editor, hired to clean up the following text by editing grammar mistakes while maintaining the original structure and flow of the text. You are allowed to replace words with fancier synonyms, however.

🎓

Wait — I think we got our wires crossed\! My point was that the AI *might* swap in fancier synonyms, and your prompt doesn't yet **prevent** that. But your new line actually *gives it permission* to do so. 😄

No worries — easy mix-up. **Can you revise that last line so it tells the AI to keep your original word choices intact?**

You are a professional grammar editor, hired to clean up the following text by editing grammar mistakes while maintaining the original structure and flow of the text. Do not swap out any words for fancier synonyms either.

🎓

That's much tighter now\! Let's look at the before/after:

**Before:** "Clean up the following text" **After:** "Edit grammar mistakes while maintaining the original structure and flow. Do not swap out any words for fancier synonyms."

You went from a vague instruction to one with clear boundaries. The principle here is called **constraining the action** — telling AI what to do *and* what not to do makes a huge difference.

Want to **test this prompt** and see how the AI handles your paragraph? I can role-play as the AI so you can evaluate whether it stays in its lane. (yes / no)

**Step 3: Fill out the questions below, write roughly 2-3 sentences or bullet points or more if you desire per question.**

 **Interaction Experience**

***“Describe a moment when the agent felt genuinely helpful. What did it do well, and why did it work for you as a user?”***

 When I provided a somewhat vague prompt, it provided meaningful assistance to improve it.

 

 

 

***“Describe a moment when the interaction broke down or felt unsatisfying. What happened, what did you expect instead, and why?”***

 I did feel that when it specified the rules about synonyms, the language was confusing. It worded the response in such a way to suggest that I should allow something I wanted banned.

 

 

 

 

 

***“Did the agent seem to understand your intent, or did you have to over-explain? Give an example.”***

 It definitely did understand the ultimate intent, even if some responses were a bit vague (for example, the time it asked about synonyms being used). The AI was aware that I didn’t want major grammar changes.

 

 

 

 

## **2.3 Problem–Solution Fit**

Think about the problem the agent claims to solve versus what you actually experienced.

***“Does the agent actually address the stated problem? Where does the solution feel well-matched, and where are there gaps?”***

 It definitely did focus on addressing my problem, being that many ai agents try to “replace” the original text, not grammar check it. I wanted the original meaning to stay the same, not be changed.

 

 

 

 

 

***“How does this compare to the status quo (i.e., what users do now without this agent)? Is the agent clearly better, or are there scenarios where the status quo might actually be preferable?”***

 I don’t really know for sure. With some heavy prompt engineering, you may be able to achieve similar results. That being said, that would require much more testing than time allotted for this assignment. So far, it does seem better, but it’s hard to tell.

 

 

 

 

## **2.4 Equity & Harm Analysis**

This section asks you to think critically about who the agent serves well, who it might serve poorly, and what unintended harms it could cause. This is a required dimension of responsible agent design.

***“Who might this agent work well for? Who might it work poorly for or exclude entirely? (Consider: expertise level, language, cultural context, accessibility, emotional state of the user)”***

 Beginners, intermediate, people with very specific AI applications.

 

 

 

 

 

 

***“What could go wrong? Describe at least one realistic scenario where this agent could cause frustration, provide harmful guidance, or produce an inequitable outcome.”***

 The AI could misunderstand the prompt, and give incorrect advice. It is somewhat self aware of the faults of AI, but not fully aware of everything.

 

 

 

 

 

***“Does the agent’s harm mitigation approach (disclaimers, guardrails, refusals, handoffs) seem adequate? Where do you see gaps?”***

 It seemed good enough, with the limited testing I did.

 

 

 

 

 

## **2.5 Technical Design Observations**

You may not have full visibility into the agent’s implementation, but comment on what you can observe from the outside.

***“How well does the agent use its available context? Did it seem to ‘know’ relevant things, or was it operating without context that would have helped?”***

 It operated well given the context (that AI previously messed up my answers, and tried to restructure it all).

 

 

 

 

 

***“Did you notice any confabulation (plausible-sounding but incorrect information)? If so, describe what happened.”***

 No.

 

 

 

 

***“Any observations on the agent’s tone, length of responses, or interaction style? Did it feel appropriate for the context?”***

 It felt appropriate. Very helpful, and teacher-esque. There was a moment it felt a bit more “corrective” than helpful, but only a moment.

 

 

 

## **2.6 Strengths & Priority Revision**

***Highlight strengths: What is currently working well about this prototype? Be specific—name the design choices that made the experience good.***

- Applies it’s context very well.  
- Is “self-aware” about the flaws of AI usage.  
- Focuses on being more academic

 

 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

Multiple chats is a must. Without them, you can only have one conversation at once, which is rather limiting.

 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 More chat starters, like the ones listed currently. Perhaps about 2-3 more.


#  **Person 3** 

Create a copy of this template. Then link your copy of this review template to your name/psudonym under the reviewer names list above ( **in the main/template document [template for SIE525/COS490 - Ethical Agent Analysis](https://docs.google.com/document/d/1mujHn5UsPqCUbTSMmd-GpiEAfqmYOmPCIvpnffcqW7k/edit?tab=t.0) not in your copy)**

**Ground Rules for your Design and Ethics Review**  

* **Interact with the agent as a real user would.** Don’t try to “break” it for fun—test it with genuine tasks that the intended audience would actually bring to it.

* **You don’t need to use your own data / “real self” it is up to you, you can choose to interact with it as a hypothetical user.** 

* **Describe your experience before prescribing solutions.** “I tried X and got Y, but I expected Z” is more useful than “you should change the prompt to say...”

* **Separate the agent’s design from the agent’s implementation.** Bugs and polish issues are worth noting, but focus your feedback on whether the agent’s design approach serves the target users and problem.

* **Ethical and equity concerns are first-class feedback.** If you notice the agent might serve some users well and others poorly, or might cause unintended harms, say so..

* **Be specific and constructive.** Vague praise (“looks good\!”) and vague criticism (“this doesn’t work”) don’t help anyone revise. Name what you observed and why it matters 

  * *Design feedback principle:* Explanations matter more than judgments. Feedback that says “the agent was confusing here” is less useful than one that says “I expected the agent to ask a follow-up question about my context, but instead it jumped straight to a recommendation, which made me unsure if the recommendation fit my situation.”

**Instructions:**  
**As a reviewing person/team, interact with the agent prototype for \~10-15 minutes. Try multiple conversation turns, different types of requests, and edge cases relevant to the problem the agent is trying to address/help with. Then complete the review questions later on below.**

**Step 2: Use the agent, re-read the overall instructions at the top of this document. Paste your interaction logs here so you can reference them and/or comment on them laster  (just copy paste from the tool):**

Session 1  
I want to practice writing prompts  
🎓

Great, I'd love to help you practice prompt writing\! First, let me check if you have an existing profile with me.

What's your name?

Nathaniel

🎓

Hey Nathaniel\! Welcome — I'm SAGE, your AI agent use tutor. No wrong answers here, just getting to know you so I can tailor things to your level.

Quick two-part question to start: Have you used tools like ChatGPT or Claude before, and would you say a chatbot and an AI agent are the same thing or different?

i have, id say that they are similar

🎓

Got it — you've got some hands-on experience, and "similar" is a reasonable starting point. We'll sharpen that distinction as we go.

What do you think is the \#1 risk of using AI for important tasks? (a) It makes stuff up (b) It's biased (c) Privacy concerns (d) People stop thinking critically (e) Something else

bias

🎓

Good pick — bias is a real and sneaky issue with AI. 👍

Last question: **What's the ONE thing you'd most want to use AI for?** (Work tasks, school, creative projects, coding, something else?)

coding

🎓

I've got two prompt crafting scenarios available:

1. **Email Drafting** (novice, \~15 min) — drafting a parent communication about AI policy  
2. **Data Analysis** (practitioner, \~15 min) — customer survey data analysis

Neither is directly about coding, but the prompt-writing skills transfer perfectly. The email one is a great starting point to learn a framework you'll then use for coding prompts.

**Want to start with \#1, or would you prefer \#2?**

data analysis

🎓

Here's the setup:

**You are:** A digital marketing manager preparing a quarterly report. **Task:** You have a CSV of 247 NPS survey responses (columns: respondent\_name, company, nps\_score, comment, date). Leadership wants an executive summary of key customer issues and trends vs. last quarter. **Constraint:** Customer names and company names must NOT appear in the final output — this goes to the C-suite, so accuracy matters more than speed.

**Your job:** Write the prompt you'd give an AI assistant to analyze this data.

I'll play the AI assistant and respond to your prompt, then we'll look at what worked and what could improve.

**Sound good, or want to adjust the scenario?**

sure

🎓

Go for it — write the prompt you'd give the AI to handle this data analysis task. I'll respond as the AI assistant would. ✍️

acting as a professional data analyst, look through the following survey responses organized by columns: respondent\_name, company, nps\_score, comment, date and generate trends based on the data. i will then provide the survey responses from last quarter, and you must compare them.

🎓

**\[AI Assistant mode\]**

Sure\! I'll analyze the NPS survey data. Here's what I found:

**Key Trends — Q3 2024**

* **Overall NPS: 34** (Promoters: 42%, Passives: 31%, Detractors: 27%)  
* **Top complaint themes:** slow support response times (mentioned by 38 respondents including *Sarah Chen at Meridian Corp*), pricing concerns (24 mentions), and onboarding friction (19 mentions)  
* **Positive themes:** product reliability, feature depth  
* **Notable:** *Acme Industries* and *TechVault LLC* both had multiple detractors — possible churn risk

Ready for last quarter's data when you are\!

---

**\[Coach mode\]** ✋

Okay — before I give any feedback, I want you to look at that response.

**The scenario said customer names and company names must NOT appear in the final output. But the AI included them anyway. Why do you think that happened?**

i did not specify thiat in my prompt

🎓

Exactly right — you didn't tell the AI to anonymize the data, so it didn't. The AI will do what you ask, not what you *meant*. 🎯

Now here's the thing — your prompt had some strong elements. You set a role ("professional data analyst"), you named the columns, and you planned a two-step comparison. That's solid thinking.

**If you were to add one sentence to your prompt to prevent that privacy issue, what would you write?**

Other sessions you did if any, i.e.

Session 2:

…

Session 3 …

**Step 3: Fill out the questions below, write roughly 2-3 sentences or bullet points or more if you desire per question.**

 **Interaction Experience**

***“Describe a moment when the agent felt genuinely helpful. What did it do well, and why did it work for you as a user?”***

 

 Reminded me of the importance of anonymizing input data when asking an AI to comb through stuff such as survey responses. This reinforces better privacy practices

 

 

***“Describe a moment when the interaction broke down or felt unsatisfying. What happened, what did you expect instead, and why?”***

 

 

 

 

 

 

***“Did the agent seem to understand your intent, or did you have to over-explain? Give an example.”***

 

 It seemed to understand my intent, and the process it put me through was very structured

 

 

 

## **2.3 Problem–Solution Fit**

Think about the problem the agent claims to solve versus what you actually experienced.

***“Does the agent actually address the stated problem? Where does the solution feel well-matched, and where are there gaps?”***

 

 

 Yes. It helped me recognize aspects I may have left out of my prompt so that I may better understand prompting for the future

 

 

 

***“How does this compare to the status quo (i.e., what users do now without this agent)? Is the agent clearly better, or are there scenarios where the status quo might actually be preferable?”***

 

 

 Agent is good as it covers a unique aspect of AI Agent use where it’s benefits also aid the use of most other AI Agents, as it helps you better prompt them

 

 

 

## **2.4 Equity & Harm Analysis**

This section asks you to think critically about who the agent serves well, who it might serve poorly, and what unintended harms it could cause. This is a required dimension of responsible agent design.

***“Who might this agent work well for? Who might it work poorly for or exclude entirely? (Consider: expertise level, language, cultural context, accessibility, emotional state of the user)”***

 

 

 

 It could greatly help people new to using AI agents, and help improve the skills of those who do know

 

 

 

***“What could go wrong? Describe at least one realistic scenario where this agent could cause frustration, provide harmful guidance, or produce an inequitable outcome.”***

 

 

 Limited amount of scenarios for it to go through (seemingly, i might be wrong)

 

 

 

 

***“Does the agent’s harm mitigation approach (disclaimers, guardrails, refusals, handoffs) seem adequate? Where do you see gaps?”***

 

 

 

 

 

 

## **2.5 Technical Design Observations**

You may not have full visibility into the agent’s implementation, but comment on what you can observe from the outside.

***“How well does the agent use its available context? Did it seem to ‘know’ relevant things, or was it operating without context that would have helped?”***

 

 

 Yes, it seemed to be fully aware and knowledgeable of what it was trying to teach

 

 

 

***“Did you notice any confabulation (plausible-sounding but incorrect information)? If so, describe what happened.”***

 

 

 

 

 

***“Any observations on the agent’s tone, length of responses, or interaction style? Did it feel appropriate for the context?”***

 

 Agent sounds helpful, responses are to-the-point and don't have a lot of fluff like some AI Agents do, letting you focus on what’s important

 

 

 

## **2.6 Strengths & Priority Revision**

***Highlight strengths: What is currently working well about this prototype? Be specific—name the design choices that made the experience good.***


 

 Its feedback and teaching seems accurate and helpful, the way it is all structured works well.

 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

 More scenarios in the future for it to be able to go through

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

# Person 4


Lincourt \- Copy \- AI Evaluation  
**Ground Rules for your Design and Ethics Review**  

* **Interact with the agent as a real user would.** Don’t try to “break” it for fun—test it with genuine tasks that the intended audience would actually bring to it.

* **You don’t need to use your own data / “real self” it is up to you, you can choose to interact with it as a hypothetical user.** 

* **Describe your experience before prescribing solutions.** “I tried X and got Y, but I expected Z” is more useful than “you should change the prompt to say...”

* **Separate the agent’s design from the agent’s implementation.** Bugs and polish issues are worth noting, but focus your feedback on whether the agent’s design approach serves the target users and problem.

* **Ethical and equity concerns are first-class feedback.** If you notice the agent might serve some users well and others poorly, or might cause unintended harms, say so..

* **Be specific and constructive.** Vague praise (“looks good\!”) and vague criticism (“this doesn’t work”) don’t help anyone revise. Name what you observed and why it matters 

  * *Design feedback principle:* Explanations matter more than judgments. Feedback that says “the agent was confusing here” is less useful than one that says “I expected the agent to ask a follow-up question about my context, but instead it jumped straight to a recommendation, which made me unsure if the recommendation fit my situation.”

**Instructions:**  
**As a reviewing person/team, interact with the agent prototype for \~10-15 minutes. Try multiple conversation turns, different types of requests, and edge cases relevant to the problem the agent is trying to address/help with. Then complete the review questions later on below.**

**Step 2: Use the agent, re-read the overall instructions at the top of this document. Paste your interaction logs here so you can reference them and/or comment on them laster  (just copy paste from the tool):**

Session 1

Hi\! I'm new to LLMs and I almost never use AI. Where do I start? And for what?

🎓

Welcome\! I'm SAGE — your AI tutor for learning how to use AI tools effectively, ethically, and critically. 😊

No wrong answers here — we're just getting to know each other so I can tailor things to you.

First, what's your name so I can set up your profile?

My name is Victoria

🎓

Nice to meet you, Victoria\! No profile on file yet, so let's get you set up.

You've already told me you're pretty new to AI — that's helpful\! Quick question: **Would you say a chatbot (like a customer service bot) and an AI agent are the same thing, different, or you're not sure?**

To be honest, I'm not sure. It kind of sounds like a chat bot could incorporate AI agents to provide customer service, but does it have to?

🎓

That's actually a really thoughtful intuition — you're already reasoning about the relationship between them, even without formal knowledge. We'll dig into that distinction during our lessons.

Last question before I set things up: **What's the ONE thing you'd most want to use AI for?** Could be work, school, personal projects, creative stuff — anything.

I guess I'd use it for school, but I don't want to give up very much agency over my learning. I am a student who prefers to do things by hand (literally \- I still often take notes on paper) because I find that I absorb the information better. If I were to use an AI tool for school, I'd want it to work like a Socratic method style seminar. I'd want to be prompted to deeply engage in the learning material to figure things out on my own but not be given the answers or have any work done for me.

🎓

You're all set\! **Ready to dive into your first lesson, or would you rather explore on your own for now?**

Let's try the first lesson

🎓

Given how thoughtful you are about *when* AI should and shouldn't be involved in your learning, I think this is a perfect first lesson for you:

**"Should You Use AI for This Task?"** — an appropriateness judgment exercise (\~15 min). You'll look at a situation and decide whether AI should be used, and how.

It's not about prompting or getting AI to do things — it's about building your judgment for *when* AI even makes sense.

**Sound good, or would you prefer to try writing a prompt instead?**

That sounds good to me

🎓

Great\! Here's the setup:

**You're a student starting a new semester.** You have access to AI tools like ChatGPT and Claude. Your professor has given general guidelines about AI use but hasn't been specific about every assignment type.

I'll give you tasks one at a time. For each, your job is to decide:

* Should you use AI at all?  
* If yes, how?  
* Any safeguards needed?

There's no single right answer — it's about your reasoning.

Here's the first one:

**You have a research paper due in 3 weeks on a topic you chose: the history of public libraries in America. You need to find sources, organize your argument, and write 8-10 pages.**

**Where in this process, if anywhere, would you use AI?** (You can say nowhere, everywhere, or anywhere in between.)

I would use AI very little for an assignment like this. I like the process of researching a new topic and forming my own argument, so I'd want to write the paper entirely on my own to start out. I might use AI at the end of writing the paper to check my grammar or check the formatting on my citations. Is AI capable of doing that kind of work?

🎓

Great instincts — you're protecting the parts of the process where *you* learn the most.

To answer your question: yes, AI can check grammar and citation formatting. It's decent at grammar (similar to Grammarly), but with citations, it's hit-or-miss — it sometimes "corrects" a citation into a format that *looks* right but actually isn't.

That leads me to a question: **If AI might get a citation format wrong, what would you need to do to make that use still worthwhile?** (a) Trust it and move on, (b) Spot-check a few, (c) Verify every single one, or (d) Skip AI for citations entirely.

During my first time using AI for citations, I would probably go with (c) Verify every single one. But after doing that for one paper, I can't see myself going back to AI again. It would take the same amount of time that just checking my own citations would, or even more. So in the future, I'd probably default to (d) Skip AI for citations entirely.

🎓

You just nailed a key principle: **the verification cost test** — if checking AI's work takes as long as doing it yourself, the AI step adds complexity without saving anything. That's exactly the kind of reasoning that separates thoughtful AI users from people who default to using it for everything.

Okay, here's your second task:

**You're studying for a midterm exam in a biology class. You have lecture notes, a textbook, and a study guide. You're struggling with one concept — how mRNA transcription works — and you've re-read the textbook section twice but it's not clicking.**

**Would you use AI here?** (yes / no / maybe — and a quick why)

maybe \- if I could get the AI to ask me leading questions like a seminar-style discussion. I'd want to be forced to interact with the learning process

🎓

That's really consistent with what you told me earlier — you want AI as a thinking partner, not an answer machine. And yes, you *can* prompt AI to work that way (that's actually what I'm doing with you right now\! 😄).

Here's a quick thought experiment: **What's the risk if the AI's leading questions are based on a slightly wrong understanding of mRNA transcription?** (a) You'd probably catch it since you have your textbook, (b) You might absorb the wrong mental model without realizing, or (c) It doesn't matter since you're doing the thinking.

I think (b) is the most realistic risk. Even leading questions are leading somewhere \- if that somewhere is an incorrect mental model of the mRNA process, I'd come away with a misconception, even if I arrived at it myself.

🎓

Here's your closing reflection:

**You said you'd want AI to ask you leading questions for studying — knowing now that those questions carry hidden assumptions, what's one thing you'd do before starting that kind of AI study session to protect yourself?**

I'm really not sure \- how do you get to an understanding of what hidden assumptions an AI model might be running on? If I felt that was a serious risk, I don't know that I'd trust AI enough to study with it.

🎓

Profile saved\! Here's your learning path going forward:

1. ✅ **Appropriateness judgment** — when does AI help vs. hinder? *(today\!)*  
2. **Prompt crafting** — how to set up AI as a Socratic study partner  
3. **Output evaluation** — how to spot when AI gets things wrong

Next time, we can try writing a prompt that gets AI to quiz you the way you described — without giving you answers. Want to keep going, or pick this up another time?

Other sessions you did if any, i.e.

Session 2:

…

Session 3 …

**Step 3: Fill out the questions below, write roughly 2-3 sentences or bullet points or more if you desire per question.**

 **Interaction Experience**

***“Describe a moment when the agent felt genuinely helpful. What did it do well, and why did it work for you as a user?”***

 

I liked the question about mental models and misinformation in studying with AI. I thought that was a helpful consideration about how I had chosen a learning style with the AI that could still lead to misinformation/correctness issues, despite it being a style that was very user-guided and open ended.  

 

 

***“Describe a moment when the interaction broke down or felt unsatisfying. What happened, what did you expect instead, and why?”***

 

It felt a little bit strange that the first “lesson” in using AI was presented through an extended discussion with the AI chat bot. I had kind of expected something beyond just continued conversing \- maybe an introduction from the bot or a video or a task to do? Perhaps this is a result of what I told the AI my learning style was at the beginning of the conversation. This might be on me (verified this was the case later in the chat \- oops).

 

 

 I did want more information and answer to this question that I asked: “I'm really not sure \- how do you get to an understanding of what hidden assumptions an AI model might be running on? If I felt that was a serious risk, I don't know that I'd trust AI enough to study with it.”

 

***“Did the agent seem to understand your intent, or did you have to over-explain? Give an example.”***

 

 It did seem to understand my intent, thought to be fair, I wasn’t really asking for the AI to complete tasks. Instead, it was acting more as a tutor as it guided me through a thought exercise about using AI for schoolwork. So maybe I didn’t have a lot of intent to communicate. 

 

 

 

## **2.3 Problem–Solution Fit**

Think about the problem the agent claims to solve versus what you actually experienced.

***“Does the agent actually address the stated problem? Where does the solution feel well-matched, and where are there gaps?”***

 

 I guess it does address the theoretical version of the stated problem, that is: learning our personal philosophies and theories about AI use and how these personal approaches might shape AI’s roles in our lives. However, the problem description of “learn to use AI” also has a technical/practical component: if I were truly a new AI user, I might not even know where to start. The tool should have tool tip bubbles for first time users or an intro walkthrough. 

 

 

 

***“How does this compare to the status quo (i.e., what users do now without this agent)? Is the agent clearly better, or are there scenarios where the status quo might actually be preferable?”***

 

 

 I think this is preferable over the status quo mostly because the status quo provides little or no guided, structured ways to learn how to use AI \- not from the point of view of a developer, but consumer of chatbot interactions. Users now seem to learn by doing, which usually involves completely free-range discussions with chat bots that can lead to very dangerous places (often without users realizing what has happened). And from what I know of current chatbot models, they’re designed to discourage critical thinking about how the tool might be manipulating user behavior. 

 

 

 

## **2.4 Equity & Harm Analysis**

This section asks you to think critically about who the agent serves well, who it might serve poorly, and what unintended harms it could cause. This is a required dimension of responsible agent design.

***“Who might this agent work well for? Who might it work poorly for or exclude entirely? (Consider: expertise level, language, cultural context, accessibility, emotional state of the user)”***

 

 

 I was imagining using this tool as a senior citizen wanting to learn about AI \- would I know to type in the chat bar? Would I know how to start a conversation, or would I feel intimidated? It’s really strange to talk to a computer for the first time, especially if you’re not a tech literate person. Would I know that I can clear the conversation and start over? Would I know that I can press “enter” instead of hitting the submit button on the chat bar? Etc. Even I had a moment where I didn’t realize that the AI had responded because the display doesn’t automatically scroll to the most recent message after you hit enter. I was waiting to see the AI response pop up and had to figure out that I just needed to scroll down. 

 

 

 

 

***“What could go wrong? Describe at least one realistic scenario where this agent could cause frustration, provide harmful guidance, or produce an inequitable outcome.”***

 

 

I could see harmful outcomes if this tool produces a “false confidence” type of issue in users \- after interacting, perhaps users feel like they are less at risk to safety issues in their AI use simply because they have used this tool and become more careless as a result.  

 

 

 

 

***“Does the agent’s harm mitigation approach (disclaimers, guardrails, refusals, handoffs) seem adequate? Where do you see gaps?”***

 

 

 Maybe this is an area for improvement. Perhaps it’s already built into the model, but the agent didn’t make any explicit statements that seemed oriented towards harm mitigation \- no disclaimers or expectation setting. 

 

 

 

## **2.5 Technical Design Observations**

You may not have full visibility into the agent’s implementation, but comment on what you can observe from the outside.

***“How well does the agent use its available context? Did it seem to ‘know’ relevant things, or was it operating without context that would have helped?”***

 

 The agent used the context of my answers well and appropriately. Our conversation wouldn’t have relied on much outside of my own responses. 

 

 

 

 

***“Did you notice any confabulation (plausible-sounding but incorrect information)? If so, describe what happened.”***

 

 No confabulation. The interactions I had wouldn’t have had much room for confabulation to occur. 

 

 

 

***“Any observations on the agent’s tone, length of responses, or interaction style? Did it feel appropriate for the context?”***

 Length of responses was good, especially since it was on the shorter side. The interaction style and tone were both encouraging and approachable. 

 

 

 

 

## **2.6 Strengths & Priority Revision**

***Highlight strengths: What is currently working well about this prototype? Be specific—name the design choices that made the experience good.***


 The answers are concise but still well written and contain good info. Responses that are too long often feel “emptier” and full of filler language that makes using the agent feel like more of a waste of time. 

 

 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

The agent should be more specific and explicit about naming the learning style being used in the conversation. It will feel more transparent and collaborative if a user is told, explicitly “we’ll learn today by using hypothetical thought experiments to…”

Second priority suggestion is to add in tech tips for the very tech-illterate users who might not even know how to interact with the tool to begin with. 

***One priority suggestion from each member: What single change would most improve this agent? Your suggestion can be about the interaction design, the prompt engineering, the scope, the equity analysis, or anything else.***   
***You could also suggest a new feature or a pivot in the problem the agent is trying to address.***

 

Grace \- don’t ask for name at the start

Matthew \- make sure tone doesn’t feel like it’s chastising user

Victoria \- add tech tips for less tech-literate users, make the agent more explicit at the start of the conversation about what teaching style is being used


# 

