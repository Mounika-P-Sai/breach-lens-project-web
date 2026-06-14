@echo off
REM BreachLens Backend Startup Script
REM Sets required environment variables and starts uvicorn

set MONGODB_URL=mongodb+srv://23r11a6282:241026@cluster0.1jan0.mongodb.net/?appName=Cluster0
set DATABASE_NAME=23r11a6282
set JWT_SECRET=breachlens_secret_key

echo Starting BreachLens Backend...
echo MongoDB URL: %MONGODB_URL:~0,30%...
echo Database: %DATABASE_NAME%

cd /d "%~dp0"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
