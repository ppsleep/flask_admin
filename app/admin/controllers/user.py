from flask import Blueprint, request
from lib.db import session
from app.models.Admins import Admins
from app.decorator import response
from app.decorator import validation
import bcrypt

user = Blueprint("user", __name__)


class User():

    @user.route("/getuser/", methods=["POST"])
    @response
    def getuser():
        return request.user

    @user.route("/password/", methods=["POST"])
    @response
    @validation
    def password():
        data = request.get_json()
        userObj = session.query(Admins).where(Admins.id == request.user["id"])
        result = userObj.first()

        if not bcrypt.checkpw(
            str.encode(str(data["password"])),
            str.encode(result.password)
        ):
            return "Password is invalid"

        userObj.update({
            "password": bcrypt.hashpw(
                str.encode(str(data["cpassword"])), bcrypt.gensalt()
            )
        })
        session.commit()
        return 0
