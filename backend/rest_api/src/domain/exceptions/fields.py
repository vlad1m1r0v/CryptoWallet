from enum import Enum
from string import Template
from typing import Type

from src.shared.exception import AppException


class ValueObjectException(AppException):
    pass


class FieldRequiredException(ValueObjectException):
    message = Template("'$field' is required.")
    example_args = {"field": "repeat_password"}

    def __init__(self, field: str):
        super().__init__(field=field)


class InvalidChoiceException(ValueObjectException):
    message = Template(
        "'$field' must be one of [$allowed_values], but got '$actual_value'."
    )
    example_args = {
        "field": "network",
        "allowed_values": "ETHEREUM, POLYGON, SEPOLIA",
        "actual_value": "BITCOIN"
    }

    def __init__(self, field: str, enum_cls: Type[Enum], actual_value: str):
        allowed_values = ", ".join([str(member.value) for member in enum_cls])
        super().__init__(field=field, allowed_values=allowed_values, actual_value=actual_value)


class MinMaxLengthException(ValueObjectException):
    message = Template("'$field' length must be between $min and $max")
    example_args = {"field": "username", "min": 5, "max": 32}

    def __init__(self, field: str, min_length: int, max_length: int):
        super().__init__(field=field, min=min_length, max=max_length)


class MinMaxValueException(ValueObjectException):
    message = Template("'$field' value must be between $min and $max")
    example_args = {"field": "decimals", "min": 0, "max": 30}

    def __init__(self, field: str, min_value: int, max_value: int):
        super().__init__(field=field, min=min_value, max=max_value)


class NegativeValueException(ValueObjectException):
    message = Template("'$field' value must be greater than zero.")
    example_args = {"field": "balance"}

    def __init__(self, field: str):
        super().__init__(field=field)


class FieldsDoNotMatchException(ValueObjectException):
    message = Template("'$field_1' and '$field_2' values do not match.")
    example_args = {"field_1": "password", "field_2": "repeat_password"}

    def __init__(self, field_1: str, field_2: str):
        super().__init__(field_1=field_1, field_2=field_2)


class InvalidStartException(AppException):
    message = Template(
        "Field '$field' must start with a letter (A-Z, a-z) or a digit (0-9)."
    )
    example_args = {"field": "username"}

    def __init__(self, field: str):
        super().__init__(field=field)


class UppercaseException(AppException):
    message = Template(
        "Field '$field' should be uppercase."
    )
    example_args = {"field": "asset_symbol"}

    def __init__(self, field: str):
        super().__init__(field=field)


class InvalidAddressStartException(AppException):
    message = Template(
        "Field '$field' must start with 0x..."
    )
    example_args = {"field": "address"}

    def __init__(self, field: str):
        super().__init__(field=field)


class InvalidEndException(AppException):
    message = Template(
        "Field '$field' must end with a letter (A-Z, a-z) or a digit (0-9)."
    )
    example_args = {"field": "username"}

    def __init__(self, field: str):
        super().__init__(field=field)


class ForbiddenConsecutiveCharactersException(AppException):
    message = Template(
        "Field '$field' cannot contain consecutive special characters like '..', '--' or '__'."
    )
    example_args = {"field": "username"}

    def __init__(self, field: str):
        super().__init__(field=field)


class ForbiddenCharactersException(AppException):
    message = Template(
        "Value '$value' contains forbidden characters. "
        "Allowed: letters (A-Z, a-z), digits (0-9), dots (.), hyphens (-), and underscores (_)."
    )
    example_args = {"value": "usern@me"}

    def __init__(self, value: str):
        super().__init__(value=value)


class InvalidEmailException(AppException):
    message = Template("Value '$email' is invalid E-Mail.")
    example_args = {"email": "example.domain.com"}

    def __init__(self, email: str):
        super().__init__(email=email)


class InvalidFilenameException(AppException):
    message = Template("Value '$filename' is invalid filename.")
    example_args = {"filename": "acde070d-8c4c-4f0d-9d8a-162843c10333"}

    def __init__(self, filename: str):
        super().__init__(filename=filename)


class InvalidPasswordException(ValueObjectException):
    message = \
        f"Password must be 8-20 characters long, " \
        "contain at least one lowercase, one uppercase, one digit, " \
        "and one special character."
