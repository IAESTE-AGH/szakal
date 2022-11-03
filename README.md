# WORK IN PROGRESS
# IAESTE Szakal

## Deployed version

Link to service: https://szakal-iaeste-7x36w6uefq-lm.a.run.app

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
    >pip install --upgrade pip
   > 
    >pip install -r requirements.txt
4. [Download](https://iaestepolska.sharepoint.com/:u:/s/GrupaITIAESTE/EbwM7zr3WZ9Biq9FxLuEldwB3cafW-AltdKbV38MaxGRhA?e=ED1995) Google Service Account file from MSTeams. Save it into repository folder but DO NOT ADD THIS FILE TO REPOSITORY!!!!!!
5. [Download and install](https://cloud.google.com/sql/docs/mysql/sql-proxy) the Cloud SQL Auth proxy to your local machine and rename it to `cloud_sql_proxy.exe`
6. In a separate terminal, go to localization where downloaded file `cloud_sql_proxy.exe` is saved and start the Cloud SQL Auth proxy, before make sure than port 5432 is free:
    >cloud_sql_proxy.exe -instances=szakal-iaeste:europe-central2:szakal-iaeste=tcp:5432 -credential_file={Absolute Path to Google Service Account file}
7. Set an environment variable to indicate you are using Cloud SQL Auth proxy `USE_CLOUD_SQL_AUTH_PROXY=true` (this value is recognised in the code)
    > (PowerShell) $env:USE_CLOUD_SQL_AUTH_PROXY="true"
    >
    > (Shell) set USE_CLOUD_SQL_AUTH_PROXY = "true"
    >
    > (Linux) export USE_CLOUD_SQL_AUTH_PROXY="true"
8. Run the Django migrations to set up your models and assets
    >python manage.py makemigrations
    > 
    >python manage.py makemigrations szakal
    > 
    >python manage.py migrate
9. Start the Django web server:
    >python manage.py runserver
10. In your browser, go to http://localhost:8000

TODO:
- [X] permission to edit user(me) data + everywhere - Szymon
- [X] phone -> default instead of None - Michał
- [X] center text in home box data - Jakub
- [X] line from left to right - Jakub
- [X] objects delete id or fix sorting by id(display) - fix sorting - reduce number of possibilities to filter - Szymon
- [x] delete https://szakal-tbvozkjslq-lm.a.run.app/user/list/ - Michał
- [ ] link fill div(hamburger) - Jakub
- [X] language code to PL and all text to PL - Daniel
- [X] add category - check how often - v2
- [X] update person name ???????????? - hide from display - Michał - to discuss
- [X] deleted + delete date - not able to check during adding - Michał
- [x] not set "Number of ratings" - Jakuba
- [ ] fix css - 
- [X] delete own username in right upper corner - Daniel
- [X] add code to add contact person + button in company details page - Michał
- [ ] add boundaries to rating(consult with JFR) - v2
- [ ] css - https://szakal-tbvozkjslq-lm.a.run.app/company/1/company_details/ - Daniel
- [X] fix contact and company update - Szymon
- [X] fix rating
- [ ] CRUD for industry company
- [ ] display all info for company
- [ ] MANY TO MANY in form, better solution
- [ ] Purpose of categories? What values?
- [ ] CRUD for contact person
- [ ] Simplify DB design
- [ ] Add common errors to README(Michał)
- [ ] Clean DB
- [ ] Fix return after update

TODO2:
- [ ] Next contact date (delete field from company and take it from contacts) - Justyna
- [ ] Style creating and actualization - Michał & Daniel
- [ ] Calculate rating base on contact rating (trigger) - Tomek
- [ ] Approving users - Szymon
- [ ] Password changing - Szymon
- [ ] "Delete" categories (company and contact)
- [ ] Ability to unassign person from company (admin)
- [ ] Actualization date for company (not working)
- [ ] Home "Statusy firm" not more than one status for company (and only from my companies)
