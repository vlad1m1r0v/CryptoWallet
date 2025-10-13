from string import Template
from typing import Any


class DomainError(Exception):
    message: str | Template = "A domain error occurred."
    example_args: dict[str, Any] | None = None

    def __init__(self, **kwargs):
        self._example_kwargs = kwargs or {}

        if isinstance(self.message, str):
            super().__init__(self.message)
        elif isinstance(self.message, Template):
            super().__init__(self.message.safe_substitute(**kwargs))

    @property
    def example(self) -> str:
        if isinstance(self.message, str):
            return self.message
        return self.message.safe_substitute(**self.example_args)


class DomainFieldError(DomainError):
    message: str = "Invalid field value."
