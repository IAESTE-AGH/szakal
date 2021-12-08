# IAESTE Szakal

## SETUP

### Install docker

```apt install docker.io```

### Pull latest mysql image

`docker pull mysql/mysql-server:latest`

### To not use sudo all the time with docker command run this (or something similar xd)

`usermod -aG docker $USER`

### Create and run docker container

`docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=<password> mysql/mysql-server -d mysql`

### Create szakal database

#### Run initial console commands from Console -> On first run, from below.

### Setup virtual environment and install requirements

`python3 -m venv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

### Setup environmental variables

`vim env.sh`

export DB_NAME=szakal

export DB_USER=XXXX

export DB_PASSWORD=XXXX

export DB_HOST=127.0.0.1

export DB_PORT=3306

export SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXX

#### Esc ->  wq to escape vim

`. ./env.sh`

### Migrate stuff

`python3 manage.py makemigrations`

`python3 manage.py migrate`

## On beginning of work

`docker start mysql`

## On finish

`docker stop mysql`

## Accessing database

### Mysql Workbench

#### Install
`sudo snap install mysql-workbench-community`

`sudo snap connect mysql-workbench-community:password-manager-service :password-manager-service`

#### Running

`mysql-workbench-community`

### Console

#### If commands don't work by default

`sudo apt install mysql-shell`

#### On first run:

`mysql -u <name> -p -h 127.0.0.1`

`create database szakal;`

`\q`

#### On every other:

`mysql -u <name> -p -h 127.0.0.1 -n szakal`

### If there is problem with access, follow these steps

`docker exec -it mysql bash`

`mysql -u <name> -p -h 127.0.0.1`

`mysql> flush privilages;`

#### And now try again
