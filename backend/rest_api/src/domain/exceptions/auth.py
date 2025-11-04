from string import Template

from src.domain.exceptions.base import DomainException

from src.domain.value_objects import Email


class EmailAlreadyExistsException(DomainException):
    message = Template("User with email '$email' already exists.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class EmailNotFoundException(DomainException):
    message = Template("User with email '$email' is not found.")
    example_args = {"email": "user@domain.com"}

    def __init__(self, email: Email):
        super().__init__(email=email.value)


class WrongPasswordException(DomainException):
    message = f"Wrong Password."


class UserNotFoundException(DomainException):
    message = f"User not found."


class UserNotActivatedException(DomainException):
    message = f"User is not activated."
