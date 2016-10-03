from prettytable import PrettyTable
from utils import get_soup, get_next, MODE
import re

MAX_COUNT = 10000


def get_answers(user, count=MAX_COUNT):
    start_url = "https://www.zhihu.com/people/%s/answers" % user
    answers = []

    def crawl(url):
        soup = get_soup(url)
        for answer in soup.find_all("div", {"class": "zm-item"}):
            question = answer.find("h2").get_text().replace("\n","")
            raw_ans = answer.find("div", {"class": "zh-summary summary clearfix"}).get_text()
            ans = raw_ans.replace("\n","").replace("显示全部", "")[:30]
            support_num = answer.find("a", {"class": "zm-item-vote-count js-expand js-vote-count"}).get_text()
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

def pprint_answer(user, count=MAX_COUNT):
    row = PrettyTable(["ID", "Support num", "Commit num", "Question", "Answer"])
    row.align["Support num"] = "l"
    row.align["Commit num"] = "l"
    row.align["Question"] = "l"
    row.align["Answer"] = "l"
    answers = get_answers(user, count)
    row.padding_width = 1
    i = 0
    for answer in answers:
        record = list(answer)
        record.insert(0, i)
        row.add_row(record)      
        i += 1
    print(row)

if __name__ == "__main__":
    pprint_answer("excited-vczh", 40)