# from datetime import datetime

# # =========================================================
# # test_execution Table Sample Data
# # Matches:
# # (
# #   testcycle_id, environment, source_filename,
# #   planned_test_cases, total_executed_test_cases,
# #   total_not_executed, total_passed_test_cases,
# #   total_failed_test_cases, critical_test_cases,
# #   non_critical_test_cases, blocked_test_cases,
# #   deferred_test_cases, scope_executed_pct,
# #   scope_pending_pct, outof_scope_testcases,
# #   active_flag, created_ts
# # )
# # =========================================================
# TEST_EXECUTION = [
#     (
#         "TC001",
#         "SIT",
#         "procurement_cycle_ii.xlsx",
#         120,
#         120,
#         0,
#         103,
#         10,
#         3,
#         107,
#         3,
#         4,
#         100.0,
#         0.0,
#         0,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC002",
#         "SIT",
#         "accounts_payable.xlsx",
#         85,
#         85,
#         0,
#         82,
#         2,
#         1,
#         84,
#         0,
#         1,
#         100.0,
#         0.0,
#         0,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC003",
#         "SIT",
#         "accounts_receivable.xlsx",
#         70,
#         70,
#         0,
#         27,
#         34,
#         4,
#         66,
#         4,
#         5,
#         100.0,
#         0.0,
#         0,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC004",
#         "UAT",
#         "fixed_assets.xlsx",
#         45,
#         37,
#         8,
#         33,
#         2,
#         1,
#         44,
#         1,
#         1,
#         82.0,
#         18.0,
#         2,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC005",
#         "SIT",
#         "inventory.xlsx",
#         55,
#         55,
#         0,
#         49,
#         3,
#         1,
#         54,
#         1,
#         2,
#         100.0,
#         0.0,
#         0,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC006",
#         "UAT",
#         "expenses.xlsx",
#         30,
#         30,
#         0,
#         26,
#         2,
#         1,
#         29,
#         1,
#         1,
#         100.0,
#         0.0,
#         0,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ),
#     (
#         "TC007",
#         "UAT",
#         "cash_management.xlsx",
#         25,
#         0,
#         25,
#         0,
#         0,
#         0,
#         25,
#         0,
#         25,
#         0.0,
#         100.0,
#         5,
#         1,
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     )
# ]

# # =========================================================
# # testcase_details Table Sample Data
# # Matches:
# # (
# #   test_scenario_id, testcycle_id, test_case_number,
# #   test_step_status, passfailstatus, numdefects,
# #   tester, module, executed, not_executed,
# #   executed_flag, clarification_flag,
# #   testcase_status, pass_percentage
# # )
# # =========================================================
# TESTCASE_DETAILS = [
#     ("TS001", "TC001", "PROC-001", "Completed", "Pass", 0, "John", "Procurement", 1, 0, 1, 0, "Closed", 100.0),
#     ("TS002", "TC001", "PROC-002", "Completed", "Fail", 2, "John", "Procurement", 1, 0, 1, 1, "Blocked", 0.0),
#     ("TS003", "TC001", "PROC-003", "Completed", "Pass", 0, "Emily", "Procurement", 1, 0, 1, 0, "Closed", 100.0),
#     ("TS004", "TC002", "AP-001", "Completed", "Pass", 0, "Sarah", "Accounts Payable", 1, 0, 1, 0, "Closed", 100.0),
#     ("TS005", "TC002", "AP-002", "Completed", "Fail", 1, "Sarah", "Accounts Payable", 1, 0, 1, 0, "Retest", 50.0),
#     ("TS006", "TC003", "AR-001", "Completed", "Fail", 3, "David", "Accounts Receivable", 1, 0, 1, 1, "Open", 25.0),
#     ("TS007", "TC003", "AR-002", "Completed", "Fail", 2, "David", "Accounts Receivable", 1, 0, 1, 1, "Open", 40.0),
#     ("TS008", "TC004", "FA-001", "Completed", "Pass", 0, "Emma", "Fixed Assets", 1, 0, 1, 0, "Closed", 100.0),
#     ("TS009", "TC004", "FA-002", "Completed", "Fail", 1, "Emma", "Fixed Assets", 1, 0, 1, 0, "Open", 50.0),
#     ("TS010", "TC005", "INV-001", "Completed", "Pass", 0, "Mike", "Inventory", 1, 0, 1, 0, "Closed", 100.0),
#     ("TS011", "TC005", "INV-002", "Completed", "Fail", 1, "Mike", "Inventory", 1, 0, 1, 0, "Open", 60.0),
#     ("TS012", "TC006", "EXP-001", "Completed", "Fail", 1, "Sophia", "Expenses", 1, 0, 1, 0, "Open", 60.0),
#     ("TS013", "TC007", "CM-001", "Not Started", "Not Executed", 0, "Chris", "Cash Management", 0, 1, 0, 0, "Pending", 0.0)
# ]

# # =========================================================
# # defects Table Sample Data
# # Matches:
# # (
# #   defect_id, cycle_name, scenario_id,
# #   testCase_id, severity, status,
# #   root_cause, discovered_week
# # )
# # =========================================================
# DEFECTS = [
#     ("DF001", "Procurement Cycle II", "TS002", "PROC-002", "Medium", "Fixed, in Retest", "Configuration issue", "2026-W08"),
#     ("DF002", "Accounts Payable", "TS005", "AP-002", "High", "Open", "Test script issue", "2026-W08"),
#     ("DF003", "Accounts Receivable", "TS006", "AR-001", "Critical", "Open", "Code defect", "2026-W09"),
#     ("DF004", "Fixed Assets", "TS009", "FA-002", "Medium", "Closed/Deferred", "Business rule gap", "2026-W09"),
#     ("DF005", "Inventory", "TS011", "INV-002", "High", "Open", "Data issue", "2026-W07"),
#     ("DF006", "Expenses", "TS012", "EXP-001", "Medium", "Open", "Code defect", "2026-W06"),
#     ("DF007", "Accounts Payable", "TS005", "AP-002", "Medium", "Fixed, in Retest", "Environment issue", "2026-W09"),
#     ("DF008", "Cash Management", "TS013", "CM-001", "Low", "Closed/Deferred", "Configuration issue", "2026-W10"),
#     ("DF009", "Accounts Receivable", "TS007", "AR-002", "Medium", "Open", "Code defect", "2026-W09"),
#     ("DF010", "Procurement Cycle II", "TS002", "PROC-002", "Low", "Closed/Deferred", "Test data issue", "2026-W08")
# ]

# # =========================================================
# # alerts Table Sample Data
# # Matches:
# # (
# #   AlertId, message, priority, is_active
# # )
# # =========================================================
# ALERTS = [
#     ("ALT001", "Cash Management start date deferred to 2/26 to refine test cases.", "High", "Yes"),
#     ("ALT002", "Accounts Receivable pass rate below target threshold.", "High", "Yes"),
#     ("ALT003", "Open high-severity defects require triage before go-live readiness review.", "Medium", "Yes"),
#     ("ALT004", "Fixed Assets has low scope coverage and pending execution.", "Medium", "Yes")
# ]
