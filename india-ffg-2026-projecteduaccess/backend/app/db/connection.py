import os
import sqlite3
from pathlib import Path

from app.core.config import DATABASE_URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)


def get_database_path() -> str:
    if DATABASE_URL.startswith("sqlite"):
        sqlite_path = DATABASE_URL.replace("sqlite:///", "", 1)
        if not os.path.isabs(sqlite_path):
            sqlite_path = str(BASE_DIR / sqlite_path)
        return sqlite_path
    return DATABASE_URL


def get_connection():
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
