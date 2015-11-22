import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rotator.db')
    DATABASE_CONNECT_OPTIONS = {}
    BACK_DBNAME = 'dbname'
    BACK_DBHOST = '0.0.0.0'
    BACK_DBPORT = 3306
    BACK_DBPASS = 'pass'
    BACK_DBUSER = 'root'
    SCHED_MINUTES = 52
    SCHED_HOUR = 17
    SCHED_JOBID = 'scheduler_backup'


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rotator.db')
    DATABASE_CONNECT_OPTIONS = {}
    BACK_DBNAME = 'firmatec'
    BACK_DBHOST = '0.0.0.0'


del os

config = ProductionConfig()
