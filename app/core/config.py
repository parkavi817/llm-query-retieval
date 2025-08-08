# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 800
    TOP_K: int = 3

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
