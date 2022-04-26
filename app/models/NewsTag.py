from sqlalchemy import Column, Integer, String
from lib.db import Base


class NewsTag(Base):
    __tablename__ = 'news_tag'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer)
    tag_id = Column(Integer)