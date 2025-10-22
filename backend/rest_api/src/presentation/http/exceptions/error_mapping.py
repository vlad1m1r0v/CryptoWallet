from typing import Union, Type

from starlette import status

from src.domain.exceptions.auth import (
    EmailAlreadyExistsException,
    EmailNotFoundException,
    UserNotFoundError,
    WrongPasswordException,
    UserNotActivatedError
)

from src.domain.exceptions.fields import (
    ValueObjectException
)

from src.infrastructure.exceptions.auth import (
    AccessTokenNotProvidedException,
    InvalidAccessTokenException
)

DOMAIN_EXCEPTION_MAP: dict[int, list[type[Exception]]] = {
    status.HTTP_400_BAD_REQUEST: [
        WrongPasswordException,
    ],
    status.HTTP_401_UNAUTHORIZED: [
        InvalidAccessTokenException,
        AccessTokenNotProvidedException
    ],
    status.HTTP_403_FORBIDDEN: [UserNotActivatedError],
    status.HTTP_404_NOT_FOUND: [
        EmailNotFoundException,
        UserNotFoundError
    ],
    status.HTTP_409_CONFLICT: [EmailAlreadyExistsException],
    status.HTTP_422_UNPROCESSABLE_CONTENT: [
        ValueObjectException
    ],
}


def get_status_code_for_exception(exc: Union[Exception, Type[Exception]]) -> int:
    """
    Повертає HTTP статус код для помилки.
    Працює як з екземплярами, так і з класами.
    """
    is_class = isinstance(exc, type)
    exc_class = exc if is_class else type(exc)

    for status_code, exc_classes in DOMAIN_EXCEPTION_MAP.items():
        if any(issubclass(exc_class, cls) for cls in exc_classes):
            return status_code

    return status.HTTP_500_INTERNAL_SERVER_ERROR
