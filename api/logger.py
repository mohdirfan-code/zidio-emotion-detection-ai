# api/logger.py

import sqlite3
from datetime import datetime

DB_PATH = "mood_logs.db"

# Initialize the SQLite database and table
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            raw_emotion TEXT,
            workplace_mood TEXT
        )
        """)
        conn.commit()

# Insert a new log into the database
def log_emotion(raw_emotion: str, workplace_mood: str):
    timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO emotion_logs (timestamp, raw_emotion, workplace_mood)
        VALUES (?, ?, ?)
        """, (timestamp, raw_emotion, workplace_mood))
        conn.commit()

# Check for 3 of last 5 logs being stress-related
def should_alert() -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT workplace_mood FROM emotion_logs
        ORDER BY id DESC
        LIMIT 5
        """)
        last_moods = [row[0] for row in cursor.fetchall()]
        stress_moods = {'stressed', 'burned out', 'anxious'}
        stress_count = sum(1 for mood in last_moods if mood in stress_moods)
        return stress_count >= 3
