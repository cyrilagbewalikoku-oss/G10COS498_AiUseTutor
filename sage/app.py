"""SAGE Web UI — Streamlit chat interface.

Run: streamlit run sage/app.py
Or:  sage-ui  (after pip install)
"""

import json
import os
import re
from datetime import datetime

import streamlit as st

from sage import components, export, session_store
from sage.prompts import SYSTEM_PROMPT as FROZEN_PROMPT
from sage.skill_loader import build_system_prompt

# Session-recap block emitted by the reflection-facilitator skill at session
# close. Extracted here so the UI can render a card and hide the raw JSON.
_RECAP_RE = re.compile(
    r"<SESSION_RECAP>\s*(\{.*?\})\s*</SESSION_RECAP>",
    re.DOTALL,
)

# Inferred-level block emitted by SAGE in anonymous mode once it's calibrated
# the learner from conversation. Lets the UI update the sidebar level
# selector without the learner having to click it themselves.
_INFERRED_LEVEL_RE = re.compile(
    r"<INFERRED_LEVEL>\s*(\{.*?\})\s*</INFERRED_LEVEL>",
    re.DOTALL,
)

_VALID_LEVELS = {"novice", "practitioner", "advanced", "critical_thinker"}

_DIMENSION_HUMAN = {
    "conceptualUnderstanding": "Conceptual Understanding",
    "promptingSkill": "Prompting Skill",
    "outputEvaluation": "Output Evaluation",
    "ethicalReasoning": "Ethical Reasoning",
    "criticalThinking": "Critical Thinking",
}

_PRACTICE_HUMAN = {
    "prompt_crafting": "Prompt Crafting",
    "output_evaluation": "Output Evaluation",
    "appropriateness_judgment": "Appropriateness Judgment",
    "workflow_design": "Workflow Design",
}


def _extract_recap(text: str) -> tuple[str, dict | None]:
    """Return (cleaned_text, recap_dict_or_none).

    The recap block, if present, is stripped from `cleaned_text` so the
    learner never sees the raw JSON. Malformed blocks are silently ignored
    (treated as if absent) to keep the UI robust.
    """
    match = _RECAP_RE.search(text)
    if not match:
        return text, None
    try:
        recap = json.loads(match.group(1))
    except json.JSONDecodeError:
        return _RECAP_RE.sub("", text).strip(), None
    cleaned = _RECAP_RE.sub("", text).strip()
    return cleaned, recap


def _extract_inferred_level(text: str) -> tuple[str, str | None]:
    """Return (cleaned_text, level_or_none). Same pattern as _extract_recap."""
    match = _INFERRED_LEVEL_RE.search(text)
    if not match:
        return text, None
    cleaned = _INFERRED_LEVEL_RE.sub("", text).strip()
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return cleaned, None
    level = payload.get("level") if isinstance(payload, dict) else None
    if level not in _VALID_LEVELS:
        return cleaned, None
    return cleaned, level


def _render_recap_card(recap: dict, profile: dict, session_id: str) -> None:
    """Render the session-recap card in the chat stream.

    Called only on fresh completions — historical assistant turns have the
    recap block stripped before being stored, so they don't re-render.
    """
    practice = _PRACTICE_HUMAN.get(recap.get("practice_type", ""), "Practice")
    dim_key = recap.get("dimension_changed", "")
    dim = _DIMENSION_HUMAN.get(dim_key, dim_key or "—")
    delta = recap.get("delta", 0)
    try:
        delta_f = float(delta)
    except (TypeError, ValueError):
        delta_f = 0.0
    suggested = (recap.get("suggested_next") or "").strip()
    arrow = "↑" if delta_f > 0 else ("↓" if delta_f < 0 else "·")
    sign = "+" if delta_f > 0 else ""

    with st.container(border=True):
        st.markdown(
            f"**\U0001f4c8 You practiced _{practice}_**  \n"
            f"{dim}  {arrow}  `{sign}{delta_f:.1f}`"
        )
        if suggested:
            if st.button(
                f"Next: {suggested}",
                key=f"recap_next_{session_id}_{hash(suggested)}",
                use_container_width=True,
            ):
                st.session_state.messages.append(
                    {"role": "user", "content": suggested}
                )
                session_store.append_turn(
                    profile, session_id, "user", suggested
                )
                st.rerun()

