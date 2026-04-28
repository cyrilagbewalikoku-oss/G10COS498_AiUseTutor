"""Chat export formatters.

Pure functions that turn a list of ``{"role", "content"}`` dicts into a
single string. Kept here (instead of inline in app.py) so app.py stays
focused on Streamlit wiring.
"""

from __future__ import annotations

_MD_LABELS = {"user": "### You", "assistant": "### SAGE"}
_TXT_LABELS = {"user": "You:", "assistant": "SAGE:"}


def messages_to_markdown(messages: list[dict]) -> str:
    parts: list[str] = []
    for msg in messages:
        label = _MD_LABELS.get(msg["role"], f"### {msg['role'].title()}")
        parts.append(f"{label}\n\n{msg['content'].strip()}")
    return "\n\n".join(parts) + "\n"


def messages_to_text(messages: list[dict]) -> str:
    parts: list[str] = []
    for msg in messages:
        label = _TXT_LABELS.get(msg["role"], f"{msg['role'].title()}:")
        parts.append(f"{label}\n{msg['content'].strip()}")
    return "\n\n".join(parts) + "\n"
