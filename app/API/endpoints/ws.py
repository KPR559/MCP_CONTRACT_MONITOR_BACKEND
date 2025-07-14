from fastapi import WebSocket, WebSocketDisconnect
from ...services.manager import manager
from ...configs.log import logger
import uuid,asyncio
import json
from datetime import datetime
from fastapi import APIRouter

# Create a new router for WebSocket endpoints
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Calling websocket.accept() in ws.py endpoint")
    await websocket.accept()
    """WebSocket endpoint for real-time contract updates."""
    client_id = str(uuid.uuid4())
    try:
        await manager.connect(websocket, client_id)
        logger.info(f"Client {client_id} connected to WebSocket")
        async def keep_alive():
            """Send periodic heartbeat messages to keep the connection alive."""
            while True:
                await asyncio.sleep(25)
                try:
                    heartbeat_msg = {
                        "type": "heartbeat",
                        "timestamp": datetime.now().isoformat(),
                        "client_id": client_id
                    }
                    await websocket.send_json(heartbeat_msg)
                except Exception as e:
                    logger.warning(f"Heartbeat failed for {client_id}: {e}")
                    break
        heartbeat_task = asyncio.create_task(keep_alive())
        
        # Main message handling loop
        while True:
            try:
                data = await websocket.receive_text()
                try:
                    message_data = json.loads(data)
                    msg_type = message_data.get("type", "unknown")
                    if msg_type == "heartbeat":
                        continue
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client {client_id}: {data}")
                        
            except WebSocketDisconnect:
                logger.info(f"Client {client_id} disconnected")
                break
            except Exception as e:
                logger.error(f"Error handling message from {client_id}: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
    finally:
        if 'heartbeat_task' in locals():
            heartbeat_task.cancel()
        await manager.disconnect(client_id)
        logger.info(f"Client {client_id} cleanup completed")
