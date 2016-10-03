from utils import get_soup, MODE

class Question(object):

    def __init__(self, id):
        self.id = id
        self.url = 'https://www.zhihu.com/question/' + self.id
        self.soup = get_soup(self.url)
    
    @property
    def title(self):
        title = self.soup.find("h2", {"class": "zm-item-title"}).get_text()
        return title.replace("\n", "")
    
    @property
    def detail(self):
        detail = self.soup.find("div", {"class": "zm-editable-content"}).get_text()
        return detail

    
    @property
    def ans_num(self):
        _ans_num = self.soup.find("h3", {"id":"zh-question-answer-num"}).get_text()
        ans_num = int(MODE.findall(_ans_num)[0])
        return ans_num
    
    @property
    def tags(self):
        tag_list = self.soup.find("div", {"class": "zm-tag-editor-labels zg-clear"})
        tags = []
        for tag in tag_list.find_all("a", {"class": "zm-item-tag"}):
            _tag = tag.get_text().replace("\n", "").replace(" ", "")
            tags.append(_tag)
        return tags
    
    @property
    def follower_num(self):
        scope = self.soup.find("div", {"class": "zm-side-section-inner zg-gray-normal"}).get_text()
        follower_num = int(MODE.findall(scope)[0])
        return follower_num
    
    def get_answer_urls(self):
        for answer in self.soup.find_all("div", {"class": "zm-item-answer  zm-item-expanded"}):
            answer_url = self.url + "/answer/" + answer.attrs['data-atoken']
            yield answer_url
    
    def get_answers(self):
        for url in self.get_answer_urls():
            yield Answer(url)

class Answer(object):

    def __init__(self, arg1=None, arg2=None):
        if arg2 == None:
            self.url = arg1
            temp = MODE.findall(self.url)
            self.question_id = temp[0]
            self.id = temp[1]
        else:
            self.question_id = arg1
            self.id = arg2
            self.url = 'https://www.zhihu.com/question/{0}/answer/{1}'.format(self.question_id, self.id)
        self.soup = get_soup(self.url)
        self.anonymous = False
    def get_question():
        return Question(self.question_id)
    
    @property
    def author(self):
        
        if self.anonymous:
            return "匿名用户"
        scope = self.soup.find("div", {"class": "zm-item-answer-author-info"})
        try:
            author_name = scope.find("span", {"class": "author-link-line"})
            return author_name.get_text().replace("\n", "")
        except:
            self.anonymous = True
            return "匿名用户"
    
    @property
    def support_count(self):
        scope = self.soup.find("button", {"class": "up"})
        count = scope.find("span", {"class": "count"}).get_text()
        return int(count)

    @property
    def author_bio(self):
        if self.anonymous:
            return "匿名用户"
        scope = self.soup.find("div", {"class": "zm-item-answer-author-info"})
        try:
            bio = scope.find("span", {"class": "bio"})
            return bio.get_text().replace("\n", "")
        except:
            self.anonymous = True
            return "匿名用户"

    @property
    def modify_date(self):
        date = self.soup.find("a", {"class": "answer-date-link meta-item"}).get_text()
        return date
    
    @property
    def content(self):
        content = self.soup.find("div", {"class": "zm-editable-content clearfix"}).get_text()
        return content.replace("\n", "")

if __name__ == "__main__":
    q = Question("27621722")
    print(q.title)
    print(q.detail)
    print(q.ans_num)
    print(q.tags)
    print(q.follower_num)
    for i in q.get_answer_urls():
        print(i)
    
    a = Answer("https://www.zhihu.com/question/36661957/answer/71253554")
    print(a.author)
    print(a.author_bio)
    print(a.support_count)
    print(a.modify_date)
    print(a.content)
        
        
        