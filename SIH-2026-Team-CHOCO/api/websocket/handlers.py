"""WebSocket event handlers — helpers to push domain events."""


from api.websocket.manager import manager


async def push_complaint_status(complaint_id: str, new_status: str) -> int:
    return await manager.send_to_complaint_subscribers(
        complaint_id,
        {"event": "complaint.status_changed",
         "payload": {"complaint_id": complaint_id, "new_status": new_status}},
    )


async def push_atm_alert(atm_id: str, probability: float, time_window: float) -> int:
    from api.websocket.manager import manager
    count = 0
    for role in ("INSPECTOR", "CONSTABLE"):
        count += await manager.broadcast_to_role(
            role,
            {"event": "atm.alert",
             "payload": {"atm_id": atm_id, "probability": probability, "time_window": time_window}},
        )
    return count


async def push_mule_detected(account_id: str, score: float, risk_level: str) -> int:
    return await manager.broadcast_to_role(
        "INSPECTOR",
        {"event": "mule.detected",
         "payload": {"account_id": account_id, "score": score, "risk_level": risk_level}},
    )


async def push_verification_result(verification_id: str, status: str, officer_id: str | None = None) -> int:
    if officer_id:
        return 1 if await manager.send_to_user(
            officer_id,
            {"event": "verification.result",
             "payload": {"verification_id": verification_id, "status": status}},
        ) else 0
    return 0
