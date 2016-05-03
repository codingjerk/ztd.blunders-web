#!/bin/bash

cd /home/blunders/ztd.blunders-web && git pull
/usr/bin/rm -f /run/nginx.pid && /usr/sbin/nginx -t && /usr/sbin/nginx &

/usr/bin/mongod -f /etc/mongod.conf &

uwsgi --uid blunders --gid=blunders /home/blunders/uwsgi.ini
