from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
)

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


def make_error_response(status: int, msg="", **extra):
    """Construct an error response"""
    result = BaseApiOut(status=status, msg=msg, **extra)
    return JSONResponse(content=result.dict())


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
        msg=_("Request parameter validation error"),
        body=exc.body,
        errors=exc.errors(),
    )
