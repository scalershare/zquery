from utils import get_xsrf, get_captcha, headers
import requests
import re

def login(session, secret, account):
    """
    通过输入的用户名判断是否是手机号。
    """
    if re.match(r"^1\d{10}$", account):
        print("Phone login \n")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(session),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print("E-mail login \n")
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(session),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)
        print(login_page.status)
        print(login_page.text)
    except:
        # 需要输入验证码后才能登录成功
        postdata["captcha"] = get_captcha(session)
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = eval(login_page.text)
        print(login_code['msg'])


if __name__ == '__main__':
    """
    测试。
    """
    session = requests.session()
    account = input('Please input your account\n>  ')
    secret = input("input your secret\n>  ")
    login(session, secret, account)
