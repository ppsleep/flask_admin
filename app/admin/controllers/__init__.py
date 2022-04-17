from flask import Blueprint, request
from app import app
controllers = Blueprint("controllers", __name__)
from app.admin.controllers.dashboard import dashboard
app.register_blueprint(dashboard, url_prefix="/admin/dashboard")

@app.before_request
def init():
    module = request.path.split("/")
    if len(module) > 1 and module[1] == "admin":
        return "403"