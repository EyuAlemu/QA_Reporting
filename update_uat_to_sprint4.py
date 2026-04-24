import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check existing cycle names in defects table
print('Cycle names before update:')
cursor.execute("SELECT DISTINCT cycle_name FROM defects ORDER BY cycle_name")
cycles = cursor.fetchall()
for row in cycles:
    print(f'  - {row[0]}')

# Count UAT defects
cursor.execute("SELECT COUNT(*) as count FROM defects WHERE cycle_name = 'UAT'")
result = cursor.fetchone()
uat_count = result[0]
print(f'\nUAT defects to update: {uat_count}')

# Update UAT to Sprint 4
cursor.execute("UPDATE defects SET cycle_name = 'Sprint 4' WHERE cycle_name = 'UAT'")
conn.commit()

print(f"Updated {cursor.rowcount} defect records from UAT to Sprint 4")

# Verify update
print('\nCycle names after update:')
cursor.execute("SELECT DISTINCT cycle_name FROM defects ORDER BY cycle_name")
cycles = cursor.fetchall()
for row in cycles:
    count_cursor = conn.cursor()
    count_cursor.execute("SELECT COUNT(*) as count FROM defects WHERE cycle_name = ?", (row[0],))
    count = count_cursor.fetchone()[0]
    print(f'  - {row[0]}: {count} defects')

conn.close()
