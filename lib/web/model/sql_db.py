"""
refer to:
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html

DML refer to:
http://docs.sqlalchemy.org/en/latest/core/dml.html
"""

from functools import wraps
import sqlalchemy
from sqlalchemy import create_engine, orm, event, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from lib.serve.config import app_config

# create session
engine = create_engine(app_config.SQL_SERVER_URL)

session_factory = sessionmaker(bind=engine)

# sql_session = SQLSession()
# when to use it , just SQL_Session() to get the save session during
# a request's lifecycle
SQL_Session = scoped_session(session_factory)


# create base for use
class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def find_one(cls, spec=None):
        spec = spec or {}

        query = SQL_Session().query(cls)
        for attr, value in spec.items():
            query = query.filter(
                getattr(cls, attr) == value
            )
        result = query.first()
        return result or None

    @classmethod
    def find_and_modify(cls, spec=None, upsert=False, multi=False, new=True, update=None):
        """find and modify"""
        pass

    def delete(self):
        """delete a record"""

        pass

    def save(self):
        """update ever changes or add new record"""
        session = SQL_Session()
        session.add(self)  # if its a new record, should add.
        session.commit()
        return self


BaseModel = declarative_base(cls=Base)