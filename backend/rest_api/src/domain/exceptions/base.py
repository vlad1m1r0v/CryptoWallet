from string import Template
from typing import Any


class DomainError(Exception):
    message: str | Template = "A domain error occurred."
    example_args: dict[str, Any] | None = None

    def __init__(self, **kwargs):
        if isinstance(self.message, str):
            super().__init__(self.message)
        elif isinstance(self.message, Template):
            super().__init__(self.message.safe_substitute(**kwargs))

    @classmethod
    def example(cls) -> str:
        if isinstance(cls.message, str):
            return cls.message
        return cls.message.safe_substitute(**cls.example_args)


class DomainFieldError(DomainError):
    message: str = "Invalid field value."
