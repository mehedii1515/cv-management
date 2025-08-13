@echo off
echo ========================================
echo Resume Parser - Automatic Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10, 3.11, or 3.12 from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

:: Check Python version compatibility
python -c "import sys; exit(0 if (3,10) <= sys.version_info[:2] <= (3,12) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python version %PYTHON_VERSION% is not supported
    echo Please install Python 3.10, 3.11, or 3.12
    echo The unstructured library requires Python 3.10-3.12
    pause
    exit /b 1
)

echo ✓ Python %PYTHON_VERSION% is compatible

:: Create virtual environment
echo.
echo Creating virtual environment...
if exist "backend\venv" (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q "backend\venv"
)

cd backend
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

:: Activate virtual environment and install dependencies
echo.
echo Installing Python dependencies...
call venv\Scripts\activate.bat

:: Upgrade pip first
python -m pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✓ Python dependencies installed

:: Download and setup Poppler
echo.
echo Setting up Poppler for PDF processing...
if not exist "poppler-24.08.0" (
    echo Downloading Poppler...
    curl -L -o poppler.zip "https://github.com/oschwartz10612/poppler-windows/releases/latest/download/Release-24.08.0-0.zip"
    if errorlevel 1 (
        echo ERROR: Failed to download Poppler
        echo Please check your internet connection
        pause
        exit /b 1
    )
    
    echo Extracting Poppler...
    powershell -command "Expand-Archive -Path 'poppler.zip' -DestinationPath '.' -Force"
    del poppler.zip
    echo ✓ Poppler installed
) else (
    echo ✓ Poppler already installed
)

:: Setup environment file
echo.
echo Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo ✓ Environment file created (.env)
    echo.
    echo IMPORTANT: Please edit the .env file and add your API keys:
    echo - OPENAI_API_KEY=your_openai_key_here
    echo - GOOGLE_API_KEY=your_gemini_key_here
    echo.
) else (
    echo ✓ Environment file already exists
)

:: Run initial Django setup
echo.
echo Setting up Django database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to setup database
    pause
    exit /b 1
)
echo ✓ Database setup complete

:: Create superuser prompt
echo.
echo Creating Django admin user...
echo You can create an admin user now or skip this step
choice /M "Do you want to create an admin user now"
if errorlevel 2 goto skip_superuser
python manage.py createsuperuser
:skip_superuser

:: Install frontend dependencies
echo.
echo Setting up frontend...
cd ..\frontend
if exist "node_modules" (
    echo Node modules already exist, skipping npm install
) else (
    :: Check if npm is installed
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo WARNING: npm is not installed
        echo Please install Node.js from https://nodejs.org
        echo Frontend setup skipped
        goto skip_frontend
    )
    
    echo Installing frontend dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        echo Please check your Node.js installation
        goto skip_frontend
    )
    echo ✓ Frontend dependencies installed
)
:skip_frontend

cd ..\backend

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Edit .env file with your API keys
echo 2. Run: start_servers.bat
echo.
echo For manual startup:
echo Backend:  cd backend && call venv\Scripts\activate && python manage.py runserver
echo Frontend: cd frontend && npm run dev
echo.
echo Admin panel: http://localhost:8000/admin/
echo Application: http://localhost:3000/
echo.
pause
