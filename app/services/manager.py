from typing import Dict
from fastapi import WebSocket
import asyncio
from ..configs.log import logger

class ContractManager():

    def __init__(self):
        self.active_connection: Dict[str,WebSocket]={}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept and register a new WebSocket client."""
        async with self.lock:
            self.active_connection[client_id] = websocket
            logger.info(f"Client connected: {client_id}")
            await websocket.send_json({
                "type": "connection",
                "status": "confirmed",
                "client_id": client_id
            })

    async def disconnect(self, client_id: str):
        """Remove a client from the active connections."""
        async with self.lock:
            if client_id in self.active_connection:
                del self.active_connection[client_id]
                logger.info(f"Client disconnected: {client_id}")

    async def broadcast(self, message: dict):
        """Send a message to all connected clients"""
        async with self.lock:
            successful = 0
            dead_connections = []
            for client_id, connection in self.active_connection.items():
                try:
                    await connection.send_json(message)
                    successful += 1
                except Exception as e:
                    logger.error(f"Failed to send to {client_id}: {e}")
                    dead_connections.append(client_id)
            for client_id in dead_connections:
                await self.disconnect(client_id)
            return successful
manager = ContractManager()