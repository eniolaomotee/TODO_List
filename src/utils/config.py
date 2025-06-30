from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expiry: int = 30
    refresh_token_expiry: int = 1440
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


settings = Settings()
