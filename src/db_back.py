# coding=utf-8
import datetime

import os
import mysql.connector
from rotator import app, db_log
from rotator.keys import BACK_DB_USER, BACK_DB_PASS, BACK_DB_HOST, BACK_DB_NAME
from rotatordb import Backup, db_session


def get_connection():
    try:
        connection = mysql.connector.connect(user=app.config[BACK_DB_USER],
                                       password=app.config[BACK_DB_PASS],
                                       host=app.config[BACK_DB_HOST])
        return connection
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
    time = datetime.datetime.now()
    name = 'back_{}_{}.sql'.format(dbname, time.strftime('%H%M_%d.%m.%Y'))
    return name, time


def create_backup():
    connection = get_connection()
    if not connection or not connection.is_connected():
        db_log.error('Brak polaczenia z baza.', dict(connection_info=str(connection)))
        return 99

    (filename, ctime) = gen_filename(app.config[BACK_DB_NAME])
    command = 'mysqldump -u {} -p{} -h {} {} > backups/{}' \
        .format(app.config[BACK_DB_USER], app.config[BACK_DB_PASS],
                app.config[BACK_DB_HOST], app.config[BACK_DB_NAME], filename)
    start = datetime.datetime.now()
    result = os.system(command)
    end = datetime.datetime.now()
    diff = end - start
    size = os.path.getsize('backups/' + filename) / 1024.0 / 1024.0
    if result == 0:
        metrics = dict(command=command, filename=filename,
                       elapsedTime=diff.total_seconds(), filesize='{0:.3f}'.format(round(size, 3)))
        db_log.info('Wykonano zrzut bazy', metrics)
        back_info = Backup(filename, ctime, result)
        db_session.add(back_info)
        db_session.commit()
    else:
        db_log.error(u'Błąd przy wykonywaniu zrzutu.', dict(command=command, errCode=result))
    return result
