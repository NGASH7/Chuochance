### Guide to Installation

## 1. Python Installation
The Platform is built using the *Django* Web Framework and thus the latest version of python (3.x) is required for the system to work.
After installing Python, clone this repository to your computer, then *create* and *activate* a *Python virtual environment* 

## 2. Virtual Environment activation & Requirements installation
Once the virtual environment is activated, navigate to the project directory on the Command Line Interface and install the required packages via the following command:

``` pip install -r requirements.txt ```

## 3. Loading the Database & Initial Data
*(Please Ensure you Virtual Environment is activated before proceeding)*
Once the requirements are loaded, First migrate the Changes to your database by running:

``` python manage.py migrate ```

That should populate the database tables for you. The next step is to load the preliminary Data (subcounties, wards, etc) required for the system to function via the following commands

Please execute these commands in the order in which they appear below.

```
python manage.py loaddata fixtures/levels.json
python manage.py loaddata fixtures/period.json
python manage.py loaddata fixtures/subcounties.json
python manage.py loaddata fixtures/wards.json

```

## 4. Create SuperUser
To create the Admin (Superuser) account, use the following command:

``` python manage.py createsuperuser ```

## 5. Runserver
The final step is to start the server on localhost via the command:

``` python manage.py runserver ```

The server should now be up and running, and on visiting the address http://127.0.0.1:8000 on your browser, you should see the landing page of the platform.