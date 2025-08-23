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

echo [INFO] Starting production servers...
echo.

REM Check if Caddy is available
where caddy >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Caddy found - will start reverse proxy
    set CADDY_AVAILABLE=1
) else (
    echo [WARNING] Caddy not found in PATH
    echo [INFO] Download Caddy from: https://caddyserver.com/download
    set CADDY_AVAILABLE=0
)

REM Start Django with Waitress in background
echo [INFO] Starting Django application server...
start "Django-Waitress" /B python production_server.py

REM Wait a moment for Django to start
timeout /t 5 /nobreak >nul

REM Start Caddy if available
if %CADDY_AVAILABLE%==1 (
    echo [INFO] Starting Caddy reverse proxy...
    start "Caddy" /B caddy run --config Caddyfile
    echo.
    echo ====================================
    echo OFFICE ACCESS INFORMATION
    echo ====================================
    echo Main Application: http://localhost:8080
    echo Direct Django:    http://localhost:8000
    echo.
    echo Office users should use: http://localhost:8080
    echo Or use your server's IP: http://[SERVER-IP]:8080
    echo ====================================
) else (
    echo.
    echo ====================================
    echo OFFICE ACCESS INFORMATION
    echo ====================================
    echo Application URL: http://localhost:8000
    echo Or use your server's IP: http://[SERVER-IP]:8000
    echo.
    echo NOTE: Install Caddy for better performance
    echo ====================================
)

echo.
echo [INFO] Production servers are starting...
echo [INFO] Check the Django window for startup status
echo [INFO] Press Ctrl+C in Django window to stop servers
echo [INFO] Check logs/ directory for server logs
echo.

REM Keep this window open
pause
