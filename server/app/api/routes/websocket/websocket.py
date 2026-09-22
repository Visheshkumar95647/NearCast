from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.routes.websocket.deps import get_current_websocket_user
from server.app.services.recommendation.websocket.manager import manager


# Create the WebSocket router
router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    auth_data=Depends(get_current_websocket_user),
):
    # Get the database session and authenticated user
    # from the WebSocket authentication dependency
    
    db, current_user = auth_data

    # Convert the user's UUID to a string because
    # ConnectionManager uses string user IDs as dictionary keys
    user_id = str(current_user.id)

    try:
        # Accept the WebSocket connection and register it
        # inside the global ConnectionManager
        await manager.connect(
            user_id=user_id,
            websocket=websocket,
        )

        # Tell the frontend that the WebSocket connection
        # has been successfully established
        await websocket.send_json(
            {
                "type": "connection",
                "status": "connected",
            }
        )

        # Keep the WebSocket connection alive
        # and wait for messages from the client
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        # A normal disconnect can happen when the user
        # closes the browser tab, refreshes the page,
        # loses the connection, or closes the app.
        #
        # We don't need to treat this as an application error.
        # The actual cleanup is handled in the finally block.
        pass

    finally:
        # Always remove this specific WebSocket connection
        # from the ConnectionManager.
        #
        # This is important when the same user has
        # multiple devices or browser tabs connected.
        manager.disconnect(
            user_id=user_id,
            websocket=websocket,
        )

        # Close the database session created
        # during WebSocket authentication.
        db.close()