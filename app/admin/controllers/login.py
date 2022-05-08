from flask import Flask, request
from app import app, redis
from lib.db import session
from app.models.Admins import Admins
from app.decorator import response
import bcrypt
import time
import json

login = Flask(__name__)


@app.route("/login/login/", methods=["POST"])
@response
def login():
    data = request.get_json()
    if "username" not in data:
        return "Please input username"
    if "password" not in data:
        return "Please input password"
    userObj = session.query(Admins).where(Admins.username == data["username"])
    result = userObj.first()
    if result == None:
        return "Username or password is invalid"
    if not bcrypt.checkpw(
        str.encode(str(data["password"])),
        str.encode(result.password)
    ):
        return "Username or password is invalid"

    userObj.update({
        "last_ip": request.remote_addr,
        "last_time": int(time.time())
    })
    session.commit()
    token = bcrypt.gensalt().decode()
    secret = bcrypt.gensalt().decode()
    resp = {
        "id": result.id,
        "username": result.username,
        "t": token,
        "s": secret
    }
    redis.setex(token, app.config["TOKEN_EXPIRY"], json.dumps(resp))
    return resp


@app.route("/login/logout/", methods=["POST"])
@response
def logout():
    token = request.headers.get("Authorization")
    if not token == None:
        redis.delete(token)
    return 0
