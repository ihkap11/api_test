from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class DBSettings(BaseModel):
    hostname: str
    port: str
    password: str
    name: str
    username: str


class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str
    expiry: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )
    db: DBSettings
    jwt: JWTSettings


settings = Settings()
logger.debug(settings.model_dump())
