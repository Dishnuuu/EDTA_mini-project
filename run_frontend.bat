@echo off
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
echo Starting Ekajalakkam Frontend...
".\venv\Scripts\streamlit.exe" run src/app.py 2>&1
pause