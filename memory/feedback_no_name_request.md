---
name: SAGE never asks for the learner's name
description: Onboarding and session-start flows in this SAGE tutor must not ask the learner to provide a name; other profile questions are fine
type: feedback
---

SAGE (the tutor agent in this repo) must NOT ask the learner for their name during onboarding or any other flow. Other personalization questions (role, experience, goals, course context) are still welcome.

**Why**: Learner feedback documented in `04-21-2026/Outstanding Feedback.md` and `04-21-2026/Summarized Feedback.md` flagged the up-front name request as uncomfortable and intrusive ("It felt really uncomfortable when the AI asked for my name, which is personal information to me, when I was just expecting an answer to my prompt."). Grace's one-line iteration priority was literally "don't ask for name at the start."

**How to apply**: When editing `.claude/skills/onboarding/`, `.claude/skills/session-start.md`, `.claude/skills/session-router/`, `data/schemas/user-profile.schema.json`, or any new skill that touches identification/greeting:
- Never include "What's your name?" or equivalent prompts.
- `name` in the user-profile schema is OPTIONAL — populated only if the learner volunteers one.
- For greetings: use a stored name only if one already exists in the profile; otherwise greet without one ("Welcome back!", "Hey!").
- For profile-file disambiguation, use a numeric suffix (`novice-student-2.json`), never a first name.
- Other onboarding questions (role, experience, goals, risk awareness) remain in scope — this rule is specific to *name*.
