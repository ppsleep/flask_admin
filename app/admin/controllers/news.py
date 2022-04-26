from flask import Blueprint, request
from lib.db import session
from lib.msg import Msg
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.Admins import Admins
from app.admin.validator.news import Post

news = Blueprint("news", __name__)


class News():
    @news.route("/", methods=["POST"])
    def index():
        return "index"

    @news.route("/post/", methods=["POST"])
    def post():
        data = request.get_json()
        v = Post.from_json(data)
        if not v.validate():
            return Msg.json(1, v.errors[next(iter(v.errors))][0])
        return Msg.json(0)

    @news.route("/del/", methods=["POST"])
    def delete():
        return "post"
