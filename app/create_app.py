from flask import Flask
import config


def create_app():
    app = Flask(__name__.split('.')[0])
    initConfig(app)
    return app


def initConfig(app):
    app.config.from_object(config.ProductConfig)
