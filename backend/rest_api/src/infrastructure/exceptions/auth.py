from src.infrastructure.exceptions.base import InfrastructureException


class AccessTokenNotProvidedException(InfrastructureException):
    message = f"Access token is not provided."


class InvalidAccessTokenException(InfrastructureException):
    message = f"Provided access token is invalid."
