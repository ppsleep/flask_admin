from .dashboard import dashboard
from .news import news
from .user import user
from .login import login
from flask import Blueprint, request, jsonify
from app import app, redis
import jwt
import json

adminController = Blueprint("controllers", __name__)
app.register_blueprint(dashboard, url_prefix="/admin/dashboard")
app.register_blueprint(news, url_prefix="/admin/news")
app.register_blueprint(user, url_prefix="/admin/user")


@app.before_request
def init():
    module = request.path.split("/")
    if len(module) > 1 and module[1] == "admin":
        authorization = request.headers.get('Authorization')
        token = request.headers.get('x-auth-token')

        if token is None or authorization is None:
            return jsonify({
                "status": -1
            })
        user = redis.get(token)
        if user is None:
            return jsonify({
                "status": -1
            })
        user = json.loads(user)

        try:
            jwt.decode(authorization, user["s"], algorithms=["HS256"])
        except:
            return jsonify({
                "status": -1
            })

        request.user = {
            "id": user["id"],
            "username": user["username"]
        }
