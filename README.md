# Funky Friday Improvement Collation

### Overview

A webapp that allows users to collate Funky Friday Improvement ideas and assign them to a system.
Supports CRUD operations

### User Guide

#### Sign up

Sign-ups require a name, email and password. All pages that provide data are login protected, so sign-up is essential.

#### Login

Visit '/login', input details and press submit

#### Logout

The header contains a logout button, you will be redirected to the homepage

### Run locally

1. `git clone git@github.com:nmozzer/funky_friday_web_app.git`
2. Run `python3 -m venv setup` in the root of the project - this will create a Python virtual environment.
3. Enter the python virtual environment `source env/bin/activate`
4. Run `pip install -r requirements.txt` to install the dependencies from the requirements file.
5. Copy the env variables in the .envtemplate file and replace with the appropriate values. Locally you can use an SQLite database for the database URI.
6. Run the application locally `python wsgi.py` - served by default at http://127.0.0.1:5000/

### Tests

To run tests use command:

-   `python3 -m pytest -v` - runs the unit tests (running with `-v` gives a more verbose output).
