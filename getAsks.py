from prettytable import PrettyTable
from utils import get_soup, get_next
import re

MAX_COUNT = 10000
MODE = re.compile(r'\d+')

def get_asks(user, count=MAX_COUNT):
    start_url = "https://www.zhihu.com/people/%s/asks" % user
    asks = []

    def crawl(url):
        soup = get_soup(url)
        for ask in soup.find_all("div", {"class": "zm-profile-section-item zg-clear"}):
            question = ask.find("h2").get_text().replace("\n","")
            vote_num = ask.find("div", {"class": "zm-profile-vote-num"}).get_text()
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

def pprint_ask(user, count=MAX_COUNT):
    row = PrettyTable(["ID", "Vote num", "Ask num", "Followers", "Question"])
    row.align["Vote num"] = "l"
    row.align["Ask num"] = "l"
    row.align["Followers"] = "l"
    row.align["Question"] = "l"
    asks = get_asks(user, count)
    row.padding_width = 1
    i = 0
    for ask in asks:
        record = list(ask)
        record.insert(0, i)
        row.add_row(record)      
        i += 1
    print(row)

if __name__ == "__main__":
    pprint_ask("excited-vczh", 30)
