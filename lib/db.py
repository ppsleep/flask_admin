from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
session = db.session
Base = db.Model
