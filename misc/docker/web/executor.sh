#!/bin/bash

echo "${GMAIL_API_TOKEN}" | base64 --ignore-garbage --decode > /home/blunders/ztd.blunders-web/gmail_api_token.key

cd /home/blunders/ztd.blunders-web && git pull
 
exec /usr/bin/supervisord -c /etc/supervisord.conf
