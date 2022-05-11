from flask import Flask, current_app, request, jsonify
from lib.redis import Redis
import config


create_app = Flask(__name__)


class App(Flask):
    def initConfig(self):
        self.config.from_object(config.ProductConfig)
        ctx = self.app_context()
        ctx.push()

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


def create_app():
    app = App(__name__.split('.')[0])
    app.initConfig()
    app.initBlueprint()
    app.before_request(app.initBeforeRequest)
    app.url_map.strict_slashes = False

    return app
