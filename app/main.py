from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI

from app.api.routes.agents import router as agents_router
from app.api.routes.runs import router as runs_router
from app.core.config import Settings, get_settings
from app.db.init_db import create_database_tables
from app.schemas.health import HealthResponse


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()

    timeout = httpx.Timeout(
        connect=5.0,
        read=settings.http_timeout_seconds,
        write=10.0,
        pool=5.0,
    )

    base_url = str(settings.ollama_base_url).rstrip("/")

    async with httpx.AsyncClient(
        base_url=base_url,
        timeout=timeout,
        headers={
            "Content-Type": "application/json",
        },
    ) as http_client:
        app.state.http_client = http_client

        yield


app = FastAPI(
    title=settings.app_name,
    description="API para gerenciamento e execução de agentes de IA.",
    version="0.3.0",
    lifespan=lifespan,
)


app.include_router(agents_router)
app.include_router(runs_router)


SettingsDependency = Annotated[
    Settings,
    Depends(get_settings),
]


@app.get(
    "/",
    include_in_schema=False,
)
async def root() -> dict[str, str]:
    return {
        "message": "AgentDesk API",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
)
async def health(
    settings: SettingsDependency,
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        application=settings.app_name,
        environment=settings.app_env,
        debug=settings.app_debug,
    )
