import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check current SIT data
print('SIT row before update:')
cursor.execute("SELECT * FROM test_execution WHERE environment = 'SIT'")
row = cursor.fetchone()
if row:
    print(f'  total_executed_test_cases: {row["total_executed_test_cases"]}')

# Update SIT executed_test_cases from 36 to 35
cursor.execute("UPDATE test_execution SET total_executed_test_cases = 35 WHERE environment = 'SIT' AND total_executed_test_cases = 36")
conn.commit()

print(f"Updated {cursor.rowcount} SIT record(s)")

# Verify update
print('\nSIT row after update:')
cursor.execute("SELECT * FROM test_execution WHERE environment = 'SIT'")
row = cursor.fetchone()
if row:
    print(f'  total_executed_test_cases: {row["total_executed_test_cases"]}')

conn.close()
