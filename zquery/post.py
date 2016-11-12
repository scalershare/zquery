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

from .utils import headers
from .error import UrlException
import requests

MAX_COUNT = 10000


class Post(object):
    """
    知乎专栏文章类,提供知乎专栏文章的API。
    """

    def __init__(self, url, *args, **kwargs):
        """初始化

        :param str url: 文章的网址
        :return: post动态对象


        注: 对传入的URL会进行检测，如果错误会抛出UrlException。
        """
        self.__url = url
        if "?" in self.__url or "http" not in self.__url or "p" not in self.__url:
            raise UrlException
        self.__id = self.__url.split("/")[4]
        self.__api = "https://zhuanlan.zhihu.com/api/posts/" + self.__id
        r = requests.get(self.__api, headers=headers)
        self.__json_data = r.json()

    @property
    def url(self):
        """
        :return: 文章的地址
        :rtype: str
        """
        return self.__url

    @property
    def id(self):
        """
        :return: 文章的ID
        :rtype: str
        """
        return self.__id

    @property
    def title(self):
        """
        :return: 文章的标题
        :rtype: str
        """
        return self.__json_data['title']

    @property
    def author(self):
        """
        :return: 文章的作者
        :rtype: str
        """
        return self.__json_data['author']['name']

    @property
    def author_des(self):
        """
        :return: 作者的描述
        :rtype: str
        """
        try:
            return self.__json_data['author']['badge']['identity']['description']
        except:
            return "NO description"

    @property
    def summary(self):
        """
        :return: 文章的总结
        :rtype: str
        """
        return self.__json_data['summary']

    @property
    def content(self):
        """
        :return: 文章的内容
        :rtype: str
        """
        return self.__json_data['content']

    def get_comments(self, count=MAX_COUNT):
        """获取评论
        :param int count: 获取数，不填代表获取全部
        :return: 评论
        :rtype: list (author, content)
        """
        comments = []
        api_1 = "https://zhuanlan.zhihu.com/api/posts/%s/comments?limit=10" % self.__id

        def crawl(api):
            r = requests.get(api, headers=headers)
            datas = r.json()
            for i in datas:
                author = i['author']['name']
                content = i['content']
                comments.append((author, content))

        crawl(api_1)
        offset = 10
        while True:
            if len(comments) % 10 or len(comments) > count:
                break
            api_2 = api_1 + "&offset=" + str(offset)
            crawl(api_2)
            offset += 10
        return comments[:count]


if __name__ == "__main__":
    p = Post("https://zhuanlan.zhihu.com/p/19780644")
    # print(p.id)

    # print(p.author)
    # print(p.author_des)
    # print(p.content)
    comments = p.get_comments()
    print(len(comments))
