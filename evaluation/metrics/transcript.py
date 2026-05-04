"""Markdown and JSON transcript parsing.

The authored transcripts in examples/interactions/ use **LEARNER**: / **SAGE**:
markers. The simulated transcripts produced by the persona simulator are JSON
with the same Turn shape. Both produce a Transcript dataclass.
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


_MARKER_RE = re.compile(r"^\*\*(LEARNER|SAGE)\*\*:", re.MULTILINE)
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
        speaker = m.group(1).lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else end_of_conversation
        text = md[start:end].strip()
        turns.append(Turn(index=i, speaker=speaker, text=text))  # type: ignore[arg-type]
    return Transcript(source_id=source_id, origin=origin, turns=turns)


def parse_simulated_json(path: Union[str, Path]) -> Transcript:
    """Load a simulator-produced JSON transcript."""
    payload = json.loads(Path(path).read_text())
    turns = [Turn(**t) for t in payload["turns"]]
    return Transcript(
        source_id=payload["source_id"],
        origin=payload["origin"],
        turns=turns,
    )
