@echo off
chcp 65001 >nul
echo ========================================
echo Windows Task Scheduler Setup (Manual)
echo ========================================
echo.

REM Get current directory
set "CURRENT_DIR=%CD%"
set "SCRIPT_PATH=%CURRENT_DIR%\run_all_tests.py"

REM Find Python path
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"

echo Current Directory: %CURRENT_DIR%
echo Python Path: %PYTHON_PATH%
echo Script Path: %SCRIPT_PATH%
echo.

REM Check if script exists
if not exist "%SCRIPT_PATH%" (
    echo ERROR: run_all_tests.py not found in current directory!
    echo Please run this script from the directory containing run_all_tests.py
    pause
    exit /b 1
)

REM Create the scheduled task using schtasks
echo Creating scheduled task...
schtasks /create /tn "ShenLongIP_DailyTests" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" /sc daily /st 09:00 /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Task created successfully!
    echo.
    echo Task Details:
    echo   Name: ShenLongIP_DailyTests
    echo   Schedule: Daily at 09:00
    echo   Command: %PYTHON_PATH% %SCRIPT_PATH%
    echo   Working Directory: %CURRENT_DIR%
    echo.
    echo To manage this task:
    echo   1. Open Task Scheduler (taskschd.msc)
    echo   2. Find the task named 'ShenLongIP_DailyTests'
    echo   3. Right-click to enable/disable/delete
    echo.
    echo To run the task manually:
    echo   schtasks /run /tn "ShenLongIP_DailyTests"
    echo.
    echo To delete the task:
    echo   schtasks /delete /tn "ShenLongIP_DailyTests" /f
) else (
    echo.
    echo ❌ Error creating task. Try running as Administrator.
    echo.
    echo To run as Administrator:
    echo   1. Right-click on this batch file
    echo   2. Select "Run as administrator"
)

echo.
pause 