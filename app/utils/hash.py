import bcrypt

from app.db import postgre

def get(username, password):
    salt = postgre.user.getSalt(username)
    passHash = bcrypt.hashpw(password.encode(), salt.encode())

    return passHash.decode()

def new(password):
    salt = bcrypt.gensalt(rounds = 12)
    passHash = bcrypt.hashpw(password.encode(), salt)

    return salt.decode(), passHash.decode()
