# dashboard/analytics.py

import sqlite3
import pandas as pd

DB_PATH = "mood_logs.db"

def get_all_logs():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM emotion_logs ORDER BY timestamp DESC", conn, parse_dates=["timestamp"])
    return df

def get_last_log():
    df = get_all_logs()
    return df.iloc[0] if not df.empty else None

# dashboard/analytics.py
def get_mood_counts(df, days=7):
    if df.empty:
        return pd.DataFrame(columns=["mood", "count"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Use 'mood' if available, otherwise fallback to 'workplace_mood'
    mood_col = "mood" if "mood" in df.columns else "workplace_mood"
    if mood_col not in df.columns:
        return pd.DataFrame(columns=["mood", "count"])

    recent = df[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(days=days)]
    return (
        recent[mood_col]
        .value_counts()
        .reset_index(name='count')
        .rename(columns={'index': 'mood'})
    )

