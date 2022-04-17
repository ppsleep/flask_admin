from flask import Flask
from app import app

login = Flask(__name__)

@app.route("/login/login/")
def login():
    return "Welcome!"

@app.route("/login/logout/")
def logout():
    return "Bye!"