st.set_page_config(
    page_title="SAGE — AI Literacy Tutor",
    page_icon="\U0001f393",
    layout="centered",
)

# Seed the data volume on first boot (no-op if users already exist).
session_store.seed_if_empty()


# ── Helpers ──────────────────────────────────────────────────────────────

_DIMENSION_LABELS = {
    "conceptualUnderstanding": "Conceptual Understanding",
    "promptingSkill": "Prompting Skill",
    "outputEvaluation": "Output Evaluation",
    "ethicalReasoning": "Ethical Reasoning",
    "criticalThinking": "Critical Thinking",
}

_LEVEL_LABELS = {
    "novice": "Novice",
    "practitioner": "Practitioner",
    "advanced": "Advanced",
    "critical_thinker": "Critical Thinker",
}


def _focus_dimension(profile: dict) -> str:
    """Pick the dimension to surface in the header strip.

    Lowest-scoring dimension wins. Ties broken by the canonical order above,
    which is the order learners tend to encounter them. Default to
    'Prompting Skill' when scores are all zero / missing — it's the most
    actionable starting point for a brand-new learner.
    """
    scores = profile.get("dimensionScores") or {}
    if not any(scores.values()):
        return _DIMENSION_LABELS["promptingSkill"]
    key = min(_DIMENSION_LABELS, key=lambda k: scores.get(k, 0.0))
    return _DIMENSION_LABELS[key]


def _level_label(profile: dict) -> str:
    return _LEVEL_LABELS.get(profile.get("level", "novice"), "Novice")


def _learner_context_block(profile: dict) -> str:
    """Runtime block appended to the static SYSTEM_PROMPT.

    Gives SAGE the identity + scores for the current learner without needing
    a tool round-trip. Static SYSTEM_PROMPT is auto-generated from CLAUDE.md
    and skills — this dynamic tail lives here.
    """
    if _is_anonymous(profile):
        current_level = profile.get("level", "novice")
        return (
            "\n\n# LEARNER_CONTEXT (runtime-injected — the current learner)\n"
            "- This learner chose 'Just chat' — fully anonymous.\n"
            "- Do NOT call load_user_profile or save_user_profile at any point.\n"
            "- Treat downstream skill instructions that say 'update the profile' as no-ops.\n"
            f"- Current level (from sidebar or prior inference): {current_level}. "
            "The learner can override this via the sidebar selector.\n"
            "- If the learner volunteers identity mid-session, you MAY offer once to save a profile; otherwise stay anonymous.\n"
            "\n## Level inference (anonymous only)\n"
            "When you have enough signal from the conversation to infer the learner's level "
            "(typically after 2-3 substantive exchanges or a brief calibration), append this block "
            "to the END of your message — silently, no commentary:\n"
            "\n"
            "<INFERRED_LEVEL>\n"
            '{"level": "<novice|practitioner|advanced|critical_thinker>"}\n'
            "</INFERRED_LEVEL>\n"
            "\n"
            "Rules:\n"
            "- Emit this block ONLY when you have genuinely inferred a level — not speculatively.\n"
            "- Emit it at most ONCE per anonymous session unless the learner's signals clearly contradict the earlier inference.\n"
            "- The UI strips the block and updates the sidebar level indicator. Do not mention the block to the learner.\n"
            f"- Do NOT emit the block if your inference matches the current level ({current_level}) — it would be a no-op."
        )

    scores = profile.get("dimensionScores") or {}
    competencies = profile.get("competencyScores") or {}
    return (
        "\n\n# LEARNER_CONTEXT (runtime-injected — the current learner)\n"
        f"- Name: {profile.get('name', 'Learner')}\n"
        f"- Level: {profile.get('level', 'novice')}\n"
        f"- Dimension scores (0-5): {scores}\n"
        f"- Competency scores (0-5): {competencies}\n"
        f"- Today's focus dimension: {_focus_dimension(profile)}\n"
        "Address the learner by name when natural. Adapt vocabulary to their level. "
        "You do NOT need to call load_user_profile at session start — the profile is already loaded."
    )


def _reset_for_new_learner() -> None:
    for k in ("learner", "session_id", "messages", "resume_decided"):
        st.session_state.pop(k, None)


def _is_anonymous(profile: dict) -> bool:
    return bool(profile.get("anonymous"))


