import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

from config import DB_PATH
# from utils.sample_data import TEST_EXECUTION, TESTCASE_DETAILS, DEFECTS, ALERTS


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(schema_path: Path | None = None) -> None:
    conn = get_connection()
    try:
        create_tables(conn)
        # seed_database(conn)
    finally:
        conn.close()


def create_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Test Execution Table
    # ---------------------------------------------------------
    # Old sample DB schema
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS test_execution (
    #         testcycle_id TEXT PRIMARY KEY,
    #         environment TEXT NOT NULL,
    #         source_filename TEXT NOT NULL,
    #         planned_test_cases INTEGER NOT NULL,
    #         total_executed_test_cases INTEGER NOT NULL,
    #         total_not_executed INTEGER,
    #         total_passed_test_cases INTEGER NOT NULL,
    #         total_failed_test_cases INTEGER NOT NULL,
    #         critical_test_cases INTEGER,
    #         non_critical_test_cases INTEGER,
    #         blocked_test_cases INTEGER,
    #         deferred_test_cases INTEGER,
    #         scope_executed_pct REAL,
    #         scope_pending_pct REAL,
    #         outof_scope_testcases INTEGER,
    #         active_flag BOOLEAN,
    #         created_ts DATETIME
    #     )
    #     """
    # )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_execution (
            testcycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            active_flag BOOLEAN,
            created_ts TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Test Suite Details Table
    # ---------------------------------------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS testsuite_details (
            test_scenario_id TEXT PRIMARY KEY,
            testcycle_id TEXT,
            test_case_number TEXT,
            test_step_status TEXT,
            passfailstatus TEXT,
            numdefects INTEGER,
            tester TEXT,
            module TEXT,
            executed INTEGER,
            not_executed INTEGER,
            executed_flag INTEGER,
            clarification_flag INTEGER,
            testcase_status TEXT,
            pass_percentage REAL,
            FOREIGN KEY (testcycle_id) REFERENCES test_execution(testcycle_id)
        )
        """
    )

    # ---------------------------------------------------------
    # Defects Table
    # ---------------------------------------------------------
    # Old sample DB schema
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS defects (
    #         defect_id TEXT PRIMARY KEY,
    #         cycle_name TEXT,
    #         scenario_id TEXT,
    #         testCase_id TEXT,
    #         severity TEXT,
    #         status TEXT,
    #         root_cause TEXT,
    #         discovered_week TEXT
    #     )
    #     """
    # )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS defects (
            defect_id TEXT PRIMARY KEY,
            cycle_name TEXT,
            scenario_id TEXT,
            testcase_id TEXT,
            severity TEXT,
            status TEXT,
            root_cause TEXT,
            discovered_week TEXT
        )
        """
    )

    # ---------------------------------------------------------
    # Alerts Table
    # ---------------------------------------------------------
    # Old sample DB schema
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS alerts (
    #         AlertId TEXT PRIMARY KEY,
    #         message TEXT,
    #         priority TEXT,
    #         is_active TEXT
    #     )
    #     """
    # )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id TEXT PRIMARY KEY,
            message TEXT,
            priority TEXT,
            is_active TEXT
        )
        """
    )

    conn.commit()


def seed_database(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Seed Test Execution Table
    # ---------------------------------------------------------
    execution_count = cursor.execute(
        "SELECT COUNT(*) FROM test_execution"
    ).fetchone()[0]

    if execution_count == 0:
        cursor.executemany(
            """
            INSERT INTO test_execution (
                testcycle_id,
                environment,
                source_filename,
                planned_test_cases,
                total_executed_test_cases,
                total_not_executed,
                total_passed_test_cases,
                total_failed_test_cases,
                critical_test_cases,
                non_critical_test_cases,
                blocked_test_cases,
                deferred_test_cases,
                scope_executed_pct,
                scope_pending_pct,
                outof_scope_testcases,
                active_flag,
                created_ts
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            TEST_EXECUTION,
        )

    # ---------------------------------------------------------
    # Seed Test Suite Details Table
    # ---------------------------------------------------------
    testsuite_count = cursor.execute(
        "SELECT COUNT(*) FROM testsuite_details"
    ).fetchone()[0]

    if testsuite_count == 0:
        cursor.executemany(
            """
            INSERT INTO testsuite_details (
                test_scenario_id,
                testcycle_id,
                test_case_number,
                test_step_status,
                passfailstatus,
                numdefects,
                tester,
                module,
                executed,
                not_executed,
                executed_flag,
                clarification_flag,
                testcase_status,
                pass_percentage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            TESTCASE_DETAILS,
        )

    # ---------------------------------------------------------
    # Seed Defects Table
    # ---------------------------------------------------------
    defect_count = cursor.execute(
        "SELECT COUNT(*) FROM defects"
    ).fetchone()[0]

    if defect_count == 0:
        # Old sample DB field name: testCase_id
        # cursor.executemany(
        #     """
        #     INSERT INTO defects (
        #         defect_id,
        #         cycle_name,
        #         scenario_id,
        #         testCase_id,
        #         severity,
        #         status,
        #         root_cause,
        #         discovered_week
        #     )
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        #     """,
        #     DEFECTS,
        # )
        cursor.executemany(
            """
            INSERT INTO defects (
                defect_id,
                cycle_name,
                scenario_id,
                testcase_id,
                severity,
                status,
                root_cause,
                discovered_week
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            DEFECTS,
        )

    # ---------------------------------------------------------
    # Seed Alerts Table
    # ---------------------------------------------------------
    alert_count = cursor.execute(
        "SELECT COUNT(*) FROM alerts"
    ).fetchone()[0]

    if alert_count == 0:
        # Old sample DB field name: AlertId
        # cursor.executemany(
        #     """
        #     INSERT INTO alerts (
        #         AlertId,
        #         message,
        #         priority,
        #         is_active
        #     )
        #     VALUES (?, ?, ?, ?)
        #     """,
        #     ALERTS,
        # )
        cursor.executemany(
            """
            INSERT INTO alerts (
                alert_id,
                message,
                priority,
                is_active
            )
            VALUES (?, ?, ?, ?)
            """,
            ALERTS,
        )

    conn.commit()


def read_table(table_name: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    finally:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> None:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()