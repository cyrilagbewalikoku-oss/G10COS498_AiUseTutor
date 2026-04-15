**COS 598/498: Generative AI Agents**

Agent Project Specification

Spring 2026  ·  University of Maine

# **Problem areas/descriptions were here [S26 AI Agent Opportunities/Problems](https://docs.google.com/document/d/1mmWxHxQtCEhV4APu-prWK_4jB0cprM6J9aZNUjZ9bN0/edit?tab=t.0)**

# **Project teams are listed here: [S26 Project Groups and Problem/Agent topics:](https://docs.google.com/document/d/16kzbBXP7A9md9a0KPnyYSwwEJI9F7ROgyYMhRXEx8YQ/edit?tab=t.0) and are by reflection group** 

| Team | Problem/area  |
| :---- | :---- |
| **Group 1** | **Neurodiversity Support Agent** |
| **Group 2** | **Goal-Aligned Education Agent** |
| **Group 3** | **Ethical Career Agent** |
| **Group 4** | **Neurodiversity Support Agent** |
| **Group 6** | **Personal AI Reflection Agent** |
| **Group 7** | **Collaborative Learning Agent** |
| **Group 9** | **Collaborative Learning Agent** |
| **Group 10** | **AI Use Tutor** |

# **Overview**

In this project, your team will design, prototype, and evaluate an AI agent that lives on the CollaborAITE platform. CollaborAITE is designed to facilitate learning and using AI within a group and class learning context, similar to how Slack or Discord works, except you can also use AI and that use shows up in channels, which makes it easy to share, discuss, and reflect on AI use and how to do it better.

Learners/users will interact with your agent by @mentioning it in channels, providing documents and context, and engaging in multi-turn dialogue.

Your agent will be deployed and usable both for the class and for another class on the CollaborAITE platform, and the tools/data provided by that platform includes:

1. User-uploaded and other class documents in a RAG database 

   1. Can include anything uploaded by the user  
   2. Will have class slides, activities, conversations in channels, group information  
   3. All AI use on CollaborAITE happens within a channel, so your agent can also access prior AI interactions/history from users  
   4. Will have information you request from the user (in a user profile “document”)  
   5. Will have, if the students/users choose to share them:   
      1. prior assignments including reading assignments, writing assignments  
      2. student reflections over time  
      3. anonymized class session transcripts  
2. Tools:  
   1. Web search (similar to prior assignments)  
   2. Asking the user for input  
   3. Run a sub-agent with a prompt and any data you give it

Thus, the users will be able to @\<your-AI-agent\> and provide data and prompt/input and do multiple rounds of interaction/dialogue. There will also be a way to display a plan to the user and separate doing each step of the plan (e.g. by organizing/showing the user each a step inside a thread).

Beyond that, users can also provide other data source or information about themselves, your agent can use tools you write (such as web search, etc), etc.

After making your specification (not a part of this assignment), your team will make a prototype of your agent using Claude Code and using Claude Code to help write skills for your agent, edit the skills, refine them, then prompt Claude Code. You will then evaluate your agent prototype by yourself and with users, get feedback, and redesign/refine their design. 

**Your group should contain 3–5 people.**

Your specification should answer five core questions, each corresponding to a section of this document. The instructor will provide you with a mostly-completed draft problem specification to choose from. Your job is to refine that problem statement and complete the remaining sections.

| The Five Core Questions |
| :---- |
| **1\. The Problem:** What are you trying to do? **2\. Why Bother:** Why is this problem important, and why should we care about solving it? **3\. Status Quo:** What are the current solutions and why do they fail? **4\. Your Proposed Agent:** If you had a solution, what would it look like? **5\. Evaluation / Metrics of Success:** How do you know if you solved the problem? |

