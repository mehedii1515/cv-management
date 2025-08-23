@echo off
REM Stop all production servers

echo Stopping production servers...

REM Stop Next.js frontend process
taskkill /F /FI "WINDOWTITLE eq Next.js-Frontend*" >nul 2>&1
if %errorLevel% == 0 echo [INFO] Next.js frontend stopped

REM Stop Django/Waitress process
taskkill /F /FI "WINDOWTITLE eq Django-Waitress*" >nul 2>&1
if %errorLevel% == 0 echo [INFO] Django server stopped

REM Stop Caddy process  
taskkill /F /FI "WINDOWTITLE eq Caddy*" >nul 2>&1
if %errorLevel% == 0 echo [INFO] Caddy server stopped

REM Also try to kill by process name as fallback
taskkill /F /IM python.exe /FI "CMDLINE eq *production_server.py*" >nul 2>&1
taskkill /F /IM node.exe /FI "CMDLINE eq *npm*start*" >nul 2>&1
taskkill /F /IM node.exe /FI "CMDLINE eq *next*start*" >nul 2>&1
taskkill /F /IM caddy.exe >nul 2>&1

echo.
echo [INFO] All production servers stopped
echo [INFO] You can now restart with start_production.bat

pause
