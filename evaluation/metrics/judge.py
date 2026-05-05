"""Thin wrapper around the Anthropic SDK for LLM-as-judge metrics.

Provides:
  - cache_key(): deterministic hash for caching judge calls
  - JudgeCache: simple JSON file cache (load/get/put/save)
  - call_judge_json(): call Claude with a system+user prompt, return parsed JSON dict
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import anthropic
from anthropic.types import TextBlock


def cache_key(model: str, template_version: str, learner_msg: str, sage_msg: str) -> str:
    payload = f"{model}\x00{template_version}\x00{learner_msg}\x00{sage_msg}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class JudgeCache:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        text = self.path.read_text()
        if not text.strip():
            return
        try:
            self._data = json.loads(text)
        except json.JSONDecodeError:
            self._data = {}

    def get(self, key: str) -> Optional[dict]:
        return self._data.get(key)

    def put(self, key: str, value: dict) -> None:
        self._data[key] = value

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))


def _extract_json(text: str) -> dict:
    """Extract the first balanced {...} object from a model response and parse it.

    Walks the string from the first `{`, tracking brace depth (ignoring braces
    that appear inside JSON string literals), and returns the substring from
    that opening brace to the matching closing brace. Raises ValueError if no
    balanced object is found.
    """
    start = text.find("{")
    if start < 0:
        raise ValueError(f"No JSON object found in judge output: {text!r}")

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise ValueError(f"Unbalanced JSON object in judge output: {text!r}")


@dataclass
class JudgeCall:
    model: str
    system: str
    user: str
    template_version: str
    max_tokens: int = 300


def call_judge_json(
    call: JudgeCall,
    *,
    cache: Optional[JudgeCache] = None,
    cache_inputs: Optional[tuple[str, str]] = None,
    client: Optional[anthropic.Anthropic] = None,
) -> dict:
    """Run a judge call. Returns parsed JSON. Optionally caches by (model, template_version, *cache_inputs)."""
    if cache is not None and cache_inputs is not None:
        key = cache_key(call.model, call.template_version, *cache_inputs)
        hit = cache.get(key)
        if hit is not None:
            return hit
    else:
        key = None

    if client is None:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=call.model,
        max_tokens=call.max_tokens,
        system=call.system,
        messages=[{"role": "user", "content": call.user}],
    )
    text_block = next(
        (b for b in response.content if isinstance(b, TextBlock)),
        None,
    )
    if text_block is None:
        raise ValueError(f"No text block in judge response: {response.content!r}")
    raw = text_block.text
    parsed = _extract_json(raw)

    if cache is not None and key is not None:
        cache.put(key, parsed)
        cache.save()
    return parsed
