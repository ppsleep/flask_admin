from flask import Blueprint, request
from lib.db import session
from app.models.Page import Page
from app.models.Tags import Tags as TagsModel
from app.decorator import response
from app.decorator import validation
import time

tags = Blueprint("tags", __name__)


class Tags():

    @tags.route("/list/", methods=["POST"])
    @response
    def list():
        page = Page(TagsModel)
        tags = page.all()
        data = [i.name for i in tags]
        return data
