import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get scope_executed_pct for each cycle
cursor.execute("SELECT environment, scope_executed_pct FROM test_execution ORDER BY environment")
rows = cursor.fetchall()

print('Scope Executed % for each cycle:')
total_pct = 0
count = 0
for row in rows:
    pct_str = row['scope_executed_pct']
    try:
        pct = float(pct_str.rstrip('%'))
        print(f'  {row["environment"]}: {pct}%')
        total_pct += pct
        count += 1
    except ValueError:
        print(f'  {row["environment"]}: {pct_str} (invalid)')

if count > 0:
    average = round(total_pct / count, 1)
    print(f'\nAverage scope_coverage_pct: {average}%')
else:
    print('\nNo valid percentages found.')

conn.close()
