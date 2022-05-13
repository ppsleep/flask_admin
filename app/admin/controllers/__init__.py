from .dashboard import dashboard
from .news import news
from .tags import tags
from .user import user
from .upload import upload
from .login import login

from flask import Flask

adminController = Flask(__name__)


def regAdminBlueprint(app):
    app.register_blueprint(dashboard, url_prefix="/admin/dashboard")
    app.register_blueprint(news, url_prefix="/admin/news")
    app.register_blueprint(tags, url_prefix="/admin/tags")
    app.register_blueprint(user, url_prefix="/admin/user")
    app.register_blueprint(upload, url_prefix="/admin/upload")
    app.register_blueprint(login, url_prefix="/login")
