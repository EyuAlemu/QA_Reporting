import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Delete the CYC-0010 row
cursor.execute("DELETE FROM test_execution WHERE environment = 'CYC-0010'")
conn.commit()

print("Deleted CYC-0010 row")

# Verify deletion
cursor.execute("SELECT COUNT(*) as count FROM test_execution WHERE environment = 'CYC-0010'")
result = cursor.fetchone()
print(f'Remaining CYC-0010 rows: {result[0]}')

# Show all remaining environments
cursor.execute("SELECT DISTINCT environment FROM test_execution ORDER BY environment")
environments = cursor.fetchall()
print('\nRemaining environments:')
for row in environments:
    print(f'  - {row[0]}')

conn.close()
