import typing
import fastapi
from starlette.types import Receive, Scope, Send

from . import error, errors, util


__all__ = ["error_handler", "default_handler", "validation_error_handler"]


def error_handler(_: typing.Any, exc: error.APIError):
    return exc.response


async def default_handler(scope: Scope, receive: Receive, send: Send):
    await errors.endpoint_not_found(extra=scope).response(scope, receive, send)


def validation_error_handler(
    _: fastapi.Request, exc: fastapi.exceptions.RequestValidationError
):
    formatted_error = util.pydantic.format_error(exc)

    return fastapi.responses.JSONResponse(
        formatted_error,
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
