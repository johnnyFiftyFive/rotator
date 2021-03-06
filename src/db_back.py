# coding=utf-8
import datetime
import subprocess

import os
import mysql.connector
import db_log
from app_config import config
from rotatordb import Backup, db_session


def get_connection():
    ping_response = subprocess.Popen(["ping", config.BACK_DBHOST, "-c", '1'],
                                     stdout=subprocess.PIPE).stdout.read()
    if 'unreachable' in ping_response:
        return None
    try:
        connection = mysql.connector.connect(user=config.BACK_DBUSER,
                                             password=config.BACK_DBPASS,
                                             host=config.BACK_DBHOST)
        return connection
    except mysql.connector.Error as err:
        db_log.error('Blad polaczenia z baza.', dict(error=err.errno))


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
    db_log.info('Tworzenie kopii rozpoczete')
    (filename, ctime) = gen_filename(config.BACK_DBNAME)
    command = 'mysqldump -u {} -p{} -h {} {} > backups/{}' \
        .format(config.BACK_DBUSER, config.BACK_DBPASS,
                config.BACK_DBHOST, config.BACK_DBNAME, filename)
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


def delete(back_id):
    back = db_session.query(Backup).filter(Backup.id == back_id).first()
    back.status = 255
    resp = dict(status='ok')
    try:
        os.remove('backups/{}'.format(back.filename))
        db_log.info('Usunieto plik kopii', dict(file=back.filename))
    except Exception as err:
        resp['status'] = 'error'
        resp['filename'] = back.filename
        db_log.error('Nie mozna usunac pliku', dict(file=back.filename, error=err.message))
    if resp['status'] == 'ok':
        db_session.merge(back)
        db_session.commit()
    return resp


def remove_oldest(directory, count):
    """
    Deletes the oldest files from given directory

    :param directory: directory to prune
    :param count: number of files, which will survive
    """
    files = os.listdir(directory)
    if len(files) < count:
        return
    files.sort(key=lambda f: os.path.getmtime(f))
    for f in files[:count]:
        os.remove(f)
