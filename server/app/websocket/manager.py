from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        # Store multiple WebSocket connections for each user
        self.active_connections: dict[str, set[WebSocket]] = {}

    # Connect a user's device or browser tab
    async def connect(
        self,
        user_id: str,
        websocket: WebSocket,
    ) -> None:

        await websocket.accept()

        # Create a connection set for the user if it doesn't exist
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()

        # Add the new connection
        self.active_connections[user_id].add(websocket)

    # Disconnect a specific device or browser tab
    def disconnect(
        self,
        user_id: str,
        websocket: WebSocket,
    ) -> None:

        connections = self.active_connections.get(user_id)

        if not connections:
            return

        # Remove only this specific connection
        connections.discard(websocket)

        # Remove the user if no connections remain
        if not connections:
            self.active_connections.pop(user_id, None)

    # Send a message to all connected devices of one user
    async def send_to_user(
        self,
        user_id: str,
        message: dict,
    ) -> None:

        connections = self.active_connections.get(user_id)

        if not connections:
            return

        disconnected_connections = set()

        # Try to send the message to every connection
        for websocket in connections:
            try:
                await websocket.send_json(message)

            except Exception:
                # Mark failed connections for removal
                disconnected_connections.add(websocket)

        # Remove dead connections
        for websocket in disconnected_connections:
            connections.discard(websocket)

        # Remove the user if no connections remain
        if not connections:
            self.active_connections.pop(user_id, None)

    # Send a message to multiple users
    async def send_to_users(
        self,
        user_ids: list[str],
        message: dict,
    ) -> None:

        # Send the message to each user's connected devices
        for user_id in user_ids:
            try:
                await self.send_to_user(
                    user_id=user_id,
                    message=message,
                )

            except Exception:
                continue


# Create the global connection manager
manager = ConnectionManager()