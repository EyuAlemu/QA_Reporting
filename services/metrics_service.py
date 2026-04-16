from __future__ import annotations

import pandas as pd


def build_dashboard_dataset(cycles_df: pd.DataFrame, defects_df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float | int]]:
    cycles = cycles_df.copy()
    defects = defects_df.copy()

    cycles["pass_rate_pct"] = (
        cycles["passed_test_cases"] / cycles["executed_test_cases"].replace(0, pd.NA)
    ) * 100
    cycles["execution_pct"] = (
        cycles["executed_test_cases"] / cycles["planned_test_cases"].replace(0, pd.NA)
    ) * 100
    cycles = cycles.fillna(0)

    defects_per_cycle = defects.groupby(["cycle_name", "severity"]).size().reset_index(name="count")
    defect_status = defects.groupby(["status", "severity"]).size().reset_index(name="count")
    root_cause = defects.groupby("root_cause").size().reset_index(name="count").sort_values("count", ascending=True)
    weekly_discovery = defects.groupby("discovered_week").size().reset_index(name="defects_found")

    total_planned = int(cycles["planned_test_cases"].sum())
    total_executed = int(cycles["executed_test_cases"].sum())
    total_passed = int(cycles["passed_test_cases"].sum())
    total_defects = int(len(defects))

    pass_rate = round((total_passed / total_executed) * 100, 1) if total_executed else 0.0
    execution_rate = round((total_executed / total_planned) * 100, 1) if total_planned else 0.0
    error_discovery_rate = round((total_defects / total_executed) * 100, 1) if total_executed else 0.0
    scope_coverage = round(cycles["scope_executed_pct"].mean(), 1) if not cycles.empty else 0.0
    closed_count = int(defects[defects["status"] == "Closed/Deferred"].shape[0])
    deferred_count = int(cycles["deferred_test_cases"].sum())

    severity_totals = defects.groupby("severity").size().to_dict()
    for sev in ["Critical", "High", "Medium", "Low"]:
        severity_totals.setdefault(sev, 0)

    kpis = {
        "total_test_cases": total_planned,
        "executed_test_cases": total_executed,
        "pass_rate_pct": pass_rate,
        "execution_rate_pct": execution_rate,
        "error_discovery_rate_pct": error_discovery_rate,
        "scope_coverage_pct": scope_coverage,
        "total_defects": total_defects,
        "closed_defects": closed_count,
        "deferred_tests": deferred_count,
        **{f"severity_{k.lower()}": int(v) for k, v in severity_totals.items()},
    }

    return {
        "cycles": cycles,
        "defects": defects,
        "defects_per_cycle": defects_per_cycle,
        "defect_status": defect_status,
        "root_cause": root_cause,
        "weekly_discovery": weekly_discovery,
        "kpis": kpis,
    }
