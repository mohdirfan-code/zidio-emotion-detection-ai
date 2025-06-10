# start.sh (for Streamlit only)
#!/bin/bash
echo "📊 Launching Streamlit Dashboard..."
streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=$PORT
