import app_config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

class RotatorDB:
    engine = None
    db_session = None

    def get_engine(self):
        if not self.engine:
            return create_engine(app_config.DATABASE_URI, convert_unicode=True, **app_config.DATABASE_CONNECT_OPTIONS)
        return self.engine

    def get_session(self):
        if not self.db_session:
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.get_engine()))
        return self.db_session

    def __init__(self):
        self.engine = self.get_engine()
        self.db_session = self.get_session()
        # Model.metadata.create_all(bind=self.engine)


Model = declarative_base(name='Model')
rotatordb = RotatorDB()
Model.query = rotatordb.get_session().query_property()


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

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Log(Model):
    __tablename__ = 'Log'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    level = Column(String, nullable=False)
    logtime = Column(DateTime, nullable=False)


class Backup(Model):
    __tablename__ = 'Backup'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    logtime = Column(DateTime)
    status = Column(Integer)
