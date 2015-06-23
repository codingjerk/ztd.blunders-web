#!/usr/bin/env python3

#pylint: disable=superfluous-parens

from flask import Flask

app = Flask(__name__)

try:
    with open('secret.key', 'rb') as keyFile:
        app.secret_key = keyFile.read()
except Exception as e:
    print(e)

    print(
        "\nIn order to use sessions you have to set a secret key.\n" +
        "\nYou must generate it and put as file secret.key in root directory\n" +
        "misc/generateSecretKey.py can generate good key for you"
    )
    exit(1)

from app import views
from app import api
