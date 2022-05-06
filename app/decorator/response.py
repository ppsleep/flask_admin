from flask import jsonify
from sqlalchemy.orm import class_mapper
import functools
from lib.db import Base


def response(fn):
    @functools.wraps(fn)
    def json(*args, **kwargs):
        data = fn(*args, **kwargs)
        resp = {
            "status": 0,
            "data": data
        }
        if data == 0:
            resp["data"] = ""
        elif isinstance(data, str):
            resp["status"] = 1
        elif isinstance(data, Base):
            resp["data"] = json_orm_data(data)
        return jsonify(resp)

    return json


def json_orm_data(data):
    resp = {}
    for i in data.__dict__:
        if i == "_sa_instance_state":
            continue
        item = getattr(data, i)

        if isinstance(item, Base):
            item = json_orm_data(item)
        elif isinstance(item, (list, tuple)):
            item = [json_orm_data(n) for n in item]

        resp[i] = item
    return resp
