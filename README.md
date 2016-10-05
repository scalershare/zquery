# Zquery——基于Python3的知乎非官方API库和交互式命令行

## Table of Contents

* [Table of Contents](#Table of Contents)

* [介绍](#介绍)

* 快速开始

  * 注意
  * 解决依赖
  * 克隆本项目
  * 使用pip直接安装

* 交互命令行的使用

  * Usage
  * Arguments
  * Options
  * Example

* 主要API

  * class zquery.User —— 用户操作类

  * class zquery.Question —— 问题操作类

  * class zquery.Answer —— 回答操作类

  * class zquery.Column —— 专栏操作类

  * class zquery.Post —— 专栏文章操作类

  * class zquery.Client —— 登录及高阶操作类

* 其他工具函数

  * login(session, secret, account)
  * get_hash_id(user)
  * get_xsrf(session)
  * get_captcha(session)



## 介绍

Zquery由Python3.5编写，可以用来获取知乎上的用户信息，问题信息，专栏信息，文章信息等，也可以方便的配合网络爬虫使用。同时，Zquery也提供了一个交互式的环境，可以用于简单的信息查询。  

例如，对于一个问题，使用如下代码就可以获得一些它的信息：

```python
from Zquery import Question

q = Question("https://www.zhihu.com/question/22731205")

print(q.title)
print("------------------------------------------")
print(q.detail)
print("------------------------------------------")
print(q.ans_num)
```

  

```
数据在电脑内是如何进行传输的？
------------------------------------------
电脑里的数据都是0和1，或者说高电压，低电压，貌似是通过电子移动实现的？
对这个东西在电脑里的传送一直缺乏感性认识，求指点。比如大型3D游戏，在内
存和显卡之间会存在大量的数据传送，硬件上是如何做到瞬间接收大量数据且不
会出错的？我想到提升传输速度的方式是并行，比如一个芯片上有N个金属引脚，
意味着这个芯片能一次接受N位数据？但是这N位数据怎么保证完整性，比如一系
列N位数据传输的时候，怎么保证每个N位数据是同步的，且不会和之前之后的比
特混淆？还有这种电脑内的数据传输是否存在极限速度？
------------------------------------------
13
```

对于交互式命令行，使用也非常方便，比如在命令行中输入：

```
$ zquery post https://zhuanlan.zhihu.com/p/19780644
```

就可以得到以下的输出了    

```
---------------------------------------                                                    
Url: https://zhuanlan.zhihu.com/p/19780644                                                  
ID: 19780644                                                                               Title: 所见（1）                                                                              Author: MJ勺子                                                                              Author description: NO description                                                         Summary: 3月在广州，观察黄埔关区，某保税区内，库房密集，
不如想象的繁忙。早前闻名四方的「红酒一条街」，漫步其间，
招牌、张贴仍在，人迹稀疏，多数店铺已撤空，毫无疑问的萧条。
据说是该区海关机构比较稳（bao）健（shou），创新力欠缺，
导致优质客户流失到别的…                  
--------------------------------------- 
```

## 快速开始

**注意**

1. 电脑中请安装python3，本项目使用的是Python3.5开发的。
2. 确保系统中安装了pip和git且保持在最新的版本。

**解决依赖**

* BeautifulSoup
* lxml
* requests
* pillow
* prettytable
* docopt

**克隆本项目**

```
$ git clone https://github.com/WiseDoge/Zquery.git
$ cd Zquery
$ python install setup.py
```

**使用pip直接安装**

`$ pip install zquery`



## 交互命令行的使用

Usage:

    zquery [(-q|-r|-a)] [--depth=<co>] <user>
    zquery question <url>
    zquery answer <url>
    zquery column <url>
    zquery post <url>

Arguments:

```
user           用户ID
url            网址
```

Options:

    -q             提问 
    -r             回答
    -a             文章
    --depth=<co>   显示的条数

Example:
```
zquery -a --depth=15 excited-vczh
zquery excited-vczh
zquery post https://zhuanlan.zhihu.com/p/19780644
```

## 主要API
### *class zquery.User* —— 用户操作类

>__init__(self, id)
>
>zqyery.User类实例化时需要传入一个用户ID作为改类对象的标识，当ID传入错误时会抛出异常。
>
>@property   name()
>
>> 返回用户的昵称
>>
>> rtype: str
>
>@property   followees()
>
>>返回用户关注的人数
>>
>>rtype: str
>
>@property   followers()
>
>> 返回关注该用户的人数
>>
>> rtype: str
>
>@property   agree_num()
>
>> 返回用户的赞同数
>>
>> rtype: int
>
>@property   thanks_num()
>
>> 返回用户的被感谢数
>>
>> rtype: int
>
>@property   presentation()
>
>> 返回用户的bio
>>
>> rtype: str
>
>@property   location_item()
>
>> 返回用户的位置
>>
>> rtype: str
>
>@property   business_item()
>
>> 返回用户的行业
>>
>> rtype: str
>
>@property employment_item()
>
>> 返回用户的公司
>>
>> rtype: str
>
>@property   position_item()
>
>> 返回用户的职位
>>
>> rtype: str
>
>@property   education_item()
>
>> 返回用户的毕业院校
>>
>> rtype: str
>
>@property   education_extra_item()
>
>> 返回用户的院系
>>
>> rtype: str
>
>get_base_info()
>
>> 返回用户的基本信息
>>
>> rtype: dict
>
>get_asks(count=MAX_COUNT)
>
>> param: count  计数，不填代表全部
>>
>> 返回指定数量的该用户的提问
>>
>> rtype: list (vote_num, ask_num, followers, question)
>
>get_articles(count=MAX_COUNT)
>
>> param: count  计数，不填代表全部
>>
>> 返回指定数量的该用户的专栏文章
>>
>> rtype: list (title, content)
>
>get_answerss(count=MAX_COUNT)
>
>> param: count  计数，不填代表全部
>>
>> 返回指定数量的该用户的回答
>>
>> rtype: list (support_num, commit_num, question, ans)

### *class zquery.Question* —— 问题操作类

> __init__(self, url)
>
> zquery.Question 类实例化时需要传入一个url作为改类对象的标识，当url传入错误时会抛出异常。
>
> @property   url()
>
> >返回问题的URL
> >
> >rtype: str
>
> @property   id()
>
> >返回问题的ID
> >
> >rtype: str
>
> @property   title()
>
> >返回问题的标题
> >
> >rtype: str
>
> @property   detail()
>
> >返回问题的描述
> >
> >rtype: str
>
> @property   ans_num()
>
> >返回问题的回答人数
> >
> >rtype: int
>
> @property   tags()
>
> >返回问题的标签
> >
> >rtype: list
>
> @property   follower_num()
>
> >返回问题的关注人数
> >
> >rtype: int
>
> get_answer_urls()
>
> >返回所有答案的URL
> >
> >yieldtype: str

### *class zquery.Answer* —— 回答操作类

>__init__(arg1=None, arg2=None)
>
>这里提供了两种构造方式，一种是通过传入URL构造，这事arg2为空，另一种是通过传入问题ID和答案ID来构造，这是arg1是问题ID，arg2是答案的ID。对传入的URL会进行检测，如果错误会抛出UrlException。
>
>@property   url()
>
>>返回回答的URL
>>
>>rtype: str
>
>@property   id()
>
>>返回回答的ID
>>
>>rtype: str
>
>@property   author()
>
>>返回回答的作者
>>
>>rtype: str
>
>@property   support_count()
>
>>返回回答的赞同数
>>
>>rtype: int
>
>@property   author_bio()
>
>>返回答主的bio
>>
>>rtype: str
>
>@property   modify_date()
>
>>返回回答的修改日期
>>
>>rtype: str
>
>@property   content()
>
>>返回回答的内容
>>
>>rtype: str
>
>@property   get_question()
>
>>返回该回答的原问题
>>
>>rtype: zqyery.Question

### *class zquery.Column* —— 专栏操作类

>__init__(self, url)
>
>zquery.Column 类实例化时需要传入一个url作为改类对象的标识，当url传入错误时会抛出异常。
>
>@property   url()
>
>>返回专栏的URL
>>
>>rtype: str
>
>@property   id()
>
>>返回专栏的ID
>>
>>rtype: str
>
>@property   title()
>
>>返回专栏的标题
>>
>>rtype: str
>
>@property   description()
>
>>返回专栏的描述
>>
>>rtype: str
>
>@property   followers_count()
>
>>返回专栏的关注者的数量
>>
>>rtype: int
>
>@property   tags()
>
>>返回专栏的标签
>>
>>rtype: list
>
>@property   posts_num()
>
>>返回专栏的文章数
>>
>>rtype: int
>
>get_posts()
>
>>返回专栏的文章
>>
>>list (id, title, content)

### *class zquery.Post* —— 专栏文章操作类

>__init__(self, url)
>
>zquery.Post 类实例化时需要传入一个url作为改类对象的标识，当url传入错误时会抛出异常。
>
>@property   url()
>
>> 返回专栏文章的URL
>>
>> rtype: str
>
>@property   id()
>
>> 返回专栏文章的ID
>>
>> rtype: str
>
>@property   title()
>
>> 返回专栏的标题
>>
>> rtype: str
>
>@property   author()
>
>>返回专栏文章的作者
>>
>>rtype: str
>
>@property   summary()
>
>>返回专栏文章的摘要
>>
>>rtype: str
>
>@property   author_des()
>
>>返回专栏文章的作者简介
>>
>>rtype: str
>
>@property   content()
>
>>返回专栏文章的内容
>>
>>rtype: str
>
>get_comments()
>
>> 返回专栏文章的评论
>>
>> rtype: list (author, content)



### *class zquery.Client* —— 登录及高阶操作类

> __init__(account, password)
>
> 本类的实例化对象接受一个用户名和密码，用于登录。类的全部曹走都必须先登录再进行.
>
> is_login()
>
> >判断是否成功登录，如果成功登录返回True，否则返回False
> >
> >rtype: bool
>
> log_in()
>
> >登录
>
> @property   session()
>
> >返回登录后的网络会话环境
> >
> >rtype: requests.Session()
>
> get_followees(user)
>
> >返回一个用户的全部关注的人的列表
> >
> >param: str user 用户的ID
> >
> >rtype: list
>
> get_followers(user)
>
> >返回关注该用户的全部的人的列表
> >
> >param: str user 用户的ID
> >
> >rtype: list

# 其他工具函数

### *login(session, secret, account)*

>  param: requests.Session() session 网络会话
>
>  param: str secret 知乎账户密码
>
>  param: str account 知乎账户
>
>  登录函数，对于一个刚刚初始化的网络会话，可以利用login函数来登录，并保存登录状态。

### *get_hash_id(user)*

> params: str user 知乎用户ID
>
> return: 知乎用户的哈希ID
>
> rtypes: str
>
> 每一个知乎用户都有一个哈希ID，通过此函数可以获取一个用户的hash_id

### *get_xsrf(session)*

> param: requests.Session() session 网络会话
>
> return: 登录时所需的_xsrf码
>
> rtypes: str
>
> 每次登录操作都需要一个操作码_xsrf，本函数可以获取操作码。

### *get_captcha(session)*

> param: requests.Session() session 网络会话
>
> 获取登录时的验证码





