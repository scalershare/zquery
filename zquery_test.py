from zquery import Question, Answer, Post, Column, Collection

q = Question("https://www.zhihu.com/question/51298741")
a = Answer("https://www.zhihu.com/question/51252716/answer/124894917")
p = Post("https://zhuanlan.zhihu.com/p/22551537")
c = Column("https://zhuanlan.zhihu.com/vczh-nichijou")

print(q.title)
print(a.content)
print(p.summary)
print(c.title)

c = Collection("http://www.zhihu.com/collection/20278142")
print(c.title)
print(c.description)
print(c.creator)
print(c.creator_des)
print(len(c.get_questions()))