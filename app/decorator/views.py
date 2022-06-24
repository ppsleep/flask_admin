from flask import render_template, current_app
import functools


def render(fn):
    @functools.wraps(fn)
    def html(*args, **kwargs):
        data = fn(*args, **kwargs)
        name = fn.__qualname__.lower().split(".")
        view = "index/views/" + name[0] + "/" + name[1] + ".html"
        return render_template(view, data=data)

    return html
