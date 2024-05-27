import os
from functools import cache

from pydantic.v1 import BaseSettings

CONFIG_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.abspath(os.path.join(CONFIG_PATH, ".."))


class Settings(BaseSettings):
    ENV: str = "dev"


@cache
def get_settings():
    return Settings()
