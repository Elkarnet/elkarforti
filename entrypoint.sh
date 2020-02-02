#!/bin/sh

echo "***********************************"
echo "********** ELKARFORTI *************"

echo " Start cron to auto open-close rooms"
echo "************************************"

if test $AUTO_OPEN_CLOSE -eq 1 
then
        # Replace values with env variables

        sed -i  's/CloseMin/'$AUTO_CLOSE_MIN'/g' /crontab.txt
        sed -i  's/CloseHour/'$AUTO_CLOSE_HOUR'/g' /crontab.txt
        sed -i  's/OpenMin/'$AUTO_OPEN_MIN'/g' /crontab.txt
        sed -i  's/OpenHour/'$AUTO_OPEN_HOUR'/g' /crontab.txt

        cat /crontab.txt >> /etc/crontabs/root

        # start cron
        /usr/sbin/crond -b -l 8

fi


echo " DB_PATH: $DB_PATH"
echo "***********************************"

if [ ! -d "dirname $DB_PATH" ]
then
  mkdir "$(dirname $DB_PATH)"
fi

cd /data/web
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
