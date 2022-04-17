from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config.CONF)
from login import login
from app.admin.controllers import controllers