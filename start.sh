#!/bin/bash

# Log start of the script
echo "Starting start.sh script for search-service..."

# Ensure the wait-for-it script is executable
chmod +x ./wait-for-it.sh
echo "wait-for-it.sh script is now executable."

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch server to be available..."
./wait-for-it.sh elasticsearch:9200 --timeout=180 --strict

if [ $? -ne 0 ]; then
  echo "Elasticsearch is not ready. Exiting..."
  exit 1
fi

# Log Elasticsearch readiness
echo "Elasticsearch is ready."

# Set the PYTHONPATH environment variable
export PYTHONPATH=/app
echo "PYTHONPATH is set to $PYTHONPATH"

# Navigate to the app directory
cd /app
echo "Current directory is $(pwd)"

# Log the files in the current directory
echo "Files in the /app directory:"
ls -l

# Check if main.py exists
if [ ! -f app/main.py ]; then
  echo "main.py does not exist in the /app/app directory. Exiting..."
  exit 1
else
  echo "main.py exists in the /app/app directory."
fi

# Start the FastAPI application with debug logs
echo "Starting search-service with debug logs..."
uvicorn app.main:app --host 0.0.0.0 --port 8011 --log-level debug
