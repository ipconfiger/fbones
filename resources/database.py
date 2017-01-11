# coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer
from configs import settings

engine = create_engine(settings.DB_URI, convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))


class DeclaredBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=DeclaredBase)
Base.query = db.query_property()
