from fastapi import FastAPI


def create_app():
    _app = FastAPI(
        title="CRUDBuilder",
        version="0.1.0",
    )

    return _app


app = create_app()
