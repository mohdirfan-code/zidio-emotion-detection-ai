#!/bin/bash
echo "🚀 Starting Zidio Services..."

# Start FastAPI backend on port 8000 (runs in background)
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend on port 8501
streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0

