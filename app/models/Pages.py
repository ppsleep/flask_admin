from sqlalchemy import Column, Integer, String
from lib.db import Base


class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    content = Column(String)
    updatetime = Column(Integer)
    posttime = Column(Integer)
