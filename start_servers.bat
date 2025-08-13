@echo off
echo ========================================
echo Resume Parser - Starting Servers
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo ERROR: .env file not found
    echo Please copy backend\.env.example to backend\.env and add your API keys
    pause
    exit /b 1
)

echo Starting backend server...
cd backend

REM Start Django server in a new window
start "Django Backend" cmd /k "venv\Scripts\activate && python manage.py runserver 8000"

cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo WARNING: Frontend dependencies not installed
    echo Run: cd frontend && npm install
    pause
) else (
    echo Starting frontend server...
    REM Start Next.js server in a new window
    start "Next.js Frontend" cmd /k "npm run dev"
)

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000/
echo Frontend: http://localhost:3000/
echo Admin:    http://localhost:8000/admin/
echo.
echo Close the command windows to stop the servers
pause
