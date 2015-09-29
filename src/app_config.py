import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rotator-dev.db')
    DATABASE_CONNECT_OPTIONS = {}
    SECRET_KEY = '_JurekOwsiak#1994'
    BACK_DBNAME = 'poligon'
    BACK_DBHOST = '192.168.1.2'
    BACK_DBPORT = 3306
    BACK_DBPASS = 'ptaszek8'
    BACK_DBUSER = 'root'
    SCHED_MINUTES = 0
    SCHED_HOUR = 12
    SCHED_JOBID = 'scheduler_backup'


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rotator.db')
    DATABASE_CONNECT_OPTIONS = {}


del os

config = Config()
