#!/bin/bash
echo "🚀 Starting Zidio Services..."

# Start FastAPI in background
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (on same network)
# streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0
streamlit run dashboard/app.py --server.port=8000 --server.address=0.0.0.0

