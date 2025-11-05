@echo off
echo ========================================
echo Starting Plex Toolbox Backend
echo ========================================
echo.

cd /d "%~dp0backend"

if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run full-reset.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate

if not exist ".env" (
    echo Creating .env file...
    (
        echo DATABASE_URL=sqlite:///./plex_toolbox.db
        echo ENVIRONMENT=development
        echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
        echo SECRET_KEY=dev-secret-key
    ) > .env
)

echo Starting FastAPI backend on http://localhost:8000
echo API Documentation: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
