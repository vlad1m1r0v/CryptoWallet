from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.presentation.http.exceptions.error_mapping import get_status_code_for_exception

from src.configs import config


def request_validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors: dict[str, list[str]] = {}

    for err in exc.errors():
        loc = err.get("loc", ())
        msg = err.get("msg", "Invalid input")

        # якщо це поле з body
        if loc and loc[0] == "body":
            if len(loc) > 1:
                field = loc[1]
            else:
                # глобальна помилка, пов'язана з моделлю (after validator)
                field = "__model__"
            errors.setdefault(field, []).append(msg)
        else:
            # інші локації (query, path, header)
            field = ".".join(str(l) for l in loc)
            errors.setdefault(field, []).append(msg)

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
