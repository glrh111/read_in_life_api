"""
refer to:
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html

DML refer to:
http://docs.sqlalchemy.org/en/latest/core/dml.html

query API:
http://docs.sqlalchemy.org/en/latest/orm/query.html

order by example:
https://stackoverflow.com/questions/15791760/multiple-order-by-sqlalchemy-flask/15792183
"""
import traceback
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
    def find(cls, spec=None, offset=None, limit=None, sort=None):
        """single table find
           spec: {}
           start: int: skip amount
           size: int: data max size
           sort: list: [('user_id':1), ('kitty_id':-1)] such as that: 1 AESC, 2 DESC
        TEST SUCCESS! VERY GOOD! by wang li in 2017-06-27
        """
        query = SQL_Session().query(cls)
        # 1. filter
        if spec:
            query = query.filter_by(**spec)
        # 2. sort
        if sort:
            sort_list = [] # [ User.user_id.asc(), User.user_id.desc() ]
            for field, sort_value in sort:
                temp_info = 'asc' if sort_value >=0 else 'desc'
                sort_list.append(
                    getattr(
                        getattr(cls, field), temp_info
                    )()
                )
            query = query.order_by(*sort_list)
        # 3. offset
        if offset >= 0:
            query = query.offset(offset)
        # 4. limit
        if limit >= 0:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def find_one(cls, spec=None):
        """"""
        spec = spec or {}
        # for attr, value in spec.items():
        #     query = query.filter(
        #         getattr(cls, attr) == value
        #     )
        result = SQL_Session().query(cls).filter_by(**spec).first()

        return result or None

    @classmethod
    def find_and_modify(cls, spec, update, multi=False):
        """find and modify
           spec : dict : find specific records to update
           update : set new value for them
           multi : if multi, update all that be found; or just update one;
        return : the first that has been updated
        """
        # TODO: test this func
        result = None
        session = SQL_Session()
        if not (update and spec):
            return result
        # update
        if multi:
            session.query(cls).filter_by(**spec).update(update)
        else:
            record = cls.find_one(spec)
            if record:
                for key, value in update.items():
                    setattr(record, key, value)
            else:
                return result
        # commit
        try:
            session.commit()
            result = cls.find_one(spec)
        except Exception:
            print 'in find and modify', traceback.format_exc()
            session.rollback()

        return result

    @classmethod
    def delete_spec(cls, spec=None, multi=False):
        """if multi==False, just delete one;
           or delete all that match spec
           refer to:
           https://stackoverflow.com/questions/27158573/how-to-delete-a-record-by-id-in-flask-sqlalchemy
        """
        spec = spec or {}
        if multi:
            SQL_Session().query(cls).filter_by(**spec).delete()
            SQL_Session().commit()
        else:
            record = cls.find_one(spec)
            if record:
                record.delete()

    def delete(self):
        """delete a record"""
        SQL_Session().delete(self)
        SQL_Session().commit()

    def save(self):
        """update ever changes or add new record"""
        session = SQL_Session()
        session.add(self)  # if its a new record, should add.
        session.commit()
        return self

    @classmethod
    def record_count(cls, spec=None):
        spec = spec or {}
        return SQL_Session().query(cls).filter_by(**spec).count()


BaseModel = declarative_base(cls=Base)