#!/bin/sh

/etc/init.d/nginx start
cd /var/www/html/kabu_beta
chmod -R 777 .
python3 manage.py collectstatic
uwsgi --ini uwsgi.ini
