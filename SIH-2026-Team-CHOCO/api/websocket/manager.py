"""WebSocket connection manager."""


import structlog
from fastapi import WebSocket

logger = structlog.get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections per user, role, and complaint subscription."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}      # user_id -> ws
        self.role_connections: dict[str, set[str]] = {}          # role -> set[user_id]
        self.complaint_subscriptions: dict[str, set[str]] = {}   # complaint_id -> set[user_id]

    async def connect(self, user_id: str, role: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.role_connections.setdefault(role, set()).add(user_id)
        logger.info("ws_connected", user_id=user_id, role=role)

    async def disconnect(self, user_id: str, role: str) -> None:
        self.active_connections.pop(user_id, None)
        if role in self.role_connections:
            self.role_connections[role].discard(user_id)
        logger.info("ws_disconnected", user_id=user_id)

    async def send_to_user(self, user_id: str, event: dict) -> bool:
        ws = self.active_connections.get(user_id)
        if ws is None:
            return False
        try:
            await ws.send_json(event)
            return True
        except Exception:
            self.active_connections.pop(user_id, None)
            return False

    async def broadcast_to_role(self, role: str, event: dict) -> int:
        count = 0
        for user_id in list(self.role_connections.get(role, set())):
            if await self.send_to_user(user_id, event):
                count += 1
        return count

    async def send_to_complaint_subscribers(self, complaint_id: str, event: dict) -> int:
        count = 0
        for user_id in list(self.complaint_subscriptions.get(complaint_id, set())):
            if await self.send_to_user(user_id, event):
                count += 1
        return count

    def subscribe(self, user_id: str, complaint_id: str) -> None:
        self.complaint_subscriptions.setdefault(complaint_id, set()).add(user_id)

    def unsubscribe(self, user_id: str, complaint_id: str) -> None:
        self.complaint_subscriptions.get(complaint_id, set()).discard(user_id)

    @property
    def connection_count(self) -> int:
        return len(self.active_connections)


manager = ConnectionManager()
