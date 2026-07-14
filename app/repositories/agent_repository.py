from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AgentSlugAlreadyExistsError
from app.models.agent import Agent


class AgentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Agent]:
        statement = select(Agent).order_by(Agent.id).offset(offset).limit(limit)

        return list(self.session.scalars(statement).all())

    def get_by_slug(
        self,
        slug: str,
    ) -> Agent | None:
        statement = select(Agent).where(Agent.slug == slug)

        return self.session.scalar(statement)

    def save(
        self,
        agent: Agent,
    ) -> Agent:
        try:
            self.session.add(agent)
            self.session.commit()
            self.session.refresh(agent)
        except IntegrityError as exception:
            self.session.rollback()

            raise AgentSlugAlreadyExistsError(agent.slug) from exception

        return agent

    def delete(
        self,
        agent: Agent,
    ) -> None:
        self.session.delete(agent)
        self.session.commit()
