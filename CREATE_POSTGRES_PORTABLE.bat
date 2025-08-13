@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Resume Parser - PostgreSQL Portable Setup
echo ========================================
echo.
echo This will create a portable version with PostgreSQL database included.
echo Users will get your complete database with all existing resumes!
echo.

REM Create portable directory structure
echo Creating portable directory structure...
if exist "portable_postgres" rmdir /s /q "portable_postgres"
mkdir portable_postgres
mkdir portable_postgres\python
mkdir portable_postgres\node
mkdir portable_postgres\poppler
mkdir portable_postgres\postgresql
mkdir portable_postgres\app

echo.
echo ========================================
echo Downloading Dependencies (~250MB total)
echo ========================================
echo.

REM Download portable Python 3.11
echo [1/5] Downloading portable Python 3.11 (~30MB)...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Write-Host 'Downloading Python...'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile 'portable_postgres\python-embed.zip'}"

echo Extracting Python...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'portable_postgres\python-embed.zip' -DestinationPath 'portable_postgres\python' -Force"
del portable_postgres\python-embed.zip

REM Download get-pip.py
echo Downloading pip installer...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'portable_postgres\python\get-pip.py'"

REM Enable site-packages in python311._pth
echo Enabling site-packages...
echo import site >> portable_postgres\python\python311._pth

REM Download portable Node.js
echo [2/5] Downloading portable Node.js (~40MB)...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Write-Host 'Downloading Node.js...'; Invoke-WebRequest -Uri 'https://nodejs.org/dist/v18.19.0/node-v18.19.0-win-x64.zip' -OutFile 'portable_postgres\node.zip'"

echo Extracting Node.js...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'portable_postgres\node.zip' -DestinationPath 'portable_postgres\node' -Force"
del portable_postgres\node.zip

REM Rename node folder
move "portable_postgres\node\node-v18.19.0-win-x64" "portable_postgres\node\nodejs" >nul

REM Download Poppler
echo [3/5] Downloading Poppler PDF tools (~20MB)...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Write-Host 'Downloading Poppler...'; Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip' -OutFile 'portable_postgres\poppler.zip'"

echo Extracting Poppler...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'portable_postgres\poppler.zip' -DestinationPath 'portable_postgres\poppler' -Force"
del portable_postgres\poppler.zip

REM Download Portable PostgreSQL
echo [4/5] Downloading Portable PostgreSQL (~100MB)...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Write-Host 'Downloading PostgreSQL...'; Invoke-WebRequest -Uri 'https://get.enterprisedb.com/postgresql/postgresql-15.4-1-windows-x64-binaries.zip' -OutFile 'portable_postgres\postgresql.zip'"

echo Extracting PostgreSQL...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path 'portable_postgres\postgresql.zip' -DestinationPath 'portable_postgres\postgresql' -Force"
del portable_postgres\postgresql.zip

echo.
echo ========================================
echo Installing Dependencies
echo ========================================
echo.

REM Set portable paths
set PYTHON_PATH=%CD%\portable_postgres\python
set NODE_PATH=%CD%\portable_postgres\node\nodejs
set POSTGRES_PATH=%CD%\portable_postgres\postgresql\pgsql\bin
set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%NODE_PATH%;%POSTGRES_PATH%;%PATH%

REM Install pip
echo Installing pip...
cd portable_postgres\python
python get-pip.py --quiet
cd ..\..

REM Copy application files
echo [5/5] Copying application files...
echo Copying backend...
xcopy /E /I /Y /Q backend portable_postgres\app\backend

echo Copying frontend...
xcopy /E /I /Y /Q frontend portable_postgres\app\frontend

REM Install Python dependencies
echo Installing Python dependencies (~60MB)...
cd portable_postgres\app\backend
set PYTHONPATH=%CD%\..\..\python;%CD%\..\..\python\Lib\site-packages
..\..\..\python\python -m pip install -r requirements.txt --target ..\..\..\python\Lib\site-packages --quiet --disable-pip-version-check
cd ..\..\..

REM Install Node.js dependencies
echo Installing Node.js dependencies (~50MB)...
cd portable_postgres\app\frontend
set PATH=%CD%\..\..\..\node\nodejs;%PATH%
npm install --silent --no-progress
cd ..\..\..

echo.
echo ========================================
echo Setting up PostgreSQL Database
echo ========================================
echo.

REM Initialize PostgreSQL data directory
set PGDATA=%CD%\portable_postgres\postgresql\data
set POSTGRES_PATH=%CD%\portable_postgres\postgresql\pgsql\bin
set PATH=%POSTGRES_PATH%;%PATH%