def _make_anonymous_profile() -> dict:
    """Sentinel in-memory profile for the 'Just chat' path.

    Not persisted. Zero scores so components that inspect the dict don't
    crash, and a level of 'novice' so LEARNER_CONTEXT can default vocabulary
    until the conversation reveals otherwise.
    """
    return {
        "anonymous": True,
        "name": "Learner",
        "level": "novice",
        "dimensionScores": {
            "conceptualUnderstanding": 0.0,
            "promptingSkill": 0.0,
            "outputEvaluation": 0.0,
            "ethicalReasoning": 0.0,
            "criticalThinking": 0.0,
        },
        "competencyScores": {
            "promptCrafting": 0.0,
            "outputEvaluation": 0.0,
            "appropriatenessJudgment": 0.0,
            "workflowDesign": 0.0,
        },
    }


def _seed_welcome_if_empty(profile: dict) -> None:
    """Drop a greeting into the chat when the message list is empty.

    Runs after the resume-or-fresh decision. If the learner resumed a
    session, messages are already populated and we no-op.
    """
    if st.session_state.messages:
        return

    if _is_anonymous(profile):
        text = (
            "Hey — I'm SAGE, a tutor for using AI agents well. "
            "I'll adapt as we go. What would you like to work on?"
        )
    elif profile.get("_just_created"):
        text = (
            f"Hi {profile.get('name', 'there')} — I'm SAGE, your AI literacy tutor. "
            "Ready to start?"
        )
    else:
        text = (
            f"Welcome back, {profile.get('name', 'learner')}. I'm SAGE. "
            "Pick up where we left off, or try something new?"
        )

    st.session_state.messages.append({"role": "assistant", "content": text})
    if not _is_anonymous(profile) and st.session_state.get("session_id"):
        session_store.append_turn(
            profile, st.session_state.session_id, "assistant", text
        )


@st.cache_resource
def _resolve_system_prompt() -> tuple[str, str]:
    """Build the system prompt once per server process.

    Rebuilds from `.claude/skills/` when that tree is present (local dev);
    in production the image ships only the frozen snapshot.
    """
    runtime = build_system_prompt()
    if runtime is not None:
        return runtime, "live .claude/skills/"
    return FROZEN_PROMPT, "frozen sage/prompts.py"


SYSTEM_PROMPT, PROMPT_SOURCE = _resolve_system_prompt()
print(f"[sage] prompt source: {PROMPT_SOURCE}")


# ── Sidebar ──────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## \U0001f393 SAGE")
    st.caption("Scaffolded AI Guidance for Engagement")
    st.divider()

    _env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if _env_key:
        api_key = _env_key
        st.success("API key loaded from environment")
    else:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Get a key at console.anthropic.com",
        )

    # The rest of the sidebar (suggestions, session controls) is rendered
    # AFTER the main column so it can reflect the learner + session state.


# ── Learner picker ───────────────────────────────────────────────────────

