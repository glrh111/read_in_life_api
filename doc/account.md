# account 模块API

获取登录状态的
1. `username`
2. `email`
3. `country_code + phone`

## 综述

产生内容的用户以及需要在本平台保存个人信息的用户, 需要提供一个唯一的id, 与平台内的信息对应起来. 新建这个对应关系操作的, 有两种,
+ 从第三方平台获取 openid, 同一个第三方账号给出的openid保持不变; 之后, 新建一个平台内保存的user_id, 与其对应起来.
+ 用户提供手机号,用户名username等在本平台内唯一的值, 给平台, 然后平台生成user_id, 与其对应起来. 

新建这种对应关系后, 用户就可以通过以上两种方式, 登录平台, 平台通过 openid or username or phone (第三方平台或者用户提供)
找到平台内存储的user_id, 随后就可以找到该用户存储的各种信息. 


## 第三方登录, 以weapp端微信为例

### 流程梳理

> 参考 `https://mp.weixin.qq.com/debug/wxadoc/dev/api/api-login.html`

0. 一些服务器资源要求用户处于登录状态方可获取, 比如提交评论. 这时候本平台会提示, 用户需要处于登录状态.
1. 调用`wx.login` 获取`code`
2. 将`code`发送到本平台, 平台携带小程序的`appid`和`secret`, 发送到微信相关API上, 获取`openid`和一个`sessionkey`
3. 本平台通过`openid`对应`user_id`, 生成`3rdsession`, 返回给用户, 即登陆成功. 
4. 用户需要将 `3rdsession` 放入localstorage里边,避免每次进入小程序, 都得登录. 体验不好. 

next time用户打开小程序, 建议进行如下操作:
1. 调用weapp提供的 `wx.checkSession` 检测当前用户登录态是否有效. 估计是 `sessionkey`有时效性.
2. 如果失效, 从`wx.login`重新来一次
3. 如果没失效, 从localstorage里边获取`3rdsession`, 登录平台. 

第二段中的步骤不是必须的, 但是如果从微信平台上获取用户的信息, 需要这个东西.



提供register, log in, log out 功能.

API前缀: /account



## 注册 POST register 

### 注册途径



以上字段, 全局唯一, 不能使用同样信息重复注册.

另外, 需要传入password字段. 不能为空

## 登录 POST log_in 

传入字段同上

## 登出 POST log_out

登录状态下的用户, 可以调用本API.

## 注意项

1. 登录信息相关字段, 需要验证合法性. 

2. 密码也需要验证合法性. middleware?

