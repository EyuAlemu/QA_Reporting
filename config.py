from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "qa_reporting.db"
APP_TITLE = "QA Functional Testing Dashboard"
PROGRAM_NAME = "AMPCUS Program"
AS_OF_DATE = "04/10/2026"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CHAT_HISTORY_LIMIT = 8
