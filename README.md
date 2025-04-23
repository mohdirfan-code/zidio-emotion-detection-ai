# 🤖 Zidio: Real-Time Workplace Emotion Detection AI

Zidio is an AI-powered emotion analysis system designed for **real-time monitoring** of employee well-being in workplace environments. It leverages **facial expression** and **voice tone** detection to infer **emotional states**, map them to **workplace moods**, and trigger alerts when stress is detected.

## 📸 Demo 

![Image](https://github.com/user-attachments/assets/408ae334-8e25-4797-8a57-17536cddc2bb)

![Image](https://github.com/user-attachments/assets/e423894c-15a4-4be9-92db-991db59fac66)

![Image](https://github.com/user-attachments/assets/d3c48fe9-b490-41c4-bbfe-e3bf0325df79)

![Image](https://github.com/user-attachments/assets/18df47a4-fff4-4e1f-8c93-71ce0151b77b)

![Image](https://github.com/user-attachments/assets/b0aeab12-6be7-420c-a71c-c31a8fe5343c)

![Image](https://github.com/user-attachments/assets/c712ff59-2730-48e0-ad6b-7f04c922c588)

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
