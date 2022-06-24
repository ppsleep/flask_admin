from flask import Blueprint, request
from lib.db import session
from app.models.Page import Page
from app.models.Pages import Pages as PagesModel
from app.decorator import response
from app.decorator import validation
import time

pages = Blueprint("pages", __name__)


class Pages():

    @pages.route("/", methods=["POST"])
    @response
    def index():
        page = Page(PagesModel)
        data = page.all()
        return data

    @pages.route("/view/", methods=["POST"])
    @response
    def view():
        post = request.get_json()
        id = post.get("id", "")
        if id != "" and str(post["id"]).isdigit():
            data = session.query(PagesModel).filter(
                PagesModel.id == post["id"]
            ).first()
            if data == None:
                return "Data does not exist"

            return data
        return "Data does not exist"

    @pages.route("/del/", methods=["POST"])
    @response
    def pageDelete():
        post = request.get_json()
        if "id" in post and str(post["id"]).isdigit():
            pageObj = session.query(PagesModel).where(
                PagesModel.id == post["id"]
            )
            if pageObj.first() == None:
                return "Data does not exist"
            pageObj.delete()
            session.commit()
            return 0
        return "Data does not exist"

    @pages.route("/post/", methods=["POST"])
    @response
    @validation
    def post():
        data = request.get_json()
        pageData = {
            "title": data["title"],
            "url": data["url"],
            "content": data["content"],
            "updatetime": 0,
            "posttime": int(time.time())
        }

        id = data.get("id", "")
        if id != "":
            pageObj = session.query(PagesModel).where(
                PagesModel.id == id
            )
            data = pageObj.first()
            if data == None:
                return "Data does not exist"
            del(pageData["posttime"])
            pageData["updatetime"] = int(time.time())
            pageObj.update(pageData)
            id = data.id
        else:
            pagesModel = PagesModel(**pageData)
            session.add(pagesModel)

        session.commit()
        return 0
