import typing

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.utils import is_body_allowed_for_status_code
from pydantic import ValidationError
from starlette.background import BackgroundTask
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_417_EXPECTATION_FAILED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from starlette.types import Receive, Scope, Send

from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.utils.translation import i18n as _

try:
    import ujson
    from fastapi.responses import UJSONResponse as JSONResponse
except ImportError:
    ujson = None
    from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI, **kwargs):
    """global exception catch"""
    app.add_exception_handler(RequestValidationError, handler=request_validation_exception_handler)
    app.add_exception_handler(HTTPException, handler=http_exception_handler)
    app.add_exception_handler(ValidationException, handler=inner_validation_exception_handler)
    app.add_exception_handler(ValidationError, handler=inner_validation_exception_handler)
    app.add_exception_handler(Exception, handler=server_error_handler)


class JSONResponseWithException(JSONResponse):
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
        exc: Exception = None,
    ) -> None:
        self.exc = exc
        super().__init__(content, status_code, headers, media_type, background)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)
        if self.exc is not None:
            raise self.exc


def make_error_response(status: int, msg="", *, exc: Exception = None, **extra):
    """Construct an error response"""
    result = BaseApiOut(status=status, msg=msg, **extra)
    return JSONResponseWithException(content=result.dict(), exc=exc)


async def http_exception_handler(request: Request, exc: HTTPException):
    """http exception"""
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    content = getattr(exc, "content", {"status": exc.status_code, "msg": exc.detail})
    return JSONResponse(content=content, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Request parameter validation exception"""
    return make_error_response(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        msg=_("Request parameter validation exception"),
        body=exc.body,
        errors=exc.errors(),
    )


async def inner_validation_exception_handler(request: Request, exc: typing.Union[ValidationException, ValidationError]):
    """Internal data validation exception.Output a json response and throw the exception again."""
    return make_error_response(
        status=HTTP_417_EXPECTATION_FAILED,
        msg=_("Internal data validation exception"),
        errors=exc.errors(),
        exc=exc,
    )


async def server_error_handler(request: Request, exc: Exception):
    """Internal server exception.Output a json response and throw the exception again."""
    return make_error_response(
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        msg=_("Internal server exception"),
        exc=exc,
    )
