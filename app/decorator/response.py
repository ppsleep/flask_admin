import string
from flask import jsonify
import functools


def response(fn):
    @functools.wraps(fn)
    def json(*args, **kwargs):
        data = fn(*args, **kwargs)
        if isinstance(data, int):
            data = str(data)
            return jsonify({
                "status": 0,
                "data": ""
            })
        elif isinstance(data, str):
            return jsonify({
                "status": 1,
                "data": data
            })
        return jsonify({
            "status": 0,
            "data": data
        })

    return json
