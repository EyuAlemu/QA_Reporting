import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "metrics.db"

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('All UAT test_execution rows (complete data):')
cursor.execute("SELECT * FROM test_execution WHERE environment = 'UAT' ORDER BY testcycle_id")
rows = cursor.fetchall()

for i, row in enumerate(rows):
    print(f'\nRow {i+1}:')
    for key in row.keys():
        print(f'  {key}: {row[key]}')

conn.close()
