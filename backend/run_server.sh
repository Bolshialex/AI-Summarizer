#!/bin/bash

echo "Starting FastAPI server on Mac..."

# Activate the virtual environment
source venv/bin/activate

# Install and update dependencies
echo "Installing dependencies..."
python -m pip install -r requirements.txt

# Run the server
echo "Starting the server..."
uvicorn main:app --reload