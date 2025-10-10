from src.domain.exceptions.base import DomainError
from src.domain.value_objects.email import Email


class EmailAlreadyExistsError(DomainError):
    def __init__(self, email: Email):
        message = f"User with email {email.value!r} already exists."
        super().__init__(message)


class EmailNotFoundError(DomainError):
    def __init__(self, email: Email):
        message = f"User with email {email.value!r} is not found."
        super().__init__(message)


class UserNotFoundError(DomainError):
    def __init__(self):
        message = f"User not found."
        super().__init__(message)


class PasswordsNotMatchError(DomainError):
    def __init__(self) -> None:
        message = f"Passwords do not match."
        super().__init__(message)


class RepeatPasswordIsNotSetError(DomainError):
    def __init__(self) -> None:
        message = f"Repeat password is not set."
        super().__init__(message)


class UserNotActivatedError(DomainError):
    def __init__(self) -> None:
        message = f"User is not activated."
        super().__init__(message)
