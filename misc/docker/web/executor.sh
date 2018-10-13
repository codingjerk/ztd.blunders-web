#!/bin/bash

GMAIL_API_TOKEN_PATH="/home/blunders/ztd.blunders-web/gmail_api_token.key"
echo "${GMAIL_API_TOKEN}" | base64 --ignore-garbage --decode > "${GMAIL_API_TOKEN_PATH}"
chown blunders:blunders "${GMAIL_API_TOKEN_PATH}"

cd /home/blunders/ztd.blunders-web && git pull
 
exec /usr/bin/supervisord -c /etc/supervisord.conf