| This assignment schedule / steps |
| :---- |
| **During class April 9:** Complete a draft of your project specification. Refine the instructor-provided problem statement and fill in all sections below. **Before Class on April 14:** Build a working initial version of your project agent using Claude Code as development and design assistance. You can use the Claude Agents SDK for your project to lowe the technical difficulty (and the flexibility) or use Smolagents or DSPy. (E.G.) Claude Code writes agent skills for CollaborAITE; you edit and refine them. Feel free to use external tools ([https://langfuse.com/](https://langfuse.com/))  **In Class on April 14:** Troubleshooting this process; “open office hours”  **before on April 16:** They use your working v1 agents and give feedback Mini-evaluation with 2–3 real learners/users on CollaborAITE or via the web or other way you have for them to use your agent.  **In class on April 16:** You process their feedback, revise your project specification, then iterate and build v2 over the weekend We will also cover security no no’s and the danger trifecta: Access to the internet (uncontrolled sources) Running prompts or code Access to secured/reviewed and validated data that needs to remain private **Before Class on April 21:** Build a working version 2 of your project agent using Claude Code as development and design assistance. …. **In Class on April 21** Troubleshooting this process; “open office hours” ; cover evaluation stuff Designing better evaluation / targeted tasks  **On April 23:** They use your working v2 agents and give feedkack Mini-evaluation with 2–3 real learners/users on CollaborAITE. Observe, collect feedback, document what you learned. Revise your specification. **On April 23:** You process their feedback, revise your project specification, then iterate and build v2 over the weekend **April 28** \- reflect on this process, evaluation based on the data and usage data you have, and write some evaluation report, what to iterate on next, deicsion/recommendation on whether this agent should exist and be deployed **April 30** \- Open careers and other discussion for revising/improving this course  |

| Deliverables |
| :---- |
| Completed project specification (this document) Working prototype deployed on CollaborAITE (agent responds to @mentions) Design workshop feedback summary (1 page) Mini-evaluation report: what happened, what you learned, what you’d change (1–2 pages) Revised specification reflecting post-evaluation insights |

# **1\. The Problem**

*What are you trying to do?*

| Problem Statement Template |
| :---- |
| **Step 1 — State the problem.** Describe a learning challenge that exists. Use one of these frames: (a) This bad thing happens in learning contexts (b) This good thing could happen for learners/users but doesn’t (c) This good thing should happen more in education **Step 2 — Concrete example.** Provide a specific, grounded example. Who is affected? What does it look like in practice? **Step 3 — Prior solutions.** Describe 1–2 existing approaches (tools, pedagogies, platforms) that partially address this problem. **Step 4 — Gap in prior solutions.** Explain what root cause or dimension of the problem prior solutions fail to address. Use one of these frames: Prior solutions don’t address this root cause Prior solutions don’t address this cause well because these reasons Prior solutions don’t address these multiple causes together **Step 5 — Design question.** How might an AI agent with access to learning context and conversational interaction provide learners with intentional practice, immediate contextualized feedback and guided reflection on their AI use, hence closing the gap between AI literacy and critical and ethical AI use? |

| Important: No Solutions in the Problem |
| :---- |
| **Your problem statement should not refer to a solution.** Saying “a tool that does X doesn’t exist” is not a problem statement. That’s like motivating the need for Instagram by saying “The world is broken because it doesn’t have Instagram.” The problem motivating Instagram would be something like: “People love sharing photos, but all existing solutions for sharing them involve clumsy, impersonal file sharing.” |

**Example Problem Statement**

*The internet and social media platforms are often used as platforms to advance racist causes and racist hate speech. For example, Facebook’s most widely shared content are regularly the perspectives of racist commentators, and Twitter is often a place where Black Americans are harassed and bullied by white supremacists. Some social media platforms offer modest ways of mitigating the harm of racist speech, such as blocking people on Twitter or muting particular news sources, but these designs do little to eradicate racism itself. Within the constraints of the United States’ First Amendment, how can the internet become a place that not only prevents the spread of racist ideas, but also helps the people that believe those ideas overcome their racist bias?*

**Your Problem Statement**

Students and professionals are increasingly expected to work with AI and it is expected of them to know how to formulate effective requests, evaluate outputs for accuracy and bias, recognize ethical boundaries, and reflect on when and why to use (or not use) these tools. Learners adopt generative AI tools through informal trial and error, developing fragile and often counterproductive habits: accepting outputs uncritically, using vague or poorly structured prompts, failing to verify claims, and lacking any framework for reasoning about the ethical dimensions of their AI use.

# **2\. Why Bother**

*Why is this problem important, and why should we care about solving it?*

Go beyond the problem statement to make a case for why this problem matters. Who is affected and how many? What are the consequences if the problem continues unsolved? Why is now the right time to address it, given what AI agents can do on a platform like CollaborAITE?

| Guiding Questions |
| :---- |
| **Scale:** How many learners/users experience this problem? In what contexts (courses, levels, institutions)? **Consequences:** What happens when this problem goes unaddressed? What do learners/users lose? **Equity dimension:** Does this problem disproportionately affect certain learners/users? Which ones and why? **Timeliness:** Why is an AI agent well-positioned to help now? What about CollaborAITE’s data and interaction model makes this tractable? |

**Your Motivation**

AI is rapidly becoming standard tools in software development, data science, writing, and research. A 2025 CSU system-wide survey of over 80,000 students found that nearly every student has used AI tools, yet most do not trust the results and want more training. The 2025 HEPI/Kortext survey found persistent gaps between students' desire for AI competence and the institutional support available to develop it. Research across multiple countries identifies similar patterns: high adoption, low literacy, minimal structured training.

If this goes unchecked, there will be an influx of graduates who cannot evaluate AI output, articulate when AI use is appropriate, or adapt their approach as tools change and are poorly prepared for a labor market where AI fluency is rapidly becoming a baseline expectation. Furthermore, this affects their reasoning about bias, privacy and ethical issues around the use of AI. The consequences of this are uneven, given the fact that digital divides in AI use/competency across gender,  and socioeconomic status especially among women of lower-income backgrounds are consistently less familiar and confident in using AI tools.

Collaboraite's infrastructure sets the right background for sage because it makes AI use shared and the user’s activity observable, it can reference real interactions that occurred in a learning community, surface patterns across a cohort's AI use, and facilitate peer-informed reflection.

# **3\. Status Quo**

*What are the current solutions and why do they fail?*

Run a deep research report to help you analyze existing solutions (tools, strategies, platforms, pedagogical approaches) that attempt to address the problem. For each, explain what it does, how learners/users interact with it, and where it falls short.

| Prior Solution Template (repeat for 2–3 solutions) |
| :---- |
| **Solution name and type** Overview paragraph: What is this solution? How does it work? **How learners/users currently use it** A task flow diagram or step-by-step description of what the learner does with this solution. (If using a diagram, provide a link to an editable version.) **Where it falls short** What root cause does this solution not address? What about the user/learner experience and human-AI coordination is unsatisfying or problematic? **How your agent will differ** A short paragraph on what your agent does differently and why that matters. |

**Prior Solution Category 1 (with at least one concrete example of prior solution in this category)**

University-designed AI literacy modules (e.g., Stanford's AI Literacy Framework modules, University of Florida's "AI Across the Curriculum" certificate program), Udemy's "Agentic AI Mastery" and Coursera's prompt engineering courses offer structured video content with coding demonstrations. Learners watch instructors use AI agents and complete exercises afterward.

**How Learners Use It**

* Watch video lecture (30-60 minutes)  
* Follow along with provided code/exercises  
* Complete quiz or project for certificate  
* Return to videos for reference

**Where It Falls Short**

* Passive learning: Watching someone else succeed doesn't build learner judgment  
* No real-time feedback: Can't ask "why did that work?" or "what if I tried this?"  
* Generic scenarios: Exercises don't match the learner's actual context or challenges  
* Ethics as add-on: Responsible AI covered in separate modules, not integrated into practice

**How Sage Differs**

Sage provides structured feedback on specific learner attempts, explanations of underlying principles (not just techniques), and prompts for ethical and metacognitive reflection. It adapts to the learner's actual context (course materials, prior attempts) and weaves ethical considerations into every exercise

**Prior Solution Category 2 (with at least one concrete example of prior solution in this category)**

\[Fill in\]

YouTube prompt engineering tutorials, Reddit communities (r/ChatGPT, r/PromptEngineering), peer advice in Discord/Slack channels. These are informal, community-driven knowledge-sharing mechanisms where learners observe others' techniques and adopt them through imitation.

**How Learners Use It**

* Learners encounter a problem and search for advice, find a “tip” and use that.  
* They are driven by immediate need so it's unstructured.  
* There is no form of assessment or formal knowledge grounding for the reason for using a technique or “tip”

**Where It Falls Short**

* The learning process is fragmented and lacks metacognitive depth.  
* Learners collect trips and tricks without understanding the principles.  
* They receive no feedback on their specific attempts, cannot distinguish between effective and ineffective adaptations.  
* They are usually not prompted to consider the ethical aspect of their AI use.

**How Sage Differs**

It will provide structured feedback to the learner, explaining the underlying principle behind the technique. It will also nudge the learner to reflect on the ethical aspects of their AI use.

**Prior Solution Category: Existing AI Agents (with at least one concrete example of prior solution in this category)**

AI tutoring agents such as **Khanmigo (Khan Academy), Flint K-12, and Georgia Tech's Jill Watson**. These are AI-powered conversational agents designed to tutor students in academic subjects like math, reading, computer science, course logistics by guiding learners through problems rather than giving answers directly.

**How learners Use It**

* Students interact with the Chatbot for help on a purely academic problem and the agent guides them step-by-step towards the answer without giving them the direct answer.  
* These agents tutor in particular subjects and not how to use AI itself.

**Where It Falls Short**

* They are not designed to make AI use the object of learning.  
* They do not teach students to evaluate their outputs, prompt engineering or recognize when AI use is appropriate. 

**How Sage Differs**  
Sage will use Ai use its subject of tutoring. It will practise scenarios where the learner interacts with the AI and then gets feedback from the AI on their approach.

# **4\. Your Proposed Agent**

*If you had a solution, what would it look like?*

| Agent Name | SAGE |
| :---- | :---- |

| Description | An agent that tutors learners in the critical, effective and ethical use of AI tools. |
| :---- | :---- |

| Team Name | *Your team’s name* |
| :---- | :---- |

| Team Members | Elvis, Gabriel, Gregory, Cyril |
| :---- | :---- |

## **4a. Agent Summary**

Write a summary paragraph describing the core functionality your agent provides. What does it do for learners/users? What’s the core loop of interaction? For each root cause or gap identified in your problem statement, include a paragraph on how the agent specifically addresses it. Be concrete about mechanisms/specific features and interactions that better address those root causes/gaps.

Sage is a conversational AI agent on CollaborAITE that tutors learners in the critical, effective, and ethical use of AI tools. SAGE operates through a hybrid deployment model: learners are **required** to engage in brief weekly reflection sessions where SAGE reviews their recent AI use in a conversational, low-pressure dialogue; additionally, SAGE surfaces **subtle contextual nudges** while learners work with AI in CollaborAITE channels — gentle, non-invasive prompts (like a sidebar suggestion) that offer a teachable moment tied to what the learner is already doing, which the learner can engage with or dismiss. This means SAGE comes to the learner at the right moment rather than relying on learners to seek out extra practice on their own.

> **v2 (CLI) adaptation:** In the current Claude Code CLI build, SAGE does not observe channels and does not fire scheduled prompts. The "contextual nudge" path is reframed as an explicit `/improve-interaction` command where the learner pastes an AI interaction they had elsewhere; the "weekly reflection" path is reframed as a `/weekly-review` command the learner invokes themselves. The pedagogy (ACKNOWLEDGE → NUDGE → EXPLAIN, single closing reflection) is identical; only the trigger mechanism differs. See §4g.

Rather than presenting abstract exercises, the agent takes the kinds of AI interactions learners are genuinely attempting and turns them into structured learning moments. When a learner completes a practice attempt, the agent does not deliver a wall of feedback all at once. Instead, it scaffolds its response: it might first highlight what the learner did, then ask a brief nudging question — "What do you think the model is actually doing when you ask it for sources?" — that pushes the learner to reflect on their own reasoning before the agent explains the stronger approach. This mid-task reflection is woven naturally into the conversation, not flagged as a separate "reflection step," so the learner experiences it as a dialogue rather than an evaluation.

This design addresses three gaps simultaneously. The scenario-based practice gives learners the deliberate, repeated attempts that standalone literacy workshops lack. The scaffolded feedback — delivered in precise, well-paced turns that interleave explanation with nudges toward self-examination — replaces the total absence of feedback in informal learning-by-doing. This scaffolding is grounded in the **"Learner Predicts"** pedagogical pattern and the related concept of **cognitive conflict**: the agent asks learners to predict or reason about what will happen before revealing the stronger approach, creating a productive gap between expectation and reality that deepens understanding. And the embedded reflection, where the agent guides learners to reconsider their own choices mid-conversation, builds the metacognitive habits that neither prior approach cultivates. At the close of each session, the agent offers a light, culminating reflection prompt — a single question that asks the learner to step back and notice a pattern in their thinking or connect what they practiced to their broader coursework. The result is a compact interaction that teaches, prods, and deepens understanding without exhausting the learner through excessive back-and-forth.

## **4b. Data Sources**

Your agent lives on CollaborAITE and has access to a RAG knowledge base (in addition to other RAG databases or other data sources you add). Describe which data sources your agent uses, what it extracts or infers from each, and how that data helps address the problem’s root cause.

| CollaborAITE Data Sources |
| :---- |
| Check and describe each data source your agent will use: **Class slides and activities:** The agent reads course slides and activity descriptions to contextualize practice scenarios. If a learner is in a research methods course, scenarios will reference research tasks rather than generic examples. This ensures practice is relevant to the learner's actual academic context. *v2 CLI: not available — learner can describe their course verbally or attach a document at interaction time.* **Channel conversations (these may/do include AI queries):** The agent can reference anonymized patterns in channel AI use to inform scenario design and group-level reflection prompts. It does not surface or quote individual students' AI queries to other students. *v2 CLI: not available — learner can paste an AI interaction transcript via `/improve-interaction`.* **User profile information:** Course enrollment, discipline, skill level, goals, and prior practice history. Used to tailor vocabulary and pick appropriately challenging scenarios. *v2 CLI: stored as local JSON in `data/users/` on first session and read back on subsequent sessions.* **User-uploaded documents:** Material the learner drops into the session (a paper they are writing, an assignment prompt, a transcript of an AI interaction). Used as the object of practice. *v2 CLI: fully supported — the learner pastes or references local files.*  **May not be provided by the system / platform (CollaborAITE):**  **Prior assignments and reflections:** The agent accesses the requesting learner's own prior reflections and practice history with the agent to track progress, avoid repetition, and scaffold increasingly complex challenges. It does not access other students' assignments or reflections. *v2 CLI: limited to what SAGE itself writes to the learner's local profile.* **Anonymized session transcripts:** The agent uses anonymized transcripts of past agent interactions (stripped of identifying information) as example material: "Here is an anonymized interaction where a student asked an AI for help with X. What would you do differently?" This provides authentic practice material without privacy risk. *v2 CLI: not available — fixed curated examples in `examples/interactions/` stand in.*  **Also describe what the agent deliberately does NOT access and why** (privacy-by-design): SAGE does not access other learners' profiles, reflections, or AI interactions (privacy by isolation); does not access content of private channels it has not been invited to; does not exfiltrate any learner data to external services. |
|  |

## **4c. Other Data Sources**

Your agent may benefit from data that is not already part of CollaborAITE’s knowledge base. If your design depends on external information, describe it here. Be specific about what the data is, where it comes from, and how you would get it into the system.

| External Data Source Template (repeat as needed) |
| :---- |
| **Data source name and type:** \[e.g., Stack Overflow Q\&A posts, textbook chapter PDFs, department course catalog, curated research papers, external API data\] **What it contains:** \[Describe the content and structure of this data source\] **Why the agent needs it:** \[What capability or interaction does this data enable that CollaborAITE’s existing data cannot support?\] **How it would be added:** \[Would it be uploaded to the RAG knowledge base? Accessed via an API? Provided by the learner at interaction time? Curated by the instructor?\] **Freshness and maintenance:** \[Is this a one-time upload or does it need regular updates? Who is responsible for keeping it current?\] **Licensing and privacy:** \[Are there copyright, licensing, or privacy considerations? Is the data publicly available or restricted?\] |

**External Data Source: AI Agent Education Research**

**What it contains:** Curated summaries of best practices from AI education research, including common misconceptions, effective scaffolding strategies, and ethical frameworks (e.g., IMPACT audit).

**Why needed:** Provides Sage with pedagogical grounding beyond the CollaborAITE course materials.

**How added:** Uploaded to RAG knowledge base by instructor/developers.

**Maintenance:** Updated each semester based on new research and course feedback.

**Licensing:** Open educational resources and original summaries of research.

No real-time external API calls are required. All external content is pre-curated and loaded into the RAG database, minimizing latency, dependency risk, and data exposure.

## **4d. Human-Agent Collaboration Flow**

Create a task flow diagram showing the full interaction cycle between the learner and your agent. The diagram should show:

* **What the user/learner does:** initiating the interaction, providing context, reviewing agent output, giving feedback

* **What the agent does:** retrieving data from the RAG knowledge base, generating responses, presenting plans in threads, asking clarifying questions

* **How they collaborate:** multi-turn refinement, learner control points, when the agent uses threaded plan displays, agent transparency about its reasoning

Provide a link to an editable version of this diagram.

INTERACTION CYCLE: SAGE Session

1. SAGE IS TRIGGERED (learner does not need to seek it out)

   Two entry paths on CollaborAITE (target state):

   A) CONTEXTUAL NUDGE (while learner is working):
      Learner is using AI in a CollaborAITE channel for coursework.
      SAGE observes the interaction and surfaces a subtle, non-invasive
      sidebar suggestion such as: "I noticed you asked the AI for sources —
      I could help you get better results from that kind of request. Want
      to try?" Learner can engage or dismiss.

      *v2 CLI adaptation:* learner explicitly invokes `/improve-interaction`
      and pastes a prompt (or prompt + AI response) they had elsewhere.
      SAGE applies the same scaffolded coaching to the pasted content.

   B) SCHEDULED REFLECTION (required, but conversational):
      At set intervals (e.g., weekly), SAGE prompts the learner to reflect
      on their recent AI use as a course requirement. Warm, short (5–10
      min), 2–3 focused questions. Tone is peer, not professor.

      *v2 CLI adaptation:* learner invokes `/weekly-review` and pastes or
      describes 2–3 recent AI interactions. SAGE walks them through the
      same reflection flow. Scheduling is on the learner; everything else
      is identical.

