@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please wait while I set it up...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install gizeh numpy Pillow cairosvg pycairo
) else (
    call venv\Scripts\activate.bat
)

:: Ensure DLLs are in path for the session
set PATH=%PATH%;%CD%

python gui.py
pause
