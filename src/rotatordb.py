from datetime import datetime

import app_config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(app_config.DATABASE_URI, convert_unicode=True, **app_config.DATABASE_CONNECT_OPTIONS)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class User(Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String)
    email = Column(String)
    status = Column(Integer)

    def __init__(self, fullname=None, name=None, password=None):
        self.name = name
        self.fullname = fullname
        self.password = password


class Log(Model):
    __tablename__ = 'Log'

    def __init__(self, level, message):
        self.level = level
        self.message = message

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    level = Column(String, nullable=False)
    logtime = Column(DateTime, nullable=False, default=datetime.now())


class Backup(Model):
    __tablename__ = 'Backup'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    last_restored = Column(DateTime)
    status = Column(Integer)

    def __init__(self, filename, created, status):
        self.filename = filename
        self.created = created
        self.status = status


class Config(Model):
    __tablename__ = 'Config'

    name = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, name, value):
        self.name = name
        self.value = value
