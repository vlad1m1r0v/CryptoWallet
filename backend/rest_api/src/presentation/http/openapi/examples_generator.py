import re
from typing import Type

from starlette import status

from src.domain.exceptions.base import DomainError

from src.infrastructure.exceptions.base import InfrastructureError

from src.domain.exceptions.user import (
    UserNotFoundError,
    UserNotActivatedError
)

from src.infrastructure.exceptions.auth import (
    AccessTokenNotProvidedError,
    InvalidAccessTokenError
)

from src.presentation.http.exceptions.error_mapping import get_status_code_for_exception


def class_name_to_snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.upper()


class ExamplesGenerator:
    @staticmethod
    def generate_nested_schema_for_code(responses, code: int):
        responses[code] = {
            "content": {
                "application/json": {}
            }
        }

    @classmethod
    def generate_examples(
            cls,
            *args: Type[DomainError] | Type[InfrastructureError],
            is_auth: bool = False
    ) -> dict:
        responses: dict = {}

        auth_errors = (
            UserNotFoundError,
            UserNotActivatedError,
            AccessTokenNotProvidedError,
            InvalidAccessTokenError
        )

        if is_auth:
            args += auth_errors

        error_codes = {get_status_code_for_exception(error) for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                if get_status_code_for_exception(error) == error_code:
                    examples[class_name_to_snake(error.__name__)] = {
                        "summary": class_name_to_snake(error.__name__),
                        "value": {
                            "description": error.example()
                        }
                    }

            cls.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        cls.change_422_validation_schema(responses)

        return responses

    @classmethod
    def change_422_validation_schema(cls, responses):
        """
        Change the 422 validation schema to match the one used in the.

        API.

        """
        cls.generate_nested_schema_for_code(
            responses, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        example = {
            "validation_errors": {
                "summary": "VALIDATION_ERROR",
                "value": {
                    "username": [
                        "String should have at least 5 characters"
                    ],
                    "__model__": [
                        "Passwords do not match"
                    ]
                }
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"][
            "examples"
        ] = example


generate_examples = ExamplesGenerator.generate_examples
