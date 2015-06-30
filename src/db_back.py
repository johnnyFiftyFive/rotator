# coding=utf-8
import mysql.connector
from rotator import app
from rotator.keys import BACK_DB_USER, BACK_DB_PASS, BACK_DB_HOST


def get_connection():
    try:
        return mysql.connector.connect(user='root', password='', host='localhost', database='')
    except mysql.connector.Error as err:
        print(u"Błąd połączenia z bazą: {}".format(err))


def fetch_dblist():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SHOW DATABASES')
    for name in cursor:
        print(name[0])
    connection.close()


def create_backup():
    command = 'mysql dump -u {} -p{} -h {} >> back.sql' \
        .format(app.config[BACK_DB_USER], app.config[BACK_DB_PASS], app.config[BACK_DB_HOST])
    print(command)
    # os.system('mysqldump -u root -pptaszek8 poligon >> back.sql')
