from src.infrastructure.exceptions.base import InfrastructureError


class AccessTokenNotProvidedError(InfrastructureError):
    message = f"Access token is not provided."


class InvalidAccessTokenError(InfrastructureError):
    message = f"Provided access token is invalid."
