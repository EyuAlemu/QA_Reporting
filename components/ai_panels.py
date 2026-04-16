from __future__ import annotations

import streamlit as st


def api_key_helper(default_configured: bool) -> str:
    st.sidebar.markdown("### AI Settings")
    if default_configured:
        st.sidebar.success("OPENAI_API_KEY found in environment")
    else:
        st.sidebar.info("Add your OpenAI API key below or set OPENAI_API_KEY in the environment.")
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="sk-...", help="Used only for this session.")
    return api_key.strip()


def render_analysis_placeholder() -> None:
    st.info(
        "AI analysis is ready. Provide an OpenAI API key in the sidebar, then click Generate AI Analysis."
    )


def render_chat_history(messages: list[dict[str, str]]) -> None:
    for msg in messages:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.markdown(msg["content"])
