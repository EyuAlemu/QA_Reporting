from __future__ import annotations

import streamlit as st


def render_top_metrics(kpis: dict) -> None:
    col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.4, 1.0])

    with col1:
        st.metric("Test Execution %", f"{kpis['execution_rate_pct']}%")
        st.caption(f"Executed: {kpis['executed_test_cases']} / {kpis['total_test_cases']}")

    with col2:
        st.metric("Pass %", f"{kpis['pass_rate_pct']}%")
        st.caption("Passed / Executed")

    with col3:
        st.markdown("**Defect Stats**")
        st.markdown(f"<span style='color:#EC4E4E; font-weight: bold;'>Critical: {kpis['severity_critical']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#F56F6F; font-weight: bold;'>High: {kpis['severity_high']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#F59C6F; font-weight: bold;'>Medium: {kpis['severity_medium']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#E4DB6A; font-weight: bold;'>Low: {kpis['severity_low']}</span>", unsafe_allow_html=True)

    with col4:
        st.metric("Closed Defects", kpis["closed_defects"])
        st.metric("Deferred Tests", kpis["deferred_tests"])
