from starlette import status

from src.domain.exceptions.user import (
    EmailAlreadyExistsError,
    EmailNotFoundError,
    PasswordsNotMatchError,
    RepeatPasswordIsNotSetError,
    UserNotActivatedError,
    UserNotFoundError
)
from src.domain.exceptions.base import DomainFieldError

from src.infrastructure.exceptions.auth import (
    AccessTokenNotProvidedError,
    InvalidAccessTokenError
)

DOMAIN_EXCEPTION_MAP: dict[int, list[type[Exception]]] = {
    status.HTTP_400_BAD_REQUEST: [PasswordsNotMatchError, RepeatPasswordIsNotSetError],
    status.HTTP_401_UNAUTHORIZED: [InvalidAccessTokenError, AccessTokenNotProvidedError],
    status.HTTP_403_FORBIDDEN: [UserNotActivatedError],
    status.HTTP_404_NOT_FOUND: [EmailNotFoundError, UserNotFoundError],
    status.HTTP_409_CONFLICT: [EmailAlreadyExistsError],
    status.HTTP_422_UNPROCESSABLE_CONTENT: [DomainFieldError],
}


def get_status_code_for_exception(exc: Exception) -> int:
    """
    Повертає статус код на основі класу помилки.
    Якщо не знайдено — повертає HTTP_400_BAD_REQUEST.
    """
    for status_code, exc_classes in DOMAIN_EXCEPTION_MAP.items():
        for exc_class in exc_classes:
            if isinstance(exc, exc_class):
                return status_code

    return status.HTTP_500_INTERNAL_SERVER_ERROR
