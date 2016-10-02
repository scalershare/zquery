from utils import get_soup
import re


def get_Base_info(user):
    start_url = "https://www.zhihu.com/people/" + user
    soup = get_soup(start_url)
    # 对于没有followees的用户来说，没有此标签。
    try:
        followees = soup.find("a", {"class": "item", "href": re.compile(
            "followees")}).find("strong").get_text()
    except AttributeError:
        followees = "0"

    # 对于没有followers的用户来说，没有此标签。
    try:
        followers = soup.find("a", {"class": "item", "href": re.compile(
            "followers")}).find("strong").get_text()
    except AttributeError:
        followers = "0"

    # 如果没有Name，说明爬虫已经被Ban（爬虫被Ban时，不会显示403错误，而是打开另一个网页），此时抛出异常，结束爬虫。
    name = soup.find("div", {"class": "title-section"}
                     ).find("span", {"class": "name"}).get_text()

    try:
        presentation = soup.find("div", {"class": "bio ellipsis"}).get_text()
    except AttributeError:
        presentation = "NODATA"

    try:
        items = soup.find("div", {"class": "items"})
    except AttributeError:
        data = {
            "Name": "NODATA",
            "Presentation": "NODATA",
            "Location_item": "NODATA",
            "Business_item": "NODATA",
            "Employment_item": "NODATA",
            "Position_item": "NODATA",
            "Education_item": "NODATA",
            "Education_extra_item": "NODATA",
            "Followees": followees,
            "Followers": followers,
        }
        return data

    try:
        location_item = items.find(
            "span", {"class": "location item"}).get_text()
    except AttributeError:
        location_item = "NODATA"
    try:
        business_item = items.find(
            "span", {"class": "business item"}).get_text()
    except AttributeError:
        business_item = "NODATA"
    try:
        employment_item = items.find(
            "span", {"class": "employment item"}).get_text()
    except AttributeError:
        employment_item = "NODATA"
    try:
        position_item = items.find(
            "span", {"class": "position item"}).get_text()
    except AttributeError:
        position_item = "NODATA"
    try:
        education_item = items.find(
            "span", {"class": "education item"}).get_text()
    except AttributeError:
        education_item = "NODATA"
    try:
        education_extra_item = items.find(
            "span", {"class": "education-extra item"}).get_text()
    except AttributeError:
        education_extra_item = "NODATA"

    data = {
        "Name": name,
        "Presentation": presentation,
        "Location_item": location_item,
        "Business_item": business_item,
        "Employment_item": employment_item,
        "Position_item": position_item,
        "Education_item": education_item,
        "Education_extra_item": education_extra_item,
        "Followees": followees,
        "Followers": followers,
    }

    return data


def pprint_base(user):
    print("---------------------------------------")
    data = get_Base_info(user)
    datalist = list(data.items())
    for i in datalist:
        print("%s: %s" % (i[0], i[1]))
    print("---------------------------------------")

if __name__ == "__main__":
    pprint_base("excited-vczh")
