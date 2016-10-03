from utils import headers
import requests

class Post(object):

    def __init__(self, url):
        self.__url = url
        self.__id = self.__url.split("/")[4]
        self.__api = "https://zhuanlan.zhihu.com/api/posts/" + self.__id   
        r = requests.get(self.__api, headers=headers)
        self.__json_data = r.json()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        return self.__json_data['title']
    
    @property
    def author(self):
        return self.__json_data['author']['name']
    
    @property
    def author_des(self):
        try:
            return self.__json_data['author']['badge']['identity']['description']
        except:
            return None
    
    @property
    def summary(self):
        return self.__json_data['summary']
    
    @property
    def content(self):
        return self.__json_data['content']


if __name__ == "__main__":
    p = Post("https://zhuanlan.zhihu.com/p/22206302")
    print(p.id)
    
    print(p.author)
    print(p.author_des)
    print(p.content)
    
