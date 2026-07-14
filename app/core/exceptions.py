class AgentNotFoundError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug

        super().__init__(f"Agent with slug '{slug}' was not found.")


class AgentSlugAlreadyExistsError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug

        super().__init__(f"An agent with slug '{slug}' already exists.")
