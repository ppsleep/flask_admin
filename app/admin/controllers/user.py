from flask import Blueprint, request
from lib.db import session
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from app.admin.validator.user import Password
from app.models.Admins import Admins
from app.decorator import response
import bcrypt

user = Blueprint("user", __name__)


class User():

    @user.route("/getuser/", methods=["POST"])
    @response
    def getuser():
        return request.user

    @user.route("/password/", methods=["POST"])
    @response
    def password():
        data = request.get_json()
        v = Password.from_json(data)
        if not v.validate():
            return v.errors[next(iter(v.errors))][0]
        stmt = select(Admins).where(Admins.id == request.user["id"])
        result = session.execute(stmt).scalar()

        if not bcrypt.checkpw(
            str.encode(str(data["password"])),
            str.encode(result.password)
        ):
            return "Password is invalid"

        stmt = update(Admins).values(
            password=bcrypt.hashpw(
                str.encode(str(data["cpassword"])), bcrypt.gensalt()
            )
        ).where(Admins.id == result.id)
        session.execute(stmt)
        session.commit()
        return 0
