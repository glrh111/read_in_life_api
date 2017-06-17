# Read In Life API服务

## API服务Config

1. 配置文件路径: spec.config. 
   文件里config字典为{`配置名称`:`配置cls`}

2. 怎样确定加载哪一个配置?
   从环境里边取得 `READ_IN_LIFE_API_ENV` 环境变量, 作为上述`配置名称`, 寻找配置文件.

3. 在代码里导入配置项目:

   from lib.serve.config import app_config
   
   app_config 这个对象代表当前使用的配置文件

## API服务启动步骤
1. 将代码根目录`read_in_life_api` 加入`sys.path`
2. collect 路由, 然后将.
3. 启动服务


## API服务部署

```
1.. 拉代码 到 ~/wordspace/里边
   git clone https://github.com/glrh111/read_in_life_api
2. 进入docker 目录
   cd spec/docker/
3. build
   docker build -t read-in-life-api:v1 .
4. cd ~/read-in-life , 将spec.runtime.env 复制到当前目录
4. run docker
   docker run -d --name read-in-life-api -p 8000:8000 --link postgres:postgres --link redis:redis --env-file runtime.env -v /home/glrh11/workspace/read_in_life_api:/home/runtime/read_in_life_api --restart always read-in-life-api:v1 serve
   read-in-life:v1
   
```

## ORM使用

1. 过滤
```
for user in session.query(User).\
       filter(User.name=='ed').\
       filter(User.fullname=='Ed Jones'):
       print(user)
       
1. equals:
   query.filter(User.name == 'ed')
2. not equals:
   query.filter(User.name != 'ed')
3. LIKE:
   query.filter(User.name.like('%ed%'))
4. ILIKE (case-insensitive LIKE):
   query.filter(User.name.ilike('%ed%'))
5. IN:
   query.filter(User.name.in_(['ed', 'wendy', 'jack']))

   # works with query objects too:
   query.filter(User.name.in_(
       session.query(User.name).filter(User.name.like('%ed%'))
   ))
6. NOT IN:
   query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
7. IS NULL:
   query.filter(User.name == None)

   # alternatively, if pep8/linters are a concern
   query.filter(User.name.is_(None))
我曹, 太多了. 自己看文档:
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-filter-operators
```

2. 增加记录
```
user = User(**{
    'nickname': 'wangli'
})

sql_session.add(user)
sql_session.commit()
```

3. 数据库migrate使用alembic

原始命令
```
# 创建迁移脚本
alembic revision --autogenerate -m "do test"
# 迁移
alembic upgrade head
```

```
# 自动迁移脚本migrate.py
1. 如果加入新表, 将新表的model加入 lib.serve.migration_env 里边, 如下
   from model import Role
2. 这样, 启动服务的时候, 会运行 lib.serve.migrate 脚本, 自动执行数据库迁移
```