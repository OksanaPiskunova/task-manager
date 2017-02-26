**`Simple Task Manager`**



_**`Installation`**_

`cd task-manager (project root)`

_`1. Python`_

`sudo apt-get install python3=3.5.2`

_`2. Pip`_

`sudo apt-get install python3-pip`

_`3. Postgresql`_

`sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`

`sudo -u postgres psql`

`CREATE DATABASE task_manager;`

`CREATE USER task_manager_admin WITH PASSWORD 'admin';`

`ALTER ROLE task_manager_admin SET client_encoding TO 'utf8';`

`ALTER ROLE task_manager_admin SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE task_manager_admin SET timezone TO 'Europe/Minsk';`

`GRANT ALL PRIVILEGES ON DATABASE task_manager TO task_manager_admin;`

`\q`

_`4. Virtual environment`_

`python3 -m venv env`

`source env/bin/activate`

_`5. Database module`_

`pip install django psycopg2`

_`6. Django + DRF`_

`pip install django`

`pip install djangorestframework`


`python manage.py migrate`

`python manage.py createsuperuser`

_`7. Redis`_

`pip install redis`

`pip install redis-server`

_`8. Celery`_

`pip install celery`



_**`Starting`**_

_`1. Start server`_

`Terminal 1:`

`python manage.py runserver`

_`2. Start celery`_

`Terminal 2:`

`celery -A task_manager worker -l info`

`Terminal 3:`

`celery -A task_manager beat -l info`

**_`THE END :)`_**
    