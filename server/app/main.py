import logging

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.exceptions.handlers import register_exception_handlers


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nearby API",
    description="Privacy-first hyperlocal social discovery platform",
    version="0.1.0",
)

register_exception_handlers(app)


@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": "nearby-api",
    }