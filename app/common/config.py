from functools import lru_cache
from os import path, environ
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)


class GlobalSettings(BaseSettings):
    ENV_STATE: str = environ.get("ENV_STATE", "dev")
    BASE_DIR: str = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    RANDOM_STRING: str = environ.get("RANDOM_STRING", "Ib75lIvT7AbUrgUa")

    # JWT
    JWT_ACCESS_TOKEN_EXPIRE_DAY: int = environ.get("JWT_ACCESS_TOKEN_EXPIRE_DAY", 30)
    JWT_REFRESH_TOKEN_EXPIRE_DAY: int = environ.get("JWT_REFRESH_TOKEN_EXPIRE_DAY", 60)
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "936de431dfbb55c59232f10d05c34a22bf957154f8814a3a0b88d893f58ef16957f176def0982871857aadb970a304160f4fa77968dbd4a0f6ef9cfd695d7af4")

    # SQL
    DB_URL: str = environ.get("DB_URL", f"sqlite:///{BASE_DIR}/database.db")
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 10)
    DB_POOL_MAX: int = environ.get("DB_POOL_MAX", 20)
    DB_POOL_RECYCLE: int = environ.get("DB_POOL_RECYCLE", 300)
    DB_POOL_TIMEOUT: int = environ.get("DB_POOL_TIMEOUT", 60)


class DevSettings(GlobalSettings):
    DOMAIN: str = "localhost"
    PORT: int = 8080
    TRUSTED_HOSTS: List[str] = ["*"]
    ALLOW_SITE: List[str] = ["*"]


class ProdSettings(GlobalSettings):
    DOMAIN: str = "nota-project.com"
    PORT: int = 8080
    TRUSTED_HOSTS: List[str] = ["*"]
    ALLOW_SITE: List[str] = ["*"]


@lru_cache()
def get_settings():
    env_state = GlobalSettings().ENV_STATE
    if env_state in ["dev"]:
        return DevSettings()
    elif env_state == "prod":
        return ProdSettings()
