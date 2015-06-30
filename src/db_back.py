# coding=utf-8
import datetime

import os
import mysql.connector
from rotator import app, db_log
from rotator.keys import BACK_DB_USER, BACK_DB_PASS, BACK_DB_HOST, BACK_DB_NAME
from rotatordb import Backup, db_session


def get_connection():
    try:
        return mysql.connector.connect(user=app.config[BACK_DB_USER], password=app.config[BACK_DB_PASS],
                                       host=app.config[BACK_DB_HOST])
    except mysql.connector.Error as err:
        db_log.error('Blad polaczenia z baza.', dict(error=err))


def fetch_dblist():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SHOW DATABASES')
    for name in cursor:
        print(name[0])
    connection.close()


def gen_filename(dbname):
    time = datetime.datetime.now().strftime('%H:%M:%S_%d.%m.%Y')
    name = 'back_{}_{}.sql'.format(dbname, time)
    return name, time


def create_backup():
    (filename, ctime) = gen_filename(app.config[BACK_DB_NAME])
    command = 'mysqldump -u {} -p{} -h {} {} > back.sql' \
        .format(app.config[BACK_DB_USER], app.config[BACK_DB_PASS], app.config[BACK_DB_HOST], app.config[BACK_DB_NAME])

    result = os.system('command')
    if result == 0:
        db_log.info('Wykonano zrzut bazy', dict(command=command, filename=filename))
        back_info = Backup(filename, ctime, result)
        db_session.add(back_info)
        db_session.commit()
    else:
        db_log.error('Błąd przy wykonywaniu zrzutu.', dict(command=command, errCode=result))
    return result
