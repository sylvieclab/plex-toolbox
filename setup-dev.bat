@echo off
echo ========================================
echo Plex Toolbox - Setup Script
echo ========================================
echo.
echo This script will help you set up Plex Toolbox for local development.
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python is installed

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js is installed

:: Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed or not in PATH
    pause
    exit /b 1
)
echo [OK] npm is installed

echo.
echo ========================================
echo Setting up Backend
echo ========================================
cd /d "%~dp0backend"

:: Create virtual environment
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo Python virtual environment already exists
)

:: Activate and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate
pip install --upgrade pip --quiet
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    echo.
    echo This is usually because psycopg2 requires PostgreSQL to be installed.
    echo Since you're using SQLite, you can ignore this error.
    echo The simplified requirements.txt has been updated.
    pause
)

:: Create .env if it doesn't exist
if not exist ".env" (
    echo Creating backend .env file...
    (
        echo DATABASE_URL=sqlite:///./plex_toolbox.db
        echo ENVIRONMENT=development
        echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
        echo SECRET_KEY=dev-secret-key-change-in-production
    ) > .env
    echo [INFO] Created backend\.env with SQLite configuration
) else (
    echo [INFO] backend\.env already exists
)

echo [OK] Backend setup complete

echo.
echo ========================================
echo Setting up Frontend
echo ========================================
cd /d "%~dp0frontend"

:: Install npm dependencies
echo Installing npm dependencies (this may take a few minutes)...
npm install --legacy-peer-deps
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install npm dependencies
    pause
    exit /b 1
)

:: Create .env if it doesn't exist
if not exist ".env" (
    echo Creating frontend .env file...
    echo REACT_APP_API_URL=http://localhost:8000/api > .env
    echo [INFO] Created frontend\.env
) else (
    echo [INFO] frontend\.env already exists
)

echo [OK] Frontend setup complete

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your development environment is ready!
echo.
echo To start development, run:
echo   start-simple.bat
echo.
echo Or run backend and frontend separately:
echo   start-backend.bat (in one terminal)
echo   start-frontend.bat (in another terminal)
echo.
echo Useful commands:
echo   cleanup.bat - Remove all dependencies and start fresh
echo.
echo Documentation:
echo   QUICK_START.md - Quick start guide
echo   Claude_Docs\LOCAL_DEV_READY.md - Full local dev guide
echo.
pause
