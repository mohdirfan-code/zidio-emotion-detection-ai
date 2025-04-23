# 🤖 Zidio: Real-Time Workplace Emotion Detection AI

Zidio is an AI-powered emotion analysis system designed for **real-time monitoring** of employee well-being in workplace environments. It leverages **facial expression** and **voice tone** detection to infer **emotional states**, map them to **workplace moods**, and trigger alerts when stress is detected.

## 📸 Demo 

![Image](https://github.com/user-attachments/assets/a7e38a63-bb71-47a7-b786-5406d28c9ae5)

![Image](https://github.com/user-attachments/assets/e97ca3a1-f8b2-4ad7-8d84-0f420ad06a08)

![Image](https://github.com/user-attachments/assets/b90dd127-8a77-4016-9e61-6d3c67ae23e8)

![Image](https://github.com/user-attachments/assets/40c96db5-2403-467e-8098-229feb3bed41)

![Image](https://github.com/user-attachments/assets/987fc339-5664-459b-bbc3-992e463d90c2)

![Image](https://github.com/user-attachments/assets/04696fb9-9084-4c85-bea7-6aee835c85bb)

### 1. 🎥 **Live Emotion Detection via Webcam**

Zidio captures **real-time facial expressions** using your webcam and detects the corresponding emotion using **DeepFace**.

---

### 2. 🧠 **Emotion Analysis Dashboard**

The **Streamlit dashboard** updates every few seconds to show:

- 🧍 **Facial Emotion**
- 🎙️ **Speech Emotion**
- 🧠 **Final Mapped Mood**
- 🚨 **Alerts if stress is detected multiple times**

---

### 3. 📊 **Mood Distribution & Logs**

A **bar chart** displays mood trends dynamically.

All detections are **logged in real time** with timestamps using a **SQLite backend**.

---

### 4. 🚨 **Email Alert System**

Zidio sends **automated email alerts** to HR when **stress or burnout** is detected repeatedly within a session.

Example:
> _"Zidio detected repeated stress indicators.  
> Final Mood: BURNED OUT  
> Please take appropriate HR action."_  

---

## 🔥 Features

✅ **Facial Emotion Detection**  
Detects emotions using DeepFace on live webcam frames every ~4 seconds.

✅ **Speech Emotion Recognition**  
Uses Whisper + HuggingFace to analyze tone and transcribe speech every ~10 seconds.

✅ **Workplace Mood Mapping**  
Emotions are mapped to states like `Calm`, `Engaged`, `Stressed`, `Burned Out`.

✅ **Stress Alerts**  
Triggers alerts when "stressed" is detected in 3 out of the last 5 readings.

✅ **Streamlit Dashboard**  
Real-time mood tracking UI with auto-refresh and filtering.

✅ **Backend Logging**  
FastAPI logs all emotion events to a local SQLite database.

---

## 🧠 Tech Stack

| Layer          | Tools/Frameworks |
|----------------|------------------|
| Frontend       | Streamlit        |
| Backend        | FastAPI          |
| ML Models      | DeepFace, Whisper, HuggingFace Transformers |
| DB             | SQLite           |
| Deployment     | Docker           |

---

## 🏗️ System Architecture

![Image](https://github.com/user-attachments/assets/c9d5a21a-bd37-4ba5-8baf-df0974478b56)
