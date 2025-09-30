#!/bin/bash

# Production startup script for Laptop Intelligence Platform (FastAPI)

set -e

echo "Starting Laptop Intelligence Platform with FastAPI..."

# Check if required environment variables are set
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "Error: DEEPSEEK_API_KEY environment variable is not set"
    exit 1
fi

# Create necessary directories
mkdir -p /app/logs
mkdir -p /app/uploads

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
while ! redis-cli -h redis ping > /dev/null 2>&1; do
    echo "Redis is not ready yet. Waiting..."
    sleep 2
done
echo "Redis is ready!"

# Start the application with Uvicorn
echo "Starting Uvicorn server..."
exec uvicorn app:app \
    --host 0.0.0.0 \
    --port 5000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-log \
    --log-level info
