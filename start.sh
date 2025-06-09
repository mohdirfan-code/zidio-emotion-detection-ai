#!/bin/bash
echo "🚀 Starting Zidio Services..."

# Start FastAPI on a secondary port (e.g., 9000)
uvicorn api.main:app --host 0.0.0.0 --port 9000 &

# Start Streamlit on port 8000 — Render will expose this one
streamlit run dashboard/app.py --server.port=8000 --server.address=0.0.0.0

