@echo off
REM Production startup script for Laptop Intelligence Platform (FastAPI) (Windows)

echo Starting Laptop Intelligence Platform with FastAPI...

REM Check if required environment variables are set
if "%DEEPSEEK_API_KEY%"=="" (
    echo Error: DEEPSEEK_API_KEY environment variable is not set
    exit /b 1
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads

REM Start the application with Uvicorn
echo Starting Uvicorn server...
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 4 --access-log --log-level info
