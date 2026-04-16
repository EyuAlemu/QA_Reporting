CREATE TABLE IF NOT EXISTS test_execution (
    testcycle_id TEXT PRIMARY KEY,
    environment TEXT NOT NULL,
    source_filename TEXT NOT NULL,
    planned_test_cases INTEGER NOT NULL,
    total_executed_test_cases INTEGER NOT NULL,
    total_not_executed INTEGER,
    total_passed_test_cases INTEGER NOT NULL,
    total_failed_test_cases INTEGER NOT NULL,
    critical_test_cases INTEGER,
    non_critical_test_cases INTEGER,
    blocked_test_cases INTEGER,
    deferred_test_cases INTEGER,
    scope_executed_pct REAL,
    scope_pending_pct REAL,
    outof_scope_testcases INTEGER,
    active_flag INTEGER DEFAULT 1,
    created_ts DATETIME
);

CREATE TABLE IF NOT EXISTS testcase_details (
    test_scenario_id TEXT PRIMARY KEY,
    testcycle_id TEXT NOT NULL,
    test_case_number TEXT NOT NULL,
    test_step_status TEXT,
    passfailstatus TEXT,
    numdefects INTEGER DEFAULT 0,
    tester TEXT,
    module TEXT,
    executed INTEGER DEFAULT 0,
    not_executed INTEGER DEFAULT 0,
    executed_flag INTEGER DEFAULT 0,
    clarification_flag INTEGER DEFAULT 0,
    testcase_status TEXT,
    pass_percentage REAL,
    FOREIGN KEY (testcycle_id) REFERENCES test_execution(testcycle_id)
);

CREATE TABLE IF NOT EXISTS defects (
    defect_id TEXT PRIMARY KEY,
    cycle_name TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    testCase_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    root_cause TEXT NOT NULL,
    discovered_week TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    AlertId TEXT PRIMARY KEY,
    message TEXT NOT NULL,
    priority TEXT NOT NULL,
    is_active TEXT NOT NULL
);