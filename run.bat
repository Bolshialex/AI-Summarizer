@echo off
:: Launches the backend and frontend in two separate Console windows.

set "ROOT=%~dp0"

cd /d "%ROOT%backend"
start "Backend" cmd /k run_server.bat

cd /d "%ROOT%frontend"
start "Frontend" cmd /k "npm install && npm run dev"

echo Backend and frontend are starting in two windows.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
