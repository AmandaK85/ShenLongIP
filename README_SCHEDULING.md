# Automated Test Scheduling Guide

This guide shows you how to set up your ShenLong IP test suite to run automatically every day at 9:00 AM.

## 🕘 Option 1: Windows Task Scheduler (Recommended)

This is the most reliable method for Windows systems.

### Setup Steps:

1. **Open PowerShell as Administrator**
   - Right-click on Start menu
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to your project directory**
   ```powershell
   cd "C:\Selenium_Tests\Github\ShenLongIP"
   ```

3. **Run the setup script**
   ```powershell
   .\create_windows_task.ps1
   ```

4. **Verify the task was created**
   - Press `Win + R`, type `taskschd.msc`, press Enter
   - Look for task named "ShenLongIP_DailyTests"

### Benefits:
- ✅ Runs even when you're not logged in
- ✅ Survives system restarts
- ✅ Built into Windows
- ✅ Can be managed through GUI

### Manage the Task:
- **Enable/Disable**: Right-click task → Enable/Disable
- **Run Manually**: Right-click task → Run
- **Delete**: Right-click task → Delete

---

## 🐍 Option 2: Python Scheduler

This method runs a Python script that stays active and schedules the tests.

### Setup Steps:

1. **Install the schedule package**
   ```bash
   pip install schedule
   ```

2. **Run the scheduler**
   ```bash
   python scheduled_test_runner.py
   ```

3. **Or use the batch file**
   ```bash
   setup_scheduler.bat
   ```

### Benefits:
- ✅ Simple to set up
- ✅ Easy to modify schedule
- ✅ Detailed logging

### Limitations:
- ❌ Must keep the script running
- ❌ Stops if you log out or restart

---

## 📊 Monitoring and Logs

### Test Results
- **Main results**: `test_results.txt` (updated after each run)
- **Scheduler logs**: `scheduled_tests.log` (if using Python scheduler)

### Check Recent Runs
```bash
# View latest test results
type test_results.txt

# View scheduler logs (if using Python scheduler)
type scheduled_tests.log
```

---

## ⚙️ Customization

### Change the Time
- **Windows Task Scheduler**: Edit the task in `taskschd.msc`
- **Python Scheduler**: Edit line 67 in `scheduled_test_runner.py`

### Change the Schedule
- **Daily**: `schedule.every().day.at("09:00")`
- **Every Monday**: `schedule.every().monday.at("09:00")`
- **Every hour**: `schedule.every().hour.do(run_test_suite)`
- **Every 30 minutes**: `schedule.every(30).minutes.do(run_test_suite)`

---

## 🔧 Troubleshooting

### Task Scheduler Issues
1. **"Access Denied"**: Run PowerShell as Administrator
2. **Task not running**: Check if Python is in PATH
3. **Wrong working directory**: Verify the script path in task properties

### Python Scheduler Issues
1. **Script stops**: Check for errors in `scheduled_tests.log`
2. **Tests fail**: Check `test_results.txt` for details
3. **Package missing**: Run `pip install schedule`

### General Issues
1. **Tests timeout**: Increase timeout in `scheduled_test_runner.py` (line 47)
2. **Unicode errors**: Ensure UTF-8 encoding is set
3. **Browser issues**: Check if Chrome is installed and accessible

---

## 📋 Quick Commands

### Create Windows Task (as Administrator)
```powershell
.\create_windows_task.ps1
```

### Start Python Scheduler
```bash
python scheduled_test_runner.py
```

### Run Tests Manually
```bash
python run_all_tests.py
```

### Check Task Status (Windows)
```powershell
Get-ScheduledTask -TaskName "ShenLongIP_DailyTests"
```

### Delete Task (Windows)
```powershell
Unregister-ScheduledTask -TaskName "ShenLongIP_DailyTests" -Confirm:$false
```

---

## 🎯 Recommended Setup

For production use, we recommend:

1. **Use Windows Task Scheduler** (Option 1)
2. **Run as Administrator** for the first setup
3. **Test manually** before relying on automation
4. **Monitor logs** for the first few days
5. **Set up email notifications** if needed (can be added to the scripts)

This ensures your tests run reliably every day at 9:00 AM, even when you're not at your computer! 