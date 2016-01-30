from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session, sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

#engine = None
engine = create_engine('mysql+pymysql://' + config['DATABASE']['Username'] + ':' + config['DATABASE']['Password'] + '@' + config['DATABASE']['Server'] + '/' + config['DATABASE']['Database'], pool_recycle=3600)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative.declarative_base()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine
