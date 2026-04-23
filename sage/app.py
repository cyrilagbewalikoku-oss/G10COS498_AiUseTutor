"""SAGE Web UI — Streamlit chat interface.

Run: streamlit run sage/app.py
Or:  sage-ui  (after pip install)
"""

import os

import streamlit as st

from sage.prompts import SYSTEM_PROMPT as FROZEN_PROMPT
from sage.skill_loader import build_system_prompt

st.set_page_config(
    page_title="SAGE — AI Literacy Tutor",
    page_icon="\U0001f393",
    layout="centered",
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
            st.rerun()

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Session state ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display chat history ─────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align:center; padding: 2rem 1rem;">
            <h1>\U0001f393 SAGE</h1>
            <p style="font-size:1.1rem; color:#666;">
                AI Literacy Tutor — learn to use AI effectively, critically, and ethically.
            </p>
            <p style="color:#888;">Type a message below or pick a suggestion from the sidebar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

for msg in st.session_state.messages:
    avatar = "\U0001f393" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Generate response if last message is from user ───────────────────────
needs_response = (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
)

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

    _runtime_prompt = build_system_prompt()
    SYSTEM_PROMPT = _runtime_prompt if _runtime_prompt is not None else FROZEN_PROMPT
    if "_prompt_source_logged" not in st.session_state:
        source = "live .claude/skills/" if _runtime_prompt is not None else "frozen sage/prompts.py"
        print(f"[sage] prompt source: {source}")
        st.session_state._prompt_source_logged = True

    with st.chat_message("assistant", avatar="\U0001f393"):
        with st.spinner("SAGE is thinking..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                runner = client.beta.messages.tool_runner(
                    model="claude-opus-4-6",
                    max_tokens=16000,
                    system=SYSTEM_PROMPT,
                    tools=ALL_TOOLS,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
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

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ── Chat input ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Message SAGE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
