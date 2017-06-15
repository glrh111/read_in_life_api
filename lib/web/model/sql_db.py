
from functools import wraps
import sqlalchemy
from sqlalchemy import create_engine, orm, event, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from lib.serve.config import app_config

# for session
print app_config.SQL_SERVER_URL
engine = create_engine(app_config.SQL_SERVER_URL)

SQLSession = sessionmaker(bind=engine)

sql_session = SQLSession()

# for Base
BaseModel = declarative_base()


if __name__ == '__main__':
    pass