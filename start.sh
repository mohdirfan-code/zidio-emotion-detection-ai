# start.sh (for FastAPI only)
#!/bin/bash
echo "🚀 Starting FastAPI (Zidio API)..."
uvicorn api.main:app --host 0.0.0.0 --port $PORT


