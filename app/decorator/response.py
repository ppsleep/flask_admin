from flask import jsonify
import functools


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
        return jsonify(resp)

    return json
