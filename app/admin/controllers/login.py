from flask import Flask, request
from app import app, redis
import bcrypt
import time
from lib.db import session
from lib.msg import Msg
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.Admins import Admins

login = Flask(__name__)


@app.route("/login/login/", methods=["POST"])
def login():
    data = request.get_json()
    if "username" not in data:
        return Msg.json(1, "Please input username")
    if "password" not in data:
        return Msg.json(1, "Please input password")
    stmt = select(Admins).where(Admins.username == data["username"])
    result = session.execute(stmt).scalar()
    if result == None:
        return Msg.json(1, "Username or password is invalid")
    if not bcrypt.checkpw(str.encode(
        data["password"]), str.encode(result.password)
    ):
        return Msg.json(1, "Username or password is invalid")

    stmt = update(Admins).values(
        last_ip=request.remote_addr,
        last_time=time.time()
    ).where(Admins.id == result.id)
    session.execute(stmt)
    session.commit()
    token = bcrypt.gensalt().decode()
    secret = bcrypt.gensalt().decode()
    resp = {
        "id": result.id,
        "username": result.username,
        "t": token,
        "s": secret
    }
    redis.setex(token, app.config["TOKEN_EXPIRY"], str(resp))
    return Msg.json(0, resp)


@app.route("/login/logout/", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if not token == None:
        redis.delete(token)
    return Msg.json(0)
