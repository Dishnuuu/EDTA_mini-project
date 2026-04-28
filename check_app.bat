@echo off
"C:\Users\LOQ\OneDrive\Desktop\mini project\ekajalakkam-main\ekajalakkam-main\venv\Scripts\python.exe" -m py_compile "C:\Users\LOQ\OneDrive\Desktop\mini project\ekajalakkam-main\ekajalakkam-main\src\app.py"
if errorlevel 1 (
    echo Compilation failed
) else (
    echo Compilation OK
)