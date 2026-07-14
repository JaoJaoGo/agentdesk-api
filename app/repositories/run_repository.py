from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import RunStatus
from app.models.run import Run


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RunRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Run]:
        statement = select(Run).order_by(Run.id.desc()).offset(offset).limit(limit)

        return list(self.session.scalars(statement).all())

    def get_by_id(
        self,
        run_id: int,
    ) -> Run | None:
        return self.session.get(
            Run,
            run_id,
        )

    def create_pending(
        self,
        *,
        agent_id: int,
        prompt: str,
        model: str,
    ) -> Run:
        run = Run(
            agent_id=agent_id,
            prompt=prompt,
            model=model,
            status=RunStatus.PENDING,
        )

        return self._save(run)

    def mark_completed(
        self,
        run: Run,
        *,
        response: str,
        duration_ms: int,
        prompt_tokens: int | None,
        completion_tokens: int | None,
    ) -> Run:
        run.status = RunStatus.COMPLETED
        run.response = response
        run.duration_ms = duration_ms
        run.prompt_tokens = prompt_tokens
        run.completion_tokens = completion_tokens
        run.error_message = None
        run.completed_at = utc_now()

        return self._save(run)

    def mark_failed(
        self,
        run: Run,
        *,
        error_message: str,
        duration_ms: int,
    ) -> Run:
        run.status = RunStatus.FAILED
        run.error_message = error_message
        run.duration_ms = duration_ms
        run.completed_at = utc_now()

        return self._save(run)

    def _save(
        self,
        run: Run,
    ) -> Run:
        try:
            self.session.add(run)
            self.session.commit()
            self.session.refresh(run)
        except Exception:
            self.session.rollback()
            raise

        return run
