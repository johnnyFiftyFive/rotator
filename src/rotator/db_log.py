import json

from database import Log, db_session


def info(message, extras=None):
    body = dict(message=message)
    if extras:
        body.update(extras)
    log = Log('INFO', json.dumps(body))
    db_session.add(log)
    db_session.commit()


def warning(message, extras=None):
    body = dict(message=message)
    if extras:
        body.update(extras)
    log = Log('WARNING', json.dumps(body))
    db_session.add(log)
    db_session.commit()
