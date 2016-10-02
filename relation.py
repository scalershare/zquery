from bs4 import BeautifulSoup
from login import login, headers, get_xsrf
from utils import get_soup
import requests
import lxml
import re


def get_hash_id(user):
    url = 'https://www.zhihu.com/people/' + user
    soup = get_soup(url)
    button = soup.find("button", {"data-follow": "m:button"})
    return button.attrs['data-id']


def get_followees(user, account, secret):
    s = requests.Session()
    login(s, secret, account)
    _xsrf = get_xsrf(s)

    url = 'https://www.zhihu.com/people/%s/followees' % user
    hash_id = get_hash_id(user)
    api_url = "https://www.zhihu.com/node/ProfileFolloweesListV2"

    followees = []
    html = s.get(url, headers=headers)
    bsobj = BeautifulSoup(html.text, "lxml")
    _followee_count = bsobj.find("a", {"class": "item", "href": re.compile(
        "followees")}).find("strong").get_text()
    followee_count = int(_followee_count)
    init_followees = []
    for i in bsobj.find_all("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"}):
        user = i.find("h2", {"class": "zm-list-content-title"}
                      ).get_text().replace("\n", "")
        init_followees.append(user)
    followees.extend(init_followees)
    for i in range(20, followee_count - 21, 20):
        form_data = {"_xsrf": _xsrf, "method": "next", "params": {
            "offset": i, "order_by": "created", "hash_id": hash_id}}
        page = s.post(api_url, data=form_data, headers=headers)
        print(page.text)

    return followees


if __name__ == "__main__":
    print(get_followees("excited-vczh", "18864802759", "xxttvv123"))
