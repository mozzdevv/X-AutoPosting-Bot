#!/bin/bash

# Configuration
PROJECT_DIR="/Users/mazo/Documents/AntiGravity Agent Folder/X AutoBot Posting"
PYTHON_PATH="$PROJECT_DIR/.venv/bin/python"
STREAMLIT_PATH="$PROJECT_DIR/.venv/bin/streamlit"

# Navigate to project directory
cd "$PROJECT_DIR"

# Kill any existing instances to prevent duplicates
pkill -f "main_bot.py"
pkill -f "streamlit.*dashboard.py"

# Wait a moment for processes to clear
sleep 2

# Start the Bot
nohup "$PYTHON_PATH" main_bot.py > bot.log 2>&1 &
echo "🚀 Bot started with PID $!"

# Start the Dashboard
nohup "$STREAMLIT_PATH" run dashboard.py --server.port 8501 --server.headless true > dashboard.log 2>&1 &
echo "📊 Dashboard started with PID $!"

exit 0
