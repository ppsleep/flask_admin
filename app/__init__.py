from app.create_app import create_app

app = create_app()


def initImport():
    from app.admin.controllers import adminController
    from app.index.controllers import indexController


initImport()
