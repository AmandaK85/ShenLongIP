@echo off
chcp 65001 >nul
echo ========================================
echo ShenLong IP Test Scheduler Setup
echo ========================================
echo.

echo Installing required packages...
pip install schedule

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install schedule package
    pause
    exit /b 1
)

echo.
echo Package installed successfully!
echo.
echo Starting the scheduler...
echo The test suite will run daily at 9:00 AM
echo Press Ctrl+C to stop the scheduler
echo.

python scheduled_test_runner.py

pause 