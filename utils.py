from bs4 import BeautifulSoup
from PIL import Image
import requests
import lxml
import time
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}

MODE = re.compile(r'\d+')

def get_soup(url):
   
    r = requests.get(url, headers=headers)       
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def get_next(soup, init_url):
    next_page = None
    for span in soup.find_all("a"):
        if span.get_text() == "下一页":
            next_page = init_url + span.attrs['href']
            break
    return next_page

def get_hash_id(user):
    url = 'https://www.zhihu.com/people/' + user
    soup = get_soup(url)
    button = soup.find("button", {"data-follow": "m:button"})
    return button.attrs['data-id']

def get_xsrf(session):
    """
    xsrf 是一个动态变化的参数，提交请求时必须提交xsrf，此函数用来获取xsrf。
    """
    index_url = 'http://www.zhihu.com'

    # 获取登录时需要用到的_xsrf
    html = session.get(index_url, headers=headers)
    pattern = r'name="_xsrf" value="(.*?)"'

    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html.text)
    return _xsrf[0]


def get_captcha(session):
    """
    获取验证码。
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)

    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)

    img = Image.open('captcha.jpg')
    img.show()
    img.close()

    captcha = input("please input the captcha\n>")
    return captcha