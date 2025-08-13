@echo off
REM Resume Parser Search System - Windows Startup
REM Usage: start_system.bat [port]

set PORT=%1
if "%PORT%"=="" set PORT=8000

echo 🚀 Starting Resume Parser Search System on port %PORT%
echo ============================================

REM Check if Elasticsearch is running
curl -s "localhost:9200" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Elasticsearch not detected on localhost:9200
    echo    Please start Elasticsearch first
    echo.
    set /p REPLY="Continue anyway? (y/n): "
    if /i not "%REPLY%"=="y" exit /b 1
)

echo Starting Django API server...
start /b python manage.py runserver 0.0.0.0:%PORT% --noreload

echo ✅ System started!
echo.
echo 📊 API Endpoints:
echo    Status:      http://localhost:%PORT%/api/search/status/
echo    Search:      http://localhost:%PORT%/api/search/search/?q=python
echo    Boolean:     http://localhost:%PORT%/api/search/boolean-search/?q=python%%20AND%%20django
echo    Suggestions: http://localhost:%PORT%/api/search/suggestions/?q=prog
echo.
echo 🔍 Test the system:
echo    curl "http://localhost:%PORT%/api/search/search/?q=python"
echo.
echo 📊 Monitor integration:
echo    python monitor_integration.py
echo.
pause
