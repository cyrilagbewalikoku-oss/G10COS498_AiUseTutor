# Merrill + Bloom: How SAGE Applies Them

SAGE's pedagogy rests on two established frameworks. This file is the one-page digest.

## Merrill's First Principles of Instruction

Merrill (2002) identified five principles common to effective instructional designs:

1. **Problem-centered** — learning is most effective when anchored to a real problem the learner cares about.
2. **Activation** — new knowledge connects to existing knowledge; surface what the learner already knows first.
3. **Demonstration** — show worked examples (both good and bad) before asking the learner to perform.
4. **Application** — let the learner practice, with feedback.
5. **Integration** — help the learner reflect on the new skill and plan how to apply it.

### How SAGE embodies each

| Principle | SAGE mechanism |
|---|---|
| Problem-centered | Scenarios are contextualized to the learner's course or role (`data/users/*.json` → `courseEnrollment`, `role`) |
| Activation | `onboarding` calibration surfaces prior knowledge before any teaching; `session-start` reads the profile at every session |
| Demonstration | `bad-agent-simulator` shows flawed AI use; `examples/interactions/positive/` shows good |
| Application | All four practice types in `scenario-runner`; also `prompt-lab`, `improve-interaction` |
| Integration | `reflection-facilitator` closing question; `weekly-review` pattern-naming across multiple interactions |

## Bloom's Revised Taxonomy

Anderson & Krathwohl (2001) revised Bloom's original taxonomy to a hierarchy of cognitive processes:

1. Remember
2. Understand
3. Apply
4. Analyze
5. Evaluate
6. Create

### How SAGE maps this to skill levels

| Skill level | Target cognitive processes | Typical practice |
|---|---|---|
| Novice | Remember, Understand | Define, recognize, match terms to examples |
| Practitioner | Apply, Analyze | Use CRAFT, evaluate outputs with a rubric |
| Advanced | Analyze, Evaluate | Debug agent behavior, design workflows with human checkpoints |
| Critical Thinker | Evaluate, Create | Critique frameworks, author policy, teach others |

`difficulty-adapter` enforces this mapping — it won't ask a Novice to design a workflow, and won't waste an Advanced learner's time on recognition quizzes.

## Why both, not one

Merrill gives the *structure* of a good lesson (problem → activation → demo → apply → integrate). Bloom gives the *altitude* of the thinking a lesson targets (remember vs. evaluate). SAGE needs both: a Merrill-structured lesson at the wrong Bloom altitude is still wrong; a Bloom-calibrated task outside a Merrill structure is floating exercises.

## Selected grounding

- Merrill, M. D. (2002). "First Principles of Instruction." *Educational Technology Research and Development*, 50(3), 43–59.
- Anderson, L. W., & Krathwohl, D. R. (Eds.) (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives.*
- Clark, R. C., & Mayer, R. E. (2016). *e-Learning and the Science of Instruction* — empirical evidence for worked examples, cognitive load management, and feedback timing.
