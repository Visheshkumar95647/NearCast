from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user.user import User
from app.services.auth.auth_service import AuthService


auth_service = AuthService()


async def get_current_websocket_user(
    websocket: WebSocket,
) -> tuple[Session, User]:

    token = websocket.cookies.get("access_token")

    if not token:
        await websocket.close(code=1008)
        raise RuntimeError("Authentication required")

    db = SessionLocal()

    try:
        current_user = auth_service.get_current_user(
            db=db,
            token=token,
        )

        return db, current_user

    except Exception:
        db.close()
        await websocket.close(code=1008)
        raise