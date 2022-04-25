from flask import Flask
from sqlalchemy import Column, Integer, String
from db import Base


class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    last_ip = Column(String)
    last_time = Column(Integer)
    create_time = Column(Integer)
