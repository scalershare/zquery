from zquery import Question, Answer, Post, Column

q = Question("https://www.zhihu.com/question/51298741")
a = Answer("https://www.zhihu.com/question/51252716/answer/124894917")
p = Post("https://zhuanlan.zhihu.com/p/22551537")
c = Column("https://zhuanlan.zhihu.com/vczh-nichijou")

print(q.title)
print(a.content)
print(p.summary)
print(c.title)