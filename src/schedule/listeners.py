import db_log


def execution_listener(event):
    db_log.info('Wykonano zaplanowane zadanie')


def error_listener(event):
    db_log.error('Blad przy wykonywaniu zaplanowego zadania', dict(job_id=event.job_id, exception=event.exception))