2. AGENT ASSESSES CONTEXT
   Agent checks:
     - Learner's course enrollment and discipline (user profile)
     - Learner's prior practice history (past interactions with agent)
     - Current course topics (class slides/activities — CollaborAITE only)
     - Competencies not yet practiced (competency framework mapping)

   Based on the trigger type and learner context, the session branches
   into one of three paths:

3. SESSION BRANCHES INTO ONE OF THREE PATHS

   PATH A — IMPROVE THIS INTERACTION (from contextual nudge / `/improve-interaction`):
     SAGE noticed something in the learner's AI use and helps them do it
     better — rewriting a prompt, evaluating an output they received, or
     recognizing when AI isn't the right tool for the task.

   PATH B — STRUCTURED PRACTICE SCENARIO (from either trigger / `/scenario-runner`):
     SAGE presents a practice scenario drawn from course context.
     Scenario types:
       - PROMPT CRAFTING: Learner writes a prompt for a described task
       - OUTPUT EVALUATION: Learner receives a real or simulated AI output
         (which may include deliberately inserted errors) and must identify
         strengths, weaknesses, errors, or biases
       - APPROPRIATENESS JUDGMENT: Learner is given a task context and must
         decide whether/how AI should be used, with justification
       - WORKFLOW DESIGN: Learner describes a multi-step process for
         completing a task that involves AI at some steps
     CONTROL POINT: Agent presents scenario and asks learner to confirm
     or request a different focus area.

   PATH C — REFLECT ON RECENT AI USE (from scheduled reflection / `/weekly-review`):
     SAGE walks the learner through reviewing their AI interactions from
     the past week — what went well, what patterns they notice, what
     they'd do differently.

