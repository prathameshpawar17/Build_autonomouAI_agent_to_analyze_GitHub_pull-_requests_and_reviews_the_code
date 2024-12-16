import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_url: str
    database_url: str
    ollama_api_key: str
    GITHUB_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
