#!/bin/bash

echo "Starting Deloitte Strategy Insight Tool..."

# Activate virtual environment (adjust path if needed)
source venv/Scripts/activate

# Start FastAPI backend in background
echo "Starting FastAPI backend at http://localhost:8000 ..."
uvicorn api.main:app --reload &

# Wait a moment for backend to spin up
sleep 3

# Start Streamlit frontend
echo "Launching Streamlit frontend at http://localhost:8501 ..."
streamlit run app.py

# Wait for user to exit Streamlit before stopping background processes
wait
