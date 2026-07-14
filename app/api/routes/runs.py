from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from app.api.dependencies import (
    RunServiceDependency,
)
from app.core.exceptions import (
    AgentInactiveError,
    AgentNotFoundError,
    OllamaError,
    OllamaTimeoutError,
    RunNotFoundError,
)
from app.schemas.run import (
    RunCreate,
    RunResponse,
)


router = APIRouter(
    tags=["Runs"],
)


@router.post(
    "/agents/{agent_slug}/runs",
    response_model=RunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def execute_agent(
    agent_slug: str,
    payload: RunCreate,
    service: RunServiceDependency,
) -> RunResponse:
    try:
        return await service.execute(
            agent_slug=agent_slug,
            payload=payload,
        )

    except AgentNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception

    except AgentInactiveError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception),
        ) from exception

    except OllamaTimeoutError as exception:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(exception),
        ) from exception

    except OllamaError as exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exception),
        ) from exception


@router.get(
    "/runs",
    response_model=list[RunResponse],
)
def list_runs(
    service: RunServiceDependency,
    offset: Annotated[
        int,
        Query(ge=0),
    ] = 0,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 20,
) -> list[RunResponse]:
    return service.list(
        offset=offset,
        limit=limit,
    )


@router.get(
    "/runs/{run_id}",
    response_model=RunResponse,
)
def get_run(
    run_id: int,
    service: RunServiceDependency,
) -> RunResponse:
    try:
        return service.get_by_id(run_id)
    except RunNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception
