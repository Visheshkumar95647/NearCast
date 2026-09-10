import logging

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.exceptions.handlers import register_exception_handlers
from app.middleware.cors import setup_cors
from app.api.routes.auth import router as auth_router

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nearby API",
    description="Privacy-first hyperlocal social discovery platform",
    version="0.1.0",
)

setup_cors(app)

register_exception_handlers(app)


@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": "nearby-api",
    }

app.include_router(auth_router)