import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Delete the inactive UAT row (testcycle_id: 4)
cursor.execute("DELETE FROM test_execution WHERE testcycle_id = '4' AND environment = 'UAT'")
conn.commit()

print("Deleted UAT row with testcycle_id: 4")

# Verify deletion
cursor.execute("SELECT COUNT(*) as count FROM test_execution WHERE environment = 'UAT'")
result = cursor.fetchone()
print(f'Remaining UAT rows: {result[0]}')

# Show remaining UAT row
cursor.execute("SELECT testcycle_id, environment, planned_test_cases, source_filename FROM test_execution WHERE environment = 'UAT'")
remaining = cursor.fetchall()
for row in remaining:
    print(f'Remaining: {dict(row)}')

conn.close()
