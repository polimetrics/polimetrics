# Polimetrics

## Description

## Setup
### Dependencies
- postgresql
- python 3
- pipenv - run `pip install pipenv`


### How to run
- Navigate to project directory
- run `pipenv shell`
- run `pipenv install`
- configure bashprofile environment variables
- setup postgres database
  - download postgres
  - windows (https://stackoverflow.com/questions/30401460/postgres-psql-not-recognized-as-an-internal-or-external-command/38296357)
    - add psql to path
    - login to psql as default postgres user (pw set at install)
        - `psql -U postgres`
    - you might need to run `createuser -d -U postgres` to set postgres user to create databases
    - `createdb -U postgres polimetrics` -U specifies the user to connect with
    - `createuser -d -U postgres admin` to create admin user (this step and the one before could be switched and createdb user could then be admin)
    - windows users: may have to update data/pg_hba.conf and set all users to Method = trust (https://dba.stackexchange.com/questions/83164/remove-password-requirement-for-user-postgres)
    - run migrations `./manage.py migrate` 
    - run server `./manage.py runserver`
  
