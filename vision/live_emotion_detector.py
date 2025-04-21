# vision/live_emotion_detector.py

"""
Live emotion detection using DeepFace + Mini-Xception,
mapped to workplace emotional states (Zidio),
with backend API integration for logging + HR alerts.
"""

import cv2
from deepface import DeepFace
import numpy as np
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/log_emotion/"  # Local FastAPI endpoint

# Map raw DeepFace emotions to workplace moods
WORKPLACE_MOOD_MAP = {
    'happy': 'engaged',
    'sad': 'burned out',
    'angry': 'stressed',
    'surprise': 'alert',
    'fear': 'anxious',
    'disgust': 'disengaged',
    'neutral': 'calm'
}

def detect_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        workplace_mood = WORKPLACE_MOOD_MAP.get(dominant_emotion, 'unknown')
        return dominant_emotion, workplace_mood
    except Exception:
        return None, None

def send_to_backend(emotion, mood):
    try:
        response = requests.post(API_URL, json={"emotion": emotion, "mood": mood})
        if response.status_code == 200:
            return response.json().get("alert", False)
    except Exception as e:
        print("❌ Error sending to backend:", e)
    return False

def start_webcam_emotion_stream():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        emotion, mood = detect_emotion(frame)

        if emotion:
            timestamp = datetime.now().strftime("%H:%M:%S")
            label = f"{timestamp} | {emotion} → {mood}"

            # Send data to FastAPI backend
            alert_triggered = send_to_backend(emotion, mood)

            # Show label on webcam feed
            cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            if alert_triggered:
                cv2.putText(frame, "⚠️ HR ALERT: STRESS DETECTED", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Zidio | Live Emotion Detector", frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_webcam_emotion_stream()
