# coding=utf8

from sqlalchemy import create_engine, inspect
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

    def as_dict(self):
        """
        格式化成字典
        :return:
        :rtype:
        """
        result_dict = {}
        mapper = inspect(self.__class__)
        for column in mapper.attrs:
            name = column.key
            value = getattr(self, name)
            result_dict[name] = value if value is not None else ''
        return result_dict

    def as_json_dict(self):
        """
        返回可以通过jsonify格式化的字典(处理了datetime和Decimal类型)
        :return:
        :rtype:
        """
        import datetime
        from decimal import Decimal
        result_dict = self.as_dict()
        for property_name in result_dict:
            if isinstance(result_dict [property_name], datetime.datetime):
                result_dict[property_name] = result_dict[property_name].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(result_dict[property_name], datetime.date):
                result_dict[property_name] = result_dict[property_name].strftime('%Y-%m-%d')
            elif isinstance(result_dict[property_name], Decimal):
                result_dict[property_name] = float(result_dict[property_name])
        return result_dict



Base = declarative_base(cls=DeclaredBase)
Base.query = db.query_property()
