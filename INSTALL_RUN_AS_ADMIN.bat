cd %~dp0

@REM Generate CSS
py manage.py tailwind build
py manage.py collectstatic

@REM Register Scheduled Task
scripts\create_task_cleandumps.bat

@REM Install Apache HTTP Server, Then Start
httpd -k install
httpd -k start

pause