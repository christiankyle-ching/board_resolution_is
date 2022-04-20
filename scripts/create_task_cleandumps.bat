@REM Replace [PROJECT_PATH] with the location of the root folder of this project
SCHTASKS /CREATE /TN "BRIS_CleanDumps" /SC DAILY /ST 00:00 /TR [PROJECT_PATH]\clean_dumps.bat