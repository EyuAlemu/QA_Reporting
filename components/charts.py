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
SCOPE_COLOR_MAP = {
    "Executed": "#0B73CE",
    "Pending": "#F59C6F",
}
ROOT_CAUSE_COLOR_SEQUENCE = [
    "#0B73CE",
    "#EC4E4E",
    "#F59C6F",
    "#7C3AED",
    "#10B981",
    "#F59E0B",
    "#14B8A6",
    "#DB2777",
    "#64748B",
]
CHART_TITLE_FONT = {"size": 18, "color": "#111827"}


def gauge_chart(value: float, title: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            domain={"x": [0, 1], "y": [0, 0.86]},
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
    fig.update_layout(
        title={"text": f"<b>{title}</b>", "x": 0.5, "xanchor": "center", "font": CHART_TITLE_FONT},
        height=320,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def scope_coverage_donut(cycles: pd.DataFrame) -> go.Figure:
    executed = cycles["scope_executed_pct"].mean()
    pending = max(0, 100 - executed)

    fig = go.Figure(
        go.Pie(
            labels=["Executed", "Pending"],
            values=[executed, pending],
            hole=0.64,
            domain={"x": [0.04, 0.78], "y": [0.06, 0.92]},
            marker={"colors": [SCOPE_COLOR_MAP["Executed"], SCOPE_COLOR_MAP["Pending"]]},
            textinfo="percent",
            textposition="inside",
            textfont=dict(size=14, color="#FFFFFF"),
            insidetextorientation="horizontal",
            hovertemplate="<b>%{label}</b><br>%{value:.1f}% of scope<extra></extra>",
            sort=False,
            direction="clockwise",
            rotation=90,
            pull=[0, 0],
        )
    )
    fig.update_layout(
        title={"text": "<b>Scope Coverage</b>", "x": 0.5, "xanchor": "center", "font": CHART_TITLE_FONT},
        height=320,
        margin=dict(l=20, r=90, t=60, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.9,
            font=dict(size=13),
        ),
        annotations=[
            dict(
                text=(
                    f"<b>{executed:.1f}%</b>"
                    "<br><span style='font-size:13px;color:#667085'>Executed</span>"
                ),
                x=0.43,
                y=0.49,
                font=dict(size=28, color="#111827"),
                showarrow=False,
            )
        ],
    )
    return fig


def dual_scope_donut(cycles: pd.DataFrame) -> go.Figure:
    return scope_coverage_donut(cycles)


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
        title={"text": "<b>Defects by Severity & Cycle</b>", "x": 0.5, "xanchor": "center", "font": CHART_TITLE_FONT},
        height=320,
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis_title="Cycle",
        yaxis_title="Defects",
    )
    return fig


def defects_by_status(defect_status: pd.DataFrame) -> go.Figure:
    status_label_map = {
        "Resolved": "Closed/Deferred",
        "In Progress": "Fixed, in Retest",
        "Open": "Open",
    }
    status_order = ["Open", "Fixed, in Retest", "Closed/Deferred"]

    defect_status = defect_status.copy()
    defect_status["status"] = defect_status["status"].replace(status_label_map)
    pivoted = defect_status.pivot_table(
        index="status",
        columns="severity",
        values="count",
        aggfunc="sum",
        fill_value=0,
    )
    pivoted = pivoted.reindex(status_order, fill_value=0)
    for sev in SEVERITY_ORDER:
        if sev not in pivoted.columns:
            pivoted[sev] = 0
    pivoted = pivoted[SEVERITY_ORDER].reset_index()
    max_status_total = pivoted[SEVERITY_ORDER].sum(axis=1).max()

    fig = go.Figure()
    for sev in SEVERITY_ORDER:
        label_color = "#FFFFFF" if sev in ["Critical", "High"] else "#374151"
        fig.add_bar(
            x=pivoted[sev],
            y=pivoted["status"],
            name=sev,
            orientation="h",
            marker_color=SEVERITY_COLOR_MAP[sev],
            text=pivoted[sev].replace(0, ""),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color=label_color, size=13),
        )
    fig.update_layout(
        barmode="stack",
        title={"text": "<b>Defects by Status & Priority</b>", "x": 0.5, "xanchor": "center", "font": CHART_TITLE_FONT},
        height=340,
        margin=dict(l=96, r=124, t=62, b=56),
        xaxis_title=dict(text="Defects", font=dict(size=15, color="#667085")),
        yaxis_title="",
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.58,
            xanchor="left",
            x=1.04,
            traceorder="normal",
            font=dict(size=14),
        ),
        font=dict(size=14, color="#667085"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        bargap=0.48,
    )
    fig.update_xaxes(
        range=[0, max(10, max_status_total + 1)],
        dtick=10,
        showgrid=True,
        gridcolor="#E1E7EF",
        zeroline=False,
        showline=True,
        linecolor="#CBD5E1",
        linewidth=1,
        ticks="outside",
        showticklabels=False,
        tickfont=dict(size=14, color="#667085"),
    )
    fig.update_yaxes(
        showgrid=False,
        showline=True,
        linecolor="#CBD5E1",
        linewidth=1,
        ticks="outside",
        ticklen=6,
        tickcolor="#CBD5E1",
        tickfont=dict(size=14, color="#667085"),
        ticklabelstandoff=4,
        categoryorder="array",
        categoryarray=status_order,
    )
    return fig


def root_cause_chart(root_cause: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        root_cause,
        x="count",
        y="root_cause",
        color="root_cause",
        color_discrete_sequence=ROOT_CAUSE_COLOR_SEQUENCE,
        orientation="h",
        title="Defects by Root Cause",
        text="count",
    )
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis_title="",
        showlegend=False,
    )
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
