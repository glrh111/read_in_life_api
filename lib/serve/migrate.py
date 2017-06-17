"""
refer to:
http://alembic.zzzcomputing.com/en/latest/api/commands.html
http://alembic.zzzcomputing.com/en/latest/api/autogenerate.html

every time: delete all migrate record! or you will have many troubles
"""
import os
import sys
import shutil

from alembic.config import Config
from alembic import command

from lib.serve.config import app_config
from lib.helpers import get_root_path
from lib.web.model.sql_db import BaseModel, engine

print '[Migrate] starting...'

# delete `alembic_version` records if have
conn = engine.connect()
try:
    engine.execute('drop table alembic_version')
except Exception:
    print 'alembic_version drop failed.'
else:
    print 'alembic_version drop successfully.'

# delete `migration` dir if exists.
root_path = get_root_path()
migration_dirname = os.path.join(root_path, 'migration')
try:
    shutil.rmtree(migration_dirname)
except Exception:
    print 'migration dir drop failed.'
else:
    print 'migration dir drop successfully.'

# config
alembic_config = Config(
    os.path.join(root_path, 'alembic.ini')
)
alembic_config.set_section_option(
    'alembic', 'sqlalchemy.url', app_config.SQL_SERVER_URL
)



# init env
command.init(
    alembic_config,
    migration_dirname
)
# copy migration_env to replace migration/env.py Good.
migration_env_abspath = os.path.abspath(os.path.join(
    root_path, 'lib/serve/migration_env.py'
))
to_env_abspath = os.path.abspath(os.path.join(
    root_path, 'migration/env.py'
))
print migration_env_abspath, to_env_abspath
shutil.copyfile(migration_env_abspath, to_env_abspath)

#
command.revision(
    alembic_config,
    autogenerate=True
)
command.upgrade(
    alembic_config, "head"
)

print '[Migrate] finish!\n'
