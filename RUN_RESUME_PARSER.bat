@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Resume Parser - Single File Launcher
echo ========================================
echo.

REM Check if portable directory exists
if not exist "portable" (
    echo ERROR: Portable setup not found
    echo Please run PORTABLE_SETUP.bat first to create the portable version
    pause
    exit /b 1
)

REM Set portable paths
set PYTHON_PATH=%~dp0portable\python
set NODE_PATH=%~dp0portable\node\nodejs
set POPPLER_PATH=%~dp0portable\poppler\poppler-24.08.0\Library\bin
set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%NODE_PATH%;%POPPLER_PATH%;%PATH%

REM Check if .env exists
if not exist "portable\app\backend\.env" (
    echo Creating environment file...
    copy "portable\app\backend\.env.example" "portable\app\backend\.env"
    echo.
    echo ========================================
    echo SETUP REQUIRED
    echo ========================================
    echo.
    echo Please edit the file: portable\app\backend\.env
    echo.
    echo Add your API keys:
    echo - OPENAI_API_KEY=your_openai_key_here
    echo - GOOGLE_API_KEY=your_gemini_key_here
    echo.
    echo Get API keys from:
    echo - OpenAI: https://platform.openai.com/api-keys
    echo - Google: https://aistudio.google.com/app/apikey
    echo.
    echo Then run this file again.
    echo.
    start notepad "portable\app\backend\.env"
    pause
    exit /b 1
)

REM Check if API keys are configured
findstr /C:"your_openai_key_here" "portable\app\backend\.env" >nul
if !ERRORLEVEL! == 0 (
    echo.
    echo WARNING: Please configure your API keys in:
    echo portable\app\backend\.env
    echo.
    start notepad "portable\app\backend\.env"
    pause
)

findstr /C:"your_gemini_key_here" "portable\app\backend\.env" >nul
if !ERRORLEVEL! == 0 (
    echo.
    echo WARNING: Please configure your API keys in:
    echo portable\app\backend\.env
    echo.
    start notepad "portable\app\backend\.env"
    pause
)

echo Starting Resume Parser...
echo.
echo Backend:  http://localhost:8000/
echo Frontend: http://localhost:3000/
echo Admin:    http://localhost:8000/admin/
echo.

REM Kill any existing processes
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

REM Start Django in background
echo Starting backend server...
cd portable\app\backend
start "Resume Parser Backend" /min cmd /c "python manage.py runserver 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Next.js frontend
echo Starting frontend server...
cd ..\frontend
start "Resume Parser Frontend" /min cmd /c "npm run dev"

echo.
echo ========================================
echo Resume Parser is Starting...
echo ========================================
echo.
echo Please wait 10-15 seconds for servers to fully start
echo.
echo Then open your browser to:
echo http://localhost:3000/
echo.
echo To stop the application:
echo - Close this window, or
echo - Press Ctrl+C and close both server windows
echo.

REM Wait for user
echo Press any key to open the application in browser...
pause >nul

REM Open browser
start http://localhost:3000/

echo.
echo Application opened in browser!
echo Keep this window open while using the application.
echo.
pause
