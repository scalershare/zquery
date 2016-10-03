from utils import get_soup, MODE
import re

MAX_COUNT = 10000


class User(object):

    def __init__(self, id):
        self.id = id
        self.url = "https://www.zhihu.com/people/" + self.id
        self.soup = get_soup(self.url)
        self.items = self.soup.find("div", {"class": "items"})

    @property
    def name(self):
        name = self.soup.find("div", {"class": "title-section"}
                              ).find("span", {"class": "name"}).get_text()
        return name

    @property
    def followees(self):
        try:
            followees = self.soup.find("a", {"class": "item", "href": re.compile(
                "followees")}).find("strong").get_text()
        except AttributeError:
            followees = "0"
        return followees

    @property
    def followers(self):
        try:
            followers = self.soup.find("a", {"class": "item", "href": re.compile(
                "followers")}).find("strong").get_text()
        except AttributeError:
            followers = "0"
        return followers
    
    @property
    def agree_num(self):
        scope = self.soup.find("span", {"class": "zm-profile-header-user-agree"})
        agree_num = scope.find("strong").get_text()
        return int(agree_num)
    
    @property
    def thanks_num(self):
        scope = self.soup.find("span", {"class": "zm-profile-header-user-thanks"})
        thanks_num = scope.find("strong").get_text()
        return int(thanks_num)

    @property
    def presentation(self):
        try:
            presentation = self.soup.find(
                "div", {"class": "bio ellipsis"}).get_text()
        except AttributeError:
            presentation = "NODATA"
        return presentation

    @property
    def location_item(self):
        try:
            location_item = self.items.find(
                "span", {"class": "location item"}).get_text()
        except AttributeError:
            location_item = "NODATA"
        return location_item

    @property
    def business_item(self):
        try:
            business_item = self.items.find(
                "span", {"class": "business item"}).get_text()
        except AttributeError:
            business_item = "NODATA"
        return business_item

    @property
    def employment_item(self):
        try:
            employment_item = self.items.find(
                "span", {"class": "employment item"}).get_text()
        except AttributeError:
            employment_item = "NODATA"
        return employment_item

    @property
    def position_item(self):
        try:
            position_item = self.items.find(
                "span", {"class": "position item"}).get_text()
        except AttributeError:
            position_item = "NODATA"
        return position_item

    @property
    def education_item(self):
        try:
            education_item = self.items.find(
                "span", {"class": "education item"}).get_text()
        except AttributeError:
            education_item = "NODATA"
        return education_item

    @property
    def education_extra_item(self):
        try:
            education_extra_item = self.items.find(
                "span", {"class": "education-extra item"}).get_text()
        except AttributeError:
            education_extra_item = "NODATA"
        return education_extra_item

    def get_base_info(self):
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
        start_url = "https://www.zhihu.com/people/%s/asks" % self.id
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
        start_url = "https://www.zhihu.com/people/%s/answers" % self.id
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
                commit_num = MODE.findall(scope)[0]
                answers.append((support_num, commit_num, question, ans))
            if len(answers) >= count:
                return
            next_page = get_next(soup, start_url)
            if next_page != None:
                crawl(next_page)
        crawl(start_url)
        return answers[:count]

    def get_articles(user, count=MAX_COUNT):
        start_url = "https://www.zhihu.com/people/%s/posts" % user
        articles = []

        def crawl(url):
            soup = get_soup(url)
            article_scope = soup.find(
                "div", {"class": "zm-profile-section-wrap zm-profile-post-page"})
            for article in article_scope.find_all("div", {"class": "zm-profile-section-item zm-item clearfix"}):
                title = article.find("h2").get_text()

                raw_content = article.find(
                    "div", {"class": "zh-summary summary clearfix"}).get_text()
                content = raw_content.replace(
                    "\n", "").replace("显示全部", "")[:45]

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


def pprint_base(user):
    print("---------------------------------------")
    data = User(user).get_base_info()
    datalist = list(data.items())
    for i in datalist:
        print("%s: %s" % (i[0], i[1]))
    print("---------------------------------------")

if __name__ == "__main__":
    pprint_base("excited-vczh")
