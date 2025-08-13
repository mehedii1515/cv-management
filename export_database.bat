@echo off
echo ========================================
echo Database Export for Portable Version
echo ========================================
echo.
echo This will export your current PostgreSQL database for the portable version.
echo.

REM Get database connection details from .env
if exist "backend\.env" (
    for /f "tokens=2 delims==" %%a in ('findstr "DB_NAME" backend\.env') do set DB_NAME=%%a
    for /f "tokens=2 delims==" %%a in ('findstr "DB_USER" backend\.env') do set DB_USER=%%a
    for /f "tokens=2 delims==" %%a in ('findstr "DB_HOST" backend\.env') do set DB_HOST=%%a
    for /f "tokens=2 delims==" %%a in ('findstr "DB_PORT" backend\.env') do set DB_PORT=%%a
    for /f "tokens=2 delims==" %%a in ('findstr "DB_PASSWORD" backend\.env') do set DB_PASSWORD=%%a
) else (
    echo Error: backend\.env file not found
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

echo Database: %DB_NAME%
echo User: %DB_USER%
echo Host: %DB_HOST%
echo Port: %DB_PORT%
echo.

REM Set password environment variable for pg_dump
set PGPASSWORD=%DB_PASSWORD%

REM Export the database
echo Creating database dump...
echo This may take a few minutes depending on your data size...
echo.

pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f portable_postgres\database_backup.sql

REM Clear the password from environment
set PGPASSWORD=

if exist "portable_postgres\database_backup.sql" (
    echo.
    echo ========================================
    echo Database Export Successful!
    echo ========================================
    echo.
    echo File: portable_postgres\database_backup.sql
    echo.
    echo Your database has been exported and will be automatically
    echo restored when users first run the portable version.
    echo.
    echo Next steps:
    echo 1. Test the portable version: cd portable_postgres && START_RESUME_PARSER.bat
    echo 2. Create distribution package: zip the portable_postgres folder
    echo 3. Share with users - they'll get your complete database!
    echo.
) else (
    echo.
    echo ========================================
    echo Database Export Failed
    echo ========================================
    echo.
    echo Possible issues:
    echo - PostgreSQL is not running
    echo - Wrong database credentials in backend\.env
    echo - pg_dump is not in PATH
    echo - Database connection issues
    echo.
    echo Please check your PostgreSQL connection and try again.
    echo.
)

pause
