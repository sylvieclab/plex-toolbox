@echo off
echo ========================================
echo Starting Plex Toolbox Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules\" (
    echo Node modules not found!
    echo Please run full-reset.bat first
    pause
    exit /b 1
)

if not exist ".env" (
    echo Creating .env file...
    echo REACT_APP_API_URL=http://localhost:8000/api > .env
)

echo Starting React development server...
echo Frontend will open at http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npm start
