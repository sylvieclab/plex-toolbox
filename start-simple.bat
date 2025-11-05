@echo off
echo ========================================
echo Plex Toolbox - Simple Start
echo ========================================
echo.

cd /d "%~dp0"

REM Check if backend is set up
if not exist "backend\venv\" (
    echo Backend not set up! Run full-reset.bat first.
    pause
    exit /b 1
)

REM Check if frontend is set up
if not exist "frontend\node_modules\" (
    echo Frontend not set up! Run full-reset.bat first.
    pause
    exit /b 1
)

REM Create backend .env if needed
if not exist "backend\.env" (
    echo Creating backend configuration...
    (
        echo DATABASE_URL=sqlite:///./plex_toolbox.db
        echo ENVIRONMENT=development
        echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
        echo SECRET_KEY=dev-secret-key
    ) > backend\.env
)

REM Create frontend .env if needed  
if not exist "frontend\.env" (
    echo Creating frontend configuration...
    echo REACT_APP_API_URL=http://localhost:8000/api > frontend\.env
)

echo.
echo ========================================
echo Starting Services
echo ========================================
echo.

REM Start backend in new window
start "Plex Toolbox Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate && echo Starting backend... && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend
cd frontend
echo.
echo ========================================
echo Services Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo Frontend: http://localhost:3000 (starting now...)
echo.
echo A new window was opened for the backend.
echo Press Ctrl+C in this window to stop the frontend.
echo You'll need to close the backend window separately.
echo ========================================
echo.

npm start
