# coding=utf-8
from functools import wraps

from rotatordb import User, db_session
from flask import request, Response
from rotator import db_log


def check_auth(auth, addr):
    user = db_session.query(User).filter(User.name == auth.username).first()
    is_correct = user and auth.password == user.password
    if is_correct and auth.username != 'log':
        db_log.info('Zalogowano uzytkownika.', dict(login=auth.username, address=addr))
    else:
        db_log.warning('Niepoprawna proba logowania', dict(login=auth.username, address=addr))
    return is_correct


def authenticate():
    return Response(
        u'Nie można zweryfikować uprawnień.\n'
        u'Podaj prawidłowe dane logowania', 401,
        {'WWW-Authenticate': u'Basic realm="Podaj haszlo!"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth, request.remote_addr):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
