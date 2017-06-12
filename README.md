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