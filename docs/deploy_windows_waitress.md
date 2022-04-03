# Using waitress + whitenoise + nssm

**IMPORTANT! When deploying, remove the `BRIS_DEBUG` environment variable!**

**IMPORTANT! When deploying, remove the `BRIS_DEBUG` environment variable!**

This method uses three components:
1. `waitress` - A pure python WSGI web server that works on Windows (alternative to gunicorn). [Docs here](https://docs.pylonsproject.org/projects/waitress/en/latest/).
2. `whitenoise` - A package to serve static files on Python. [Docs here](http://whitenoise.evans.io/en/stable/).
3. `nssm` - A binary (exe) for Windows that enables us to install a `*.py` file as a Windows service (to automatically start the app on PC startup).

## Install using nssm
1. Clone this repository preferably in the root of `C:\` drive.
2. Open a `cmd (Admin)` inside the repository folder.
3. Use `nssm32.exe` or `nssm.64.exe` depending on the platform (32-bit or 64-bit).
  - Run this command:
  - `nssm.exe install BRISService "C:\Python310\python.exe" "C:\board_resolution_is\start_server.py"` (assuming you installed Python in `C:\` as well)

## Redirect logs to App's Path
We need to instruct nssm to redirect logs from standard output to a `.log` file.

Create the `*.log` files first.
```bat
cd . > logs/service.log
cd . > logs/service-error.log
```

Then set the service variables (assuming you installed the repository in `C:\`).
```bat
nssm.exe set BRISService AppStdout C:\board_resolution_is\logs\service.log
nssm.exe set BRISService AppStderr C:\board_resolution_is\logs\service-error.log
```

<!--
nssm64.exe set BRISService AppStdout C:\Users\Kyle\repos\board_resolution_is\logs\service.log
nssm64.exe set BRISService AppStderr C:\Users\Kyle\repos\board_resolution_is\logs\service-error.log
-->

## Start Service
`nssm.exe start ProjectService`

## Stop Service
`nssm.exe stop ProjectService`

## Stop Service
`nssm.exe stop ProjectService`

## Uninstall the Service
`nssm.exe remove ProjectService confirm`

Read more [here](https://stackoverflow.com/a/46450007).