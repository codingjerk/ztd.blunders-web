#!/bin/bash

cd /home/blunders/ztd.blunders-web && git pull
 
exec /usr/bin/supervisord -c /etc/supervisord.conf
