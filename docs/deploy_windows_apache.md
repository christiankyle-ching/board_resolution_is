# Deployment on Windows using Apache24 and mod_wsgi

## Installing and Compiling mod_wsgi

### Setup Apache
https://www.apachelounge.com/download/

1. Download.
2. Extract Apache24 folder to C:\
3. Add `C:\Apache24\bin` to PATH (environment variable).

### Setup of MSVC C++ Build Tools
1. Go to [Visual Studio Downloads](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022). Under **Tools for Visual Studio**, download **Build Tools for Visual Studio**.
2. Run the installer, then click **Install**.
3. After installation, click **More > Import Config**
![import_config](/docs/images/import_config.png)
4. Select the [mod-wsgi_compilers.vsconfig](mod-wsgi_compilers.vsconfig) file in this project.
5. Wait for installation and done.

### Installing mod_wsgi
Run `pipenv install` again while in venv (`pipenv shell`).

## Collect all Static Files:
In the **venv** (`pipenv shell` to activate), run:
```bat
py manage.py tailwind build
py manage.py collectstatic
```

## Update wsgi_windows.py
Open the [board_resolution_is/wsgi_windows.py](board_resolution_is/wsgi_windows.py) and edit the following lines:
```py
# TODO: Add the repo's directory to the PYTHONPATH
# These 2 lines are needed on a Windows server
# Root folder and django project folder
sys.path.append('C:/...')
sys.path.append('C:/.../board_resolution_is')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_resolution_is.settings')
```

## Update requirements.txt and Installing Packages Globally
1. Activate venv: `pipenv shell`
2. Generate requirements.txt: `pipenv run pip freeze > requirements.txt`
3. **Exit venv! (type `exit` in cmd)**. Use regular cmd on project folder. Install packages globally on server: `pip install -r requirements.txt`

## Update httpd.conf

1. Copy the template, and paste on the end of httpd.conf (Default Location: `C:\Apache24\conf\httpd.conf`).
2. In the httpd.conf (`C:\Apache24\conf\httpd.conf`) file (NOT THE TEMPLATE), change the following values:
   1. Run `mod_wsgi-express module-config` **(not on venv)**. Copy the three lines and replace in .
   <!-- 2. Replace SetEnv values for the actual server (see these [environment variables](README.md#postgresql-database)). -->
   3. Replace paths with "..." to point to the project folder (static, media, and wsgi). **NOTE**: Use forward slashes `/`.

## Install httpd service
`httpd -k install`

## Start the service (server)
`httpd -k start`

## Verify if it's working
- Use Task Manager to see if `Apache HTTP Server` is running.
- Visit `localhost:80` on a browser and the web app should be visible.

## Troubleshooting
If errors occur, you can check the logs at `C:\Apache24\logs`.
