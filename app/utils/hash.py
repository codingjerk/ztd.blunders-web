import bcrypt

from app.db import postgre

def get(username, password):
    salt = postgre.getSalt(username)
    passHash = bcrypt.hashpw(password.encode(), salt.encode())

    return passHash