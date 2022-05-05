from sqlalchemy import Column, Integer
from lib.db import Base


class NewsTag(Base):
    __tablename__ = 'news_tags'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer)
    tag_id = Column(Integer)
