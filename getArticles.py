from prettytable import PrettyTable
from utils import get_soup, get_next

MAX_COUNT = 10000


def get_articles(user, count=MAX_COUNT):
    start_url = "https://www.zhihu.com/people/%s/posts" % user
    articles = []

    def crawl(url):
        soup = get_soup(url)
        article_scope = soup.find("div", {"class": "zm-profile-section-wrap zm-profile-post-page"})
        for article in article_scope.find_all("div", {"class": "zm-profile-section-item zm-item clearfix"}):
            title = article.find("h2").get_text()

            raw_content = article.find("div", {"class": "zh-summary summary clearfix"}).get_text()
            content = raw_content.replace("\n", "").replace("显示全部", "")[:45]

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

def pprint_article(user, count=MAX_COUNT):
    row = PrettyTable(["ID", "Title", "Summary"])
    row.align["Title"] = "l"
    row.align["Summary"] = "l"
    articles = get_articles(user, count)
    row.padding_width = 1
    i = 0
    for article in articles:
        record = list(article)
        record.insert(0, i)
        row.add_row(record)      
        i += 1
    print(row)


if __name__ == "__main__":
    pprint_article("excited-vczh", 30)

