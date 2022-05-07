from flask import jsonify
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
        else:
            resp["data"] = check_data(data)

        return jsonify(resp)

    return json


def check_data(data):
    if isinstance(data, dict):
        data = check_dict_data(data)
    elif isinstance(data, (list, tuple)):
        data = check_list_data(data)
    elif isinstance(data, Base):
        data = json_orm_data(data)
    return data


def check_dict_data(data):
    for i in data:
        data[i] = check_data(data[i])
    return data


def check_list_data(data):
    return [check_data(i) for i in data]


def json_orm_data(data):
    if not isinstance(data, Base):
        return data
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
