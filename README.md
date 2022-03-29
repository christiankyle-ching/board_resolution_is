# Board Resolution Information System (BRIS)

## How to setup a local development server?

### Python and Django
1. Download [Python 3.10](https://www.python.org/downloads/).
2. **(IMPORTANT)** Use these steps to install your Python!
   1. Check **Add to PATH**.
   2. Click **Custom Install**.
   3. Click **Next**.
   4. Check **Install for All Users**.
   5. **IMPORTANT!** Change install location to `C:\Python310` only! **Remove the Program Files**.
   6. Install and done.
3. Install pipenv.
   - `pip install pipenv`
4. Clone this and `cd` to that directory. Create a virtual environment using:
   - `pipenv shell`
5. Comment out `'mod_wsgi.server'` in `settings.py > INSTALLED_APPS`:
```py
INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   # 'mod_wsgi.server',

   ...
]
```
6. Install required packages in this project:
   - `pipenv install`
   - If **mod-wsgi** throws errors, ignore first (only for local development server).

### PostgreSQL Database
**Database Name: `db_board_resolution_is`**

1. Install [PostgreSQL](https://www.postgresql.org/download/).
   - **NOTE**: Remember your password!
   - 14.2 (Latest)
2. Create a database by:
   1. Run `psql`. On Windows, search for `psql`.
   2. Enter your password.
   3. Run `CREATE DATABASE db_board_resolution_is;`
      - Take note of the semicolon.
   4. Verify if database is created by entering `\l` in `psql`.

### Set Environment Variables
Setup [environment variables](https://www.computerhope.com/issues/ch000549.htm) in your PC / server:
- `PSQL_BRIS_DBNAME` = `db_board_resolution_is`
- `PSQL_USER` = `postgres` (default)
- `PSQL_PASSWORD` = Your password set when installing PostgreSQL.
- `PSQL_HOST` = `127.0.0.1` (localhost)
- `PSQL_PORT` = `5432` (default)
- `BRIS_SECRET` = Run this command in a `cmd` and get the value: `py -c "import secrets; print(secrets.token_hex(64))"`

For password reset using email, you need to add a **Gmail Account with 2FA enabled**. [Add an App Password](https://support.google.com/accounts/answer/185833?hl=en), and take note of the password. Then assign the following environment variables:
- `BRIS_EMAIL_USERNAME` - Your Gmail Account (email address).
- `BRIS_EMAIL_PASSWORD` - The generated App Password.

Note: If you changed your password on Google, all App Passwords are revoked and you'll need to generate one (and replace the environment variable).

### Generate Database Tables
1. Go to root folder of project.
2. (venv) Run `py manage.py migrate`.

### TailwindCSS (Front-end CSS Framework)

1. Install [node.js](https://nodejs.org/en/download/) first.
2. We need to tell django where the npm is installed if it cannot find it. On a cmd (Windows), run:

```bat
where npm
```

**Copy the full file path** with the `npm.cmd`: then replace the variable value in the [settings.py](board_resolution_is/settings.py) like so:

```py
# Replace with the file path you got from `where npm`
NPM_BIN_PATH = r"C:\...\nodejs\npm.cmd"
```

3. `py manage.py tailwind install`

Read more [here](https://django-tailwind.readthedocs.io/en/latest/installation.html#configuration-of-the-path-to-the-npm-executable).

#### Use VSCode Tailwind CSS IntelliSense extension for previews.
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss

### Setup Python Interpreter (For automatic activation of virtual environment)
Install the [Python Extension in VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

Then, we can setup the VSCode Terminal (`` CTRL + ` ``) to always activate our virtualenv, where our required packages are installed. Use `CTRL + SHIFT + P` and search for `Python: Select Interpreter`. Select the one created at the earlier step (`pipenv shell`).

After doing so, everytime we open a terminal in VSCode, we should see the name of virtualenv in the beginning of each line, like so:

`(board_resolution_is) C:\Users\...\board_resolution_is>`

### Run the local server

Run the following:
```bat
py manage.py runserver
py manage.py tailwind start
```

This will run a local server and setup TailwindCSS hot-reload. Open the web app using the link shown.

**NOTE**: If `os.environ` throws a KeyError, and you already made sure you set the environment variables, restart the cmd (or vscode) because this variables are not loaded on old console sessions.

## Important Contribution Notes

### Auto-formatting in VSCode

When you're using `Alt + Shift + F` to automatically beautify / format the code, make sure that you use **[Beautify](https://marketplace.visualstudio.com/items?itemName=HookyQR.beautify) instead of Prettier**. Prettier breaks the templating language by forcing multiple lines into a single one.

1. Open an HTML file.
2. Open the command palette `CTRL + SHIFT + P`
3. `Format Document With...`
4. `Configure Default Formatter...` 
5. Select `Beautify`

## How to Deploy?

### For Windows

Follow the [deployment guide using Apache HTTP Server and mod_wsgi](/docs/deploy_windows_apache.md).
