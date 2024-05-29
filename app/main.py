from fastapi import FastAPI

from app.adapter.incoming.web.base import router


def create_app():
    _app = FastAPI(
        title="CRUDBuilder",
        version="0.1.0",
    )

    _app.include_router(router)

    return _app


app = create_app()
