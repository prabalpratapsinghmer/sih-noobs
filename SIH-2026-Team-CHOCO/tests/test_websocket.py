"""WebSocket tests: connection manager unit tests (no live server needed)."""

import pytest

from api.websocket.manager import ConnectionManager


class FakeWS:
    def __init__(self):
        self.sent = []
        self.closed = False

    async def accept(self):
        pass

    async def send_json(self, event):
        self.sent.append(event)

    async def close(self, code=None, reason=None):
        self.closed = True


@pytest.fixture
def manager():
    return ConnectionManager()


async def test_connect_and_count(manager):
    ws = FakeWS()
    await manager.connect("u1", "INSPECTOR", ws)
    assert manager.connection_count == 1
    assert "u1" in manager.role_connections["INSPECTOR"]


async def test_send_to_user(manager):
    ws = FakeWS()
    await manager.connect("u1", "INSPECTOR", ws)
    ok = await manager.send_to_user("u1", {"event": "notification.new"})
    assert ok
    assert ws.sent == [{"event": "notification.new"}]


async def test_send_to_missing_user(manager):
    ok = await manager.send_to_user("ghost", {"event": "x"})
    assert not ok


async def test_broadcast_to_role(manager):
    ws1, ws2 = FakeWS(), FakeWS()
    await manager.connect("u1", "INSPECTOR", ws1)
    await manager.connect("u2", "INSPECTOR", ws2)
    await manager.connect("u3", "CONSTABLE", FakeWS())
    count = await manager.broadcast_to_role("INSPECTOR", {"event": "atm.alert"})
    assert count == 2
    assert ws1.sent and ws2.sent


async def test_subscribe_and_notify(manager):
    ws = FakeWS()
    await manager.connect("u1", "VICTIM", ws)
    manager.subscribe("u1", "CMP-1")
    count = await manager.send_to_complaint_subscribers("CMP-1", {"event": "complaint.status_changed"})
    assert count == 1
    assert ws.sent


async def test_unsubscribe(manager):
    ws = FakeWS()
    await manager.connect("u1", "VICTIM", ws)
    manager.subscribe("u1", "CMP-1")
    manager.unsubscribe("u1", "CMP-1")
    count = await manager.send_to_complaint_subscribers("CMP-1", {"event": "x"})
    assert count == 0
