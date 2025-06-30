from typing import Any, Callable

from fastapi import FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class TODOErrors(Exception):
    "Base class for all TODO-related exceptions."

    pass


class InvalidToken(TODOErrors):
    pass


class TokenNotFound(TODOErrors):
    pass


class UserNotFound(TODOErrors):
    pass


class UserAlreadyExists(TODOErrors):
    pass


class InvalidCredentials(TODOErrors):
    pass


class AccessTokenRequired(TODOErrors):
    pass


class RefreshTokenRequired(TODOErrors):
    pass


class TODONotFound(TODOErrors):
    pass


def create_exception_handler(
    status_code: int, detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    """
    Factory function to create an exception handler that returns a JSON response.

    Args:
        status_code (int): The HTTP status code for the response.
        detail (Any): The detail message to include in the response.

    Returns:
        Callable[[Request, Exception], JSONResponse]: The exception handler function.
    """

    def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(detail)})

    return exception_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Token is invalid Or expired",
                "error_code": "Please get a new token",
                "resolution": "Please get a new token",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid credentials provided",
                "error_code": "InvalidCredentials",
                "resolution": "Please check your credentials and try again",
            },
        ),
    )

    app.add_exception_handler(
        TODONotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Todo item not found",
                "error_code": "TODONotFound",
                "resolution": "Please check the todo ID and try again",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Todo item not found",
                "error_code": "TODONotFound",
                "resolution": "Please check the todo ID and try again",
            },
        ),
    )
