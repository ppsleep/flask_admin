from lib.db import session
from flask import request


class Page:
    def __init__(self, model):
        self.__stmt = session.query(model).order_by(model.id.desc())
        self.__page = 1
        self.__limit = 10

    def get(self):
        count = self.__stmt.count()
        self.__stmt = self.__stmt.limit(self.__limit).offset(
            self.__offset()
        )
        results = self.__stmt.all()
        session.close()
        return {
            "data": results,
            "page": self.__page,
            "total": count,
        }

    def all(self):
        data = self.__stmt.all()
        session.close()
        return data

    def select_from(self, model):
        self.__stmt = self.__stmt.select_from(model)
        return self

    def join(self, model, where):
        self.__stmt = self.__stmt.join(
            model, where
        )
        return self

    def where(self, where):
        self.__stmt = self.__stmt.where(where)
        return self

    def filter_by(self, where):
        self.__stmt = self.__stmt.filter_by(**where)
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
