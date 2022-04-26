from sqlalchemy import Column, Integer, String
from lib.db import Base


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)
