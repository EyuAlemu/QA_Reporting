from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]
SEVERITY_COLOR_MAP = {
    "Critical": "#EC4E4E",
    "High": "#F56F6F",
    "Medium": "#F59C6F",
    "Low": "#E4DB6A",
    "Critical+High": "#ff7875",
}


def gauge_chart(value: float, title: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#5b8ff9"},
                "steps": [
                    {"range": [0, 50], "color": "#fff1f0"},
                    {"range": [50, 80], "color": "#fff7e6"},
                    {"range": [80, 100], "color": "#f6ffed"},
                ],
            },
        )
    )
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def dual_scope_donut(cycles: pd.DataFrame) -> go.Figure:
    executed = cycles["scope_executed_pct"].mean()
    pending = max(0, 100 - executed)

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=["Executed", "Pending"],
            values=[executed, pending],
            hole=0.55,
            domain={"x": [0.0, 0.45], "y": [0.1, 0.9]},
            title="Executed",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Pie(
            labels=["Pending", "Executed"],
            values=[pending, executed],
            hole=0.55,
            domain={"x": [0.55, 1.0], "y": [0.1, 0.9]},
            title="Pending",
            showlegend=False,
        )
    )
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=10), title="Scope Coverage")
    return fig


def defects_by_severity_and_cycle(defects_per_cycle: pd.DataFrame) -> go.Figure:
    pivoted = defects_per_cycle.pivot(index="cycle_name", columns="severity", values="count").fillna(0)
    for sev in SEVERITY_ORDER:
        if sev not in pivoted.columns:
            pivoted[sev] = 0
    pivoted = pivoted[SEVERITY_ORDER].reset_index()

    fig = go.Figure()
    for sev in SEVERITY_ORDER:
        fig.add_bar(
            x=pivoted["cycle_name"],
            y=pivoted[sev],
            name=sev,
            marker_color=SEVERITY_COLOR_MAP[sev],
        )
    fig.update_layout(
        barmode="group",
        title="Defects by Severity & Cycle",
        height=320,
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis_title="Cycle",
        yaxis_title="Defects",
    )
    return fig


def defects_by_status(defect_status: pd.DataFrame) -> go.Figure:
    pivoted = defect_status.pivot(index="status", columns="severity", values="count").fillna(0)
    for sev in SEVERITY_ORDER:
        if sev not in pivoted.columns:
            pivoted[sev] = 0
    pivoted = pivoted[SEVERITY_ORDER].reset_index()

    fig = go.Figure()
    for sev in SEVERITY_ORDER:
        fig.add_bar(
            x=pivoted["status"],
            y=pivoted[sev],
            name=sev,
            marker_color=SEVERITY_COLOR_MAP[sev],
        )
    fig.update_layout(
        barmode="stack",
        title="Defects by Severity & Status",
        height=300,
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis_title="Status",
        yaxis_title="Count",
    )
    return fig


def root_cause_chart(root_cause: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        root_cause,
        x="count",
        y="root_cause",
        orientation="h",
        title="Defects by Root Cause",
        text="count",
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), yaxis_title="")
    return fig


def test_execution_chart(cycles: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        cycles.sort_values("execution_pct", ascending=False),
        x="cycle_name",
        y="execution_pct",
        color="cycle_name",
        text="execution_pct",
        title="Test Execution by Cycle",
    )
    fig.update_traces(texttemplate="%{text:.1f}%")
    fig.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=50, b=40))
    return fig


def pass_rate_chart(cycles: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        cycles.sort_values("pass_rate_pct", ascending=False),
        x="cycle_name",
        y="pass_rate_pct",
        color="cycle_name",
        text="pass_rate_pct",
        title="Pass Rate by Cycle",
    )
    fig.update_traces(texttemplate="%{text:.1f}%")
    fig.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=50, b=40))
    return fig


def defect_trend_chart(weekly_discovery: pd.DataFrame) -> go.Figure:
    fig = px.line(
        weekly_discovery,
        x="discovered_week",
        y="defects_found",
        markers=True,
        title="Error Discovery Trend",
    )
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=20), xaxis_title="Week", yaxis_title="Defects")
    return fig
