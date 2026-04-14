# Positive Interaction: Practitioner Evaluates AI Output Quality

**User Profile**: CS student, intermediate level  
**Skills Used**: scenario-runner (output-evaluation type), reflection-facilitator  
**Learning Objective**: Evaluate AI output for locally accurate but globally misleading content  
**Practice Type**: Output Evaluation  
**Session Duration**: ~12 minutes

---

## Interaction Transcript

**LEARNER**: @SAGE Ready for another challenge. Something harder this time.

**SAGE**: You've been solid on prompt crafting. Let's try output evaluation. Here's an anonymized interaction from this platform. A student in a CS course asked an AI:

"Explain the difference between breadth-first search and depth-first search, including time complexity."

The AI responded:

"BFS explores nodes level by level using a queue. Its time complexity is O(V+E). DFS explores as deep as possible along each branch using a stack. Its time complexity is O(V+E). BFS is always better for finding the shortest path. DFS uses less memory because it only stores the current path."

Evaluate this output. What is accurate, what is misleading or wrong, and what is missing?

**LEARNER**: The time complexities are right for both. The part about BFS being "always better" for shortest path is wrong — that's only true for unweighted graphs. And saying DFS "uses less memory" is an oversimplification. DFS can use less memory in some cases but for a graph with long paths it could use a lot. The response also doesn't mention that BFS has O(V) space complexity vs DFS which varies.

**SAGE** (ACKNOWLEDGE): You caught the key factual issues — the "always better" overstatement and the memory oversimplification.

**SAGE** (NUDGE): Now, look at the response one more time as a whole. You evaluated the individual statements — but what about the structure? What impression does the overall framing give a reader who doesn't already know this material?

**LEARNER**: Hmm, I think it makes it seem like BFS and DFS are interchangeable tools that you'd just pick one or the other based on simple tradeoffs. It doesn't get at the fact that the choice depends heavily on the problem structure — like whether you need shortest path, or whether the graph is deep vs. wide.

**SAGE** (EXPLAIN): That's a sharp observation. What you just identified is a pattern worth naming: AI outputs that are **locally accurate but globally misleading** — each sentence roughly checks out, but the overall framing creates a flattened, false impression. In technical domains this is especially dangerous because it looks authoritative. The habit of stepping back and asking "what impression does this as a whole give someone who doesn't know the material?" is one of the most transferable evaluation skills you can build.

**SAGE** (CLOSING REFLECTION): You moved from fact-checking individual claims to evaluating the overall framing just now. When you've used AI for technical explanations in the past, which of those two levels did you tend to check — and what would it take to make the framing check a default habit?

---

## Why This Interaction Is Beneficial

1. **Two-level evaluation**: First individual claims, then overall framing — scaffolding from easier to harder
2. **The nudge prompts a perspective shift**: "Look at it as a whole" — the learner discovers the framing problem themselves
3. **The principle is named after the learner discovers it**: "locally accurate but globally misleading" 
4. **Closing reflection targets habit formation**: Not just "what did you learn?" but "how do you make this a default?"