from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import RunStatus


class RunCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    prompt: str = Field(
        min_length=3,
        max_length=20_000,
    )


class RunResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    agent_id: int
    prompt: str
    response: str | None
    status: RunStatus
    model: str

    duration_ms: int | None
    prompt_tokens: int | None
    completion_tokens: int | None

    error_message: str | None

    created_at: datetime
    completed_at: datetime | None
