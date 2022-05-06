from flask import Flask, request
from app import app, redis
import bcrypt
import time
from lib.db import session
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.Admins import Admins
from app.decorator import response

login = Flask(__name__)


@app.route("/login/login/", methods=["POST"])
@response
def login():
    data = request.get_json()
    if "username" not in data:
        return "Please input username"
    if "password" not in data:
        return "Please input password"
    stmt = select(Admins).where(Admins.username == data["username"])
    result = session.execute(stmt).scalar()
    if result == None:
        return "Username or password is invalid"
    if not bcrypt.checkpw(
        str.encode(str(data["password"])),
        str.encode(result.password)
    ):
        return "Username or password is invalid"

    stmt = update(Admins).values(
        last_ip=request.remote_addr,
        last_time=int(time.time())
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
    return resp


@app.route("/login/logout/", methods=["POST"])
@response
def logout():
    token = request.headers.get("Authorization")
    if not token == None:
        redis.delete(token)
    return 0
