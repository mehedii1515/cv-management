@echo off
REM Production startup script for Windows office environment
REM Run this script as Administrator for better performance

echo ====================================
echo Resume Parser Production Server
echo Windows Office Environment Setup
echo ====================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with Administrator privileges - Good for production
) else (
    echo [WARNING] Not running as Administrator - some optimizations may not work
    echo [WARNING] For best performance, run as Administrator
)
echo.

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "backend\media\uploads" mkdir backend\media\uploads
if not exist "backend\staticfiles" mkdir backend\staticfiles

REM Activate virtual environment
echo [INFO] Activating Python virtual environment...
call backend\venv\Scripts\activate.bat
if %errorLevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    echo [ERROR] Make sure backend\venv exists and is properly set up
    pause
    exit /b 1
)

REM Set environment variables for production
set DJANGO_SETTINGS_MODULE=resume_parser.settings
set NODE_ENV=production

echo [INFO] Starting production servers...
echo.

REM Check if Caddy is available
where caddy >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Caddy found - will start reverse proxy
    set CADDY_AVAILABLE=1
) else (
    if exist "caddy.exe" (
        echo [INFO] Local Caddy found - will start reverse proxy
        set CADDY_AVAILABLE=1
    ) else (
        echo [WARNING] Caddy not found in PATH or current directory
        echo [INFO] Download Caddy from: https://caddyserver.com/download
        set CADDY_AVAILABLE=0
    )
)

REM Build frontend for production (if not already built)
echo [INFO] Checking frontend build...
if not exist "frontend\.next" (
    echo [INFO] Building Next.js frontend...
    cd frontend
    call npm run build
    if %errorLevel% neq 0 (
        echo [ERROR] Frontend build failed
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo [INFO] Frontend build completed
) else (
    echo [INFO] Frontend already built
)

REM Start Django with Waitress in background
echo [INFO] Starting Django application server...
start "Django-Waitress" /B python production_server.py

REM Wait a moment for Django to start
ping 127.0.0.1 -n 4 >nul

REM Start Next.js frontend in production mode
echo [INFO] Starting Next.js frontend server...
cd frontend
start "Next.js-Frontend" /B npm start
cd ..

REM Wait a moment for Next.js to start
ping 127.0.0.1 -n 6 >nul

REM Start Caddy if available
if %CADDY_AVAILABLE%==1 (
    echo [INFO] Starting Caddy reverse proxy...
    if exist "caddy.exe" (
        start "Caddy" /B caddy.exe run --config Caddyfile
    ) else (
        start "Caddy" /B caddy run --config Caddyfile
    )
    echo.
    echo ====================================
    echo OFFICE ACCESS INFORMATION
    echo ====================================
    echo Main Application: http://localhost:8080
    echo Frontend Direct:  http://localhost:3000
    echo Backend Direct:   http://localhost:8000
    echo.
    echo FOR OFFICE NETWORK ACCESS:
    echo Office users should use: http://192.168.1.2:8080
    echo Alternative access: http://localhost:8080 (from server)
    echo ====================================
) else (
    echo.
    echo ====================================
    echo OFFICE ACCESS INFORMATION
    echo ====================================
    echo Frontend: http://localhost:3000
    echo Backend:  http://localhost:8000
    echo.
    echo FOR OFFICE NETWORK ACCESS:
    echo Frontend: http://192.168.1.2:3000
    echo Backend:  http://192.168.1.2:8000
    echo.
    echo NOTE: Install Caddy for integrated access
    echo ====================================
)

echo.
echo [INFO] Production servers are starting...
echo [INFO] Check the server windows for startup status
echo [INFO] Press Ctrl+C in each server window to stop
echo [INFO] Check logs/ directory for server logs
echo.

REM Keep this window open
pause
