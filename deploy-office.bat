@echo off
echo =====================================
echo    Resume Parser Docker Deployment
echo =====================================

REM Get server IP automatically
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set SERVER_IP=%%b
        goto :found
    )
)
:found

REM Remove leading spaces
for /f "tokens=* delims= " %%a in ("%SERVER_IP%") do set SERVER_IP=%%a

echo Server IP detected: %SERVER_IP%

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop and start it.
    pause
    exit /b 1
)

echo Docker is available...

REM Copy environment file
if not exist ".env" (
    echo Creating environment file...
    copy ".env.docker" ".env"
    echo.
    echo IMPORTANT: Please edit .env file and update:
    echo - SERVER_IP=%SERVER_IP%
    echo - OPENAI_API_KEY or GEMINI_API_KEY
    echo - SECRET_KEY for production
    echo - Database passwords
    echo.
    pause
)

REM Update SERVER_IP in .env file
powershell -Command "(gc .env) -replace 'YOUR_OFFICE_SERVER_IP', '%SERVER_IP%' | Out-File -encoding ASCII .env"

echo Stopping any existing containers...
docker-compose down -v

echo Building and starting Resume Parser...
docker-compose up --build -d

echo Waiting for services to start...
timeout /t 30 /nobreak

echo Checking service status...
docker-compose ps

echo.
echo =====================================
echo    Resume Parser is now running!
echo =====================================
echo.
echo Access URLs:
echo  Frontend: http://%SERVER_IP%
echo  API: http://%SERVER_IP%/api
echo  Admin: http://%SERVER_IP%/admin
echo  Documentation: http://%SERVER_IP%/docs
echo  Health Check: http://%SERVER_IP%/health
echo.
echo Share these URLs with your office team!
echo.
echo Management Commands:
echo  Stop: docker-compose down
echo  View logs: docker-compose logs -f
echo  Restart: docker-compose restart
echo  Update: docker-compose pull ^&^& docker-compose up -d
echo.

REM Test the deployment
echo Testing deployment...
curl -s http://%SERVER_IP%/health >nul
if errorlevel 1 (
    echo WARNING: Health check failed. Check logs with: docker-compose logs
) else (
    echo SUCCESS: Resume Parser is responding correctly!
)

echo.
echo Setup complete! Press any key to view logs...
pause
docker-compose logs --tail=50
