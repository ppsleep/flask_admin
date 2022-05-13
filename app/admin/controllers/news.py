from flask import Blueprint, request
from lib.db import session
from app.models.Page import Page
from app.models.News import News as NewsModel
from app.models.Tags import Tags
from app.models.NewsTag import NewsTag
from app.decorator import response
from app.decorator import validation
import time

news = Blueprint("news", __name__)


class News():

    @news.route("/", methods=["POST"])
    @response
    def index():
        post = request.get_json()
        page = Page(NewsModel)
        author = post.get("author", "")
        title = post.get("title", "")
        tag = post.get("tag", "")
        if author != "":
            page.where(NewsModel.author == author)
        if title != "":
            page.like(NewsModel.title, title)
        if tag != "":
            tags = session.query(Tags).where(Tags.name == tag).first()
            if tags is None:
                return []
            page.join(
                NewsTag,
                NewsModel.id == NewsTag.news_id
            ).where(NewsTag.tag_id == tags.id)
        data = page.get()
        return data

    @news.route("/view/", methods=["POST"])
    @response
    def view():
        post = request.get_json()
        id = post.get("id", "")
        if id != "" and str(post["id"]).isdigit():
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
            news.tags = [i.name for i in tags]
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
    @validation
    def post():
        data = request.get_json()
        newsData = {
            "title": data["title"],
            "uid": request.user["id"],
            "author": data["author"],
            "content": data["content"],
            "updatetime": 0,
            "posttime": int(time.time())
        }

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
            id = data.get("id", "")
            if id != "":
                newsObj = session.query(NewsModel).where(
                    NewsModel.id == id
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
        finally:
            session.close()
        return 0
