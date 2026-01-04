from fastapi import Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.response import StandardResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    error_messages = []
    for error in exc.errors():
        loc = [str(x) for x in error["loc"] if x != "body"]
        field = ".".join(loc)
        msg = error["msg"]
        error_messages.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardResponse(
            success=False,
            message="Error in data validation",
            data={"errors": error_messages},
        ).model_dump(),
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            success=False, message=str(exc.detail), data=None
        ).model_dump(),
    )


async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=StandardResponse(
            success=False,
            message="Data conflict. Duplicated possible register",
            # TODO em produção cuidado ao expor exc.orig
            data=str(exc.orig),
        ).model_dump(),
    )


async def database_error_handler(
    request: Request,
    exc: SQLAlchemyError
) -> JSONResponse:
    # TODO adicionar logger
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=StandardResponse(
            success=False,
            message="Database error occurred, please try again later.",
            data=None,
        ).model_dump(),
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    # TODO adicionar logger
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=StandardResponse(
            success=False,
            message="An unexpected error occurred. Please try again later.",
            data=None,
        ).model_dump(),
    )


def configure_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError, validation_exception_handler  # type: ignore
    )
    app.add_exception_handler(
        StarletteHTTPException, http_exception_handler  # type: ignore
    )
    app.add_exception_handler(
        IntegrityError, integrity_error_handler  # type: ignore
    )
    app.add_exception_handler(
        SQLAlchemyError, database_error_handler  # type: ignore
    )
    app.add_exception_handler(
        Exception, general_exception_handler  # type: ignore
    )
