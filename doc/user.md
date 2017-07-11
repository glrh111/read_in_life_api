# user资源相关

## API整理

1.  /user/<id number> 
   + GET 某个用户相关的信息
   + 新建,删除等其他用处, 在account里边.

2. /user/
   + GET 获取用户本人的信息
   + PUT 更新用户密码等信息. 分为更新密码1, 更新其他信息2
     + 修改密码的时候, 需要同时提供新老密码, 做校验
     + 可以更新的其他内容有: email, penname, avatar, 
       motto, brief_introduction, country

3. /user/<id number>/post
   + GET 这个用户发表的全部文章

4. /user/post
   + GET 获得用户本人的文章列表