from app.create_app import create_app
from lib.redis import Redis

app = create_app()
redis = Redis(config=app.config)


def initImport():
    from app.admin.controllers import adminController
    from app.index.controllers import indexController


initImport()
