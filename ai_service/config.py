import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Settings
    POSTGRES_DB: str = "newsbias"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433

    # Neo4j Settings
    NEO4J_URI: str = "bolt://localhost:7688"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"

    # Qdrant Settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6335
    QDRANT_COLLECTION: str = "news_articles"

    # AI API Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "mock"  # gemini, openai, or mock

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Auto-detect provider if keys are set
if settings.GEMINI_API_KEY:
    settings.LLM_PROVIDER = "gemini"
elif settings.OPENAI_API_KEY:
    settings.LLM_PROVIDER = "openai"
