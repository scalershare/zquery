from bs4 import BeautifulSoup
from login import login
from utils import get_soup, get_hash_id, get_xsrf
import json
import requests
import lxml
import re

def get_followees(user, account, secret):
    
    s = requests.Session()
    login(s, secret, account)
    _xsrf = get_xsrf(s)

    url = 'https://www.zhihu.com/people/%s/followees' % user
    refer_headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    'Host': "www.zhihu.com",
    'Origin': 'https://www.zhihu.com',
    'Referer': url,
    'X-Requested-With': 'XMLHttpRequest'
    }
    hash_id = get_hash_id(user)
    api_url = "https://www.zhihu.com/node/ProfileFolloweesListV2"

    followees = []
    html = s.get(url, headers=refer_headers)
    bsobj = BeautifulSoup(html.text, "lxml")
    _followee_count = bsobj.find("a", {"class": "item", "href": re.compile(
        "followees")}).find("strong").get_text()
    followee_count = int(_followee_count)
    for i in bsobj.find_all("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"}):
        user = i.find("h2", {"class": "zm-list-content-title"}
                      ).get_text().replace("\n", "")
        followees.append(user)

    for i in range(20, followee_count - 21, 20):
        params = json.dumps({"hash_id":hash_id, "order_by":"created", "offset":i,})
        payload={"method":"next", "params":params, "_xsrf":_xsrf,}

        r = s.post(api_url, data=payload, headers=refer_headers)
        page = r.json()['msg']
        for msg in page:
            soup = BeautifulSoup(msg, "lxml")
            div = soup.find("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"})
            name = div.find("a", {"class":"zg-link author-link"}).attrs['title']
            followees.append(name)
    return followees

def get_followers(user, account, secret):
    
    s = requests.Session()
    login(s, secret, account)
    _xsrf = get_xsrf(s)

    url = 'https://www.zhihu.com/people/%s/followers' % user
    refer_headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    'Host': "www.zhihu.com",
    'Origin': 'https://www.zhihu.com',
    'Referer': url,
    'X-Requested-With': 'XMLHttpRequest'
    }
    hash_id = get_hash_id(user)
    api_url = "https://www.zhihu.com/node/ProfileFollowersListV2"

    followers = []
    html = s.get(url, headers=refer_headers)
    bsobj = BeautifulSoup(html.text, "lxml")
    _follower_count = bsobj.find("a", {"class": "item", "href": re.compile(
        "followers")}).find("strong").get_text()
    follower_count = int(_follower_count)
    for i in bsobj.find_all("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"}):
        user = i.find("h2", {"class": "zm-list-content-title"}
                      ).get_text().replace("\n", "")
        followers.append(user)

    for i in range(20, follower_count - 21, 20):
        params = json.dumps({"hash_id":hash_id, "order_by":"created", "offset":i,})
        payload={"method":"next", "params":params, "_xsrf":_xsrf,}

        r = s.post(api_url, data=payload, headers=refer_headers)
        page = r.json()['msg']
        for msg in page:
            soup = BeautifulSoup(msg, "lxml")
            div = soup.find("div", {"class": "zm-profile-card zm-profile-section-item zg-clear no-hovercard"})
            name = div.find("a", {"class":"zg-link author-link"}).attrs['title']
            print(name)
            followers.append(name)
    return followers


if __name__ == "__main__":
    print(len(get_followers("excited-vczh", "18864802759", "xxttvv123")))
