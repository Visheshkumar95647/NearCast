from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.routes.websocket.chat_deps import get_current_chat_websocket_user
from app.websocket.manager import manager


router = APIRouter(
    prefix="/ws/chat",
    tags=["Chat WebSocket"],
)


@router.websocket("/{chat_id}")
async def chat_websocket_endpoint(
    websocket: WebSocket,
    chat_id: str,
    current_user=Depends(get_current_chat_websocket_user),
):
    user_id = str(current_user.id)

    try:
        await manager.connect(
            user_id=user_id,
            websocket=websocket,
        )

        await websocket.send_json(
            {
                "type": "chat_connection",
                "status": "connected",
                "chat_id": chat_id,
            }
        )

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(
            user_id=user_id,
            websocket=websocket,
        )