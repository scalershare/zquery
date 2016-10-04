# Copyright 2016 wisedoge

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .utils import get_xsrf, get_captcha, headers
import requests
import re


def login(session, secret, account):
    """登录
    :param requests.Session session: 网络会话
    :param str secret: 知乎密码
    :param str account: 知乎用户名
    。
    """
    if re.match(r"^1\d{10}$", account):
        print("Phone login")
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(session),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print("E-mail login")
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
        if "登录成功" in login_code['msg']:
            return True
        else:
            return False


if __name__ == '__main__':
    """
    测试。 
    """
    session = requests.session()
    account = input('Please input your account\n>  ')
    secret = input("input your secret\n>  ")
    login(session, secret, account)
