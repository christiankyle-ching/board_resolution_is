FORFILES /P "%~dp0temp_dumps" /D -7 /C "cmd /c IF @isdir == TRUE rd /S /Q @path"
FORFILES /P "%~dp0temp_imports" /D -7 /C "cmd /c IF @isdir == TRUE rd /S /Q @path"