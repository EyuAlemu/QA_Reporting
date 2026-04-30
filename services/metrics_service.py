from __future__ import annotations

import pandas as pd

SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]
ROOT_CAUSE_ORDER = ["Code", "Stored Proc", "UI", "Environment", "Configuration", "Database"]
ROOT_CAUSE_LABEL_MAP = {
    "Code defect": "Code",
    "Null pointer exception in auth module": "Code",
    "Session timeout not handled correctly": "Code",
    "Checkout total calculation rounding error": "Code",
    "Test script issue": "Code",
    "Payment gateway timeout on large amounts": "Stored Proc",
    "UI label mismatch on confirmation screen": "UI",
    "Login page not loading on Safari browser": "UI",
    "Export to PDF missing header row": "UI",
    "Environment issue": "Environment",
    "Configuration issue": "Configuration",
    "Business rule gap": "Configuration",
    "Report filter returns incorrect date range": "Database",
    "Data issue": "Database",
    "Test data issue": "Database",
}
STATUS_ORDER = ["Open", "Fixed, in Retest", "Closed/Deferred"]
STATUS_LABEL_MAP = {
    "Resolved": "Closed/Deferred",
    "Closed": "Closed/Deferred",
    "Deferred": "Closed/Deferred",
    "In Progress": "Fixed, in Retest",
    "Fixed": "Fixed, in Retest",
    "Fixed in Retest": "Fixed, in Retest",
}


def build_dashboard_dataset(cycles_df: pd.DataFrame, defects_df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float | int]]:
    cycles = cycles_df.copy()
    defects = defects_df.copy()
    if "status" in defects.columns:
        defects["status"] = defects["status"].replace(STATUS_LABEL_MAP)
    if "root_cause" in defects.columns:
        defects["root_cause"] = defects["root_cause"].replace(ROOT_CAUSE_LABEL_MAP)

    # Support metrics.db column naming
    if "total_executed_test_cases" in cycles.columns:
        cycles["executed_test_cases"] = pd.to_numeric(cycles["total_executed_test_cases"], errors="coerce").fillna(0)
    if "total_passed_test_cases" in cycles.columns:
        cycles["passed_test_cases"] = pd.to_numeric(cycles["total_passed_test_cases"], errors="coerce").fillna(0)
    if "total_failed_test_cases" in cycles.columns:
        cycles["failed_test_cases"] = pd.to_numeric(cycles["total_failed_test_cases"], errors="coerce").fillna(0)
    if "environment" in cycles.columns and "cycle_name" not in cycles.columns:
        cycles["cycle_name"] = cycles["environment"]

    numeric_columns = [
        "planned_test_cases",
        "executed_test_cases",
        "passed_test_cases",
        "failed_test_cases",
        "blocked_test_cases",
        "deferred_test_cases",
        "total_not_executed",
        "outof_scope_testcases",
    ]
    for col in numeric_columns:
        if col in cycles.columns:
            cycles[col] = pd.to_numeric(cycles[col], errors="coerce").fillna(0)

    if "scope_executed_pct" in cycles.columns:
        cycles["scope_executed_pct"] = pd.to_numeric(cycles["scope_executed_pct"].astype(str).str.rstrip("%"), errors="coerce").fillna(0)
    if "scope_pending_pct" in cycles.columns:
        cycles["scope_pending_pct"] = pd.to_numeric(cycles["scope_pending_pct"].astype(str).str.rstrip("%"), errors="coerce").fillna(0)

    # Old column naming for sample DB
    # cycles["pass_rate_pct"] = (
    #     cycles["passed_test_cases"] / cycles["executed_test_cases"].replace(0, pd.NA)
    # ) * 100
    # cycles["execution_pct"] = (
    #     cycles["executed_test_cases"] / cycles["planned_test_cases"].replace(0, pd.NA)
    # ) * 100

    cycles["pass_rate_pct"] = (
        cycles["passed_test_cases"] / cycles["executed_test_cases"].replace(0, pd.NA)
    ) * 100
    cycles["execution_pct"] = (
        cycles["executed_test_cases"] / cycles["planned_test_cases"].replace(0, pd.NA)
    ) * 100
    cycles = cycles.fillna(0)

    defects_per_cycle = defects.groupby(["cycle_name", "severity"]).size().reset_index(name="count")
    status_index = pd.MultiIndex.from_product([STATUS_ORDER, SEVERITY_ORDER], names=["status", "severity"])
    defect_status = defects.groupby(["status", "severity"]).size().reindex(status_index, fill_value=0).reset_index(name="count")
    root_cause = defects.groupby("root_cause").size().reindex(ROOT_CAUSE_ORDER, fill_value=0).reset_index(name="count")
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
    for sev in SEVERITY_ORDER:
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
