import os
from collections.abc import Generator
from functools import cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import ROOT_PATH

DB_PATH = os.path.join(ROOT_PATH, "db.sqlite3")


@cache
def get_engine() -> Engine:
    engine = create_engine(
        url=f"sqlite:///{DB_PATH}",
        connect_args={"check_same_thread": False}
    )
    return engine


@cache
def get_session_maker(engine: Engine):
    _Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _Session


def get_db() -> Generator[Session, None, None]:
    _Session = get_session_maker(get_engine())

    with _Session() as session:
        yield session
