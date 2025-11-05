@echo off
echo ========================================
echo Plex Toolbox - Complete Reset and Reinstall
echo ========================================
echo.
echo This will:
echo 1. Remove all installed dependencies
echo 2. Reinstall everything from scratch
echo 3. Use the simplest installation method
echo.
echo Press Ctrl+C to cancel, or
pause

cd /d "%~dp0"

echo.
echo ========================================
echo Step 1: Cleaning Up
echo ========================================

if exist "backend\venv\" (
    echo Removing backend virtual environment...
    rd /s /q "backend\venv" 2>nul
)

if exist "frontend\node_modules\" (
    echo Removing frontend node_modules...
    rd /s /q "frontend\node_modules" 2>nul
)

if exist "backend\plex_toolbox.db" (
    echo Removing old database...
    del "backend\plex_toolbox.db" 2>nul
)

if exist "backend\logs\" (
    echo Removing log files...
    rd /s /q "backend\logs" 2>nul
)

echo Cleanup complete!

echo.
echo ========================================
echo Step 2: Setting up Backend
echo ========================================

cd backend

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

call venv\Scripts\activate

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing Python packages (one at a time)...
pip install fastapi
pip install "uvicorn[standard]"
pip install "pydantic>=2.0,<3.0"
pip install pydantic-settings
pip install PlexAPI
pip install sqlalchemy
pip install python-dotenv
pip install loguru

echo.
echo Creating backend .env file...
(
    echo DATABASE_URL=sqlite:///./plex_toolbox.db
    echo ENVIRONMENT=development
    echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
    echo SECRET_KEY=dev-secret-key
) > .env

cd ..

echo.
echo ========================================
echo Step 3: Setting up Frontend
echo ========================================

cd frontend

echo Installing npm packages...
call npm install --legacy-peer-deps
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] npm install had issues, trying alternative method...
    call npm install --force
)

echo.
echo Creating frontend .env file...
echo REACT_APP_API_URL=http://localhost:8000/api > .env

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start development:
echo   start-simple.bat
echo.
echo Or manually:
echo   Terminal 1: start-backend.bat
echo   Terminal 2: start-frontend.bat
echo.
pause
