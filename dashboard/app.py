# dashboard/app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dashboard.analytics import get_all_logs, get_mood_counts
from dashboard.fusion_worker import launch_fusion_thread, session_state

import streamlit as st
import pandas as pd
import sqlite3
import cv2
from PIL import Image
import time
import threading
import pyttsx3

DB_PATH = "emotion_logs.db"
REFRESH_INTERVAL = 5

if 'fusion_thread_started' not in st.session_state:
    st.session_state.fusion_thread_started = True
    launch_fusion_thread()
    print("🚀 Fusion thread launched.")

st.set_page_config(page_title="Zidio Dashboard", layout="centered")
st.title("📊 Zidio | Real-Time Emotional Insights")
st.caption(f"🔄 Auto-refreshing every {REFRESH_INTERVAL} seconds...")

def speak_message(msg):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.setProperty("volume", 1.0)
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print("🔇 TTS error:", e)
    threading.Thread(target=_speak, daemon=True).start()

def maybe_tts():
    mood = session_state.get("final_mood")
    alert_triggered = session_state.get("alert_triggered", False)
    if alert_triggered and not session_state.get("tts_spoken"):
        speak_message("You seem stressed. Please consider taking a short break.")
        session_state["tts_spoken"] = True
    elif not alert_triggered:
        session_state["tts_spoken"] = False

def load_logs(since_days=7):
    if not os.path.exists(DB_PATH):
        st.error("Database not found.")
        return pd.DataFrame()
    try:
        since = pd.Timestamp.now() - pd.Timedelta(days=since_days)
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM emotion_log", conn, parse_dates=["timestamp"])
        return df[df["timestamp"] >= since]
    except Exception as e:
        st.error(f"Error loading DB: {e}")
        return pd.DataFrame()

def render_frame(frame):
    if frame is None:
        st.warning("No webcam frame.")
        return
    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(Image.fromarray(rgb), caption="📷 Live Snapshot", use_container_width=True)
    except Exception as e:
        st.error(f"Render error: {e}")

def display_session_state():
    render_frame(session_state.get("latest_frame"))
    st.markdown("## 🧠 Current Session Mood")

    if session_state.get("alert_triggered"):
        st.warning("🚨 **HR ALERT**: Multiple signs of stress detected!")

    st.markdown(f"**Last Updated**: `{session_state.get('last_updated', 'pending')}`")

    emoji_map = {
        "engaged": "🟢", "calm": "🔵", "alert": "🟠",
        "anxious": "⚪", "burned out": "🟣",
        "stressed": "🔴", "disengaged": "🟤"
    }

    mood = session_state.get("final_mood", "loading")
    emoji = emoji_map.get(mood, "❓")

    if mood and mood != "loading":
        st.markdown(f"""
        <div style='
            display: inline-block;
            padding: 0.4em 1em;
            border-radius: 8px;
            background-color: #ffffff;
            color: #c70000;
            font-weight: bold;
            font-size: 18px;
        '>
            {emoji} Final Mood: {mood.upper()}
        </div>
        """, unsafe_allow_html=True)
        maybe_tts()
    else:
        st.warning("Waiting for detection...")

    col1, col2 = st.columns(2)
    col1.metric("🧍 Facial Mood", session_state.get("face_mood", "-"))
    col2.metric("🗣️ Speech Mood", session_state.get("speech_mood", "-"))

def display_history(logs):
    st.subheader("📊 Mood Distribution")
    if logs.empty:
        st.info("No data logged yet.")
        return
    if "mood" in logs.columns:
        st.bar_chart(logs["mood"].value_counts())
    else:
        st.warning("Column 'mood' not found in logs.")

    st.subheader("🕒 Recent Logs")
    if "timestamp" in logs.columns:
        st.dataframe(logs.sort_values("timestamp", ascending=False).head(10))
    else:
        st.warning("Column 'timestamp' not found in logs.")

# 🔁 Main Loop
while True:
    logs = load_logs()
    display_session_state()
    display_history(logs)
    time.sleep(REFRESH_INTERVAL)
    st.rerun()
