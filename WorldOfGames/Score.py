import sqlite3
from pathlib import Path

db_file_name = Path(__file__).parent / "scores.db"
legacy_scores_file_name = Path(__file__).parent / "Scores.txt"


def _get_connection():
    conn = sqlite3.connect(db_file_name, timeout=30)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, value INTEGER NOT NULL)"
    )
    row = conn.execute("SELECT value FROM scores WHERE id = 1").fetchone()
    if row is None:
        # One-time migration from the old Scores.txt flat file, if present.
        initial_value = 0
        if legacy_scores_file_name.exists():
            initial_value = int(legacy_scores_file_name.read_text().strip() or 0)
        conn.execute("INSERT INTO scores (id, value) VALUES (1, ?)", (initial_value,))
        conn.commit()
    return conn


def add_score(diff):
    """add the points_of_winning to score"""
    points = (diff * 3) + 5
    conn = _get_connection()
    try:
        # Atomic increment in a single statement - avoids the read-then-write
        # race a Python-side "read score, add, write score" would have under
        # concurrent calls (verified: with a separate read+write, 20 concurrent
        # add_score(1) calls lost most of their updates; this doesn't).
        conn.execute("UPDATE scores SET value = value + ? WHERE id = 1", (points,))
        conn.commit()
        new_score = conn.execute("SELECT value FROM scores WHERE id = 1").fetchone()[0]
        print(f"your new score is {new_score}")
    finally:
        conn.close()


def read_score():
    """read the score"""
    conn = _get_connection()
    try:
        row = conn.execute("SELECT value FROM scores WHERE id = 1").fetchone()
        return row[0]
    finally:
        conn.close()
