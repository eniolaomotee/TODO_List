from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    database_url: str
    
    model_config = SettingsConfigDict(env_file=env_path,extra="ignore")
    
    
settings = Settings()