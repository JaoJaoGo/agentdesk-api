from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response,
    status,
)

from app.api.dependencies import AgentServiceDependency
from app.core.exceptions import (
    AgentNotFoundError,
    AgentSlugAlreadyExistsError,
)
from app.schemas.agent import (
    AgentCreate,
    AgentResponse,
    AgentUpdate,
)


router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    payload: AgentCreate,
    service: AgentServiceDependency,
) -> AgentResponse:
    try:
        return service.create(payload)
    except AgentSlugAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception),
        ) from exception


@router.get(
    "",
    response_model=list[AgentResponse],
)
def list_agents(
    service: AgentServiceDependency,
    offset: Annotated[
        int,
        Query(ge=0),
    ] = 0,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 20,
) -> list[AgentResponse]:
    return service.list(
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{slug}",
    response_model=AgentResponse,
)
def get_agent(
    slug: str,
    service: AgentServiceDependency,
) -> AgentResponse:
    try:
        return service.get_by_slug(slug)
    except AgentNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception


@router.patch(
    "/{slug}",
    response_model=AgentResponse,
)
def update_agent(
    slug: str,
    payload: AgentUpdate,
    service: AgentServiceDependency,
) -> AgentResponse:
    try:
        return service.update(
            slug=slug,
            payload=payload,
        )
    except AgentNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception
    except AgentSlugAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception),
        ) from exception


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_agent(
    slug: str,
    service: AgentServiceDependency,
) -> Response:
    try:
        service.delete(slug)
    except AgentNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception

    return Response(status_code=status.HTTP_204_NO_CONTENT)
