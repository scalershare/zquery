# Copyright 2016 wisedoge

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
交互式命令行模块
"""


from prettytable import PrettyTable
from .user import User
from .post import Post
from .column import Column
from .question import Question
from .answer import Answer
from .collection import Collection

MAX_COUNT = 10000


def pprint_user_answer(id, count=MAX_COUNT):
    """输出该用户的回答
    :param str id: 用户ID
    :param int count: 输出数，不填代表全部输出
    """
    user = User(id)
    row = PrettyTable(
        ["ID", "Support num", "Commit num", "Question", "Answer"])
    row.align["Support num"] = "l"
    row.align["Commit num"] = "l"
    row.align["Question"] = "l"
    row.align["Answer"] = "l"
    answers = user.get_answers(count)
    row.padding_width = 1
    i = 0
    for answer in answers:
        record = list(answer)
        record.insert(0, i)
        row.add_row(record)
        i += 1
    print(row)


def pprint_user_article(id, count=MAX_COUNT):
    """输出该用户的专栏文章
    :param str id: 用户ID
    :param int count: 输出数，不填代表全部输出
    """
    user = User(id)
    row = PrettyTable(["ID", "Title", "Summary"])
    row.align["Title"] = "l"
    row.align["Summary"] = "l"
    articles = user.get_articles(count)

    row.padding_width = 1
    i = 0
    for article in articles:
        record = list(article)
        record.insert(0, i)
        row.add_row(record)
        i += 1
    print(row)


def pprint_user_ask(id, count=MAX_COUNT):
    """输出该用户的提问
    :param str id: 用户ID
    :param int count: 输出数，不填代表全部输出
    """
    user = User(id)
    row = PrettyTable(["ID", "Vote num", "Ask num", "Followers", "Question"])
    row.align["Vote num"] = "l"
    row.align["Ask num"] = "l"
    row.align["Followers"] = "l"
    row.align["Question"] = "l"
    asks = user.get_asks(count)
    row.padding_width = 1
    i = 0
    for ask in asks:
        record = list(ask)
        record.insert(0, i)
        row.add_row(record)
        i += 1
    print(row)


def pprint_user_base(id):
    """输出该用户的基本信息
    :param str id: 用户ID
    """
    print("---------------------------------------")
    data = User(id).get_base_info()
    datalist = list(data.items())
    for i in datalist:
        print("%s: %s" % (i[0], i[1]))
    print("---------------------------------------")


def pprint_post(url):
    """输出一片专栏文章的信息
    :param str url: 网址
    """
    p = Post(url)
    print("---------------------------------------")
    print("Url: " + p.url)
    print("ID: " + p.id)
    print("Title: " + p.title)
    print("Author: " + p.author)
    print("Author description: " + p.author_des)
    print("Summary: " + p.summary)
    print("---------------------------------------")


def pprint_column(url):
    """输出一个专栏的信息
    :param str url: 网址
    """
    c = Column(url)
    print("---------------------------------------")
    print("Url: " + c.url)
    print("ID: " + c.id)
    print("Title: " + c.title)
    print("Description: " + c.description)
    print("Tags: " + str(c.tags))
    print("Posts num: " + str(c.posts_num))
    print("Followers number: " + str(c.followers_count))
    print("---------------------------------------")


def pprint_question(url):
    """输出一个问题的信息
    :param str url: 网址
    """
    q = Question(url)
    print("---------------------------------------")
    print("Url: " + q.url)
    print("ID: " + q.id)
    print("Title: " + q.title)
    print("Answers number: " + str(q.ans_num))
    print("Tags: " + str(q.tags))
    print("Followers number: " + str(q.follower_num))
    print("---------------------------------------")


def pprint_answer(url):
    """输出一个回答的信息
    :param str url: 网址
    """
    a = Answer(url)
    print("---------------------------------------")
    print("Url: " + a.url)
    print("ID: " + a.id)
    print("Author: " + a.author)
    print("Author bio: " + a.author_bio)
    print("Support number: " + str(a.support_count))
    print("Modify date: " + a.modify_date)
    print("Content: " + a.content)
    print("---------------------------------------")


def pprint_collection(url):
    """输出一个收藏夹的信息
    :param str url: 网址
    """
    c = Collection(url)
    print("---------------------------------------")
    print("Url: " + c.url)
    print("ID: " + c.id)
    print("Title: " + c.title)
    print("Description: " + c.description)
    print("Creator : " + c.creator)
    print("Creator Description: " + c.creator_des)
    print("---------------------------------------")



if __name__ == "__main__":
    # pprint_user_article("excited-vczh",30)
    pprint_column("https://zhuanlan.zhihu.com/vczh-nichijou")
    pprint_answer("https://www.zhihu.com/question/51249091/answer/124869004")
    pprint_post("https://zhuanlan.zhihu.com/p/22551537")
    pprint_question("https://www.zhihu.com/question/51249091")
