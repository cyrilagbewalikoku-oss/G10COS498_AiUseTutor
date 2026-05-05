"""Persona-driven SAGE simulation.

Drives a conversation between a persona-LLM (acting as the learner) and SAGE.
Both run on Anthropic.

The agent-under-test's system prompt comes from one of three places, in order:
    1. ``--sage-prompt FILE`` CLI flag (highest priority)
    2. ``SAGE_SYSTEM_PROMPT_FILE`` environment variable
    3. The ``sage.prompts.SYSTEM_PROMPT`` module attribute, if importable

If none are available the simulator exits with a clear error. This decoupling
keeps ``evaluation/`` self-contained: a user evaluating a different agent can
just point ``--sage-prompt`` at their own prompt file.

Usage:
    python -m evaluation.personas.simulator --persona novice-curious
    python -m evaluation.personas.simulator --all
    python -m evaluation.personas.simulator --all --sage-prompt my-agent.txt
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import anthropic
from anthropic.types import TextBlock

from evaluation.metrics.transcript import Transcript, Turn

PERSONAS_PATH = Path(__file__).parent / "personas.json"
OUT_DIR = Path(__file__).parent.parent / "fixtures" / "simulated"

SAGE_MODEL = "claude-opus-4-7"
PERSONA_MODEL = "claude-haiku-4-5"
MAX_TOKENS = 800


def _load_agent_system_prompt(cli_path: Optional[str]) -> str:
    """Resolve the agent-under-test's system prompt.

    Priority: CLI flag > SAGE_SYSTEM_PROMPT_FILE env var > sage.prompts module.
    Exits with a clear message if none of the three sources is available.
    """
    if cli_path:
        return Path(cli_path).read_text()
    env_path = os.environ.get("SAGE_SYSTEM_PROMPT_FILE")
    if env_path:
        return Path(env_path).read_text()
    try:
        from sage.prompts import SYSTEM_PROMPT
        return SYSTEM_PROMPT
    except ImportError as e:
        raise SystemExit(
            "No agent system prompt available. Provide one of:\n"
            "  --sage-prompt PATH                    (CLI flag)\n"
            "  SAGE_SYSTEM_PROMPT_FILE=PATH          (environment variable)\n"
            "  sage.prompts.SYSTEM_PROMPT            (importable module)\n"
            f"\nFallback import error: {e}"
        )


def _extract_text(response) -> str:
    """Find the first text block in an Anthropic response and return its text."""
    block = next((b for b in response.content if isinstance(b, TextBlock)), None)
    if block is None:
        raise ValueError(f"No text block in response: {response.content!r}")
    return block.text


def _invert_roles(history: list[dict]) -> list[dict]:
    """Swap user<->assistant so the persona LLM sees SAGE's outputs as 'user'."""
    swapped = []
    for msg in history:
        role = "assistant" if msg["role"] == "user" else "user"
        swapped.append({"role": role, "content": msg["content"]})
    return swapped


def _should_stop(text: str, stop_phrases: list[str]) -> bool:
    """Match stop phrases on word boundaries so 'tired' doesn't fire on 'tiredness'."""
    low = text.lower()
    return any(
        re.search(rf"\b{re.escape(phrase.lower())}\b", low)
        for phrase in stop_phrases
    )


def simulate(
    persona: dict,
    client: anthropic.Anthropic,
    sage_system_prompt: str,
) -> Transcript:
    history: list[dict] = [{"role": "user", "content": persona["opening"]}]

    for _ in range(persona["max_turns"]):
        sage_response = client.messages.create(
            model=SAGE_MODEL,
            max_tokens=MAX_TOKENS,
            system=sage_system_prompt,
            messages=history,
        )
        sage_text = _extract_text(sage_response)
        history.append({"role": "assistant", "content": sage_text})

        persona_response = client.messages.create(
            model=PERSONA_MODEL,
            max_tokens=MAX_TOKENS,
            system=persona["system"],
            messages=_invert_roles(history),
        )
        persona_text = _extract_text(persona_response)
        if _should_stop(persona_text, persona["stop_phrases"]):
            break
        history.append({"role": "user", "content": persona_text})

    turns: list[Turn] = []
    for i, msg in enumerate(history):
        speaker = "learner" if msg["role"] == "user" else "sage"
        turns.append(Turn(index=i, speaker=speaker, text=msg["content"].strip()))
    return Transcript(
        source_id=f"simulated/{persona['id']}",
        origin="simulated",
        turns=turns,
    )


def _save(transcript: Transcript) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    persona_id = transcript.source_id.split("/", 1)[1]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT_DIR / f"{persona_id}-{timestamp}.json"
    path.write_text(json.dumps(transcript.to_dict(), indent=2))
    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--persona", help="Persona id from personas.json")
    group.add_argument("--all", action="store_true", help="Run all personas")
    parser.add_argument(
        "--sage-prompt",
        help="Path to a text file containing the agent's system prompt. "
             "Overrides SAGE_SYSTEM_PROMPT_FILE and sage.prompts.SYSTEM_PROMPT.",
    )
    args = parser.parse_args(argv)

    sage_system_prompt = _load_agent_system_prompt(args.sage_prompt)

    personas = json.loads(PERSONAS_PATH.read_text())
    if args.all:
        chosen = personas
    else:
        chosen = [p for p in personas if p["id"] == args.persona]
        if not chosen:
            raise SystemExit(f"Unknown persona: {args.persona}")

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    for persona in chosen:
        print(f"Running persona: {persona['id']}...")
        transcript = simulate(persona, client, sage_system_prompt)
        path = _save(transcript)
        print(f"  -> wrote {path} ({len(transcript.turns)} turns)")


if __name__ == "__main__":
    main()
