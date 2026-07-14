from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

from app.api.routes.agents import router as agents_router
from app.core.config import Settings, get_settings
from app.db.init_db import create_database_tables
from app.schemas.health import HealthResponse


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_database_tables()

    yield


app = FastAPI(
    title=settings.app_name,
    description="API para gerenciamento e execução de agentes de IA.",
    version="0.2.0",
    lifespan=lifespan,
)


app.include_router(agents_router)


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
