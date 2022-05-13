from distutils.command.upload import upload
from flask import Blueprint, request, current_app
from lib.db import session
from app.models.Page import Page
from app.models.Tags import Tags as TagsModel
from app.decorator import response
import puremagic
import base64
import time
import os
import random
import traceback

upload = Blueprint("upload", __name__)


class Upload():

    @upload.route("/pic/", methods=["POST"])
    @response
    def pic():
        post = request.get_json()
        data = post.get("data", "").partition(";base64,")[2]
        if data == "":
            return "Please upload file"
        data = base64.b64decode(data)
        try:
            ext = puremagic.from_string(data)
        except:
            return "Unsupported file type"
        if ext == ".jfif":
            ext = ".jpg"
        if ext not in [".jpg", ".gif", ".png"]:
            return "Unsupported file type"
        date = time.strftime("%Y%m", time.localtime())
        dir = date + "/"
        path = current_app.config["UP_PATH"] + dir
        if not os.path.isdir(path):
            os.mkdir(path)
        filename = dir + \
            str(int(time.clock_gettime_ns(time.CLOCK_REALTIME) / 1000)) + \
            str(random.randint(10, 90)) + \
            ext
        filepath = current_app.config["UP_PATH"] + filename
        fileurl = current_app.config["UP_URL"] + filename

        try:
            fo = open(filepath, "xb")
            fo.write(data)
        except:
            return "Upload error"
        finally:
            fo.close()

        return {
            "default": fileurl
        }
