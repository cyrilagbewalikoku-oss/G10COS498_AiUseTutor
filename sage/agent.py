#!/usr/bin/env python3
"""SAGE Agent — Scaffolded AI Guidance for Engagement.

A conversational AI literacy tutor built on the Anthropic Claude API.
Run: python -m sage.agent
"""

import sys

import anthropic

from sage.prompts import SYSTEM_PROMPT as FROZEN_PROMPT
from sage.skill_loader import build_system_prompt
from sage.tools import ALL_TOOLS

MODEL = "claude-opus-4-6"
MAX_TOKENS = 16000

_runtime_prompt = build_system_prompt()
SYSTEM_PROMPT = _runtime_prompt if _runtime_prompt is not None else FROZEN_PROMPT
PROMPT_SOURCE = "live .claude/skills/" if _runtime_prompt is not None else "frozen sage/prompts.py"


def extract_text(message) -> str:
    """Extract all text content from a BetaMessage."""
    parts = []
    for block in message.content:
        if block.type == "text":
            parts.append(block.text)
    return "\n".join(parts)


def run():
    """Main conversation loop."""
    client = anthropic.Anthropic()
    messages: list[dict] = []

    print("=" * 60)
    print("  SAGE — Scaffolded AI Guidance for Engagement")
    print("  AI Literacy Tutor")
    print("=" * 60)
    print(f"  prompt source: {PROMPT_SOURCE}")
    print("Type your message to begin. Type 'quit' to exit.\n")

    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        # Run the tool runner — handles tool calls automatically
        try:
            runner = client.beta.messages.tool_runner(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=ALL_TOOLS,
                messages=messages,
                thinking={"type": "adaptive"},
            )

            final_message = None
            for message in runner:
                final_message = message

            if final_message is None:
                print("\nSAGE: (no response)\n")
                messages.pop()  # remove the user message that got no response
                continue

            response_text = extract_text(final_message)
            messages.append({"role": "assistant", "content": response_text})
            print(f"\nSAGE: {response_text}\n")

        except anthropic.AuthenticationError:
            print(
                "\nError: Invalid API key. Set ANTHROPIC_API_KEY environment variable."
            )
            sys.exit(1)
        except anthropic.RateLimitError:
            print("\nError: Rate limited. Please wait a moment and try again.")
            messages.pop()
        except anthropic.APIError as e:
            print(f"\nAPI error: {e.message}")
            messages.pop()


if __name__ == "__main__":
    run()
