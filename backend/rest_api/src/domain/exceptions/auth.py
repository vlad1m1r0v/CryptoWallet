from string import Template

from src.domain.exceptions.base import DomainError

from src.domain.value_objects.user.email import Email


class EmailAlreadyExistsException(DomainError):
    message = Template("User with email '$email' already exists.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class EmailNotFoundException(DomainError):
    message = Template("User with email '$email' is not found.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class WrongPasswordException(DomainError):
    message = f"Wrong Password."


class UserNotFoundError(DomainError):
    message = f"User not found."


class UserNotActivatedError(DomainError):
    message = f"User is not activated."
