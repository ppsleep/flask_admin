from lib.db import session
from flask import request
from sqlalchemy.future import select


class Page:
    def __init__(self, model):
        self.__stmt = select(model.__table__).order_by(model.id.desc())
        self.__count = session.query(model)
        self.__page = 1
        self.__limit = 10

    def get(self):
        count = self.__count.count()
        self.__stmt = self.__stmt.limit(self.__limit).offset(
            self.__offset()
        )
        results = session.execute(self.__stmt).mappings()
        data = []
        for row in results:
            data.append(dict(row))
        return {
            "data": data,
            "page": self.__page,
            "total": count,
        }

    def all(self):
        results = session.execute(self.__stmt).mappings()
        data = []
        for row in results:
            data.append(dict(row))
        return data

    def select_from(self, model):
        self.__stmt = self.__stmt.select_from(model.__table__)
        return self

    def join(self, model, where):
        self.__stmt = self.__stmt.join(model, where)
        return self

    def where(self, where):
        self.__stmt = self.__stmt.where(where)
        self.__count = self.__count.where(where)
        return self

    def filter_by(self, where):
        self.__stmt = self.__stmt.filter_by(**where)
        self.__count = self.__count.filter_by(**where)
        return self

    def like(self, field, value):
        self.__stmt = self.__stmt.filter(field.like(f"%{value}%"))
        return self

    def limit(self, limit):
        self.__limit = int(limit)
        return self

    def __offset(self):
        post = request.get_json()
        if "page" in post:
            if str(post["page"]).isdigit():
                p = int(post["page"])
                self.__page = p if p > 0 else 1
        return (self.__page - 1) * self.__limit
