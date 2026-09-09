"""SQLite storage for weekly pulls (roster, settings, projections)."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "fbd_agent.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS weekly_pulls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id TEXT NOT NULL,
    week INTEGER NOT NULL,
    pulled_at TEXT NOT NULL,
    raw_roster_json TEXT NOT NULL,
    raw_projections_json TEXT NOT NULL
);
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn
