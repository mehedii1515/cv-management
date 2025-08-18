@echo off
echo =====================================
echo    Resume Parser Management
echo =====================================

:menu
echo.
echo 1. Start Resume Parser
echo 2. Stop Resume Parser
echo 3. View Logs
echo 4. Check Status
echo 5. Update Application
echo 6. Backup Database
echo 7. Reset Everything
echo 8. Exit
echo.
set /p choice="Choose an option (1-8): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto status
if "%choice%"=="5" goto update
if "%choice%"=="6" goto backup
if "%choice%"=="7" goto reset
if "%choice%"=="8" goto exit

echo Invalid choice. Please try again.
goto menu

:start
echo Starting Resume Parser...
docker-compose up -d
echo Resume Parser started!
goto menu

:stop
echo Stopping Resume Parser...
docker-compose down
echo Resume Parser stopped!
goto menu

:logs
echo Viewing logs (Press Ctrl+C to exit)...
docker-compose logs -f
goto menu

:status
echo Service Status:
docker-compose ps
echo.
echo Disk Usage:
docker system df
goto menu

:update
echo Updating Resume Parser...
docker-compose pull
docker-compose up -d
echo Update complete!
goto menu

:backup
echo Creating database backup...
set backup_file=backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.sql
docker-compose exec postgres pg_dump -U resume_parser_user resume_parser > %backup_file%
echo Database backed up to %backup_file%
goto menu

:reset
echo WARNING: This will delete all data!
set /p confirm="Are you sure? (y/N): "
if /i "%confirm%"=="y" (
    docker-compose down -v
    docker system prune -f
    echo Everything reset!
) else (
    echo Reset cancelled.
)
goto menu

:exit
echo Goodbye!
exit /b 0
