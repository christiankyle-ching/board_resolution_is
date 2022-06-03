# Deployment on Windows using Apache24 and mod_wsgi

## Installing and Compiling mod_wsgi

### Setup Apache
https://www.apachelounge.com/download/

1. Download.
2. Extract Apache24 folder to C:\
3. Add `C:\Apache24\bin` to PATH (environment variable).

### Setup of MSVC C++ Build Tools
**This step requires at least 1GB of internet download. Use the [Offline Installer method](#offline-installer)**
1. Go to [Visual Studio Downloads](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022). Under **Tools for Visual Studio**, download **Build Tools for Visual Studio**.
2. Run the installer, then click **Install**.
3. After installation, click **More > Import Config**
![import_config](/docs/images/import_config.png)
4. Select the [mod-wsgi_compilers.vsconfig](/etc/mod-wsgi_compilers.vsconfig) file in this project.
5. Wait for installation and done.

#### Offline Installer

(Alternative) You can **create an offline installer** instead. Follow the [README](/vs_BuildTools/README.md) at [vs_BuildTools](/vs_BuildTools/).

### Installing mod_wsgi
Run `pipenv install` again while in venv (`pipenv shell`).

## Update httpd.conf

1. Copy the template, and paste on the end of httpd.conf (Default Location: `C:\Apache24\conf\httpd.conf`).
2. In the httpd.conf (`C:\Apache24\conf\httpd.conf`) file (NOT THE TEMPLATE), change the following values:
   1. Run `mod_wsgi-express module-config` **(not on venv)**. Copy the three lines and replace in the `httpd.conf`.
   2. Replace paths with "..." to point to the project folder (static, media, and wsgi). **NOTE**: Use forward slashes `/`.

## Set Static IP of the server
Change the IP settings of the server from DHCP (Automatic) to Static. For Windows: follow this guide (https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/change-ip-address-network-adapter#how-to-specify-an-ip-address).

## Install httpd service
`httpd -k install`

## Start the service (server)
`httpd -k start`

## Stop the service (server)
`httpd -k stop`

## Verify if it's working
- Use Task Manager to see if `Apache HTTP Server` is running.
- Visit `localhost:80` on a browser and the web app should be visible.

## Troubleshooting
If errors occur, you can check the logs at `C:\Apache24\logs`.

## User Accessibility
Create shortcuts for the batch files in [scripts](/scripts/) for starting and stopping the server.
