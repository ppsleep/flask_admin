from app.admin.controllers.dashboard import dashboard
from app.admin.controllers.news import news
from app.admin.controllers.login import login
from flask import Blueprint, request
from app import app
adminController = Blueprint("controllers", __name__)
app.register_blueprint(dashboard, url_prefix="/admin/dashboard")
app.register_blueprint(news, url_prefix="/admin/news")


@app.before_request
def init():
    module = request.path.split("/")
    if len(module) > 1 and module[1] == "admin":
        # do some permissions validation
        # test user info
        request.user = {
            "id": 1,
            "username": "admin"
        }
