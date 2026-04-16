from __future__ import annotations

import streamlit as st

from database.db import get_connection, read_table


def page() -> None:
    st.markdown("## Data Management")

    with st.expander("Add test cycle"):
        with st.form("add_cycle_form"):
            cycle_name = st.text_input("Cycle name")
            planned = st.number_input("Planned test cases", min_value=0, step=1)
            executed = st.number_input("Executed test cases", min_value=0, step=1)
            passed = st.number_input("Passed test cases", min_value=0, step=1)
            failed = st.number_input("Failed test cases", min_value=0, step=1)
            blocked = st.number_input("Blocked test cases", min_value=0, step=1)
            deferred = st.number_input("Deferred test cases", min_value=0, step=1)
            scope_executed = st.slider("Scope executed %", 0.0, 100.0, 80.0, 1.0)
            scope_pending = st.slider("Scope pending %", 0.0, 100.0, 20.0, 1.0)
            submitted = st.form_submit_button("Save cycle")
            if submitted and cycle_name:
                conn = get_connection()
                try:
                    conn.execute(
                        """
                        INSERT INTO test_cycles (
                            cycle_name, planned_test_cases, executed_test_cases, passed_test_cases,
                            failed_test_cases, blocked_test_cases, deferred_test_cases,
                            scope_executed_pct, scope_pending_pct, active_flag
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                        """,
                        (cycle_name, planned, executed, passed, failed, blocked, deferred, scope_executed, scope_pending),
                    )
                    conn.commit()
                    st.success("Test cycle added.")
                finally:
                    conn.close()

    with st.expander("Add defect"):
        with st.form("add_defect_form"):
            defect_title = st.text_input("Defect title")
            cycle_name = st.selectbox("Cycle", read_table("test_cycles")["cycle_name"].tolist())
            severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"])
            status = st.selectbox("Status", ["Open", "Fixed, in Retest", "Closed/Deferred"])
            root_cause = st.selectbox(
                "Root cause",
                ["Code defect", "Configuration issue", "Environment issue", "Data issue", "Test script issue", "Business rule gap", "Test data issue"],
            )
            week = st.text_input("Discovered week", value="2026-W10")
            submitted = st.form_submit_button("Save defect")
            if submitted and defect_title:
                conn = get_connection()
                try:
                    conn.execute(
                        """
                        INSERT INTO defects (defect_title, cycle_name, severity, status, root_cause, discovered_week)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (defect_title, cycle_name, severity, status, root_cause, week),
                    )
                    conn.commit()
                    st.success("Defect added.")
                finally:
                    conn.close()

    st.markdown("### Current data")
    st.write("#### Test Cycles")
    st.dataframe(read_table("test_cycles"), use_container_width=True)
    st.write("#### Defects")
    st.dataframe(read_table("defects"), use_container_width=True)
