from starlette.requests import Request
from starlette.responses import JSONResponse

from src.presentation.http.exceptions.error_mapping import get_status_code_for_exception

from src.configs import config

def error_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=get_status_code_for_exception(exc),
        content={"description": str(exc)},
        headers={
            "Access-Control-Allow-Origin": config.frontend.url,
            "Access-Control-Allow-Credentials": "true",
        }
    )