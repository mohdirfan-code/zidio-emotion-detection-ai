# dashboard/utils.py
import cv2
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
# Removed: from transformers import pipeline (will be passed in)
from deepface import DeepFace
import os
import logging # Use logging for better messages

AUDIO_FILE = "temp_audio.wav"
AUDIO_DURATION = 5  # seconds

# --- Load Whisper Model ONCE ---
whisper_model = None
try:
    print("Loading Whisper model (this may take a moment)...")
    whisper_model = whisper.load_model("base") # Or "tiny", "small" etc. for speed
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"FATAL: Failed to load Whisper model: {e}")
    # You might want to exit or prevent speech detection if this fails
# -------------------------------


# Emotion → Workplace Mood mapping (keep as is)
MOOD_MAP = {
    "happy": "engaged", "sad": "burned out", "angry": "stressed",
    "surprise": "alert", "fear": "anxious", "disgust": "disengaged",
    "neutral": "calm", "joy": "engaged", "sadness": "burned out",
    "anger": "stressed", "love": "engaged"
    # Removed duplicate 'surprise'
}

def detect_face_emotion():
    cap = None # Initialize to None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Failed to open webcam.")
            return None, None, None
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to capture frame from webcam.")
            return None, None, None

        # Analyze *before* releasing
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
        if result and isinstance(result, list):
             emotion = result[0]["dominant_emotion"]
             mood = MOOD_MAP.get(emotion.lower(), "calm")
             return frame, emotion, mood
        else:
            logging.warning(f"DeepFace analysis did not return expected result: {result}")
            return frame, None, None # Return frame even if analysis fails?

    except Exception as e:
        logging.error(f"Face detection failed: {e}", exc_info=True) # Log traceback
        return None, None, None
    finally:
        if cap is not None and cap.isOpened():
            cap.release()


# --- Accept the text emotion model as an argument ---
def detect_speech_emotion(text_emotion_model):
# -------------------------------------------------
    global whisper_model # Refer to the globally loaded model
    if not whisper_model:
        logging.error("Whisper model not loaded. Cannot perform speech detection.")
        return None, None

    # --- Check if the text_emotion_model is valid ---
    if not text_emotion_model:
         logging.error("Text emotion model not provided to detect_speech_emotion.")
         return None, None
    # --------------------------------------------

    try:
        fs = 44100 # Sample rate
        logging.info("🎙️ Recording audio...")
        audio = sd.rec(int(AUDIO_DURATION * fs), samplerate=fs, channels=1, dtype='int16') # Specify dtype
        sd.wait() # Wait for recording to complete
        write(AUDIO_FILE, fs, audio) # Save the recorded data
        logging.info("Audio recording complete.")

        logging.info("📝 Transcribing audio...")
        # Use the pre-loaded model
        result = whisper_model.transcribe(AUDIO_FILE, fp16=False) # fp16=False can help CPU inference
        text = result["text"].strip()
        logging.info(f"Transcription result: '{text}'")

        if not text:
            logging.warning("Transcription resulted in empty text.")
            return None, None

        logging.info(f"🔍 Analyzing text emotion: '{text}'")
        # --- Use the passed-in model ---
        emotion_result = text_emotion_model(text)
        # -------------------------------

        # Check the structure of the result (can vary between pipeline versions)
        if emotion_result and isinstance(emotion_result, list) and isinstance(emotion_result[0], list):
             # Assuming nested list structure, e.g., [[{'label': 'joy', 'score': 0.9}]]
             top_emotion = emotion_result[0][0]
             emotion = top_emotion["label"]
             score = top_emotion["score"]
             logging.info(f"Detected text emotion: {emotion} (Score: {score:.2f})")
             mood = MOOD_MAP.get(emotion.lower(), "calm")
             return emotion, mood
        else:
            logging.warning(f"Unexpected format from text emotion model: {emotion_result}")
            return None, None

    except Exception as e:
        logging.error(f"Speech detection failed: {e}", exc_info=True) # Log traceback
        return None, None
    finally:
        # Clean up the audio file
        if os.path.exists(AUDIO_FILE):
            try:
                os.remove(AUDIO_FILE)
            except Exception as e:
                logging.error(f"Failed to remove temp audio file {AUDIO_FILE}: {e}")