import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseModel, Field

# config.py está em app/core/.
# parents[2] aponta para a raiz do projeto.
ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / ".env")

class Settings(BaseModel):
    app_name: str
    app_env: Literal["development", "testing", "production"]
    app_debug: bool

    database_url: str

    ollama_base_url: AnyHttpUrl
    http_timeout_seconds: float = Field(gt=0, le=300)

@lru_cache
def get_settings() -> Settings:
    """
    Carrega as variáveis do ambiente e deixa o Pydantic
    responsável por validar e converter os tipos.
    """

    return Settings.model_validate(
        {
            "app_name": os.getenv("APP_NAME", "AgentDesk API"),
            "app_env": os.getenv("APP_ENV", "development"),
            "app_debug": os.getenv("APP_DEBUG", "true"),
            "database_url": os.getenv(
                "DATABASE_URL", 
                "sqlite:///./agentdesk.db"
            ),
            "ollama_base_url": os.getenv(
                "OLLAMA_BASE_URL", 
                "http://localhost:11434"
            ),
            "http_timeout_seconds": os.getenv(
                "HTTP_TIMEOUT_SECONDS", 
                "30"
            ),
        }
    )