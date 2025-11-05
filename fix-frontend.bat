@echo off
echo ========================================
echo Fixing Frontend Dependencies
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Removing node_modules and package-lock.json...
if exist "node_modules\" rd /s /q "node_modules"
if exist "package-lock.json" del "package-lock.json"

echo.
echo Installing dependencies with --force flag...
npm install --force

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Now run: start-frontend.bat
echo.
pause
