from flask import Blueprint, request
from lib.db import session
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
            newsObj = session.query(NewsModel).where(
                NewsModel.id == post["id"]
            )
            if newsObj.first() == None:
                return "Data does not exist"
            newsObj.delete()
            session.query(NewsTag).where(
                NewsTag.news_id == post["id"]
            ).delete()
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
            "updatetime": 0,
            "posttime": int(time.time())
        }

        data["tags"] = data["tags"].replace("，", ",").split(",")
        tags = [i.strip() for i in data["tags"] if i.strip() != ""]

        tagsData = session.query(Tags.name).where(Tags.name.in_(tags)).all()
        tagsData = [i[0]for i in tagsData]
        newTags = list(set(tags) - set(tagsData))
        tagsData = [Tags(name=i) for i in newTags]
        session.close()
        session.begin()
        try:
            # insert new tags
            if len(tagsData) > 0:
                session.add_all(tagsData)
                session.flush()
            # get all tags id
            tagsData = session.query(Tags.id).where(Tags.name.in_(tags)).all()
            tagsData = [i[0]for i in tagsData]
            id = 0
            if "id" in data:
                newsObj = session.query(NewsModel).where(
                    NewsModel.id == data["id"]
                )
                news = newsObj.first()
                if news == None:
                    return "Data does not exist"
                del(newsData["posttime"])
                newsData["updatetime"] = int(time.time())
                newsObj.update(newsData)
                id = news.id
                # delete old tags and news link
                session.query(NewsTag).where(
                    NewsTag.news_id == news.id
                ).delete()
                session.flush()
            else:
                newsModel = NewsModel(**newsData)
                session.add(newsModel)
            session.flush()
            id = id if id else newsModel.id

            # add tags and news link
            news_tag = [NewsTag(news_id=id, tag_id=i) for i in tagsData]
            session.add_all(news_tag)
            session.commit()
        except:
            session.rollback()
            return "System error"
        return 0
