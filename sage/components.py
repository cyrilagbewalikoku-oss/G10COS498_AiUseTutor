"""Pure render helpers for the SAGE Streamlit UI.

Each helper takes a profile dict and renders into the current Streamlit
container. No side effects, no state — safe to call from any position in the
rerun script.

The drawer intentionally uses plain progress bars instead of a radar chart.
Research (Open Learner Models, Bodily & Verbert 2018) flags high-inference-
cost visualizations as a motivation killer; a labeled bar + one-sentence
gloss gives the learner the same information with less to parse.
"""

from __future__ import annotations

import streamlit as st

_DIMENSIONS: list[tuple[str, str, str]] = [
    (
        "conceptualUnderstanding",
        "Conceptual Understanding",
        "Can explain what AI agents are and how they work.",
    ),
    (
        "promptingSkill",
        "Prompting Skill",
        "Writes clear, specific, well-constrained prompts.",
    ),
    (
        "outputEvaluation",
        "Output Evaluation",
        "Critically assesses AI-generated content.",
    ),
    (
        "ethicalReasoning",
        "Ethical Reasoning",
        "Identifies and navigates ethical implications.",
    ),
    (
        "criticalThinking",
        "Critical Thinking",
        "Reasons about AI limitations and failure modes.",
    ),
]

_COMPETENCIES: list[tuple[str, str, str]] = [
    (
        "promptCrafting",
        "Prompt Crafting",
        "Context, specificity, and constraint handling.",
    ),
    (
        "outputEvaluation",
        "Output Evaluation",
        "Fact-checking, error detection, bias recognition.",
    ),
    (
        "appropriatenessJudgment",
        "Appropriateness Judgment",
        "Stakeholder awareness, risk, task-AI fit.",
    ),
    (
        "workflowDesign",
        "Workflow Design",
        "Human-in-the-loop, verification, escalation.",
    ),
]

_LEVEL_LABELS = {
    "novice": "Novice",
    "practitioner": "Practitioner",
    "advanced": "Advanced",
    "critical_thinker": "Critical Thinker",
}

_MAX_SCORE = 5.0


def render_level_badge(profile: dict) -> None:
    """Compact level + name label. Used inside the drawer header."""
    name = profile.get("name", "Learner")
    level = _LEVEL_LABELS.get(profile.get("level", "novice"), "Novice")
    st.markdown(f"**{name}** · {level}")


def _render_score_row(label: str, gloss: str, score: float) -> None:
    pct = max(0.0, min(1.0, score / _MAX_SCORE))
    st.markdown(f"**{label}** — {score:.1f}/5")
    st.progress(pct)
    st.caption(gloss)


def render_dimension_bars(profile: dict) -> None:
    """One progress bar per assessment dimension.

    Named "bars" rather than "radar" — see module docstring.
    """
    st.markdown("#### Assessment dimensions")
    scores = profile.get("dimensionScores") or {}
    for key, label, gloss in _DIMENSIONS:
        _render_score_row(label, gloss, float(scores.get(key, 0.0)))


def render_competency_bars(profile: dict) -> None:
    """One progress bar per practice-type competency."""
    st.markdown("#### Practice competencies")
    scores = profile.get("competencyScores") or {}
    for key, label, gloss in _COMPETENCIES:
        _render_score_row(label, gloss, float(scores.get(key, 0.0)))


def render_reflection_log(profile: dict, max_items: int = 5) -> None:
    """Recent closing-reflection responses, newest first.

    The schema supports a `reflectionResponses` array with timestamped entries.
    If empty, show a small hint instead of an empty list.
    """
    st.markdown("#### Recent reflections")
    reflections = list(profile.get("reflectionResponses") or [])
    if not reflections:
        st.caption("No reflections yet. Finish a practice session to see one here.")
        return

    reflections.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    for entry in reflections[:max_items]:
        question = entry.get("question", "").strip()
        response = entry.get("response", "").strip()
        timestamp = entry.get("timestamp", "")[:10]
        skipped = bool(entry.get("skipped"))

        st.markdown(
            f"<div style='border-left: 3px solid #ddd; padding: 0.4rem 0.8rem; margin: 0.5rem 0;'>"
            f"<em>{question}</em><br>"
            + (
                "<span style='color:#888;'>— skipped —</span>"
                if skipped
                else f"<span>{response or '<em>no response</em>'}</span>"
            )
            + f"<br><small style='color:#999;'>{timestamp}</small>"
            "</div>",
            unsafe_allow_html=True,
        )

    if len(reflections) > max_items:
        with st.expander(f"Show {len(reflections) - max_items} older reflection(s)"):
            for entry in reflections[max_items:]:
                q = entry.get("question", "").strip()
                r = entry.get("response", "").strip()
                t = entry.get("timestamp", "")[:10]
                st.markdown(f"- *{q}* — {r or '(no response)'} · {t}")


def render_progress_drawer(profile: dict) -> None:
    """Render the full drawer body. Call this inside `with st.expander(...):`."""
    render_level_badge(profile)
    st.divider()
    render_dimension_bars(profile)
    st.divider()
    render_competency_bars(profile)
    st.divider()
    render_reflection_log(profile)
