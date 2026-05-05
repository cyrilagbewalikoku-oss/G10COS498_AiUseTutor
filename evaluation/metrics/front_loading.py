"""Metric 1: Front-Loading Discipline (rule-based).

Two sub-checks per SAGE turn:
  - Question Discipline: count of '?' must be <= 1.
  - Pre-Pause Length: sentence count up to first '?' (or full turn if no '?')
    must be <= 4.
"""
from __future__ import annotations

import re
from typing import Any

from evaluation.metrics.transcript import Transcript

_SENTENCE_END_RE = re.compile(r"[.!]")
_PRE_PAUSE_THRESHOLD = 4


def _count_sentences(text: str) -> int:
    """Count completed sentences by tallying terminal punctuation (. or !).

    We deliberately exclude '?' because pre-pause text is always sliced
    *before* the first '?', so any '?' in the fragment would be a false
    positive. Using terminal-punctuation count rather than split-based
    counting avoids off-by-one errors when the fragment ends mid-sentence.
    """
    return len(_SENTENCE_END_RE.findall(text))


def _score_turn(text: str) -> dict[str, Any]:
    qmarks = text.count("?")
    qd_passed = qmarks <= 1

    if "?" in text:
        pre_pause_text = text[: text.index("?")]
    else:
        pre_pause_text = text
    sentences = _count_sentences(pre_pause_text)
    pp_passed = sentences <= _PRE_PAUSE_THRESHOLD

    return {
        "question_discipline": {
            "question_marks": qmarks,
            "passed": qd_passed,
        },
        "pre_pause": {
            "sentences": sentences,
            "passed": pp_passed,
        },
        "passed": qd_passed and pp_passed,
    }


def score_front_loading(transcript: Transcript) -> list[dict[str, Any]]:
    """Score every SAGE turn in the transcript. Learner turns are skipped."""
    results: list[dict[str, Any]] = []
    for turn in transcript.turns:
        if turn.speaker != "sage":
            continue
        scored = _score_turn(turn.text)
        scored["turn_index"] = turn.index
        results.append(scored)
    return results
