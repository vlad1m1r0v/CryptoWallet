from string import Template

from src.domain.exceptions.base import (
    DomainError,
    DomainFieldError
)

from src.domain.value_objects.email import Email


class EmailAlreadyExistsError(DomainError):
    message = Template("User with email $email already exists.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class EmailNotFoundError(DomainError):
    message = Template("User with email 'user@domain.com' is not found.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class UserNotFoundError(DomainError):
    message = f"User not found."


class IncorrectRepeatPasswordError(DomainError):
    message = f"'Password' and 'Repeat password' do not match."


class PasswordsNotMatchError(DomainError):
    message = f"Passwords do not match."


class RepeatPasswordIsNotSetError(DomainError):
    message = f"Repeat password is not set."


class UserNotActivatedError(DomainError):
    message = f"User is not activated."
