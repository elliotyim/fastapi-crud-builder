import asyncio
import os
from collections.abc import Generator

import pytest
from app.config import ROOT_PATH
from app.dependency.db import get_db, get_session_maker
from app.domain.entity import Base, Post, User
from app.main import create_app
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

DB_PATH = os.path.join(ROOT_PATH, "db.sqlite3")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

_Session = get_session_maker(_engine)


@pytest.fixture
def test_app() -> Generator[FastAPI, any, None]:
    Base.metadata.create_all(_engine)
    _app = create_app()
    yield _app


@pytest.fixture
def test_db(test_app: FastAPI) -> Generator[Session, any, None]:
    connection = _engine.connect()
    transaction = connection.begin()
    session = _Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(
    test_app: FastAPI, test_db: Session
) -> Generator[TestClient, any, None]:
    def _get_test_db():
        yield test_db

    test_app.dependency_overrides[get_db] = _get_test_db

    with TestClient(
        test_app, backend_options={"loop_factory": asyncio.new_event_loop}
    ) as _test_client:
        yield _test_client


@pytest.fixture
def dummy_users(test_db: Session) -> list[User]:
    users = [User(name=f"dummy_user_{i}") for i in range(3)]
    test_db.add_all(users)
    test_db.commit()
    return users


@pytest.fixture
def dummy_posts(test_db: Session, dummy_users: list[User]) -> list[Post]:
    posts = [
        Post(author=user, title=f"dummy_title_{i}", content=f"dummy_content_{i}")
        for i, user in enumerate(dummy_users)
    ]
    test_db.add_all(posts)
    test_db.commit()
    return posts
