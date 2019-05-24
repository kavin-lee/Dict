# Dict
## 简单的英英词典
### 1. 确定技术

> 通信    tcp通信
> 并发    多进程并发
> 数据库  mysql

### 2. 确定数据库 ： 建立几个表，每个表作用和存储内容

- 建表

> `create database dict charset=utf8;`

> `用户表 ： id   name   passwd`

> `create table user (id int primary key auto_increment,name varchar(32) not null,passwd varchar(128) not null);`

> `历史记录：id   name   word   time`

> `create table hist (id int primary key auto_increment,name varchar(32) not null,word varchar(32) not null,time varchar(64) not null);`

> `单词表： id   word  mean`

- 编写程序将单词本存入到数据库

> `create table words (id int primary key auto_increment,word varchar(32),mean text);`

### 3. 结构设计

> 客户端
> 服务端 （处理数据）

### 4. 功能分析

> 客户端和服务端分别需要实现哪些功能

> 网络模型

> 注册

> 客户端  :
>
> - 输入注册信息
>
> - 将信息发送给服务端
> - 等待反馈

> 服务端  
>
> - 接收注册信息
> - 验证用户是否存在
> - 将信息反馈个客户端

> 登录 
>    客户端 
>
> - 输入登录信息
> - 发送请求
> - 得到回复

> 服务端 
>
> - 接收请求
> - 判断是否允许登录
> - 反馈结果

> 单词查询:
>
> 客户端 ： 
>
> -  输入单词
> - 发送给服务器

> 服务端 ：
>
> - 接收请求
> -  查找单词
> - 将结果发送给客户端
> -  插入历史记录

>  历史记录:
>
> 客户端：
>
> - 发送请求
> - 循环接收历史记录
>
> 服务端：
>
> - 接收请求
>
> - 查询历史记录
> - 历史记录

### 5. 协议指定 ：  

- 注册  R name passwd
- 登录  L name  passwd
- 查词 ： Q name word
- 历史记录 ： H  name

### 6. 扩展

> cookie ： 
>         import  getpass
> 	getpass.getpass()
> 	功能: 隐藏输入内容
> 	返回值： 输入的内容字符串

> cookie ：
>   import hashlib

> 生成加密对象 参数为 "盐"
>   hash = hashlib.md5(("Levi"+"the-sat").encode())

> 对密码进行算法加密
>   hash.update(passwd.encode())

> 获取加密后的密码字串
>   hash.hexdigest()
