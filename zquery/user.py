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

from .utils import get_soup, get_next, MODE
from .error import IdException
import re

MAX_COUNT = 10000


class User(object):
    """
    用户类，提供关于用户操作的API
    """

    def __init__(self, id):
        """初始化

        :param str id: 用户的ID
        :return: User动态对象


        注: 1.对传入的URL会进行检测，如果错误会抛出UrlException。
            2.构造器会生成self.__items, 改域内包含了该用户的基本信息。

        """
        self.__id = id
        if "https://" in self.__id:
            raise IdException
        self.__url = "https://www.zhihu.com/people/" + self.__id
        self.__soup = get_soup(self.__url)
        self.__items = self.__soup.find("div", {"class": "items"})

    @property
    def name(self):
        """
        :return: 用户的名字
        :rtype: str
        """
        name = self.__soup.find("div", {"class": "title-section"}
                                ).find("span", {"class": "name"}).get_text()
        return name

    @property
    def followees(self):
        """
        :return: 用户的关注人数
        :rtype: str
        """
        try:
            followees = self.__soup.find("a", {"class": "item", "href": re.compile(
                "followees")}).find("strong").get_text()
        except AttributeError:
            followees = "0"
        return followees

    @property
    def followers(self):
        """
        :return: 关注该用户的人数
        :rtype: str
        """
        try:
            followers = self.__soup.find("a", {"class": "item", "href": re.compile(
                "followers")}).find("strong").get_text()
        except AttributeError:
            followers = "0"
        return followers

    @property
    def agree_num(self):
        """
        :return: 用户的赞同数
        :rtype: int
        """
        scope = self.__soup.find(
            "span", {"class": "zm-profile-header-user-agree"})
        agree_num = scope.find("strong").get_text()
        return int(agree_num)

    @property
    def thanks_num(self):
        """
        :return: 用户的感谢
        :rtype: int
        """
        scope = self.__soup.find(
            "span", {"class": "zm-profile-header-user-thanks"})
        thanks_num = scope.find("strong").get_text()
        return int(thanks_num)

    @property
    def presentation(self):
        """
        :return: 用户的bio
        :rtype: str
        """
        try:
            presentation = self.__soup.find(
                "div", {"class": "bio ellipsis"}).get_text()
        except AttributeError:
            presentation = "NODATA"
        return presentation

    @property
    def location_item(self):
        """
        :return: 用户的位置
        :rtype: str
        """
        try:
            location_item = self.__items.find(
                "span", {"class": "location item"}).get_text()
        except AttributeError:
            location_item = "NODATA"
        return location_item

    @property
    def business_item(self):
        """
        :return: 用户的行业
        :rtype: str
        """
        try:
            business_item = self.__items.find(
                "span", {"class": "business item"}).get_text()
        except AttributeError:
            business_item = "NODATA"
        return business_item

    @property
    def employment_item(self):
        """
        :return: 用户的就业
        :rtype: str
        """
        try:
            employment_item = self.__items.find(
                "span", {"class": "employment item"}).get_text()
        except AttributeError:
            employment_item = "NODATA"
        return employment_item

    @property
    def position_item(self):
        """
        :return: 用户的职位
        :rtype: str
        """
        try:
            position_item = self.__items.find(
                "span", {"class": "position item"}).get_text()
        except AttributeError:
            position_item = "NODATA"
        return position_item

    @property
    def education_item(self):
        """
        :return: 用户的毕业院校
        :rtype: str
        """
        try:
            education_item = self.__items.find(
                "span", {"class": "education item"}).get_text()
        except AttributeError:
            education_item = "NODATA"
        return education_item

    @property
    def education_extra_item(self):
        """
        :return: 用户的学院
        :rtype: str
        """
        try:
            education_extra_item = self.__items.find(
                "span", {"class": "education-extra item"}).get_text()
        except AttributeError:
            education_extra_item = "NODATA"
        return education_extra_item

    def get_base_info(self):
        """返回用户的基本信息

        :return: 用户的基本信息
        :rtype: dict
        """
        data = {
            "Name": self.name,
            "Presentation": self.presentation,
            "Location_item": self.location_item,
            "Business_item": self.business_item,
            "Employment_item": self.employment_item,
            "Position_item": self.position_item,
            "Education_item": self.education_item,
            "Education_extra_item": self.education_extra_item,
            "Followees": self.followees,
            "Followers": self.followers,
            "Agree_num": self.agree_num,
            "Thanks_num": self.thanks_num,
        }
        return data

    def get_asks(self, count=MAX_COUNT):
        """获取提问
        :param int count: 获取数，不填代表获取全部
        :return: 该用户的提问
        :rtype: list (vote_num, ask_num, followers, question)
        """
        start_url = "https://www.zhihu.com/people/%s/asks" % self.__id
        asks = []

        def crawl(url):
            soup = get_soup(url)
            for ask in soup.find_all("div", {"class": "zm-profile-section-item zg-clear"}):
                question = ask.find("h2").get_text().replace("\n", "")
                vote_num = ask.find(
                    "div", {"class": "zm-profile-vote-num"}).get_text()
                scope = ask.find("div", {"class": "meta zg-gray"}).get_text()
                zg_gray = MODE.findall(scope)
                ask_num = zg_gray[0]
                followers = zg_gray[1]
                asks.append((vote_num, ask_num, followers, question))
            if len(asks) >= count:
                return
            next_page = get_next(soup, start_url)
            if next_page != None:
                crawl(next_page)
        crawl(start_url)
        return asks[:count]

    def get_answers(self, count=MAX_COUNT):
        """获取回答
        :param int count: 获取数，不填代表获取全部
        :return: 该用户的回答
        :rtype: list (support_num, commit_num, question, ans)
        """
        start_url = "https://www.zhihu.com/people/%s/answers" % self.__id
        answers = []

        def crawl(url):
            soup = get_soup(url)
            for answer in soup.find_all("div", {"class": "zm-item"}):
                question = answer.find("h2").get_text().replace("\n", "")
                raw_ans = answer.find(
                    "div", {"class": "zh-summary summary clearfix"}).get_text()
                ans = raw_ans.replace("\n", "").replace("显示全部", "")[:30]
                support_num = answer.find(
                    "a", {"class": "zm-item-vote-count js-expand js-vote-count"}).get_text()
                scope = answer.find("a", {"name": "addcomment"}).get_text()
                try:
                    commit_num = MODE.findall(scope)[0]
                except:
                    commit_num = 0
                answers.append((support_num, commit_num, question, ans))
            if len(answers) >= count:
                return
            next_page = get_next(soup, start_url)
            if next_page != None:
                crawl(next_page)
        crawl(start_url)
        return answers[:count]

    def get_articles(self, count=MAX_COUNT):
        """获取用户的专栏文章
        :param int count: 获取数，不填代表获取全部
        :return: 该用户的文章
        :rtype: list (title, content)
        """
        start_url = "https://www.zhihu.com/people/%s/posts" % self.__id
        articles = []

        def crawl(url):
            soup = get_soup(url)
            for article in soup.find_all("div", {"class": "zm-profile-section-item zm-item clearfix"}):
                title = article.find("h2").get_text()
                raw_content = article.find(
                    "div", {"class": "zh-summary summary clearfix"}).get_text()
                content = raw_content.replace(
                    "\n", "").replace("显示全部", "")[:40]

                if not content:
                    content = "NO"
                articles.append((title, content))
            if len(articles) >= count:
                return
            next_page = get_next(soup, start_url)
            if next_page != None:
                crawl(next_page)
        crawl(start_url)
        return articles[:count]