if "learner" not in st.session_state:
    st.markdown(
        """
        <div style="text-align:center; padding: 2rem 1rem 1rem 1rem;">
            <h1>\U0001f393 SAGE</h1>
            <p style="font-size:1.1rem; color:#666;">
                AI Literacy Tutor — learn to use AI effectively, critically, and ethically.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    profiles = session_store.list_profiles_for_ui()
    options = ["— pick a learner —"] + [
        f"{p['name']} · {_LEVEL_LABELS.get(p['level'], p['level'])}" for p in profiles
    ] + ["➕  New learner"]

    choice = st.selectbox(
        "Who are you?",
        options,
        index=0,
        help="Cohort demo — no passwords. Pick your profile or create a new one.",
    )

    if choice.startswith("➕"):
        new_name = st.text_input(
            "Your name (first name is fine)",
            key="new_learner_name_input",
            placeholder="e.g., Alice",
        )
        if st.button("Create profile", type="primary", disabled=not new_name.strip()):
            profile = session_store.create_new_learner(new_name.strip())
            profile["_just_created"] = True
            st.session_state.learner = profile
            st.session_state.messages = []
            st.session_state.resume_decided = True
            st.session_state.session_id = session_store.new_session(profile)
            st.rerun()
    elif choice != options[0]:
        # Existing profile — load by matching index in the profiles list
        idx = options.index(choice) - 1
        picked = profiles[idx]
        profile = session_store.load_profile_by_filename(picked["filename"])
        if profile:
            st.session_state.learner = profile
            st.session_state.messages = []
            st.session_state.resume_decided = False
            st.rerun()

    st.markdown("---")
    st.caption("Or skip signing in:")
    if st.button(
        "\U0001f464  Just chat (anonymous)",
        use_container_width=True,
        help="Dive straight in. Nothing saved to disk — refresh wipes the conversation.",
    ):
        st.session_state.learner = _make_anonymous_profile()
        st.session_state.messages = []
        st.session_state.resume_decided = True
        st.session_state.session_id = None
        st.rerun()

    st.stop()


# ── Resume-or-fresh prompt ───────────────────────────────────────────────

profile = st.session_state.learner

if not _is_anonymous(profile) and not st.session_state.get("resume_decided", False):
    latest = session_store.latest_session_id(profile)
    has_resumable = (
        latest is not None
        and session_store.session_turn_count(profile, latest) >= 2
    )

    if has_resumable:
        st.markdown(
            f"<div style='text-align:center; padding: 1.5rem 1rem;'>"
            f"<h3>\U0001f44b Welcome back, {profile.get('name', 'learner')}.</h3>"
            "<p style='color:#666;'>You have a conversation in progress. "
            "Pick up where you left off, or start fresh?</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            if st.button("Resume last session", use_container_width=True, type="primary"):
                st.session_state.session_id = latest
                st.session_state.messages = session_store.load_session_messages(
                    profile, latest
                )
                st.session_state.resume_decided = True
                session_store.touch_last_active(profile)
                st.rerun()
        with col_b:
            if st.button("Start fresh", use_container_width=True):
                st.session_state.session_id = session_store.new_session(profile)
                st.session_state.messages = []
                st.session_state.resume_decided = True
                session_store.touch_last_active(profile)
                st.rerun()
        with col_c:
            if st.button("Switch learner", use_container_width=True):
                _reset_for_new_learner()
                st.rerun()
        st.stop()
    else:
        # No prior session to resume — mint a new one silently.
        st.session_state.session_id = session_store.new_session(profile)
        st.session_state.resume_decided = True
        session_store.touch_last_active(profile)


# For anonymous, session_id stays None and there's no prior session to resume —
# everything below must handle that.
if _is_anonymous(profile):
    st.session_state.resume_decided = True
    st.session_state.setdefault("session_id", None)


_seed_welcome_if_empty(profile)


# ── Sidebar (post-picker: suggestions + session controls) ───────────────

_LEVEL_KEYS = ["novice", "practitioner", "advanced", "critical_thinker"]

with st.sidebar:
    st.divider()

    if _is_anonymous(profile):
        st.markdown("**\U0001f464 Just chatting**  \n*(no profile saved)*")
        st.caption(
            "Pick a level to tune the conversation. SAGE will also update "
            "this based on onboarding signals."
        )
        current_level = profile.get("level", "novice")
        try:
            level_idx = _LEVEL_KEYS.index(current_level)
        except ValueError:
            level_idx = 0
        picked_level = st.selectbox(
            "Level",
            options=_LEVEL_KEYS,
            index=level_idx,
            format_func=lambda k: _LEVEL_LABELS.get(k, k),
            key="anon_level_selector",
        )
        if picked_level != current_level:
            profile["level"] = picked_level
            st.session_state.learner = profile
            st.rerun()
    else:
        st.markdown(f"**Signed in as**  \n{profile.get('name', 'Learner')}")
        st.caption(f"Level: {_level_label(profile)}")
        with st.expander("\U0001f4ca My Progress", expanded=False):
            components.render_progress_drawer(profile)

    st.divider()
    st.markdown("**Try one of these:**")

    suggestions = [
        "I'm new to AI agents",
        "I want to practice writing prompts",
        "Give me an AI output to evaluate",
        "Should I use AI for this task?",
        "Help me improve this prompt I used",
        "Let's do a weekly review",
    ]
    for text in suggestions:
        if st.button(text, key=f"btn_{text}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": text})
            if not _is_anonymous(profile):
                session_store.append_turn(
                    profile, st.session_state.session_id, "user", text
                )
            st.rerun()

    if st.session_state.messages:
        st.divider()
        st.markdown("**Export chat**")
        fmt = st.selectbox(
            "Format",
            options=[".md", ".txt"],
            index=0,
            label_visibility="collapsed",
            key="export_format",
        )
        if fmt == ".md":
            data = export.messages_to_markdown(st.session_state.messages)
            mime = "text/markdown"
        else:
            data = export.messages_to_text(st.session_state.messages)
            mime = "text/plain"
        slug = re.sub(r"[^A-Za-z0-9]+", "-", profile.get("name") or "anon").strip("-").lower() or "anon"
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        st.download_button(
            "Download",
            data=data,
            file_name=f"sage-chat-{slug}-{stamp}{fmt}",
            mime=mime,
            use_container_width=True,
        )

    st.divider()
    if st.button("Start new session", use_container_width=True):
        if _is_anonymous(profile):
            st.session_state.session_id = None
        else:
            st.session_state.session_id = session_store.new_session(profile)
        st.session_state.messages = []
        st.rerun()

    if st.button("Switch learner", use_container_width=True):
        _reset_for_new_learner()
        st.rerun()


# ── Header strip ────────────────────────────────────────────────────────

if _is_anonymous(profile):
    st.caption(
        f"\U0001f464 Just chatting · {_level_label(profile)} · no profile saved"
    )
else:
    st.caption(
        f"\U0001f44b {profile.get('name', 'Learner')} · "
        f"{_level_label(profile)} · "
        f"Today's focus: {_focus_dimension(profile)}"
    )


# ── Display chat history ─────────────────────────────────────────────────

for msg in st.session_state.messages:
    avatar = "\U0001f393" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ── Generate response if last message is from user ───────────────────────

needs_response = (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
)

# Cap thread length before sending to the API (see plan §Technical Notes).
_MAX_API_TURNS = 40

if needs_response:
    if not api_key:
        with st.chat_message("assistant", avatar="\U0001f393"):
            st.error(
                "Please enter your Anthropic API key in the sidebar to get started."
            )
        st.stop()

    # Lazy import of anthropic SDK keeps empty-state page load fast
    import anthropic
    from sage.tools import ALL_TOOLS

    system_with_learner = SYSTEM_PROMPT + _learner_context_block(profile)

    with st.chat_message("assistant", avatar="\U0001f393"):
        with st.spinner("SAGE is thinking..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[-_MAX_API_TURNS:]
                ]
                runner = client.beta.messages.tool_runner(
                    model="claude-opus-4-6",
                    max_tokens=16000,
                    system=system_with_learner,
                    tools=ALL_TOOLS,
                    messages=api_messages,
                    thinking={"type": "adaptive"},
                )

                final_message = None
                for message in runner:
                    final_message = message

                if final_message is None:
                    response = "I didn't get a response. Please try again."
                else:
                    parts = []
                    for block in final_message.content:
                        if block.type == "text":
                            parts.append(block.text)
                    response = "\n\n".join(parts) if parts else "..."

            except anthropic.AuthenticationError:
                response = "Invalid API key. Please check the key in the sidebar."
            except anthropic.RateLimitError:
                response = "Rate limited — please wait a moment and try again."
            except anthropic.APIError as e:
                response = f"API error: {e.message}"

        # Strip the SESSION_RECAP block from what we show + store, render it
        # separately as a card. Only happens on fresh completions — historical
        # messages are already clean because we store the cleaned version.
        # Also strip INFERRED_LEVEL blocks (anonymous-only); apply them to the
        # in-memory profile so the sidebar reflects SAGE's inference.
        response, inferred_level = _extract_inferred_level(response)
        cleaned_response, recap = _extract_recap(response)
        st.markdown(cleaned_response)
        if recap is not None:
            _render_recap_card(recap, profile, st.session_state.session_id)
        if inferred_level and _is_anonymous(profile) and inferred_level != profile.get("level"):
            profile["level"] = inferred_level
            st.session_state.learner = profile

    st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
    if not _is_anonymous(profile):
        session_store.append_turn(
            profile, st.session_state.session_id, "assistant", cleaned_response
        )
        session_store.touch_last_active(profile)


# ── Chat input ───────────────────────────────────────────────────────────

if prompt := st.chat_input("Message SAGE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    if not _is_anonymous(profile):
        session_store.append_turn(
            profile, st.session_state.session_id, "user", prompt
        )
    st.rerun()
