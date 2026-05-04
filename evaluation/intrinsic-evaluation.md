### TODO: Please fill in your intrinsic evaluation design here.

- Metric 1: Front-Loading Discipline

Question Discipline

- How it's computed: Count the number of question marks in the agent's turn.
- What it hopes to reflect: Whether the agent is asking multiple questions at the user in a single turn rather than asking one focused question at a time.

Pre-Pause Length

- How it's computed: Count the number of sentences the agent sends before its first question mark.(it passes if <= 4)
- What it hopes to reflect: Whether the agent is front loading too much content before inviting the user in.

- Metric 2: Answer first Adherence
  - How it's computed: Using LLM-as-a-judge to check if the user's previous question was a direct question(Requiring a yes/no). Only the yes tturned as scored and on those turns, the judge evaluates whether the agent answered the question before steering toward anything else.
  - What it hopes to reflect: Whether the agent actually addresses what the user asked before redirecting

Then provide a link to a branch on your project's github repository with your implmentation of these metrics.

Note that if you find it challenging to complete this coding part, filling in this section will still allow you to earn partial credit.
