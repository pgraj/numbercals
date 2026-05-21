@echo off
REM NumberCals -- one-command runner for Windows.
REM Usage:  double-click run.bat, or run "run.bat" from cmd / PowerShell.

setlocal enabledelayedexpansion

cd /d "%~dp0backend"

REM 1. Find Python
set "PY="
for %%C in (py python python3) do (
  where %%C >nul 2>nul
  if !errorlevel! == 0 (
    set "PY=%%C"
    goto :found_python
  )
)

echo ERROR: Python is not installed or not in your PATH.
echo Install Python 3.9+ from https://www.python.org/downloads/
echo Make sure to tick "Add Python to PATH" during install.
pause
exit /b 1

:found_python
echo Using %PY%
%PY% --version

REM 2. Create venv if missing
if not exist ".venv\Scripts\activate.bat" (
  echo Creating virtual environment in backend\.venv ...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
  )
)

REM 3. Activate + install
call ".venv\Scripts\activate.bat"

if not exist ".venv\.installed" (
  echo Installing dependencies ^(this may take a minute^) ...
  python -m pip install --quiet --upgrade pip
  python -m pip install --quiet -r requirements.txt
  if errorlevel 1 (
    echo Install failed. See messages above.
    pause
    exit /b 1
  )
  echo. > ".venv\.installed"
)

REM 4. Start the server
echo.
echo ==========================================
echo   NumberCals is starting at:
echo     http://localhost:8000
echo.
echo   Press Ctrl+C to stop.
echo ==========================================
echo.

python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause
