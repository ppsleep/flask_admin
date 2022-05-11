from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import Session

scheme = current_app.config["DB"]
engine = create_engine(
    scheme, pool_size=current_app.config["DB_POOL_SIZE"], pool_recycle=3600, future=True
)
session = Session(engine, future=True)

mapper_registry = registry()
Base = mapper_registry.generate_base()
mapper_registry.metadata.create_all(engine)
