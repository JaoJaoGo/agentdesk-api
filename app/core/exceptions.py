class AgentNotFoundError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug

        super().__init__(f"Agent with slug '{slug}' was not found.")


class AgentSlugAlreadyExistsError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug

        super().__init__(f"An agent with slug '{slug}' already exists.")


class AgentInactiveError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug

        super().__init__(f"Agent with slug '{slug}' is inactive.")


class RunNotFoundError(Exception):
    def __init__(self, run_id: int) -> None:
        self.run_id = run_id

        super().__init__(f"Run with id '{run_id}' was not found.")


class OllamaError(Exception):
    pass


class OllamaUnavailableError(OllamaError):
    def __init__(self) -> None:
        super().__init__("Could not connect to the Ollama service.")


class OllamaTimeoutError(OllamaError):
    def __init__(self) -> None:
        super().__init__("Ollama took too long to generate a response.")


class OllamaRequestError(OllamaError):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ) -> None:
        self.status_code = status_code
        self.detail = detail

        super().__init__(f"Ollama returned HTTP {status_code}: {detail}")


class OllamaInvalidResponseError(OllamaError):
    def __init__(self) -> None:
        super().__init__("Ollama returned an invalid response.")
