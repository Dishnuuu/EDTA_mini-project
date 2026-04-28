@echo off
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%src"
echo Starting Ekajalakkam Backend...
"..\venv\Scripts\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 2>&1
pause