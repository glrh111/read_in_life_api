服务配置

- API服务, tornado改造版本, SQLALCHEMY提供ORM.

- pgsql服务存取一般数据

- redis服务提供快速读取服务

- 搜索服务: 使用elasticsearch.

- 队列服务: 使用rabbitmq或者kafkamq. 处理异步任务

* 数据库服务相关配置与API写在一起.

- 后台服务: 管理docker, 管理线上数据, 部署管理等

- WEAPP代码

- 通用浏览器前端代码

## API服务启动步骤
1. 将代码根目录`read_in_life_api` 加入`sys.path`
2. 运行服务: 首先collect 路由, 然后将路由作为参数传递给服务启动项目.

## API服务Config

1. 配置文件路径: spec.config. 
   文件里config字典为{配置名称: 配置cls}

2. 怎样确定加载哪一个配置?
   从环境里边取得 `READ_IN_LIFE_API_ENV` 环境变量, 作为上述`配置名称`, 寻找配置文件.

3. 在代码里导入配置项目:

   from lib.serve.config import app_config
   
   app_config 就代表当前使用的配置文件

## Run postgresql

1. 拉镜像 `docker pull postgres`

2. run 容器`docker run --name postgres -e POSTGRES_PASSWORD=wocao -d postgres`

3. 进入docker `docker exec -it postgres bash`

4. 初始化数据库 数据库名称 read_in_life 密码 wocao 
```
adduser read_in_life  # 新建用户
su - postgres         # 切换用户
psql                  # 进入DBMS

CREATE USER read_in_life WITH PASSWORD 'wocao'; # 创建数据库角色
CREATE DATABASE read_in_life OWNER read_in_life; # 创建app专属数据库
GRANT ALL PRIVILEGES ON DATABASE read_in_life to read_in_life; # 授全权
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