4. AGENT SCAFFOLDS FEEDBACK WITH EMBEDDED REFLECTION (all paths converge)
   Agent does NOT dump all feedback at once. Instead it sequences the
   response across a few precise turns:
     - ACKNOWLEDGE: name what the learner did, specifically
     - NUDGE (Learner Predicts): pose a brief question that pushes the
       learner to predict or reason about what will happen BEFORE hearing
       the explanation (e.g., "What do you think happens when the model
       gets this kind of request?")
     - LEARNER RESPONDS to the nudge — thinking through their own logic
     - EXPLAIN: build on the learner's reflection to explain the stronger
       approach, connecting to a transferable principle
   Mid-task reflection feels like natural dialogue, not a quiz step.
   CONTROL POINT: learner can ask follow-up, challenge the feedback, or
   redirect.

5. LIGHT CLOSING REFLECTION
   One brief question that guides the learner to notice a pattern in
   their thinking or connect the practice to their broader coursework.
   Lightweight by design — learner responds or defers.

6. AGENT UPDATES LEARNER PROGRESS
   Logs competencies practiced, performance level, mid-task reflection
   responses, scenario difficulty. Next session draws on this history.
   *v2 CLI: written to the learner's local profile JSON in `data/users/`.*

CYCLE REPEATS — next session is triggered by SAGE on CollaborAITE
(contextual nudge or scheduled reflection); in v2 CLI, the learner
invokes the relevant command.

## **4e. Example Interactions**

Write 2–3 example @agent conversations showing realistic multi-turn exchanges on CollaborAITE. These should demonstrate different use cases or learner needs.

| Interaction Template (repeat 2–3×) |
| :---- |
| **Scenario title:** A short name for this use case **Learner context:** What class is the learner in? What are they working on? What just happened? **Conversation:**     @learner: \[what the learner types, including any documents or context they attach\]     @YourAgent: \[agent response, noting any plan steps displayed in threads\]     @learner: \[follow-up or feedback\]     @YourAgent: \[refined response\] **Data sources used:** Which RAG data did the agent draw on? |

**Interaction 1**

Learner: @SAGE I want to practice using AI better. I'm in SOC 101 and we have a paper due.

SAGE: Welcome\! Let's start with something tied to your SOC 101 context. Here's the situation:

You're writing a short paper on social media's effects on adolescent well-being. You want to find relevant academic sources. You're about to ask an AI chatbot for help.

Write the prompt you would use — just type it here as if you were talking to the AI.

Learner: Find me 5 academic sources about social media effects on teen mental health published after 2020\.

SAGE: Okay, I can see what you're going for — you added a topic, a number, a type, and a date range. That's more structured than many first attempts. But let me ask you something before I go further: what do you think the model is actually doing when it gets a request like "find me 5 academic sources"? Is it searching a database?

Learner: I guess I assumed it was looking things up somewhere. But now that you ask… I think it's just generating text that looks like citations?

SAGE: That's exactly right — and the fact that you caught that distinction is important. Language models generate plausible-sounding text, including plausible-sounding citations. They don't search databases. So when you ask for "5 academic sources," you're likely to get a mix of real and fabricated references that all look legitimate. A stronger approach would be to use the model for what it does well: generating search terms and strategies. Something like: "Suggest 5 search term combinations I could use in Google Scholar or PsycINFO for a paper on social media and adolescent well-being, and explain why each might surface different types of results." That keeps you in the verification loop — the AI helps you search, but you verify what you find.

Light closing reflection: One quick thing to carry with you: in what other assignments have you asked AI to produce information you then used without checking? What made it feel safe to trust it?

**Interaction 2**

Learner: @SAGE Ready for another challenge. Something harder this time.

SAGE: You've been solid on prompt crafting. Let's try output evaluation. Here's an anonymized interaction from this platform. A student in a CS course asked an AI:

"Explain the difference between breadth-first search and depth-first search, including time complexity."

The AI responded:

"BFS explores nodes level by level using a queue. Its time complexity is O(V+E). DFS explores as deep as possible along each branch using a stack. Its time complexity is O(V+E). BFS is always better for finding the shortest path. DFS uses less memory because it only stores the current path."

Evaluate this output. What is accurate, what is misleading or wrong, and what is missing?

Learner: The time complexities are right for both. The part about BFS being "always better" for shortest path is wrong—that's only true for unweighted graphs. And saying DFS "uses less memory" is an oversimplification. DFS can use less memory in some cases but for a graph with long paths it could use a lot. The response also doesn't mention that BFS has O(V) space complexity vs DFS which varies.

SAGE: You caught the key factual issues — the "always better" overstatement and the memory oversimplification. Those are exactly the kind of confident-but-incomplete claims AI outputs frequently contain. Now, look at the response one more time as a whole. You evaluated the individual statements — but what about the structure? What impression does the overall framing give a reader who doesn't already know this material?

Learner: Hmm, I think it makes it seem like BFS and DFS are interchangeable tools that you'd just pick one or the other based on simple tradeoffs. It doesn't get at the fact that the choice depends heavily on the problem structure — like whether you need shortest path, or whether the graph is deep vs. wide.

SAGE: That's a sharp observation. What you just identified is a pattern worth naming: AI outputs that are locally accurate but globally misleading — each sentence roughly checks out, but the overall framing creates a flattened, false impression. In technical domains this is especially dangerous because it looks authoritative. The habit of stepping back and asking "what impression does this as a whole give someone who doesn't know the material?" is one of the most transferable evaluation skills you can build.

Light closing reflection: You moved from fact-checking individual claims to evaluating the overall framing just now. When you've used AI for technical explanations in the past, which of those two levels did you tend to check — and what would it take to make the framing check a default habit?

**Interaction 3 (optional)**

\[Write your third example interaction here\]

## **4f. Harm Considerations**

AI agents in learning contexts can cause real harm. Consider your agent’s specific domain and identify the most serious risks.

| Harm Dimensions to Consider |
| :---- |
| **Accuracy harms:** Could the agent give wrong information? Hallucinate sources? Misrepresent course content? **Equity harms:** Could the agent work better for some learners/users than others? Whose language, culture, or learning style might it fail to serve? **Agency harms:** Could the agent make learners/users passive? Undermine their metacognition? Do the thinking for them? **Privacy harms:** The agent accesses learner reflections, conversations, and assignments. What could go wrong? **Trust harms:** Could learners/users over-trust or under-trust the agent? What happens when it’s wrong? |

For your agent, describe the 2–3 most serious potential harms and how your design mitigates each:

| Potential Harm | Likelihood | Design Safeguard | What If It Fails? |
| :---- | :---- | :---- | :---- |
| Learners may treat SAGE's feedback as the authoritative last word on what constitutes "good" AI use | High | SAGE's scaffolded feedback style inherently mitigates this risk: by nudging learners to articulate their own reasoning before the agent explains | If we notice from the logs that students are mostly ignoring the reflection questions, we might add a "challenge the agent" exercise where learners must identify weaknesses in SAGE's own reasoning. |
| Students with more prior AI experience may benefit more from the agent (they have more to build on), while students with less experience may find practice scenarios intimidating or alienating | Medium | We first included a low stakes orientation to the learner and also the scenario difficulty begins at a deliberately accessible level for all learners, and the agent adjusts upward based on demonstrated competence rather than assumed background | In cases where we see lower engagement from first time users, the team will conduct targeted feedback sessions with low-engagement learners to understand barriers and will redesign onboarding scenarios accordingly. |
| **v2 CLI evaluation under-represents the full system:** evaluators using the Claude Code CLI build will not see contextual sidebar nudges, scheduled weekly reflections, or channel-pattern retrieval — and may conclude SAGE is less engaging than it is designed to be on CollaborAITE. | Medium | Evaluators are briefed before the session on which paths are adapted for CLI (paste-based Path A, manually-invoked Path C) and which are deferred to CollaborAITE deployment. The underlying pedagogy (ACKNOWLEDGE → NUDGE → EXPLAIN, Learner Predicts, single closing reflection) is identical across both deployments and is what the evaluation targets. | If evaluators still report that the prototype feels passive or hard to discover, we will add CLI-friendly affordances — e.g., a session-start menu that surfaces the three paths — before v3. |

## **4g. Deployment Model (v2 CLI vs. Target State)**

SAGE is designed for CollaborAITE but is evaluated in v2 on the Claude Code CLI. This section names what is present in each deployment so that readers (and evaluators) can tell the two apart.

| Capability | v2 (Claude Code CLI) | Target (CollaborAITE) |
| :---- | :---- | :---- |
| **Invocation** | Learner runs the CLI and invokes skills (`/onboarding`, `/scenario-runner`, `/improve-interaction`, `/weekly-review`) | Learner @mentions SAGE in a channel; SAGE also proactively nudges |
| **Contextual nudges (Path A)** | Learner pastes an AI interaction via `/improve-interaction` | SAGE surfaces a sidebar suggestion when it sees a teachable moment in the learner's channel AI use |
| **Weekly reflection (Path C)** | Learner runs `/weekly-review` when they choose to | SAGE sends a scheduled prompt on a weekly cadence |
| **Practice scenarios (Path B)** | Fully supported | Fully supported |
| **Course slides / materials RAG** | Learner describes course or attaches a document | Retrieved automatically from CollaborAITE |
| **Channel conversation retrieval** | Not available; learner pastes transcripts | Retrieved (anonymized peer patterns + learner's own history) |
| **Learner profile persistence** | Local JSON in `data/users/` | CollaborAITE data layer |
| **Anonymized cohort examples** | Fixed curated examples in `examples/interactions/` | Pulled from anonymized channel corpora |

The pedagogy — ACKNOWLEDGE → NUDGE → EXPLAIN, Learner Predicts, CRAFT, four practice types, single closing reflection, Merrill + Bloom alignment — is **identical in both deployments**. Only the delivery surface changes. v2 evaluation therefore targets the pedagogy; evaluators should be briefed that the always-on, proactive behaviors of CollaborAITE are deferred.

## **5\. Technical Architecture and Design for the Agent**

* **Scenario Engine** — Selects and parameterizes practice scenarios based on learner context (course, discipline, prior history) and competency coverage. Draws from a scenario template library stored in the RAG database. Uses course slides and activity data to contextualize scenarios. *v2 CLI: scenarios in `data/scenarios/`; course context provided by learner.*
* **Nudge Detector** *(CollaborAITE target; not implemented in v2)* — Monitors the learner's AI interactions in CollaborAITE channels and identifies moments where a subtle contextual nudge would be valuable (e.g., a prompt that could be improved, an output that should be evaluated critically, or a use case where AI may not be appropriate). Surfaces non-invasive sidebar suggestions that the learner can engage with or dismiss. *v2 CLI analog: the `improve-interaction` skill, triggered manually by the learner pasting an interaction.*
* **Scheduled Reflection Trigger** *(CollaborAITE target; not implemented in v2)* — Fires on a weekly cadence to initiate Path C. *v2 CLI analog: the `weekly-review` skill, invoked on-demand by the learner.*
* **Feedback Generator** — Takes the learner's practice attempt as input and produces scaffolded, multi-turn feedback rather than a single block of assessment. Grounded in the **"Learner Predicts"** pedagogical pattern and the concept of **cognitive conflict**: the agent first asks learners to predict or reason about what will happen before revealing the stronger approach, creating a productive gap between expectation and reality. Sequences acknowledgment of what the learner did, a predict-before-reveal nudge, and then a precise explanation connecting to transferable principles. Uses the LLM with structured prompting to ensure each feedback turn is concise and avoids information-dumping.
* **Reflection Prompter** — Generates two types of reflection: mid-task nudging questions (woven into the feedback dialogue, using the Learner Predicts pattern to prompt the learner to think before the agent explains) and light closing reflections (a single question at session end). Draws on the practice type, learner history, and competency focus. Tracks reflection responses for use in future scaffolding.
* **Progress Tracker** — Maintains a per-learner record of competencies practiced, difficulty levels completed, and reflection engagement. Informs the Scenario Engine's selection logic. *v2 CLI: persisted as JSON in `data/users/<learner>.json` on the local filesystem. CollaborAITE target: CollaborAITE's data persistence layer.*
* **Data Access Layer** — Manages retrieval from CollaborAITE data sources (course slides, anonymized channel patterns, user profile, learner's own history) and the RAG database (competency frameworks, misconception catalogs, discipline norms). Enforces privacy constraints: no access to other learners' data, no access to uploaded documents the learner didn't surface. *v2 CLI: reads local `data/` directory only.*
* **Conversation Manager** — Handles multi-turn interaction flow, threading, and control-point logic (scenario confirmation, reflection skip/defer). Built on the Claude Agents SDK's conversation state management.

# **6\. Evaluation / Metrics of Success**

*How do you know if you solved the problem?*

Define what success looks like for your agent. This section guides both your design workshop (Day 5\) and your mini-evaluation with real learners/users (Days 6–7).

## **5a. Success Criteria**

What would need to be true for your agent to have “worked”? Define 2–3 concrete success criteria tied to the problem you identified.

| Success Criteria Template |
| :---- |
| **Criterion 1:** \[e.g., learners/users can identify connections between lecture concepts they didn’t previously see\] **How you’d observe it:** \[e.g., In the evaluation, learners/users articulate at least one new connection after interacting with the agent\] **Criterion 2:** \[e.g., learners/users feel the agent respects their autonomy rather than doing their thinking for them\] **How you’d observe it:** \[e.g., Post-interaction survey question; observe whether learners/users rephrase agent output or copy it directly\] **Criterion 3:** \[e.g., The agent uses RAG data accurately and doesn’t hallucinate course content\] **How you’d observe it:** \[e.g., Manually check 5 agent responses against source materials\] |

### 

| Criterion | Observation Method |
| :---- | :---- |
| Learners produce more specific and critical AI interactions after practice sessions. | Compare learner attempts across sessions using a rubric applied to interaction logs. The rubric scores: specificity of prompts, number and type of issues identified in output evaluation, number of ethical dimensions considered.Transfer: when learners use AI outside of “practice” sessions, \<what happens? Fill this in\> |
| Learners exhibitreport increased metacognitive awareness of their AI use habits. | Pre- and post-engagement survey with open-ended items (e.g., "Describe how you decide whether and how to use AI for an academic task" and "What do you check when evaluating AI output?"). |
| The agent's feedback is perceived as specific, explanatory, and non-prescriptive. | Post-session Likert-scale items: "The feedback was specific to my attempt (not generic)," "The agent's questions helped me think through my own reasoning before it explained," "The feedback felt like it was teaching me to think, not telling me what to think," "The conversation felt like a natural dialogue, not a quiz." Qualitative follow-up: "Can you give an example of a moment in the conversation that was particularly helpful or unhelpful?" |

### 

## **5b. Design Workshop Plan** 

Describe how you will present your agent to peers and collect structured feedback:

* What will you demo or walk through?

* What specific questions will you ask your peers?

* How will you capture and organize the feedback?

We will do this with some colleagues in class and with some friends outside of class who are seniors. We will also try a live walkthrough of one of our practice sessions coupled with one other session where our friends suggest the approach to demonstrate. We will then ask them these questions: 

1. Does the practice scenario feel realistic—like something you'd actually encounter in coursework?  
2. Is the feedback specific enough to be useful? Too specific? About right?  
3. Does the feedback feel like it's building your understanding, or just evaluating you?  
4. What's missing? What would make you want to come back for another session?  
5. Are there scenario types or competency areas we haven't covered that feel important?

## **5c. Mini-Evaluation Plan** 

Describe how you will evaluate your prototype with 2–3 real learners/users on CollaborAITE:

| Mini-Evaluation Plan Template |
| :---- |
| **Participants:** Who will you recruit? From which class? **Task:** What will you ask learners/users to do with the agent? Be specific. **Observation method:** Will you watch live? Review conversation logs? Both? **Feedback collection:** Short interview? Survey? Think-aloud? What questions will you ask? **Analysis:** How will you make sense of what you observe? What are you looking for? |

| Element | Description |
| :---- | :---- |
| **Participants** | 2-3 students from COS 598/498 or another course using CollaborAITE; mix of experience levels (one beginner, one intermediate) |
| **Task** | "Spend 15-20 minutes with Sage learning about AI agents. Try at least 2 exercises and complete one reflection. Think aloud as you work." |
| **Observation method** | Live observation via screen share; recording of interaction logs |
| **Feedback collection** | Short semi-structured interview (10 min): What worked? What was confusing? Would you use this again? What would make it better? |
| **Analysis** | Thematic analysis of interview transcripts; review of interaction logs for completion rates, error patterns, engagement markers |

## **5c. Final Evaluation Plan** 

Describe how you will evaluate your AI Agent with the gathered user interaction logs (chats etc) from using your agent and/or other data and ways of gathering evaluation data.

**Source 1: Interaction log analysis.** All practice sessions from both user testing rounds are analyzed using the competency rubric. The primary question: do learners' practice attempts improve across sessions? Secondary questions: which scenario types produce the most engagement? Where do learners most frequently struggle? Are there patterns in how learners use (or skip) reflection prompts?

**Source 2: Survey and interview data.** Pre/post survey comparisons from the mini-evaluation assess whether engagement with the agent is associated with shifts in self-reported AI use confidence, metacognitive awareness, and critical habits. Interview data is analyzed for themes related to perceived value, barriers, and suggestions.

**Source 3: Feedback quality audit.** A sample of 15–20 agent feedback responses is evaluated by two team members against a quality rubric: Was the feedback specific to the learner's attempt? Did it include an explanation of *why*? Did it connect to a transferable principle? Was it non-prescriptive? This assesses whether the agent is delivering on its core design promise.

