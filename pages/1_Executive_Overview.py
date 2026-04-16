from __future__ import annotations

import streamlit as st

from components.charts import (
    defects_by_severity_and_cycle,
    defects_by_status,
    dual_scope_donut,
    gauge_chart,
    root_cause_chart,
)
from components.kpi_cards import render_top_metrics
from database.db import read_table
from services.metrics_service import build_dashboard_dataset
from config import AS_OF_DATE, PROGRAM_NAME


def page() -> None:
    cycles_df = read_table("test_cycles")
    defects_df = read_table("defects")
    alerts_df = read_table("alerts")
    dataset = build_dashboard_dataset(cycles_df, defects_df)
    kpis = dataset["kpis"]

    st.markdown(f"## {PROGRAM_NAME} Functional Testing Dashboard Overview")
    st.caption(f"As of {AS_OF_DATE}")
    render_top_metrics(kpis)

    row1_col1, row1_col2, row1_col3 = st.columns([1.0, 1.2, 1.5])
    with row1_col1:
        st.plotly_chart(gauge_chart(kpis["error_discovery_rate_pct"], "Error Discovery Rate"), use_container_width=True)
    with row1_col2:
        st.plotly_chart(dual_scope_donut(dataset["cycles"]), use_container_width=True)
    with row1_col3:
        st.plotly_chart(defects_by_severity_and_cycle(dataset["defects_per_cycle"]), use_container_width=True)

    row2_col1, row2_col2, row2_col3 = st.columns([1.2, 1.0, 1.0])
    with row2_col1:
        st.plotly_chart(defects_by_status(dataset["defect_status"]), use_container_width=True)
    with row2_col2:
        st.plotly_chart(root_cause_chart(dataset["root_cause"]), use_container_width=True)
    with row2_col3:
        st.subheader("Alerts")
        active_alerts = alerts_df[alerts_df["is_active"] == 1]
        if active_alerts.empty:
            st.success("No active alerts.")
        else:
            for _, row in active_alerts.iterrows():
                priority = row["priority"]
                message = row["message"]
                if priority == "High":
                    st.error(message)
                elif priority == "Medium":
                    st.warning(message)
                else:
                    st.info(message)
