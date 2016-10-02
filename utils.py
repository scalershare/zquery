from bs4 import BeautifulSoup
import requests
import lxml


def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}
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