#!/bin/bash
# Script to start both API and UI development servers

# Function to clean up background processes on exit
cleanup() {
    echo "\nShutting down servers..."
    # Kill all processes in the current process group
    kill 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run cleanup function
trap cleanup SIGINT SIGTERM

# Determine Python command
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "Error: Python (as 'python' or 'python3') is not installed or not in your PATH."
  exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
  echo "Activating Python virtual environment..."
  source venv/bin/activate
else
  echo "Error: Virtual environment 'venv' not found. Please run ./scripts/setup-dev.sh first."
  exit 1
fi

# Get the root directory of the project
PROJECT_ROOT=$(pwd)

# Start API server
echo "\nStarting API server in the background..."
cd "$PROJECT_ROOT/packages/api"
# Using exec to replace shell, so that kill 0 works as expected with uvicorn's process management
(uvicorn my_personal_assistant_api.main:app --reload --port 8000) &
API_PID=$!
echo "API server started with PID $API_PID on port 8000."

# Start UI server
if command -v npm >/dev/null 2>&1; then
  echo "\nStarting UI development server in the background..."
  cd "$PROJECT_ROOT/packages/ui"
  (npm start) &
  UI_PID=$!
  echo "UI server started with PID $UI_PID on port 3000."
else
  echo "\nSkipping UI server start: npm not found."
fi

echo "\nBoth servers are starting. Press Ctrl+C to stop both."

# Wait for all background processes to complete
# This keeps the script running and allows the trap to catch Ctrl+C
wait $API_PID
if [ ! -z "$UI_PID" ]; then
  wait $UI_PID
fi

echo "All servers have been shut down."
