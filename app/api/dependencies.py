from typing import Annotated

import httpx
from fastapi import Depends, Request

from app.db.session import SessionDependency
from app.integrations.ollama import OllamaClient
from app.repositories.agent_repository import AgentRepository
from app.repositories.run_repository import RunRepository
from app.services.agent_service import AgentService
from app.services.run_service import RunService


def get_http_client(
    request: Request,
) -> httpx.AsyncClient:
    return request.app.state.http_client


HttpClientDependency = Annotated[
    httpx.AsyncClient,
    Depends(get_http_client),
]


def get_agent_service(
    session: SessionDependency,
) -> AgentService:
    repository = AgentRepository(session)

    return AgentService(repository)


AgentServiceDependency = Annotated[
    AgentService,
    Depends(get_agent_service),
]


def get_run_service(
    session: SessionDependency,
    http_client: HttpClientDependency,
) -> RunService:
    return RunService(
        agent_repository=AgentRepository(session),
        run_repository=RunRepository(session),
        ollama_client=OllamaClient(http_client),
    )


RunServiceDependency = Annotated[
    RunService,
    Depends(get_run_service),
]
