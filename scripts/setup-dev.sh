#!/bin/bash
# Setup script for the My Personal Assistant monorepo development environment

set -e  # Exit on error

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Determine Python command
PYTHON_CMD=""
if command_exists python3; then
  PYTHON_CMD="python3"
elif command_exists python; then
  PYTHON_CMD="python"
else
  echo "Error: Python (as 'python' or 'python3') is not installed or not in your PATH."
  echo "Please ensure Python 3.9 or higher is installed and accessible."
  echo "You can download it from: https://www.python.org/downloads/"
  echo "If Python is installed, make sure its directory is in your system's PATH."
  exit 1
fi

echo "Using Python command: $PYTHON_CMD"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install shared package in development mode
echo "Installing shared package..."
cd packages/shared
pip install -e ".[dev]"

# Install API package in development mode
echo "Installing API package..."
cd ../api
pip install -e ".[dev]"

# Check for npm before attempting to install UI dependencies
if command_exists npm; then
  # Install UI dependencies
  echo "Installing UI dependencies..."
  cd ../ui
  
  # Clean up any existing installation that might cause issues
  if [ -d "node_modules" ] || [ -f "package-lock.json" ]; then
    echo "Cleaning up previous installation..."
    rm -rf node_modules package-lock.json
  fi
  
  # Install with legacy peer deps to handle dependency conflicts
  echo "Installing UI dependencies with legacy peer deps..."
  npm install --legacy-peer-deps
  
  # Check if installation was successful
  if [ $? -ne 0 ]; then
    echo "\nWARNING: UI dependencies installation encountered issues."
    echo "You may need to manually resolve them:"
    echo "  cd packages/ui"
    echo "  npm install --legacy-peer-deps --force"
  else
    echo "UI dependencies installed successfully!"
  fi
else
  echo "\nWARNING: npm not found. Skipping UI dependencies installation."
  echo "To complete setup, please install Node.js and npm:"
  echo "  - macOS: brew install node"
  echo "  - Linux: apt install nodejs npm"
  echo "  - Windows: Download from https://nodejs.org/"
  echo "\nAfter installing Node.js and npm, run:"
  echo "  cd packages/ui && npm install --legacy-peer-deps"
  
  # Continue with the script but skip npm install
  cd ../ui
fi

echo "\nFormatting Python code with Ruff..."
if command_exists ruff; then
  ruff format .
  echo "Python code formatting complete."
else
  echo "WARNING: ruff command not found. Skipping Python code formatting."
  echo "Ensure ruff is installed in your virtual environment (it should be a dev dependency)."
fi

echo "\nDevelopment environment setup complete!"

if ! command_exists npm; then
  echo "\nNOTE: UI setup was skipped because npm is not installed."
  echo "Install Node.js and npm to complete the UI setup."
fi

echo "\nNext steps:"
echo "1. To start the API server: cd packages/api && uvicorn my_personal_assistant_api.main:app --reload"

if command_exists npm; then
  echo "2. To start the UI server: cd packages/ui && npm start"
fi

echo "3. To start both API and UI servers together: ./scripts/start-dev.sh"

# Ask user if they want to start the development servers
read -p "\nDo you want to start the development servers now? (y/N) " choice
case "$choice" in 
  y|Y ) 
    echo "\nStarting development servers..."
    if [ -f "./scripts/start-dev.sh" ]; then
      chmod +x ./scripts/start-dev.sh # Ensure it's executable
      ./scripts/start-dev.sh
    else
      echo "Error: ./scripts/start-dev.sh not found."
    fi
    ;;
  * ) 
    echo "You can start the servers later using the commands above or ./scripts/start-dev.sh."
    ;;
esac
