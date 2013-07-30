#!/usr/bin/env bash

BASEDIR="explodio/"

if [ -z $1 ]; then
   echo "App name requirement required."
   exit;
elif [ ! -d "${BASEDIR}$1" ]; then
   echo "App not found."
   exit;
fi

echo "Make and perform new migrations"

./manage.py schemamigration $1 --auto
./manage.py migrate $1

echo "Delete south migrations for $1"

./manage.py dbshell <<< "DELETE FROM south_migrationhistory WHERE app_name = '$1' AND migration <> '0001_initial';"

echo "Clean old migrations"

rm -rf ${BASEDIR}$1/migrations
./manage.py schemamigration $1 --initial

