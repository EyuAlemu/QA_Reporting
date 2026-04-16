from __future__ import annotations

import streamlit as st

from components.ai_panels import api_key_helper, render_analysis_placeholder, render_chat_history
from config import CHAT_HISTORY_LIMIT, OPENAI_API_KEY
from database.db import read_table
from services.metrics_service import build_dashboard_dataset
from services.openai_service import ask_dashboard_chat, generate_program_analysis, is_openai_configured


def page() -> None:
    st.markdown("## AI Analysis & Chatbot")
    st.caption("Use OpenAI to generate release insights and chat with the QA dashboard data.")

    cycles_df = read_table("test_cycles")
    defects_df = read_table("defects")
    dataset = build_dashboard_dataset(cycles_df, defects_df)

    entered_key = api_key_helper(default_configured=is_openai_configured())
    effective_key = entered_key or OPENAI_API_KEY

    tab1, tab2 = st.tabs(["AI Analysis", "QA Copilot Chat"])

    with tab1:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.markdown("### Analysis inputs")
            st.write("The AI will analyze the current dashboard snapshot, including KPIs, cycles, defects, trends, and root causes.")
            st.json(dataset["kpis"])
            if st.button("Generate AI Analysis", type="primary"):
                if not is_openai_configured(effective_key):
                    st.error("Provide an OpenAI API key in the sidebar or set OPENAI_API_KEY before generating analysis.")
                else:
                    with st.spinner("Generating AI analysis..."):
                        try:
                            analysis = generate_program_analysis(dataset, api_key=effective_key)
                            st.session_state["qa_ai_analysis"] = analysis
                        except Exception as exc:
                            st.error(f"AI analysis failed: {exc}")
        with right:
            st.markdown("### Latest output")
            if st.session_state.get("qa_ai_analysis"):
                st.markdown(st.session_state["qa_ai_analysis"])
            else:
                render_analysis_placeholder()

    with tab2:
        st.markdown("### Ask the QA Copilot")
        st.write("Examples: Which cycle is riskiest? Why is pass rate low? What actions should the team take this week?")
        history = st.session_state.setdefault("qa_chat_history", [])
        render_chat_history(history)

        prompt = st.chat_input("Ask about test execution, pass rate, defects, or release readiness")
        if prompt:
            if not is_openai_configured(effective_key):
                st.error("Provide an OpenAI API key in the sidebar or set OPENAI_API_KEY before using chat.")
                return
            history.append({"role": "user", "content": prompt})
            trimmed_history = history[-CHAT_HISTORY_LIMIT:]
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = ask_dashboard_chat(prompt, dataset, trimmed_history[:-1], api_key=effective_key)
                    except Exception as exc:
                        answer = f"AI chat failed: {exc}"
                    st.markdown(answer)
            history.append({"role": "assistant", "content": answer})
            st.session_state["qa_chat_history"] = history[-(CHAT_HISTORY_LIMIT * 2):]

        if st.button("Clear chat history"):
            st.session_state["qa_chat_history"] = []
            st.success("Chat history cleared.")
