from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import AuthFailedCredential,ResourceNotFoundError,ResourceExistedError
from core.logger import logger

def register_handlers(app: FastAPI):
    @app.exception_handler(AuthFailedCredential)
    async def auth_failed_credential_handler(request: Request, exc: AuthFailedCredential):
        logger.info(
            "%s %s - invalid credential",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=401,
            content={
                "error": "INVALID_CREDENTIAL",
                "message": str(exc),
            },
        )

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
        logger.info(
            "%s %s - %s not found (id=%s)",
            request.method,
            request.url.path,
            exc.resource,
            exc.identifier,
        )
        return JSONResponse(
            status_code=404,
            content={
                "error": "NOT_FOUND",
                "resource": exc.resource,
                "message": str(exc),
            },
        )

    @app.exception_handler(ResourceExistedError)
    async def resource_existed_handler(request: Request, exc: ResourceExistedError):
        logger.info(
            "%s %s - %s existed (id=%s)",
            request.method,
            request.url.path,
            exc.resource,
            exc.identifier,
        )
        return JSONResponse(
            status_code=409,
            content={
                "error": "EXISTED",
                "resource": exc.resource,
                "message": str(exc),
            },
        )

    @app.exception_handler(Exception)
    async def general_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")  # includes traceback
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )