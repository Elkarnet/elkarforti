#!/bin/sh

echo "***********************************"
echo "********** ELKARFORTI *************"
echo " DB_PATH: $DB_PATH"
echo "***********************************"

if [ ! -d "dirname $DB_PATH" ]
then
  mkdir "$(dirname $DB_PATH)"
fi

cd /data/web
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
