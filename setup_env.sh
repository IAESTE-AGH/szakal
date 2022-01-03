#!/bin/sh

echo DEBUG=0 > .env

echo SECRET_KEY=$SECRET_KEY >> .env
echo DB_NAME=$DB_NAME >> .env
echo DB_USER=$DB_USER >> .env
echo DB_PASSWORD=$DB_PASSWORD >> .env
echo DB_HOST=$DB_HOST >> .env
echo DB_PORT=$DB_PORT >> .env