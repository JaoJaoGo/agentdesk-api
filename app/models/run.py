from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import RunStatus
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id"),
        index=True,
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[RunStatus] = mapped_column(
        SqlEnum(
            RunStatus,
            name="run_status",
            native_enum=False,
            values_callable=lambda enum_class: [item.value for item in enum_class],
        ),
        default=RunStatus.PENDING,
        nullable=False,
        index=True,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    prompt_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    completion_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
