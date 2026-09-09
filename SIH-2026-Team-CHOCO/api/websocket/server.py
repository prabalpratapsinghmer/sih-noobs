"""WebSocket server — connection handler + message routing."""

import json

import structlog
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.auth.jwt import decode_token
from api.websocket.manager import manager

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint at /ws.

    Query param `token` = JWT access token for auth.
    """
    token = websocket.query_params.get("token", "")
    user_id = None
    role = None

    try:
        payload = decode_token(token)
        user_id = payload["sub"]
        role = payload.get("role", "")
    except Exception:
        await websocket.close(code=4401, reason="Invalid token")
        return

    await manager.connect(user_id, role, websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                msg = {"type": "ping", "data": raw}

            msg_type = msg.get("type", "ping")

            if msg_type == "ping":
                await websocket.send_json({"event": "pong"})

            elif msg_type == "subscribe":
                complaint_id = msg.get("complaint_id")
                if complaint_id:
                    manager.subscribe(user_id, complaint_id)
                    await websocket.send_json({"event": "subscribed", "complaint_id": complaint_id})

            elif msg_type == "unsubscribe":
                complaint_id = msg.get("complaint_id")
                if complaint_id:
                    manager.unsubscribe(user_id, complaint_id)
                    await websocket.send_json({"event": "unsubscribed"})

            elif msg_type == "message":
                await websocket.send_json({"event": "echo", "data": msg.get("data")})

            else:
                await websocket.send_json({"event": "unknown", "type": msg_type})

    except WebSocketDisconnect:
        await manager.disconnect(user_id, role)
    except Exception as e:
        logger.warning("ws_error", error=str(e))
        await manager.disconnect(user_id, role)
