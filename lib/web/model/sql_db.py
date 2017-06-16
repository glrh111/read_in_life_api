"""
refer to:
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html
"""

from functools import wraps
import sqlalchemy
from sqlalchemy import create_engine, orm, event, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from lib.serve.config import app_config

# create session
engine = create_engine(app_config.SQL_SERVER_URL)

SQLSession = sessionmaker(bind=engine)

sql_session = SQLSession()


# create base for use
class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def find_one(cls, spec=None):
        spec = spec or {}
        query = sql_session.query(cls)
        for attr, value in spec.items():
            query = query.filter(
                getattr(cls, attr) == value
            )
        result = query.first()
        return result or None


BaseModel = declarative_base(cls=Base)