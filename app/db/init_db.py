from app.db.base import Base
from app.db.session import engine
from app.models.agent import Agent  # noqa: F401
from app.models.run import Run  # noqa: F401


def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)
