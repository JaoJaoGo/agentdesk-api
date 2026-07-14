from time import perf_counter

from app.core.exceptions import (
    AgentInactiveError,
    AgentNotFoundError,
    OllamaError,
    RunNotFoundError,
)
from app.integrations.ollama import OllamaClient
from app.models.run import Run
from app.repositories.agent_repository import AgentRepository
from app.repositories.run_repository import RunRepository
from app.schemas.run import RunCreate


class RunService:
    def __init__(
        self,
        *,
        agent_repository: AgentRepository,
        run_repository: RunRepository,
        ollama_client: OllamaClient,
    ) -> None:
        self.agent_repository = agent_repository
        self.run_repository = run_repository
        self.ollama_client = ollama_client

    async def execute(
        self,
        *,
        agent_slug: str,
        payload: RunCreate,
    ) -> Run:
        agent = self.agent_repository.get_by_slug(agent_slug)

        if agent is None:
            raise AgentNotFoundError(agent_slug)

        if not agent.active:
            raise AgentInactiveError(agent_slug)

        run = self.run_repository.create_pending(
            agent_id=agent.id,
            prompt=payload.prompt,
            model=agent.model,
        )

        started_at = perf_counter()

        try:
            ollama_response = await self.ollama_client.chat(
                model=agent.model,
                system_prompt=agent.system_prompt,
                user_prompt=payload.prompt,
                temperature=agent.temperature,
            )
        except OllamaError as exception:
            duration_ms = self._duration_ms(started_at)

            self.run_repository.mark_failed(
                run,
                error_message=str(exception),
                duration_ms=duration_ms,
            )

            raise

        duration_ms = self._duration_ms(started_at)

        return self.run_repository.mark_completed(
            run,
            response=ollama_response.message.content,
            duration_ms=duration_ms,
            prompt_tokens=(ollama_response.prompt_eval_count),
            completion_tokens=(ollama_response.eval_count),
        )

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Run]:
        return self.run_repository.list(
            offset=offset,
            limit=limit,
        )

    def get_by_id(
        self,
        run_id: int,
    ) -> Run:
        run = self.run_repository.get_by_id(run_id)

        if run is None:
            raise RunNotFoundError(run_id)

        return run

    @staticmethod
    def _duration_ms(
        started_at: float,
    ) -> int:
        elapsed_seconds = perf_counter() - started_at

        return round(elapsed_seconds * 1000)
