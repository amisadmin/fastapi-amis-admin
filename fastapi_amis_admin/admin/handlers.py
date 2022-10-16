import logging
import traceback
from typing import Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import ClientDisconnect, Request
from starlette.responses import Response
from starlette.status import (
    HTTP_417_EXPECTATION_FAILED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from fastapi_amis_admin.crud import BaseApiOut

try:
    from fastapi.utils import is_body_allowed_for_status_code
except ImportError:  # fastapi < 0.83.0

    def is_body_allowed_for_status_code(status_code: Union[int, str, None]) -> bool:
        if status_code is None:
            return True
        current_status_code = int(status_code)
        return not (current_status_code < 200 or current_status_code in {204, 304})


try:
    import ujson
    from fastapi.responses import UJSONResponse as JSONResponse
except ImportError:
    ujson = None
    from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI, logger: logging.Logger = None):
    """global exception catch"""
    app.add_exception_handler(
        ValidationError,
        handler=log_exception(logging.ERROR, logger)(inner_validation_exception_handler),
    )
    app.add_exception_handler(
        RequestValidationError,
        handler=log_exception(logging.WARNING, logger)(request_validation_exception_handler),
    )
    app.add_exception_handler(HTTPException, handler=http_exception_handler)
    app.add_exception_handler(Exception, handler=log_exception(logging.ERROR, logger)(all_exception_handler))


def log_exception(level: Union[int, str] = logging.ERROR, logger: logging.Logger = None):
    """The decorator outputs exception information to the log"""
    logger = logger or logging.getLogger("fastapi_amis_admin")

    def wrapper(func):
        async def function(request: Request, exc: Exception):
            if isinstance(
                exc,
                (
                    ClientDisconnect,
                    Warning,
                ),
            ):  # Ignore client disconnection; ignore warnings for now
                return None
            logger.log(level, f"Error: {exc}\nTraceback: {traceback.format_exc()}")
            return await func(request, exc)

        return function

    return wrapper


def make_error_response(status: int, msg="", **extra):
    """Construct an error response"""
    result = BaseApiOut(status=status, msg=msg, **extra)
    return JSONResponse(content=result.dict())


async def http_exception_handler(request: Request, exc: HTTPException):
    """http exception"""
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    result = BaseApiOut(status=exc.status_code, msg=exc.detail).dict()
    return JSONResponse(result, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Request parameter validation exception"""
    return make_error_response(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        body=exc.body,
        errors=exc.errors(),
    )


async def inner_validation_exception_handler(request: Request, exc: ValidationError):
    """Internal parameter validation exception"""
    return make_error_response(status=HTTP_417_EXPECTATION_FAILED, errors=exc.errors())


async def all_exception_handler(request: Request, exc: Exception):
    """All exceptions"""
    return Response(status_code=HTTP_500_INTERNAL_SERVER_ERROR)
