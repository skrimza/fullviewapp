from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        case_sensitive=False
    )
    HOST: str
    DATABASE_URL: str



BASE_DIR = Path(__file__).resolve().parent
SETTINGS = Settings()