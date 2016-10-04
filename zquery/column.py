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

from .utils import get_soup, headers
from .error import UrlException
import requests
import re

# 最大获取数，默认10000，代表全部。
MAX_COUNT = 10000


class Column(object):
    """
    知乎专栏类,提供知乎专栏的API。
    """

    def __init__(self, url):
        """初始化

        :param str url: 专栏的网址
        :return: column动态对象


        注: 对传入的URL会进行检测，如果错误会抛出UrlException。
        """
        self.__url = url
        if "?" in self.__url or "http" not in self.__url:
            raise UrlException
        self.__id = self.__url.split("/")[3]
        self.__api = "https://zhuanlan.zhihu.com/api/columns/" + self.__id
        r = requests.get(self.__api, headers=headers)
        self.__json_data = r.json()

    @property
    def url(self):
        """
        :return: 专栏的地址
        :rtype: str
        """
        return self.__url

    @property
    def id(self):
        """
        :return: 专栏的id
        :rtype: str
        """
        return self.__id

    @property
    def title(self):
        """
        :return: 专栏的标题
        :rtype: str
        """
        return self.__json_data['name']

    @property
    def description(self):
        """
        :return: 专栏的描述
        :rtype: str
        """
        return self.__json_data['description']

    @property
    def followers_count(self):
        """
        :return: 专栏的关注者人数
        :rtype: int
        """
        return self.__json_data['followersCount']

    @property
    def tags(self):
        """
        :return: 专栏的标签
        :rtype: list
        """
        datas = self.__json_data['postTopics']
        tags = [i['name'] for i in datas]
        return tags

    @property
    def posts_num(self):
        """
        :return: 专栏的文章数
        :rtype: int
        """
        return self.__json_data['postsCount']

    def get_posts(self, count=MAX_COUNT):
        """
        :param ing count: 获取数，不填代表获取全部
        :return: 获取专栏的文章
        :rtype: list (id, title, content)
        """
        posts = []
        api_1 = "https://zhuanlan.zhihu.com/api/columns/%s/posts?limit=20" % self.__id

        def crawl(api):
            r = requests.get(api, headers=headers)
            datas = r.json()
            for i in datas:
                title = i["title"]
                content = i["content"]
                id = i['href'].split("/")[3]
                posts.append((id, title, content))

        crawl(api_1)
        offset = 20
        while True:
            if len(posts) % 20 or len(posts) > count:
                break
            api_2 = api_1 + "&offset=" + str(offset)
            crawl(api_2)
            offset += 20

        return posts[:count]


if __name__ == "__main__":
    c = Column("https://zhuanlan.zhihu.com/he110world")
    print(c.description)
    posts = c.get_posts(12)
    for i in posts:
        print(i[0])
