#!/usr/bin/env python

from app import app

app.run(host = '0.0.0.0', port = 8089, debug = True, threaded = False, processes = 1)
