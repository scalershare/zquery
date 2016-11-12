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

from .utils import get_soup, MODE
from .error import UrlException
from .question import Question


class Answer(object):
    """
    答案类，提供关于问题答案的操作API
    """

    def __init__(self, arg1=None, arg2=None, *args, **kwargs):
        """初始化

        :param str arg1: URL or 问题ID
        :param str arg2: None or 答案ID
        :return: answer动态对象


        注: 1.这里提供了两种构造方式，一种是通过传入URL构造，这事arg2为空，另一种是
            通过传入问题ID和答案ID来构造，这是arg1是问题ID，arg2是答案的ID。
            2.对传入的URL会进行检测，如果错误会抛出UrlException。
        """
        if arg2 == None:
            self.__url = arg1
            temp = MODE.findall(self.__url)
            self.__question_id = temp[0]
            self.__id = temp[1]
        else:
            self.__question_id = arg1
            self.__id = arg2
            self.__url = 'https://www.zhihu.com/question/{0}/answer/{1}'.format(
                self.__question_id, self.__id)

        if "http" not in self.__url:
            raise UrlException
        self.__soup = get_soup(self.__url)
        self.__anonymous = False

    def get_question(self):
        """将该解答的原问题返回

        :return: 原问题
        :rtype: Question
        """
        return Question(self.__question_id)

    @property
    def url(self):
        """
        :return: 答案的URL
        :rtype: str
        """
        return self.__url

    @property
    def id(self):
        """
        :return: 答案的ID 
        :rtype: str
        """
        return self.__id

    @property
    def author(self):
        """返回答案的作者

        :return: 答主
        :rtype: str

        注: 如果找不到作者，则返回“匿名用户”。

        """
        if self.__anonymous:
            return "匿名用户"
        scope = self.__soup.find(
            "div", {"class": "zm-item-answer-author-info"})
        try:
            author_name = scope.find("span", {"class": "author-link-line"})
            return author_name.get_text().replace("\n", "")
        except:
            self.__anonymous = True
            return "匿名用户"

    @property
    def support_count(self):
        """
        :return: 答案赞同者的数目
        :rtype: int
        """
        scope = self.__soup.find("button", {"class": "up"})
        count = scope.find("span", {"class": "count"}).get_text()
        return int(count)

    @property
    def author_bio(self):
        """
        :return: 答主的bio
        :rtype: str
        """
        if self.__anonymous:
            return "匿名用户"
        scope = self.__soup.find(
            "div", {"class": "zm-item-answer-author-info"})
        try:
            bio = scope.find("span", {"class": "bio"})
            return bio.get_text().replace("\n", "")
        except:
            self.__anonymous = True
            return "匿名用户"

    @property
    def modify_date(self):
        """
        :return: 答案最近修改的时间
        :rtype: str
        """
        date = self.__soup.find(
            "a", {"class": "answer-date-link meta-item"}).get_text()
        return date

    @property
    def content(self):
        """
        :return: 答案的内容
        :rtype: str
        """
        content = self.__soup.find(
            "div", {"class": "zm-editable-content clearfix"}).get_text()
        return content.replace("\n", "")


if __name__ == "__main__":
    a = Answer("https://www.zhihu.com/question/36661957/answer/71253554")
    print(a.author)
    print(a.author_bio)
    print(a.support_count)
    print(a.modify_date)
    print(a.content)