echo Initializing PostgreSQL database...
"%POSTGRES_PATH%\initdb" -D "%PGDATA%" -U postgres --auth-local=trust --auth-host=trust

echo.
echo ========================================
echo Creating Database Export Script
echo ========================================
echo.

REM Create database export script
(
echo @echo off
echo echo Exporting your current PostgreSQL database...
echo echo.
echo.
echo REM Get database connection details from .env
echo for /f "tokens=2 delims==" %%%%a in ^('findstr "DB_NAME" backend\.env'^) do set DB_NAME=%%%%a
echo for /f "tokens=2 delims==" %%%%a in ^('findstr "DB_USER" backend\.env'^) do set DB_USER=%%%%a
echo for /f "tokens=2 delims==" %%%%a in ^('findstr "DB_HOST" backend\.env'^) do set DB_HOST=%%%%a
echo for /f "tokens=2 delims==" %%%%a in ^('findstr "DB_PORT" backend\.env'^) do set DB_PORT=%%%%a
echo.
echo echo Database: %%DB_NAME%%
echo echo User: %%DB_USER%%
echo echo Host: %%DB_HOST%%
echo echo Port: %%DB_PORT%%
echo echo.
echo.
echo REM Export the database
echo echo Creating database dump...
echo pg_dump -h %%DB_HOST%% -p %%DB_PORT%% -U %%DB_USER%% -d %%DB_NAME%% -f portable_postgres\database_backup.sql
echo.
echo if exist "portable_postgres\database_backup.sql" ^(
echo     echo Database exported successfully!
echo     echo File: portable_postgres\database_backup.sql
echo ^) else ^(
echo     echo Error: Database export failed
echo     echo Please check your PostgreSQL connection
echo ^)
echo.
echo pause
) > export_database.bat

echo.
echo ========================================
echo Creating Portable Launcher
echo ========================================
echo.

