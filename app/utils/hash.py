import bcrypt

from app.db import postgre

def get(username, password):
    salt = postgre.getSalt(username)
    passHash = bcrypt.hashpw(password.encode(), salt.encode())

    return passHash.decode()

def new(username, password):
    salt = bcrypt.gensalt(rounds = 12)
    passHash = bcrypt.hashpw(password.encode(), salt)

    return salt.decode(), passHash.decode()