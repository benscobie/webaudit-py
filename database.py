from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session

engine = None
db_session = scoped_session(lambda: create_session(bind=engine))

Base = declarative.declarative_base()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine
