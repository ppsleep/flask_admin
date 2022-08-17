from flask import Flask, request, jsonify
from lib.db import db
from lib.redis import Redis
import config
import time
import logging


create_app = Flask(__name__)


class App(Flask):
    def initConfig(self):
        self.config.from_object(config.ProductConfig)
        ctx = self.app_context()
        ctx.push()

    def initDB(self):
        db.init_app(self)

    def initRedis(self):
        self.redis = Redis(config=self.config)
        return self.redis

    def initBlueprint(self):
        from app.index.controllers import regIndexBlueprint
        from app.admin.controllers import regAdminBlueprint
        regIndexBlueprint(self)
        regAdminBlueprint(self)

    def initBeforeRequest(self):
        import jwt
        import json
        module = request.path.split("/")
        if len(module) > 1 and module[1] == "admin":
            authorization = request.headers.get('Authorization')
            token = request.headers.get('x-auth-token')

            if token is None or authorization is None:
                return jsonify({
                    "status": -1
                })
            user = self.redis.get(token)
            if user is None:
                return jsonify({
                    "status": -1
                })
            user = json.loads(user)

            try:
                jwt.decode(authorization, user["s"], algorithms=["HS256"])
            except:
                return jsonify({
                    "status": -1
                })

            request.user = {
                "id": user["id"],
                "username": user["username"]
            }


def date(timestamp):
    return time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(timestamp)
    )


def create_app():
    app = App(
        __name__.split('.')[0], template_folder="./", static_folder="../static/"
    )

    @app.errorhandler(Exception)
    def handle_exception(e):
        handler = logging.FileHandler("./logs/logs.log")
        logging_format = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.info(e)

    app.initConfig()
    app.initDB()
    app.initBlueprint()
    app.before_request(app.initBeforeRequest)
    app.url_map.strict_slashes = False
    app.jinja_env.filters['date'] = date

    return app
