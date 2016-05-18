#!/bin/bash

cd /home/blunders/ztd.blunders-web && git pull
 
/usr/bin/supervisord -c /etc/supervisord.conf
