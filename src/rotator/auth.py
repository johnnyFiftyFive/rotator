# coding=utf-8
from functools import wraps
from database import RotatorDB

from flask import request, Response


def check_auth(username, password):

    return username == 'admin' and password == 'secret'


def authenticate():
    return Response(
        u'Nie można zweryfikować uprawnień.\n'
        u'Podaj prawidłowe dane logowania', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
