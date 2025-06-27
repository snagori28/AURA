@echo off
for /f "tokens=5" %%p in ('netstat -aon ^| findstr :8000') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| findstr :3000') do taskkill /PID %%p /F >nul 2>&1
echo Processes on ports 8000 and 3000 stopped.
