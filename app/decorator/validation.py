from flask import request
import functools
import importlib


def validation(fn):
    @functools.wraps(fn)
    def check(*args, **kwargs):
        name = fn.__qualname__.split(".")
        path = "app.admin.validator." + name[0].lower()
        validator = importlib.import_module(path)
        data = request.get_json()
        v = getattr(validator, name[1].title()).from_json(data)
        if not v.validate():
            return v.errors[next(iter(v.errors))][0]

        data = fn(*args, **kwargs)
        return data

    return check
