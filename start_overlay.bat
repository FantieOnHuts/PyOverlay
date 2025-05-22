@echo off
setlocal

set VENV_DIR=.venv
set SCRIPT_NAME=overlay_app.py
set REQUIREMENTS=PyQt5 PyQtWebEngine keyboard

REM check for python.
python --version >nul 2>&1
if %errorlevel% neq 0 (
    No python.
    exit /b 1
)

REM create virtual room if there is none.
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo no virtual room "%VENV_DIR%".  Creating one.
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo Error creating virtual room.
        pause
        exit /b 1
    )
    echo virtual room created.
)

REM get into virtual.
echo Activate virtual room...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo error activating virtual room.
    pause
    exit /b 1
)

REM  update dependencies.
echo Getting dependencies: %REQUIREMENTS%
pip install --upgrade pip >nul
pip install %REQUIREMENTS%
if %errorlevel% neq 0 (
    echo error installing dependecies.
    pause
    exit /b 1
)

REM start.
echo Start %SCRIPT_NAME%...
echo F9 to toggle see trough.
echo F8 to click trough mode.

python "%SCRIPT_NAME%"

echo closed.
deactivate
endlocal
pause