REM Create portable launcher with PostgreSQL
(
echo @echo off
echo setlocal enabledelayedexpansion
echo.
echo echo ========================================
echo echo Resume Parser - PostgreSQL Portable
echo echo ========================================
echo echo.
echo.
echo REM Set portable paths
echo set PYTHON_PATH=%%~dp0python
echo set NODE_PATH=%%~dp0node\nodejs
echo set POPPLER_PATH=%%~dp0poppler\poppler-24.08.0\Library\bin
echo set POSTGRES_PATH=%%~dp0postgresql\pgsql\bin
echo set PGDATA=%%~dp0postgresql\data
echo set PATH=%%PYTHON_PATH%%;%%PYTHON_PATH%%\Scripts;%%NODE_PATH%%;%%POPPLER_PATH%%;%%POSTGRES_PATH%%;%%PATH%%
echo.
echo REM Check if database is restored
echo if not exist "%%PGDATA%%\resume_parser_db" ^(
echo     echo First time setup - Setting up database...
echo     echo.
echo     echo Starting PostgreSQL server...
echo     start /min "PostgreSQL" "%%POSTGRES_PATH%%\pg_ctl" -D "%%PGDATA%%" start
echo     timeout /t 5 /nobreak ^>nul
echo.
echo     echo Creating resume_parser database...
echo     "%%POSTGRES_PATH%%\createdb" -U postgres resume_parser
echo.
echo     if exist "database_backup.sql" ^(
echo         echo Restoring your data from database_backup.sql...
echo         "%%POSTGRES_PATH%%\psql" -U postgres -d resume_parser -f database_backup.sql
echo         echo Database restored successfully!
echo     ^) else ^(
echo         echo No database backup found. Starting with empty database.
echo     ^)
echo.
echo     echo. ^> "%%PGDATA%%\resume_parser_db"
echo ^) else ^(
echo     echo Starting PostgreSQL server...
echo     start /min "PostgreSQL" "%%POSTGRES_PATH%%\pg_ctl" -D "%%PGDATA%%" start
echo     timeout /t 3 /nobreak ^>nul
echo ^)
echo.
echo REM Check if .env exists
echo if not exist "app\backend\.env" ^(
echo     echo Creating environment configuration...
echo     copy "app\backend\.env.example" "app\backend\.env" ^>nul
echo.
echo     REM Update .env for portable PostgreSQL
echo     ^(
echo     echo # Django Configuration
echo     echo DEBUG=True
echo     echo SECRET_KEY=your-secret-key-here
echo     echo ALLOWED_HOSTS=localhost,127.0.0.1
echo     echo.
echo     echo # PostgreSQL Database
echo     echo DB_NAME=resume_parser
echo     echo DB_USER=postgres
echo     echo DB_PASSWORD=
echo     echo DB_HOST=localhost
echo     echo DB_PORT=5432
echo     echo.
echo     echo # OpenAI Configuration
echo     echo OPENAI_API_KEY=your_openai_key_here
echo     echo OPENAI_MODEL=gpt-4o-mini
echo     echo.
echo     echo # Gemini Configuration
echo     echo GOOGLE_API_KEY=your_gemini_key_here
echo     echo GEMINI_MODEL=gemini-1.5-flash
echo     echo.
echo     echo # AI Provider Selection
echo     echo AI_PROVIDER=both
echo     ^) ^> "app\backend\.env"
echo.
echo     echo ========================================
echo     echo API KEYS REQUIRED
echo     echo ========================================
echo     echo.
echo     echo Please edit the file: app\backend\.env
echo     echo.
echo     echo Add your API keys:
echo     echo - OPENAI_API_KEY=your_openai_key_here
echo     echo - GOOGLE_API_KEY=your_gemini_key_here
echo     echo.
echo     echo Get API keys from:
echo     echo - OpenAI: https://platform.openai.com/api-keys
echo     echo - Google: https://aistudio.google.com/app/apikey
echo     echo.
echo     echo The .env file will open now. Edit it and save, then run this file again.
echo     echo.
echo     start notepad "app\backend\.env"
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Starting Resume Parser with PostgreSQL...
echo echo.
echo echo Backend:  http://localhost:8000/
echo echo Frontend: http://localhost:3000/
echo echo Admin:    http://localhost:8000/admin/
echo echo Database: PostgreSQL ^(localhost:5432^)
echo echo.
echo.
echo REM Kill any existing processes
echo taskkill /F /IM python.exe 2^>nul
echo taskkill /F /IM node.exe 2^>nul
echo.
echo REM Run Django migrations
echo cd app\backend
echo echo Running database migrations...
echo python manage.py migrate ^>nul 2^>^&1
echo.
echo REM Start Django in background
echo echo Starting backend server...
echo start "Resume Parser Backend" /min cmd /c "python manage.py runserver 8000"
echo.
echo REM Wait for backend to start
echo timeout /t 3 /nobreak ^>nul
echo.
echo REM Start Next.js frontend
echo echo Starting frontend server...
echo cd ..\frontend
echo start "Resume Parser Frontend" /min cmd /c "npm run dev"
echo.
echo echo.
echo echo ========================================
echo echo Resume Parser Started Successfully!
echo echo ========================================
echo echo.
echo echo Please wait 10-15 seconds for servers to start completely.
echo echo.
echo echo Application URLs:
echo echo - Main App: http://localhost:3000/
echo echo - Admin:    http://localhost:8000/admin/
echo echo - API:      http://localhost:8000/api/
echo echo - Database: PostgreSQL on localhost:5432
echo echo.
echo echo To stop the application:
echo echo - Close this window, or
echo echo - Press Ctrl+C and close the server windows
echo echo - PostgreSQL will stop automatically
echo echo.
echo.
echo REM Wait and open browser
echo echo Opening application in browser...
echo timeout /t 8 /nobreak ^>nul
echo start http://localhost:3000/
echo.
echo echo Application is now running with PostgreSQL!
echo echo Keep this window open while using the application.
echo echo.
echo pause
echo.
echo REM Stop PostgreSQL when exiting
echo echo Stopping PostgreSQL server...
echo "%%POSTGRES_PATH%%\pg_ctl" -D "%%PGDATA%%" stop
) > portable_postgres\START_RESUME_PARSER.bat

echo.
echo ========================================
echo PostgreSQL Portable Setup Complete!
echo ========================================
echo.
echo Created: portable_postgres\ folder
echo.
echo ✅ What's included:
echo - Python 3.11 (embedded)
echo - Node.js 18 (portable)
echo - PostgreSQL 15 (portable)
echo - Poppler PDF tools
echo - All dependencies pre-installed
echo - Your complete Resume Parser application
echo.
echo 🔄 Next steps:
echo 1. Run 'export_database.bat' to export your current PostgreSQL data
echo 2. Copy the generated 'database_backup.sql' to portable_postgres\ folder
echo 3. Test the portable version
echo 4. Distribute the portable_postgres\ folder
echo.
echo Users will get your complete database with all existing resumes!
echo.
pause
