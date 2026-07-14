from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AgentBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    slug: str = Field(
        min_length=3,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    system_prompt: str = Field(
        min_length=10,
        max_length=10_000,
    )

    model: str = Field(
        default="qwen2.5:7b",
        min_length=1,
        max_length=100,
    )

    temperature: float = Field(
        default=0.2,
        ge=0,
        le=2,
    )

    active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    slug: str | None = Field(
        default=None,
        min_length=3,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    system_prompt: str | None = Field(
        default=None,
        min_length=10,
        max_length=10_000,
    )

    model: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    temperature: float | None = Field(
        default=None,
        ge=0,
        le=2,
    )

    active: bool | None = None


class AgentResponse(AgentBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime
    updated_at: datetime
