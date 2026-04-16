from __future__ import annotations

import streamlit as st

from components.charts import defect_trend_chart, defects_by_severity_and_cycle, defects_by_status, root_cause_chart
from database.db import read_table
from services.metrics_service import build_dashboard_dataset


def page() -> None:
    dataset = build_dashboard_dataset(read_table("test_cycles"), read_table("defects"))

    st.markdown("## Defect Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(defects_by_severity_and_cycle(dataset["defects_per_cycle"]), use_container_width=True)
    with col2:
        st.plotly_chart(defect_trend_chart(dataset["weekly_discovery"]), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(defects_by_status(dataset["defect_status"]), use_container_width=True)
    with col4:
        st.plotly_chart(root_cause_chart(dataset["root_cause"]), use_container_width=True)

    st.dataframe(dataset["defects"], use_container_width=True)
