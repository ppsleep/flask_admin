from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import Session
from app import app

scheme = app.config["DB"]
engine = create_engine(scheme, pool_recycle=7200, future=True)
session = Session(engine, future=True)

mapper_registry = registry()
Base = mapper_registry.generate_base()
mapper_registry.metadata.create_all(engine)
