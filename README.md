# WORK IN PROGRESS
# IAESTE Szakal

## Local Project Setup
1. You can either [download the sample](https://github.com/IAESTE-AGH/szakal/archive/refs/heads/main.zip) as a ZIP file and extract it or clone the repository to your local machine:
    >git clone https://github.com/IAESTE-AGH/szakal.git
2. [Install](https://cloud.google.com/sdk/docs/install) and [initialize](https://cloud.google.com/sdk/docs/initializing) the Google Cloud CLI
3. Confirm your Python is at least version 3.8.  
    >python -V
4. Create a Python virtual environment and install dependencies  
    >python -m venv env 
   > 
    >venv\scripts\activate 
   > 
    >pip install --upgrade pip
   > 
    >pip install -r requirements.txt
5. [Download and install](https://cloud.google.com/sql/docs/mysql/sql-proxy) the Cloud SQL Auth proxy to your local machine
6. [Download](https://iaestepolska.sharepoint.com/:u:/s/GrupaITIAESTE/EbwM7zr3WZ9Biq9FxLuEldwB3cafW-AltdKbV38MaxGRhA?e=ED1995) Google Service Account file from MSTeams. DO NOT ADD THIS FILE TO REPOSITORY!!!!!!
7. In a separate terminal, start the Cloud SQL Auth proxy
    >cloud_sql_proxy.exe -instances=szakal-365017:europe-central2:szakal=tcp:5432 -credential_file={Path to Google Service Account file}
8. Set an environment variable to indicate you are using Cloud SQL Auth proxy `USE_CLOUD_SQL_AUTH_PROXY=true` (this value is recognised in the code)
9. Run the Django migrations to set up your models and assets
    >python manage.py makemigrations
   > 
    >python manage.py makemigrations polls
   > 
    >python manage.py migrate
   > 
    >python manage.py collectstatic
10. Start the Django web server:
    >python manage.py runserver
11. In your browser, go to http://localhost:8000

## TODO
 - Adjust docker files