# api/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

DB_PATH = "emotion_logs.db"

# Create table on startup
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS emotion_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                emotion TEXT,
                mood TEXT
            )
        ''')
init_db()

# Pydantic model
class EmotionLog(BaseModel):
    emotion: str
    mood: str


@app.post("/log_emotion/")
def log_emotion(data: EmotionLog):
    timestamp = datetime.now().isoformat()
    
    # Insert new log
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO emotion_log (timestamp, emotion, mood)
            VALUES (?, ?, ?)
        ''', (timestamp, data.emotion, data.mood))

        # Get last 5 moods
        cursor = conn.execute('''
            SELECT mood FROM emotion_log
            ORDER BY timestamp DESC
            LIMIT 5
        ''')
        recent_moods = [row[0] for row in cursor.fetchall()]
        stress_count = recent_moods.count("stressed")
        alert = stress_count >= 3

    return {
        "status": "logged",
        "timestamp": timestamp,
        "recent_moods": recent_moods,
        "stress_count": stress_count,
        "alert": alert
    }

