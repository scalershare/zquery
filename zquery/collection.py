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

from .utils import get_soup, headers, get_next
from .error import UrlException


# 最大获取数，默认10000，代表全部。
MAX_COUNT = 10000

class Collection(object):
    def __init__(self, url):
        self.__url = url
        if "?" in self.__url or "http" not in self.__url:
            raise UrlException
        self.__id = self.__url.split("/")[4]
        self.__soup = get_soup(self.__url)
    
    @property
    def url(self):
        return self.__url

    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        raw_title = self.__soup.find("h2", {"class": "zm-item-title zm-editable-content"}).get_text()
        title = raw_title.replace("\n", "").replace(" ", "")
        return title
    
    @property
    def description(self):
        raw_des = self.__soup.find("div", {"class": "zm-editable-content"}).get_text()
        des = raw_des.replace("\n", "").replace(" ", "")
        return des

    @property
    def creator(self):
        raw_creator = self.__soup.find("h2", {"class": "zm-list-content-title"}).get_text()
        creator = raw_creator.replace("\n", "").replace(" ", "")
        return creator

    @property
    def creator_des(self):
        try:
            raw_des = self.__soup.find("div", {"class": "summary-wrapper summary-wrapper--short"}).get_text()
            des = raw_des.replace("\n", "").replace(" ", "")
        except:
            des = "No description"
        return des

    def get_questions(self, count=MAX_COUNT):
        start_url = self.__url
        questions = []
        def crawl(url):
            soup = get_soup(url)
            scope = soup.find_all("div", {"class": "zm-item", "data-type": "Answer"})
            for question in scope:
                title_scope = question.find("h2", {"class": "zm-item-title"})
                div = title_scope.find("a")
                title = div.get_text().replace("\n", "").replace(" ", "")
                url = "https://www.zhihu.com" + div.attrs['href']
                questions.append((title, url))
            if len(questions) >= count:
                return
            next_page = get_next(soup, start_url)
            if next_page != None:
                crawl(next_page)

        crawl(start_url)
        return questions[:count]

if __name__ == "__main__":
    c = Collection("http://www.zhihu.com/collection/20278142")
    print(c.title)
    print(c.description)
    print(c.creator)
    print(c.creator_des)
    print(len(c.get_questions()))
    
