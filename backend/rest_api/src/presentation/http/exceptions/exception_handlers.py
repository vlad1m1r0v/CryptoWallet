import typing

from pydantic import ValidationError

from starlette.requests import Request
from starlette.responses import JSONResponse

from slowapi.errors import RateLimitExceeded

from src.presentation.http.exceptions.error_mapping import get_status_code_for_exception
from src.presentation.http.exceptions.exceptions import TooManyRequestsException

from src.configs import config


def validation_error_handler(_: Request, exc: Exception) -> JSONResponse:
    exc = typing.cast(ValidationError, exc)

    errors: dict[str, list[str]] = {}

    for err in exc.errors():
        loc = err.get("loc", ())
        msg = err.get("msg", "Invalid input")

        if loc:
            if loc[0] in ("body", "form", "file"):
                field = loc[1] if len(loc) > 1 else "__model__"
            else:
                field = ".".join(str(l) for l in loc)
        else:
            field = "__model__"

        errors.setdefault(field, []).append(msg)

    return JSONResponse(
        status_code=422,
        content=errors,
        headers={
            "Access-Control-Allow-Origin": config.frontend.url,
            "Access-Control-Allow-Credentials": "true",
        }
    )


def rate_limit_error_handler(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    raise TooManyRequestsException()


def error_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=get_status_code_for_exception(exc),
        content={"description": str(exc)},
        headers={
            "Access-Control-Allow-Origin": config.frontend.url,
            "Access-Control-Allow-Credentials": "true",
        }
    )
