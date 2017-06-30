# account 模块API

## 综述

产生内容的用户以及需要在本平台保存个人信息的用户, 需要提供一个唯一的id, 与平台内的信息对应起来. 新建这个对应关系操作的, 有两种,
+ 从第三方平台获取 openid, 同一个第三方账号给出的openid保持不变; 之后, 新建一个平台内保存的user_id, 与其对应起来.
+ 用户提供手机号,用户名username等在本平台内唯一的值, 给平台, 然后平台生成user_id, 与其对应起来. 

新建这种对应关系后, 用户就可以通过以上两种方式, 登录平台, 平台通过 openid or username or phone (第三方平台或者用户提供)
找到平台内存储的user_id, 随后就可以找到该用户存储的各种信息. 

还有比较关键的一点，一些用户使用微信小程序登录app后，发表了一些内容；
以后希望通过网页登录的时候，希望关联到同一个账号上，初步思考的API实现如下：

1. 只开通`a 用户名+密码`和`b 微信第三方登录`两种产生新用户的方式。
   - a. 用户需要提供 用户名 + 密码
   - b. 用户用微信成功登录以后，
     - 如果没有用户名和密码关联，需要设置用户名和密码。
       - 如果输入的用户名已经存在，执行关联操作：
         - 如果这个用户名和密码没有与微信(或者其他同一个)平台的第三方账号关联，那么可以关联
         - 如果已经与同一个平台的微信发生关联，那么，不可以关联。
       - 如果输入的用户名唯一且可用，执行新建操作
   - 其后，无论用户先使用a还是b注册，均可以通过用户名+密码登录。
2. 用户在网页上可选择a 方式注册；在weapp端可以选择两种方式注册。


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


### 第三方登录注册流程如下

1. 在哪里注册？
   - 用户为了发表评论等，根据服务端LoginRequired提示，转到弹框页面；
   - 用户主动点击第三方登录按钮。

2. 点击登录后，执行如下操作:
   - wx.login 获取 js_code
   - weapp将js_code发送到 /account/login {js_code, platform=1}
   - 服务端用appid+secret+js_code获取用户的openid,session_key
   - 服务端取得openid, 这里分了两种情况：
     , session_key到redis里边。openid: session_key。
     
     1. 这个openid已经设置了username和password。直接变为登录状态。
     2. 通过这个openid找不到相关后台设置。那么强制执行关联操作，
     
     
   - 

## 相关API

1. POST /account/log_in 登录接口

请求参数

+ weapp登录: 
  - 请求参数：login_type==2, platform==2, js_code
  - 返回字段：
    code: 
      + 1 登录成功；
      + 2 需要强制关联账号信息 这时候需要openid;
      + 3 服务端没有获取到openid和其他错误

+ 网页端登录: 
  - 请求参数：login_type==1, username, password
  - 返回字段：code：1 登录成功；其他：登录失败。提示用户名不存在或者密码不对。
  
2. POST /account/associate openid关联账号操作。
   
   + stage 2 / 3执行之后，如果成功，即可进入登录状态。
   
   + 同一个open_id要确保不能和不同的username关联。
   
   按照stage划分请求阶段： 
   + stage == 1:
     + 用处：携带username 进行进行查询操作
     + 请求参数：platform=2, openid=..., username=..., stage=1
     + 返回参数：
       + code == 1:
           + stage==2: username可以使用。需要设置password
           + stage==4: username以前用过。而且已经关联过weapp账号。
           + stage==3: username以前用过。但是没有关联过。需要验证密码。
       + code == 其他：username不可用或者其他错误
       
   + stage == 2:
     + 用处：携带username和password进行绑定操作
     + 请求参数：platform=2, openid=..., username=..., stage=2， password
     + 返回参数： 
       + code==1：成功绑定账户。
   + stage == 3:
     + 用处：验证密码
     + 请求参数：platform=2, openid=..., username=..., stage=2， password
     + 返回参数：
       + code==1: 成功关联用户
       + code==其他：密码不可用。
   + stage==4:
     + 用处：没有后续操作。提示用户username不可用。
     
3. POST /account/log_out 登出接口

4. POST /account/register 网页端使用。
   - 请求参数: username password

## 表设计

### 用户在平台内的信息

用户标识符相关
+ user_id 平台自动生成， 主要关联字段
+ username 用户设定，唯一
+ password_hash 存储加密的密码

用户信息相关
+ email
+ penname 
+ avatar 
  - 用户首次注册成功，取得头像。其后，用户主动换头像，再变。
+ motto 一句话介绍
+ brief_introduction 简要介绍
+ country 国家

登录记录相关
+ ctime 本记录建立时间
+ last_login_time 上次登录时间

### 第三方平台关联信息

+ user_id user表里的用户id
+ openid 
+ platform 哪个第三方平台
+ ctime 本条记录建立时间



