@REM Move to current directory, move 1 up to project root
cd %~dp0
cd ..

@REM Register Scheduled Task
@REM Running Daily, Remove folders older than 30 days
SCHTASKS /CREATE /TN "BRIS_CleanDumps" /SC DAILY /ST 00:00 /TR "%CD%\clean_dumps.bat"

cd %~dp0