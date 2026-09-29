from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from taximetro import settings
from taximetro.api.routes import auth, history, ride, rates
from taximetro.infrastructure.logging_setup import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.LOG_PATH)
    logging.getLogger("taximetro").info("Taximetro started")
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Taximetro API", lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        errors = [{key: error[key] for key in ("type", "loc", "msg")} for error in exc.errors()]
        return JSONResponse(status_code=422, content={"detail": errors})

    for module in (auth, ride, history, rates):
        app.include_router(module.router)
    if settings.FRONT_DIST.is_dir():
        app.mount("/", StaticFiles(directory=settings.FRONT_DIST, html=True), name="web-panel")
    return app
