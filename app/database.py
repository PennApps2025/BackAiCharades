import sqlite3
import os
from pathlib import Path
from app.models import Score

# Use an absolute path to the project root so the DB is always created
# next to the repository root (one level above the `app` package).
DB_NAME = str(Path(__file__).resolve().parent.parent / "leaderboard.db")

def init_db():
    # Ensure directory exists (should be repo root), create DB and table
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print(f"init_db: database initialized")


def reset_db():
    """Drop the leaderboard table if it exists and recreate it.

    Useful for tests or manual reinitialization. This keeps the DB file
    location consistent and only affects the schema.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS leaderboard")
    cur.execute("""
        CREATE TABLE leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"reset_db: database reset")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def submit_score(score: Score):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (score.username, score.score))

    conn.commit()
    conn.close()

def get_leaderboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT username, score 
        FROM leaderboard 
        ORDER BY score DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]