# dashboard/fusion_worker.py

import os
from playsound import playsound
import smtplib
from email.mime.text import MIMEText
import threading
import time
import requests
import logging
import uuid
import pyttsx3

from dashboard.utils import detect_face_emotion, detect_speech_emotion
from transformers import pipeline
from collections import deque

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

INTENSITY_RANK = {
    "calm": 1, "engaged": 2, "alert": 3, "anxious": 4,
    "burned out": 5, "stressed": 6, "disengaged": 7
}

session_state = {
    "session_id": None,
    "latest_frame": None,
    "face_mood": None,
    "face_emotion": None,
    "speech_mood": None,
    "speech_emotion": None,
    "final_mood": None,
    "final_emotion": None,
    "last_updated": None,
    "alert_triggered": False
}

mood_history = deque(maxlen=5)
RED_FLAGS = {"stressed", "burned out", "anxious"}

def check_hr_alert(new_mood):
    mood_history.append(new_mood)
    red_count = sum(1 for mood in mood_history if mood in RED_FLAGS)
    return red_count >= 2

API_URL = "http://127.0.0.1:8000/log_emotion/"

# ✅ Email Alert Logic
def send_email_alert(subject, body):
    sender = "irfanvmeg@gmail.com"  # Replace with your Gmail
    recipient = "irfan1114318@gmail.com"    # Replace with HR's email
    password = "zbnj ykac ffyg mldr"  # Replace with 16-digit Gmail App Password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            logging.info("📧 Email alert sent to HR.")
    except Exception as e:
        logging.warning(f"❌ Email alert failed: {e}")

# Load HuggingFace model once
text_emotion_model = None
try:
    logging.info("Loading text emotion model...")
    text_emotion_model = pipeline(
        "text-classification",
        model="bhadresh-savani/distilbert-base-uncased-emotion",
        top_k=1
    )
    logging.info("Text emotion model loaded successfully.")
except Exception as e:
    logging.error(f"FATAL: Failed to load text emotion model: {e}", exc_info=True)

def fuse_moods(m1, m2):
    if not m1: return m2
    if not m2: return m1
    r1 = INTENSITY_RANK.get(m1, 0)
    r2 = INTENSITY_RANK.get(m2, 0)
    return m1 if r1 >= r2 else m2

def facial_detection_worker():
    while True:
        frame, face_emotion, face_mood = detect_face_emotion()
        if frame is not None:
            session_state["latest_frame"] = frame
        if face_emotion:
            session_state["face_emotion"] = face_emotion
            session_state["face_mood"] = face_mood
            logging.info(f"🧠 [Face Thread] {face_emotion} → {face_mood}")
        time.sleep(0.25)

def start_fusion_loop():
    session_id = str(uuid.uuid4())
    session_state["session_id"] = session_id
    logging.info(f"Starting fusion loop for session: {session_id}")

    voice_timer = 0
    last_logged_mood = None

    while True:
        now = time.time()

        if now - voice_timer > 10:
            speech_emotion, speech_mood = detect_speech_emotion(text_emotion_model)
            if speech_emotion:
                session_state["speech_mood"] = speech_mood
                session_state["speech_emotion"] = speech_emotion
                logging.info(f"🗣️ Speech: {speech_emotion} -> {speech_mood}")
            voice_timer = now

        fused_mood = fuse_moods(session_state.get("face_mood"), session_state.get("speech_mood"))

        if fused_mood:
            if fused_mood == session_state.get("face_mood"):
                fused_emotion = session_state.get("face_emotion")
            elif fused_mood == session_state.get("speech_mood"):
                fused_emotion = session_state.get("speech_emotion")
            else:
                fused_emotion = session_state.get("face_emotion") or session_state.get("speech_emotion")

            if fused_mood != session_state.get("final_mood"):
                session_state["final_mood"] = fused_mood
                session_state["final_emotion"] = fused_emotion
                session_state["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

                previous_alert = session_state["alert_triggered"]
                current_alert = check_hr_alert(fused_mood)
                session_state["alert_triggered"] = current_alert

                if current_alert and not previous_alert:
                    try:
                        playsound(r"C:\Users\Dr.Mohd.Mohinoddin\Desktop\zidio-vscode\dashboard\assets\hr_alert_loud.mp3")
                        speak_message("Multiple stress indicators detected. Please consider taking a short break.")

                    except Exception as e:
                        logging.warning(f"Sound alert failed: {e}")

                    try:
                        send_email_alert(
                            subject="🚨 Zidio Alert: Stress Detected",
                            body=f"⚠️ Zidio detected repeated stress indicators.\nFinal Mood: {fused_mood.upper()}\nPlease take appropriate HR action."
                        )

                    except Exception as e:
                        logging.warning(f"Email alert failed: {e}")

                logging.info(f"✅ Fused Mood Updated: {fused_mood} (Emotion: {fused_emotion}) | HR Alert: {session_state['alert_triggered']}")

                if fused_mood != last_logged_mood:
                    try:
                        log_data = {
                            "emotion": fused_emotion,
                            "mood": fused_mood,
                            "face_emotion": session_state.get("face_emotion"),
                            "speech_emotion": session_state.get("speech_emotion"),
                        }

                        log_data = {k: v for k, v in log_data.items() if v is not None}
                        response = requests.post(API_URL, json=log_data, timeout=10)
                        response.raise_for_status()
                        logging.info(f"📡 Session mood logged successfully: {log_data}")
                        last_logged_mood = fused_mood
                    except requests.exceptions.RequestException as e:
                        logging.error(f"❌ Failed to log mood via API: {e}")
                    except Exception as e:
                        logging.error(f"❌ Unexpected error during API logging: {e}", exc_info=True)
        else:
            if session_state.get("final_mood") is not None:
                logging.info("Clearing fused mood as no source data is available.")
                session_state["final_mood"] = None
                session_state["final_emotion"] = None
                session_state["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

        time.sleep(0.5)

def speak_message(message):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        logging.warning(f"TTS failed: {e}")

def launch_fusion_thread():
    logging.info("Launching fusion + facial detection threads...")
    threading.Thread(target=start_fusion_loop, name="FusionWorkerThread", daemon=True).start()
    threading.Thread(target=facial_detection_worker, name="FaceThread", daemon=True).start()
