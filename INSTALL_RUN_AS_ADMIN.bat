@echo OFF

cd %~dp0

@REM Generate CSS
py manage.py tailwind install
py manage.py tailwind build
py manage.py collectstatic

@REM Register Scheduled Task
call scripts\create_task_cleandumps.bat

@REM Install Apache HTTP Server, Then Start
call httpd -k install
call httpd -k start

@REM Get Local IPv4 IP - https://superuser.com/a/230326/1640718
for /f "tokens=14" %%a in ('ipconfig ^| findstr IPv4') do set _IPaddr=%%a

echo.
echo Access PLV-BRS in other devices using this address: http://%_IPaddr%
echo.

pause