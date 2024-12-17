import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str
    OPENAI_API_KEY: str
    GITHUB_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
