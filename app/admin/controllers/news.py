from hashlib import new
from flask import Blueprint, request
from lib.db import session
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from app.models.Page import Page
from app.models.News import News as NewsModel
from app.models.Tags import Tags
from app.models.NewsTag import NewsTag
from app.admin.validator.news import Post
from app.decorator import response
import time

news = Blueprint("news", __name__)


class News():

    @news.route("/", methods=["POST"])
    @response
    def index():
        post = request.get_json()
        page = Page(NewsModel)
        author = post.get("author", "")
        if author != "":
            page.where(NewsModel.author == author)
        if "title" in post and post["title"] != "":
            page.like(NewsModel.title, post["title"])
        data = page.get()
        return data

    @news.route("/view/", methods=["POST"])
    @response
    def view():
        post = request.get_json()
        if "id" in post and str(post["id"]).isdigit():
            news = session.query(NewsModel).filter(
                NewsModel.id == post["id"]
            ).first()
            if news == None:
                return "Data does not exist"

            tags = session.query(Tags).select_from(
                NewsTag
            ).join(
                Tags, NewsTag.tag_id == Tags.id
            ).where(
                NewsTag.news_id == post["id"]
            ).all()

            news.tags = tags
            return news
        return "Data does not exist"

    @news.route("/del/", methods=["POST"])
    @response
    def newsDelete():
        post = request.get_json()
        if "id" in post and str(post["id"]).isdigit():
            stmt = select(NewsModel.__table__).where(
                NewsModel.id == post["id"])

            news = session.execute(stmt).first()
            if news == None:
                return "Data does not exist"
            stmt = delete(NewsModel).where(NewsModel.id == post["id"])
            session.execute(stmt)
            session.commit()
            return 0
        return "Data does not exist"

    @news.route("/post/", methods=["POST"])
    @response
    def post():
        data = request.get_json()
        v = Post.from_json(data)
        if not v.validate():
            return v.errors[next(iter(v.errors))][0]

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
                    return "Data does not exist"
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
            return "System error"
        return 0
