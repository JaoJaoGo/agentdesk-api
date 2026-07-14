from app.core.exceptions import (
    AgentNotFoundError,
    AgentSlugAlreadyExistsError,
)
from app.models.agent import Agent
from app.repositories.agent_repository import AgentRepository
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentService:
    def __init__(
        self,
        repository: AgentRepository,
    ) -> None:
        self.repository = repository

    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Agent]:
        return self.repository.list(
            offset=offset,
            limit=limit,
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> Agent:
        agent = self.repository.get_by_slug(slug)

        if agent is None:
            raise AgentNotFoundError(slug)

        return agent

    def create(
        self,
        payload: AgentCreate,
    ) -> Agent:
        existing_agent = self.repository.get_by_slug(payload.slug)

        if existing_agent is not None:
            raise AgentSlugAlreadyExistsError(payload.slug)

        agent = Agent(**payload.model_dump())

        return self.repository.save(agent)

    def update(
        self,
        slug: str,
        payload: AgentUpdate,
    ) -> Agent:
        agent = self.get_by_slug(slug)

        update_data = payload.model_dump(exclude_unset=True)

        new_slug = update_data.get("slug")

        if new_slug is not None and new_slug != agent.slug:
            existing_agent = self.repository.get_by_slug(new_slug)

            if existing_agent is not None:
                raise AgentSlugAlreadyExistsError(new_slug)

        for field, value in update_data.items():
            setattr(agent, field, value)

        return self.repository.save(agent)

    def delete(
        self,
        slug: str,
    ) -> None:
        agent = self.get_by_slug(slug)

        self.repository.delete(agent)
