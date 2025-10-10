import typing

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.presentation.http.exceptions.error_mapping import get_status_code_for_exception

from src.configs import config


def request_validation_error_handler(_: Request, exc: Exception) -> JSONResponse:
    exc = typing.cast(RequestValidationError, exc)

    errors: dict[str, list[str]] = {}

    for err in exc.errors():
        loc = err.get("loc", [])
        if len(loc) >= 2 and loc[0] == "body":
            field = loc[1]
            errors.setdefault(field, []).append(err.get("msg", "Invalid input"))

    return JSONResponse(
        status_code=422,
        content=errors,
        headers={
            "Access-Control-Allow-Origin": config.frontend.url,
            "Access-Control-Allow-Credentials": "true",
        }
    )


def error_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=get_status_code_for_exception(exc),
        content={"description": str(exc)},
        headers={
            "Access-Control-Allow-Origin": config.frontend.url,
            "Access-Control-Allow-Credentials": "true",
        }
    )
