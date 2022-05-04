# IAESTE Szakal

## SETUP

### Download Docker Desktop for Windows

[Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Download MySQL Workbench

[MySQL Workbench](https://dev.mysql.com/downloads/file/?id=509428)

## PyCharm CONFIG

### Clone repo

Let PyCharm create venv using requirements.txt

If it doesn't suggest it, do it manually, google how to. Later you can point Python Interpreter in run configuration to created venv.

### Enable Docker access via PyCharm

If PyCharm PRO -> it should be somewhere listed as services

If PyCharm Community -> it can be downloaded in plugins tab

NOTE: There should be a simple way to connet to previously downloaded docker desktop. Keep in mind that the docker desktop needs to be turned on the whole time.

#### After setup it should be access this way

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_services.PNG)

### Pull latest mysql/mysql-server image

Can be done from services tab, in images.

### Create and run docker container

Right click on previously downloaded image and configure it like that:

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_docker_sql.PNG)

### Create szakal database and solve connections issues

#### Connect to running container by right clicking the container and selecting "Create terminal"

#### In terminal run following commands:

`mysql -u root -p` (password is root)

(In opened SQL terminal)

`CREATE USER 'root'@'%' IDENTIFIED BY 'root';`

`GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;`

`FLUSH PRIVILEGES;`

`create database szakal;`

Now MySQL should be accessible from outside of the container.

### Configure PyCharm run configs

#### Server configuration

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_django_server.PNG)

This step can also be configured as the next ones, if there is no django server available. Just pick Python and set ```runserver``` parameter.

Environmental variables (SECRET_KEY can be whatever, it doesnt matter in test env, just keep it long and random)

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_django_envs.PNG)

#### Makemigrations configuration

You can Ctrl+C, Ctrl+V env variables from the previous config.

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_makemigrations.PNG)

#### Migrate configuration

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/pycharm_migrate.PNG)

#### Superuser configuration

Same as with makemigrations and migrate, create new configuration, but in this case use ```createsuperuser --username=admin --email=admin@admin.com --noinput``` parameters. You also need to add additional env variable: ```DJANGO_SUPERUSER_PASSWORD=admin```. This way, after creating superuser you will be able to log into this account with set credentials.

## RUN

### Run Makemigrations configuration

### Run Migrate configuration

### Run Createsuperuser configuration

### Run Server configuration

Server should be working fine right now.

#### Additional steps

Create superuser, can be done analogically to makemigrations and migrate
or you can do it via terminal...

You will need to use project venv:

![](https://github.com/IAESTE-AGH/szakal/blob/main/windows_setup/venv_activate.PNG)

Also remember to set environmental variables for your powershell terminal. Google how to do it, there should be some way. (or stick to the first method)
