from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, ValidationError

from app.core.exceptions import (
    OllamaInvalidResponseError,
    OllamaRequestError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)


class OllamaMessageResponse(BaseModel):
    role: str
    content: str


class OllamaChatResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    model: str
    message: OllamaMessageResponse
    done: bool

    total_duration: int | None = None
    prompt_eval_count: int | None = None
    eval_count: int | None = None


class OllamaClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
    ) -> None:
        self.http_client = http_client

    async def chat(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
    ) -> OllamaChatResponse:
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            response = await self.http_client.post(
                "/api/chat",
                json=payload,
            )

            response.raise_for_status()

        except httpx.TimeoutException as exception:
            raise OllamaTimeoutError() from exception

        except httpx.ConnectError as exception:
            raise OllamaUnavailableError() from exception

        except httpx.HTTPStatusError as exception:
            detail = self._extract_error(
                exception.response
            )

            raise OllamaRequestError(
                status_code=exception.response.status_code,
                detail=detail,
            ) from exception

        except httpx.RequestError as exception:
            raise OllamaUnavailableError() from exception

        try:
            parsed_response = OllamaChatResponse.model_validate(
                response.json()
            )
        except (ValueError, ValidationError) as exception:
            raise OllamaInvalidResponseError() from exception

        if not parsed_response.message.content.strip():
            raise OllamaInvalidResponseError()

        return parsed_response

    @staticmethod
    def _extract_error(
        response: httpx.Response,
    ) -> str:
        try:
            body = response.json()
        except ValueError:
            return (
                response.text.strip()
                or "Unknown Ollama error."
            )

        if isinstance(body, dict):
            error = body.get("error")

            if isinstance(error, str):
                return error

        return "Unknown Ollama error."