from src.infrastructure.exceptions.base import InfrastructureError


class AccessTokenNotProvidedError(InfrastructureError):
    def __init__(self) -> None:
        message = f"Access token is not provided."
        super().__init__(message)


class InvalidAccessTokenError(InfrastructureError):
    def __init__(self) -> None:
        message = f"Provided access token is invalid."
        super().__init__(message)
