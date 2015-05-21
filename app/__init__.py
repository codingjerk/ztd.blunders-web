#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)
app.secret_key = 'Ifs1H=+[_O0:OI(>>?oAivO[bMVt`By?' # TODO: Read from file

from app import views
from app import api