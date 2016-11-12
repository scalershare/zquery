from zquery import Question, Answer, Post, Column, Collection
import unittest


class ZqueryTestCase(unittest.TestCase):
    """
    TestCase
    """

    def test_question(self):
        q = Question("https://www.zhihu.com/question/51298741")
        assert q.title != None

    def test_answer(self):
        a = Answer("https://www.zhihu.com/question/51252716/answer/124894917")
        assert a.content != None

    def test_post(self):
        p = Post("https://zhuanlan.zhihu.com/p/22551537")
        assert p.summary != None

    def test_column(self):
        c = Column("https://zhuanlan.zhihu.com/vczh-nichijou")
        assert c.title != None

    def test_col(self):
        c = Collection("http://www.zhihu.com/collection/20278142")
        assert c.title != None

if __name__ == "__main__":
    unittest.main()

