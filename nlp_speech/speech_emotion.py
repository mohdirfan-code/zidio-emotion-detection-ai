# nlp_speech/speech_emotion.py

"""
Speech emotion detection using Whisper + HuggingFace DistilBERT.
"""

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import torch
from transformers import pipeline
import requests
import os
import time

API_URL = "http://127.0.0.1:8000/log_emotion/"
AUDIO_FILE = "temp_audio.wav"
DURATION = 5  # seconds

# Emotion to workplace mood mapping
MOOD_MAP = {
    "joy": "engaged",
    "sadness": "burned out",
    "anger": "stressed",
    "fear": "anxious",
    "surprise": "alert",
    "love": "engaged",
}

def record_audio(filename=AUDIO_FILE, duration=DURATION):
    print(f"🎙️ Recording {duration} seconds of audio...")
    fs = 44100  # Sample rate
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("✅ Recording complete.")

def transcribe_audio(filename=AUDIO_FILE):
    print("📝 Transcribing with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

def load_emotion_model():
    print("📦 Loading HuggingFace emotion model...")
    return pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)

def analyze_text_emotion(text, model):
    print(f"🔍 Analyzing text: {text}")
    results = model(text)

    # Handle double-wrapped result from top_k=1
    if isinstance(results, list) and len(results) > 0:
        inner = results[0]  # inner list
        if isinstance(inner, list) and len(inner) > 0:
            top = inner[0]  # first emotion result
            emotion = top["label"]
            mood = MOOD_MAP.get(emotion.lower(), "calm")
            return emotion, mood

    return "neutral", "calm"




def send_to_backend(emotion, mood):
    try:
        response = requests.post(API_URL, json={"emotion": emotion, "mood": mood})
        if response.status_code == 200:
            print("📡 Mood logged successfully.")
    except Exception as e:
        print("❌ Failed to send to backend:", e)

if __name__ == "__main__":
    record_audio()
    text = transcribe_audio()

    emotion_model = load_emotion_model()
    emotion, mood = analyze_text_emotion(text, emotion_model)

    print(f"🧠 Speech Emotion: {emotion} → {mood}")
    send_to_backend(emotion, mood)

    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
