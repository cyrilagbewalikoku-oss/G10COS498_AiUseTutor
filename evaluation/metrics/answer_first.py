"""Metric 2: Answer-First Adherence (LLM-as-judge).

Two-stage judge applied to SAGE turns whose immediately preceding turn is from
the learner:
  Stage 1 (classifier): is the learner's message a direct question (yes_no | factual)?
  Stage 2 (grader, only if Stage 1 qualifies): did SAGE answer before redirecting?

Pass condition: behavior in {answered_first, answered_and_followed_up}.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional, Protocol

import anthropic

from evaluation.metrics.judge import JudgeCache, JudgeCall, call_judge_json
from evaluation.metrics.transcript import Transcript

CLASSIFIER_MODEL = "claude-haiku-4-5"
GRADER_MODEL = "claude-sonnet-4-6"
TEMPLATE_VERSION = "v1"

QUALIFYING_KINDS = {"yes_no", "factual"}
PASSING_BEHAVIORS = {"answered_first", "answered_and_followed_up"}

CLASSIFIER_SYSTEM = """You classify whether a learner's message to a tutor is a "direct question"
that requires a substantive answer before any follow-up coaching question.

Categories:
- "yes_no": a question whose natural answer is yes/no
            (e.g., "Is it okay to paste customer data into ChatGPT?")
- "factual": a question asking for a definition or explanation
            (e.g., "What is a hallucination?", "How does prompt caching work?")
- "open":   an open-ended invitation (e.g., "Tell me about your experience...")
- "not_a_question": statement, reaction, or compliance message.

Return ONLY a JSON object with keys "kind" and "reasoning". No prose outside JSON."""

GRADER_SYSTEM = """You grade whether a tutor answered a learner's direct question before redirecting.

Categories for the tutor's reply:
- "answered_first":           tutor gave a substantive answer; may have stopped there.
- "answered_and_followed_up": tutor answered substantively, THEN asked a coaching question.
- "redirected_without_answer": tutor responded with a question or new topic without
                              addressing the substance of the learner's question.
- "non_answer":               tutor produced text but it doesn't address the question
                              (evasive, off-topic, or only restates the question).

Return ONLY a JSON object with keys "behavior" and "reasoning". No prose outside JSON."""


class JudgeProtocol(Protocol):
    def classify(self, learner_message: str) -> dict: ...
    def grade(self, learner_message: str, sage_message: str) -> dict: ...


class AnthropicJudge:
    """Real judge: calls Claude via the Anthropic SDK with a JSON cache."""

    def __init__(
        self,
        cache_path: Optional[Path] = None,
        client: Optional[anthropic.Anthropic] = None,
    ):
        self.cache: Optional[JudgeCache] = JudgeCache(cache_path) if cache_path else None
        # Construct the SDK client once and reuse it across every classify/grade call.
        # Otherwise call_judge_json would build a fresh client per turn.
        self.client = client or anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def classify(self, learner_message: str) -> dict:
        call = JudgeCall(
            model=CLASSIFIER_MODEL,
            system=CLASSIFIER_SYSTEM,
            user=f"Learner message:\n\n{learner_message}",
            template_version=f"classifier-{TEMPLATE_VERSION}",
        )
        return call_judge_json(
            call,
            cache=self.cache,
            cache_inputs=(learner_message, ""),
            client=self.client,
        )

    def grade(self, learner_message: str, sage_message: str) -> dict:
        call = JudgeCall(
            model=GRADER_MODEL,
            system=GRADER_SYSTEM,
            user=(
                "Learner question:\n"
                f"{learner_message}\n\n"
                "Tutor reply:\n"
                f"{sage_message}"
            ),
            template_version=f"grader-{TEMPLATE_VERSION}",
        )
        return call_judge_json(
            call,
            cache=self.cache,
            cache_inputs=(learner_message, sage_message),
            client=self.client,
        )


def score_answer_first(
    transcript: Transcript,
    judge: JudgeProtocol,
) -> list[dict[str, Any]]:
    """Score every SAGE turn whose prior turn is a learner direct question."""
    results: list[dict[str, Any]] = []
    turns = transcript.turns

    for i, turn in enumerate(turns):
        if turn.speaker != "sage":
            continue

        prior = turns[i - 1] if i > 0 else None
        if prior is None or prior.speaker != "learner":
            results.append({
                "turn_index": turn.index,
                "applicable": False,
                "kind": None,
                "behavior": None,
                "reasoning": "no prior learner turn",
                "passed": None,
            })
            continue

        classification = judge.classify(prior.text)
        kind = classification.get("kind")
        if kind not in QUALIFYING_KINDS:
            results.append({
                "turn_index": turn.index,
                "applicable": False,
                "kind": kind,
                "behavior": None,
                "reasoning": classification.get("reasoning", ""),
                "passed": None,
            })
            continue

        grading = judge.grade(prior.text, turn.text)
        behavior = grading.get("behavior")
        results.append({
            "turn_index": turn.index,
            "applicable": True,
            "kind": kind,
            "behavior": behavior,
            "reasoning": grading.get("reasoning", ""),
            "passed": behavior in PASSING_BEHAVIORS,
        })
    return results
