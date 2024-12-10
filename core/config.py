from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    # api_token: str
    # admin_id: str



    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()