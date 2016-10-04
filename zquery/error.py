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


class UrlException(Exception):
    """
    异常类，如果构造方法的URL错误，则抛出此异常
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("You must provide a valid URL.")


class IdException(Exception):
    """
    异常类，如果构造方法的ID错误，则抛出此异常
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("You must provide a valid id(rather than a url).")


class BanException(Exception):
    """
    异常类，如果爬虫被禁止，则抛出此异常
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("The crawler has been forbidden.")


class UnLoginException(Exception):
    """
    异常类，如果未登陆就进行操作，则抛出此异常
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("You must login before do this.")
