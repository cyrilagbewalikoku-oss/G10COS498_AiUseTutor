"""Markdown and JSON transcript parsing.

The authored transcripts in examples/interactions/ use **LEARNER**: / **SAGE**:
markers, or named-learner markers like **JAKE**: / **PRIYA**: / **CHEN**:. Any
all-caps token maps to "sage" if it is SAGE or AI AGENT (simulation mode), and
"learner" otherwise. The simulated transcripts produced by the persona simulator
are JSON with the same Turn shape. Both produce a Transcript dataclass.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal, Union

Speaker = Literal["learner", "sage"]
Origin = Literal["authored", "simulated"]


@dataclass
class Turn:
    index: int
    speaker: Speaker
    text: str


@dataclass
class Transcript:
    source_id: str
    origin: Origin
    turns: list[Turn]

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "origin": self.origin,
            "turns": [asdict(t) for t in self.turns],
        }


_MARKER_RE = re.compile(r"^\*\*([A-Z][A-Z ]*[A-Z])\*\*:", re.MULTILINE)
# All-caps tokens that represent SAGE (including SAGE in simulation/agent mode).
_SAGE_TOKENS: frozenset[str] = frozenset({"SAGE", "AI AGENT"})
_SEP_LINE_RE = re.compile(r"^---\s*$", re.MULTILINE)


def parse_markdown(md: str, source_id: str, origin: Origin) -> Transcript:
    """Parse a SAGE markdown transcript into a Transcript.

    Conventions:
    - Speaker markers: lines that start with **LEARNER**: or **SAGE**:.
    - Conversation ends at the first --- line that appears AFTER the last marker.
    - Anything before the first marker (e.g., title, profile, frontmatter --- separator)
      is ignored.
    """
    matches = list(_MARKER_RE.finditer(md))
    if not matches:
        return Transcript(source_id=source_id, origin=origin, turns=[])

    last_marker_end = matches[-1].end()
    sep_after = _SEP_LINE_RE.search(md, pos=last_marker_end)
    end_of_conversation = sep_after.start() if sep_after else len(md)

    turns: list[Turn] = []
    for i, m in enumerate(matches):
        raw = m.group(1).upper()
        speaker: Speaker = "sage" if raw in _SAGE_TOKENS else "learner"
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else end_of_conversation
        text = md[start:end].strip()
        turns.append(Turn(index=i, speaker=speaker, text=text))
    return Transcript(source_id=source_id, origin=origin, turns=turns)


def parse_simulated_json(path: Union[str, Path]) -> Transcript:
    """Load a simulator-produced JSON transcript."""
    p = Path(path)
    try:
        payload = json.loads(p.read_text())
        turns = [Turn(**t) for t in payload["turns"]]
        transcript = Transcript(
            source_id=payload["source_id"],
            origin=payload["origin"],
            turns=turns,
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid simulated transcript at {p}: {e}") from e
    # Runtime guard: catch typos in speaker values that the static Literal can't.
    for t in transcript.turns:
        if t.speaker not in ("learner", "sage"):
            raise ValueError(f"Invalid speaker {t.speaker!r} in {p}")
    return transcript
