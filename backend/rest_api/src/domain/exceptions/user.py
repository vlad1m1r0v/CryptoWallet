from string import Template

from src.domain.exceptions.base import DomainError

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


class PasswordsNotMatchError(DomainError):
    message = f"Passwords do not match."


class UserNotActivatedError(DomainError):
    message = f"User is not activated."
