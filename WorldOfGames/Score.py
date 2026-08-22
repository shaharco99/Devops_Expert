import os

import pg8000.dbapi

# pg8000 is pure-python (no libpq/gcc needed on alpine, unlike psycopg2).
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
DB_NAME = os.environ.get("POSTGRES_DB", "wog")
DB_USER = os.environ.get("POSTGRES_USER", "wog")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "wog")


def _get_connection():
    conn = pg8000.dbapi.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, value INTEGER NOT NULL)"
    )
    cur.execute("SELECT value FROM scores WHERE id = 1")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO scores (id, value) VALUES (1, 0)")
    conn.commit()
    cur.close()
    return conn


def add_score(diff):
    """add the points_of_winning to score"""
    points = (diff * 3) + 5
    conn = _get_connection()
    try:
        cur = conn.cursor()
        # Atomic increment in a single statement - avoids the read-then-write
        # race a Python-side "read score, add, write score" would have under
        # concurrent calls (verified: with a separate read+write, 20 concurrent
        # add_score(1) calls lost most of their updates; this doesn't).
        cur.execute("UPDATE scores SET value = value + %s WHERE id = 1", (points,))
        cur.execute("SELECT value FROM scores WHERE id = 1")
        new_score = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"your new score is {new_score}")
    finally:
        conn.close()


def read_score():
    """read the score"""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT value FROM scores WHERE id = 1")
        row = cur.fetchone()
        cur.close()
        return row[0]
    finally:
        conn.close()
