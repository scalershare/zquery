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

from .utils import get_soup, get_hash_id, get_xsrf, PARSER
from .error import UnLoginException
from bs4 import BeautifulSoup
from .login import login
import requests
import json
try:
    import lxml
except:
    pass
import re


class Client(object):
    """
    登录类，本类的实例化对象接受一个用户名和密码，用于登录。
    此类可以用于一些需要登录的操作。
    例如：获取一个用户的全部关注者和被关注者的列表。
    除此之外的其他操作可以通过本类返回的session来进行
    类的全部曹走都必须先登录再进行
    """

    def __init__(self, account, password):
        """
        :param str account: 知乎用户名
        :param str account: 知乎密码
        :return: 登录后的动态对象
        :rtype: Activity
        """
        self.__account = account
        self.__password = password
        self.__session = requests.Session()
        self.__is_login = False

    @property
    def session(self):
        """
        :return: 使用的网络会话
        :rtype: requests.Session()
        """
        return self.__session

    def is_login(self):
        """
        :return: 登陆状态
        :rtype: bool
        """
        return self.__is_login

    def log_in(self):
        """
        登录
        """
        self.__is_login = login(
            self.__session, self.__password, self.__account)

    def get_followees(self, user):
        """
        :param str user: 用户的ID
        :return: 用户的关注者
        :rtype: list
        """
        if self.__is_login == False:
            raise UnLoginException
        _xsrf = get_xsrf(self.__session)

        url = 'https://www.zhihu.com/people/%s/followees' % user
        refer_headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': 'https://www.zhihu.com',
            'Referer': url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        hash_id = get_hash_id(user)
        api_url = "https://www.zhihu.com/node/ProfileFolloweesListV2"

        followees = []
        html = self.__session.get(url, headers=refer_headers)
        bsobj = BeautifulSoup(html.text, PARSER)
        _followee_count = bsobj.find("a", {"class": "item", "href": re.compile(
            "followees")}).find("strong").get_text()
        followee_count = int(_followee_count)
        for i in bsobj.find_all("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"}):
            user = i.find("h2", {"class": "zm-list-content-title"}
                          ).get_text().replace("\n", "")
            followees.append(user)

        for i in range(20, followee_count - 21, 20):
            params = json.dumps(
                {"hash_id": hash_id, "order_by": "created", "offset": i, })
            payload = {"method": "next", "params": params, "_xsrf": _xsrf, }

            r = self.__session.post(
                api_url, data=payload, headers=refer_headers)
            page = r.json()['msg']
            for msg in page:
                soup = BeautifulSoup(msg, PARSER)
                div = soup.find(
                    "div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"})
                name = div.find(
                    "a", {"class": "zg-link author-link"}).attrs['title']
                followees.append(name)
        return followees

    def get_followers(self, user):
        """
        :param str user: 用户的ID
        :return: 关注该用户的人
        :rtype: list
        """
        if self.__is_login == False:
            raise UnLoginException

        _xsrf = get_xsrf(self.__session)

        url = 'https://www.zhihu.com/people/%s/followers' % user
        refer_headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': 'https://www.zhihu.com',
            'Referer': url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        hash_id = get_hash_id(user)
        api_url = "https://www.zhihu.com/node/ProfileFollowersListV2"

        followers = []
        html = self.__session.get(url, headers=refer_headers)
        bsobj = BeautifulSoup(html.text, PARSER)
        _follower_count = bsobj.find("a", {"class": "item", "href": re.compile(
            "followers")}).find("strong").get_text()
        follower_count = int(_follower_count)
        for i in bsobj.find_all("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"}):
            user = i.find("h2", {"class": "zm-list-content-title"}
                          ).get_text().replace("\n", "")
            followers.append(user)

        for i in range(20, follower_count - 21, 20):
            params = json.dumps(
                {"hash_id": hash_id, "order_by": "created", "offset": i, })
            payload = {"method": "next", "params": params, "_xsrf": _xsrf, }

            r = self.__session.post(
                api_url, data=payload, headers=refer_headers)
            page = r.json()['msg']
            for msg in page:
                soup = BeautifulSoup(msg, PARSER)
                div = soup.find(
                    "div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"})
                name = div.find(
                    "a", {"class": "zg-link author-link"}).attrs['title']
                print(name)
                followers.append(name)
        return followers


if __name__ == "__main__":
    c = Client("***", "***")
    c.log_in()
    f = c.get_followees("excited-vczh")
    print(len(f))
