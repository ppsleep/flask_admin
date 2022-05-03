from flask import Blueprint, request
from lib.db import session
from lib.msg import Msg
from sqlalchemy.future import select
from sqlalchemy import exc, insert, update, delete
from app.models.News import News as NewsModel
from app.models.Tags import Tags
from app.models.NewsTag import NewsTag
from app.admin.validator.news import Post
import time

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

        newsData = {
            "title": data["title"],
            "uid": request.user["id"],
            "author": data["author"],
            "content": data["content"],
            "posttime": int(time.time())
        }

        data["tags"] = data["tags"].replace("，", ",").split(",")
        tags = [i.strip() for i in data["tags"] if i.strip() != ""]

        stmt = select(Tags.name).where(Tags.name.in_(tags))
        tagsData = session.execute(stmt).all()
        tagsData = [i[0]for i in tagsData]
        newTags = list(set(tags) - set(tagsData))
        tagsData = []
        for i in newTags:
            tagsData.append({"name": i})

        session.close()
        session.begin()
        try:
            # insert new tags
            if len(tagsData) > 0:
                stmt = insert(Tags).values(
                    tagsData
                )
                session.execute(stmt)
                session.flush()
            # get all tags id
            stmt = select(Tags.id).where(Tags.name.in_(tags))
            tagsData = session.execute(stmt).all()
            tagsData = [i[0]for i in tagsData]
            id = 0
            if "id" in data:
                stmt = select(NewsModel).where(NewsModel.id == data["id"])
                news = session.execute(stmt).scalar()
                if news == None:
                    return Msg.json(1, "Data does not exist")
                del(newsData["posttime"])
                newsData["updatetime"] = int(time.time())
                stmt = update(NewsModel).values(
                    newsData
                ).where(NewsModel.id == news.id)
                id = news.id
                # delete old tags and news link
                stmt = delete(NewsTag).where(NewsTag.news_id == news.id)
                session.execute(stmt)
                session.flush()
            else:
                stmt = insert(NewsModel).values(
                    newsData
                )
            result = session.execute(stmt)
            session.flush()
            id = id if id else result.lastrowid

            # add tags and news link
            news_tag = []
            for i in tagsData:
                news_tag.append({
                    "news_id": id,
                    "tag_id": i,
                })
            stmt = insert(NewsTag).values(
                news_tag
            )
            session.execute(stmt)
            session.commit()
        except:
            session.rollback()
            return Msg.json(1, "System error")
        return Msg.json(0)

    @ news.route("/del/", methods=["POST"])
    def delete():
        return "post"
