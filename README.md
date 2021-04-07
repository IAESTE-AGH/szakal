# IAESTE Szakal Backend

## Running
cd into backend dir, then

```docker-compose up --build```

if you need to build the cointainers; ditch the build option when you have nothing new to build

## Accessing app
Web app can be accessed at localhost:8000

## Accessing pgadmin
Pgadmin can be accessed at localhost:5051.
Login credentials are (email) pgadmin4@pgadmin.org (password) root
To connect to DB, create server connection and in the connection tab put:
hostname: db
port: 5432
maintenance database: postgres
username: postgres