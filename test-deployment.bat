@echo off
echo =====================================
echo    Quick Resume Parser Test
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

echo Stopping any existing containers...
docker-compose -f docker-compose.simple.yml down -v

echo Starting basic Resume Parser (PostgreSQL + Backend + Frontend)...
docker-compose -f docker-compose.simple.yml up --build -d

echo Waiting for services to start...
timeout /t 30 /nobreak

echo Checking service status...
docker-compose -f docker-compose.simple.yml ps

echo.
echo =====================================
echo    Basic Resume Parser is running!
echo =====================================
echo.
echo Access URLs:
echo  Frontend: http://%SERVER_IP%:3000
echo  Backend: http://%SERVER_IP%:8000
echo  API: http://%SERVER_IP%:8000/api
echo  Admin: http://%SERVER_IP%:8000/admin
echo.

REM Test the deployment
echo Testing frontend...
curl -s http://%SERVER_IP%:3000 >nul
if errorlevel 1 (
    echo WARNING: Frontend not responding
) else (
    echo SUCCESS: Frontend is working!
)

echo Testing backend...
curl -s http://%SERVER_IP%:8000/api/health/ >nul
if errorlevel 1 (
    echo WARNING: Backend health check failed
) else (
    echo SUCCESS: Backend is working!
)

echo.
echo Management Commands:
echo  Stop: docker-compose -f docker-compose.simple.yml down
echo  Logs: docker-compose -f docker-compose.simple.yml logs -f
echo  Restart: docker-compose -f docker-compose.simple.yml restart
echo.
echo Press any key to view logs...
pause
docker-compose -f docker-compose.simple.yml logs --tail=50
