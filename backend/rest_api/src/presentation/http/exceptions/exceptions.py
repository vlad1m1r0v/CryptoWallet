from src.shared import AppException


class PresentationException(AppException):
    pass


class TooManyRequestsException(PresentationException):
    message = "Rate limit exceeded."
