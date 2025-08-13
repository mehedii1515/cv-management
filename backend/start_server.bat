@echo off
REM Windows batch file to set up environment and start Django server
REM Double-click this file to start your server

echo Setting up environment...

REM Set Poppler PATH for this session
set "POPPLER_PATH=%~dp0poppler-24.08.0\Library\bin"
set "PATH=%POPPLER_PATH%;%PATH%"

REM Test Poppler
"%POPPLER_PATH%\pdfinfo.exe" -v >nul 2>&1
if errorlevel 1 (
    echo Error: Poppler not found at %POPPLER_PATH%
    pause
    exit /b 1
)
echo Poppler is ready

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Could not activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated

echo.
echo Environment setup complete!
echo Starting Django development server...
echo.

REM Start Django server
python manage.py runserver

pause
