from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    cognodb_uri: str = "bolt+s://localhost:7687"
    cognodb_user: str = "cognodb"
    cognodb_password: str = ""
    frontend_url: str = ""

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
