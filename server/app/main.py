import logging

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.exceptions.handlers import register_exception_handlers
from app.middleware.cors import setup_cors

from app.api.routes.auth.auth import router as auth_router

from app.api.routes.user.user import router as user_router

from app.api.routes.activity.activity import router as activity_router
from app.api.routes.activity.activity_location import router as activity_location_router
from app.api.routes.activity.activity_participant import router as activity_participant_router
from app.api.routes.activity.saved_activity import router as saved_activity_router
from app.api.routes.activity.activity_interaction import router as activity_interaction_router

from app.api.routes.group.group import router as group_router
from app.api.routes.group.group_location import router as group_location_router
from app.api.routes.group.group_member import router as group_member_router
from app.api.routes.group.join_request import router as join_request_router
from app.api.routes.group.broadcast import router as broadcast_router

from app.api.routes.websocket.websocket import router as websocket_router
from app.api.routes.websocket.chat import router as chat_websocket_router

from app.api.routes.chat.chat import router as chat_router
from app.api.routes.chat.message import router as message_router
from app.api.routes.chat.poll import router as poll_router

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
app.include_router(user_router)
app.include_router(activity_router)
app.include_router(activity_location_router)
app.include_router(activity_participant_router)
app.include_router(saved_activity_router)
app.include_router(activity_interaction_router)
app.include_router(group_router)
app.include_router(group_location_router)
app.include_router(group_member_router)
app.include_router(join_request_router)
app.include_router(broadcast_router)

app.include_router(websocket_router)
app.include_router(chat_websocket_router)

app.include_router(chat_router)
app.include_router(message_router)
app.include_router(poll_router)