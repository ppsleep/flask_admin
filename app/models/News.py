from sqlalchemy import Column, Integer, String
from lib.db import Base


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    author = Column(String)
    title = Column(String)
    content = Column(String)
    updatetime = Column(Integer)
    posttime = Column(Integer)


# def __repr__(self):
#     return f"News(id={self.id!r}, uid={self.uid!r}, author={self.author!r}), title={self.title!r}"
