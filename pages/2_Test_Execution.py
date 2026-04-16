from __future__ import annotations

import streamlit as st

from components.charts import pass_rate_chart, test_execution_chart
from database.db import read_table
from services.metrics_service import build_dashboard_dataset


def page() -> None:
    dataset = build_dashboard_dataset(read_table("test_cycles"), read_table("defects"))
    cycles = dataset["cycles"]

    st.markdown("## Test Execution and Pass Rate")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(test_execution_chart(cycles), use_container_width=True)
    with col2:
        st.plotly_chart(pass_rate_chart(cycles), use_container_width=True)

    st.dataframe(
        cycles[[
            "cycle_name", "planned_test_cases", "executed_test_cases", "passed_test_cases",
            "failed_test_cases", "blocked_test_cases", "deferred_test_cases",
            "execution_pct", "pass_rate_pct", "scope_executed_pct", "scope_pending_pct"
        ]],
        use_container_width=True,
    )
