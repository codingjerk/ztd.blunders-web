#!/usr/bin/env python

import os

with open('secret.key', 'wb') as keyFile:
    secret = os.urandom(24)
    keyFile.write(secret)