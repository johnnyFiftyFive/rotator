# coding=utf-8
from functools import wraps

from database import User, db_session
from flask import request, Response
from rotator import db_log


def check_auth(username, password):
    user = db_session.query(User).filter(User.name == username).first()
    is_correct = user and password == user.password
    if is_correct:
        db_log.info('Zalogowano uzytkownika: {0}'.format(username))
    else:
        db_log.warning('Niepoprawna proba logowania', dict(login=username))
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
        if not auth or not check_auth(auth.username, auth.password):
            db_log.info('Proba logowania', dict(address=request.remote_addr))
            return authenticate()
        return f(*args, **kwargs)

    return decorated
