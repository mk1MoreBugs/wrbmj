from typing import Any

from fastapi.websockets import WebSocket

import logging

class WsConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        logging.info(f"➕ Connected: {websocket.url}. Total: {len(self.active_connections)}")


    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

        logging.info(f"➖ Disconnected: {websocket.url}. Total: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict[str, str], websocket: WebSocket):
        await websocket.send_text(message)


    async def broadcast(self, message: Any):
        for connection in self.active_connections:
            await connection.send_text(message)

            logger = logging.getLogger(__name__)
            logging.info(f"Broadcast to {len(self.active_connections)} clients")

ws_connection_manager = WsConnectionManager()
