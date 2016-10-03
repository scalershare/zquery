from utils import get_soup, headers
import requests
import json
import re

MAX_COUNT = 10000

class Column(object):

    def __init__(self, url):
        self.__url = url
        self.__id = self.__url.split("/")[3]
        self.__api = "https://zhuanlan.zhihu.com/api/columns/" + self.__id   
        r = requests.get(self.__api, headers=headers)
        self.__json_data = r.json()

    @property
    def url(self):
        return self.__url
    
    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        return self.__json_data['name']
    
    @property
    def description(self):
        return self.__json_data['description']
    
    @property
    def followers_count(self):
        return self.__json_data['followersCount'] 

    @property
    def tags(self):
        datas = self.__json_data['postTopics']
        tags = [i['name'] for i in datas]
        return tags
    
    def get_articles(self, count=MAX_COUNT):
        articles = []
        api_1 = "https://zhuanlan.zhihu.com/api/columns/%s/posts?limit=20" % self.__id

        def crawl(api):
            r = requests.get(api, headers=headers)
            datas = r.json()
            for i in datas:
                title = i["title"]
                content = i["content"]
                articles.append((title, content))
        
        crawl(api_1)
        offset = 20
        while True:
            api_2 = api_1 + "&offset=" + str(offset)
            crawl(api_2)
            offset += 20
            
            if len(articles) % 20 or len(articles) > count:
                break

                
        return articles[:count]
        


if __name__ == "__main__":
    c = Column("https://zhuanlan.zhihu.com/he110world")
    print(c.description)
    print(len(c.get_articles(12)))

    
