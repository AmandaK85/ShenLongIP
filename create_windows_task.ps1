# PowerShell script to create Windows Task Scheduler task
# This will run the test suite daily at 9:00 AM

param(
    [string]$TaskName = "ShenLongIP_DailyTests",
    [string]$Time = "09:00"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Windows Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the current directory
$CurrentDir = Get-Location
$ScriptPath = Join-Path $CurrentDir "run_all_tests.py"
$PythonPath = (Get-Command python).Source

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host "Python Path: $PythonPath" -ForegroundColor Yellow
Write-Host "Script Path: $ScriptPath" -ForegroundColor Yellow
Write-Host ""

# Check if the script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: run_all_tests.py not found in current directory!" -ForegroundColor Red
    Write-Host "Please run this script from the directory containing run_all_tests.py" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create the action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory $CurrentDir

# Create the trigger (daily at 9:00 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Create the settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Create the task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Run ShenLong IP Admin Panel tests daily at 9:00 AM"
    
    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at $Time" -ForegroundColor White
    Write-Host "  Command: $PythonPath $ScriptPath" -ForegroundColor White
    Write-Host "  Working Directory: $CurrentDir" -ForegroundColor White
    Write-Host ""
    Write-Host "To manage this task:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
    Write-Host "  2. Find the task named '$TaskName'" -ForegroundColor White
    Write-Host "  3. Right-click to enable/disable/delete" -ForegroundColor White
    Write-Host ""
    Write-Host "To run the task manually:" -ForegroundColor Yellow
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host ""
    Write-Host "To delete the task:" -ForegroundColor Yellow
    Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:$false" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error creating task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running PowerShell as Administrator" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit" 