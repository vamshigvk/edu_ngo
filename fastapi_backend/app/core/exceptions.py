"""Custom exceptions and centralized exception handlers.

All errors are rendered as a consistent JSON envelope: ``{"error": {...}}``.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppError(Exception):
    """Base class for domain/business-rule errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND


class ValidationError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT


class AuthError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN


def _envelope(status_code: int, message, details=None) -> JSONResponse:
    payload: dict = {"error": {"code": status_code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=payload)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach JSON exception handlers to the FastAPI app."""

    @app.exception_handler(AppError)
    async def _app_error_handler(_: Request, exc: AppError):
        return _envelope(exc.status_code, exc.message)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error_handler(_: Request, exc: StarletteHTTPException):
        return _envelope(exc.status_code, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def _validation_error_handler(_: Request, exc: RequestValidationError):
        return _envelope(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Request validation failed.",
            details=exc.errors(),
        )
