import imp
from flask import Blueprint

dashboard = Blueprint("dashboard", __name__)

class Dashborad():
    @dashboard.route("/")
    def index():
        return "Dashboard"
