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


class Question(object):
    """
    问题类，提供问题操作的API
    """

    def __init__(self, url):
        """初始化

        :param str url: 问题的网址
        :return: question动态对象


        注: 对传入的URL会进行检测，如果错误会抛出UrlException。
        """
        self.__url = url
        if "http" not in self.__url:
            raise UrlException
        self.__id = self.__url.split("/")[4]
        self.__soup = get_soup(self.__url)

    @property
    def url(self):
        """
        :return: 问题的地址
        :rtype: str
        """
        return self.__url

    @property
    def id(self):
        """
        :return: 问题的ID
        :rtype: str
        """
        return self.__id

    @property
    def title(self):
        """
        :return: 问题的标题
        :rtype: str
        """
        title = self.__soup.find("h2", {"class": "zm-item-title"}).get_text()
        return title.replace("\n", "")

    @property
    def detail(self):
        """
        :return: 问题的描述
        :rtype: str
        """
        detail = self.__soup.find(
            "div", {"class": "zm-editable-content"}).get_text()
        return detail.replace("\n", " ").replace(" ", "")

    @property
    def ans_num(self):
        """返回一个问题的答案数量

        :return: 答案数
        :rtype: str

        注: 这里的返回值使用了str代替int，因为网页会根据回答数的不同，自动调整HTML的结构，当
            回答数很少时，不会显示。所以当回答数量很少时，用“less”来代替。

        """
        try:
            _ans_num = self.__soup.find(
                "h3", {"id": "zh-question-answer-num"}).get_text()
            ans_num = str(MODE.findall(_ans_num)[0])
        except:
            ans_num = "less"
        return ans_num

    @property
    def tags(self):
        """
        :return: 问题的标签
        :rtype: list 
        """
        tag_list = self.__soup.find(
            "div", {"class": "zm-tag-editor-labels zg-clear"})
        tags = []
        for tag in tag_list.find_all("a", {"class": "zm-item-tag"}):
            _tag = tag.get_text().replace("\n", "").replace(" ", "")
            tags.append(_tag)
        return tags

    @property
    def follower_num(self):
        """
        :return: 关注问题的人数
        :rtype: int
        """
        scope = self.__soup.find(
            "div", {"class": "zm-side-section-inner zg-gray-normal"}).get_text()
        follower_num = str(MODE.findall(scope)[0])
        return follower_num

    def get_answer_urls(self):
        """获取答案的URL

        :yield: 答案的url
        :rtype: str

        注: 这里只能获取第一页的答案URL，要想获取全部的答案，需要进行登录操作。与登录后有关的API，请
            使用Client类。

        """
        for answer in self.__soup.find_all("div", {"class": "zm-item-answer  zm-item-expanded"}):
            answer_url = self.__url + "/answer/" + answer.attrs['data-atoken']
            yield answer_url


if __name__ == "__main__":
    q = Question("https://www.zhihu.com/question/27621722")
    print(q.title)
    print(q.detail)
    print(q.ans_num)
    print(q.tags)
    print(q.follower_num)
    for i in q.get_answer_urls():
        print(i)
