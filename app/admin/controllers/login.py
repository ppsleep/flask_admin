from flask import Flask, request
from app import app
import bcrypt
from db import session
from lib.msg import Msg
from sqlalchemy.future import select
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
    result = session.execute(stmt).first()
    if result == None:
        return Msg.json(1, "Username or password is invalid")
    if not bcrypt.checkpw(str.encode(
        data["password"]), str.encode(result[0].password)
    ):
        return Msg.json(1, "Username or password is invalid")

    return Msg.json(0)


@app.route("/login/logout/", methods=["POST"])
def logout():
    return "Bye!"
