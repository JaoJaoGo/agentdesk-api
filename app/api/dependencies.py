from typing import Annotated

from fastapi import Depends

from app.db.session import SessionDependency
from app.repositories.agent_repository import AgentRepository
from app.services.agent_service import AgentService


def get_agent_service(
    session: SessionDependency,
) -> AgentService:
    repository = AgentRepository(session)

    return AgentService(repository)


AgentServiceDependency = Annotated[
    AgentService,
    Depends(get_agent_service),
]
