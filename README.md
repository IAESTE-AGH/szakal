# WORK IN PROGRESS
# IAESTE Szakal

## Local Project Setup
1. You can either [download the sample](https://github.com/IAESTE-AGH/szakal/archive/refs/heads/main.zip) as a ZIP file and extract it or clone the repository to your local machine:
    >git clone https://github.com/IAESTE-AGH/szakal.git
2. Confirm your Python is at least version 3.8.  
    >python -V
3. Create a Python virtual environment and install dependencies  
    >python -m venv venv 
   > 
    >venv\scripts\activate
   > 
    >pip install -r requirements.txt
4. [Download and install](https://cloud.google.com/sql/docs/mysql/sql-proxy) the Cloud SQL Auth proxy to your local machine
5. [Download](https://iaestepolska.sharepoint.com/:u:/s/GrupaITIAESTE/EbwM7zr3WZ9Biq9FxLuEldwB3cafW-AltdKbV38MaxGRhA?e=ED1995) Google Service Account file from MSTeams. DO NOT ADD THIS FILE TO REPOSITORY!!!!!!
6. Add Downloaded file to folder with repository
7. In a separate terminal, start the Cloud SQL Auth proxy
    >cloud_sql_proxy.exe -instances=szakal-365017:europe-central2:szakal=tcp:5432 -credential_file={Path to Google Service Account file}
8. Set an environment variable to indicate you are using Cloud SQL Auth proxy `USE_CLOUD_SQL_AUTH_PROXY=true` (this value is recognised in the code)
9. Run the Django migrations to set up your models and assets
    >python manage.py makemigrations
   > 
    >python manage.py makemigrations szakal
   > 
    >python manage.py migrate
10. Start the Django web server:
    >python manage.py runserver
11. In your browser, go to http://localhost:8000

TODO:
- permission to edit user(me) data + everywhere - Szymon
- phone -> default instead of None - Michał
- center text in home box data - Jakub
- line from left to right - Jakub
- objects delete id or fix sorting by id(display) - fix sorting - reduce number of possibilities to filter - Szymon
- delete https://szakal-tbvozkjslq-lm.a.run.app/user/list/ - Michał
- link fill div(hamburger) - Jakub
- language code to PL and all text to PL - Daniel
- add category - check how often - v2
- update person name ???????????? - hide from display - Michał
- deleted + delete date - not able to check during adding - Michał
- not set "Number of ratings" - Jakuba
- fix css - 
- delete own username in right upper corner - Daniel
- add code to add contact person + button in company details page - Michał
- add boundaries to rating(consult with JFR) - v2
- css - https://szakal-tbvozkjslq-lm.a.run.app/company/1/company_details/ - Daniel
- fix contact and company update - Szymon