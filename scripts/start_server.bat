@REM Make sure that Apache is installed and httpd.config is set correctly
httpd -k start

@echo OFF

@REM Get Local IPv4 IP - https://superuser.com/a/230326/1640718
for /f "tokens=14" %%a in ('ipconfig ^| findstr IPv4') do set _IPaddr=%%a

echo.
echo Access PLV-BRS in other devices using this address: http://%_IPaddr%
echo.

pause