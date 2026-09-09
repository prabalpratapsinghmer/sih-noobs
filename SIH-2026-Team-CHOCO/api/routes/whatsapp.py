"""WhatsApp routes — Meta webhook verification + message processing."""

from fastapi import APIRouter, HTTPException, Request

from api.config import get_settings
from api.services.whatsapp import process_incoming, verify_webhook

router = APIRouter()
settings = get_settings()


@router.get("/webhook")
async def webhook_verify(hub_mode: str | None = None, hub_verify_token: str | None = None,
                         hub_challenge: str | None = None):
    """Meta webhook verification (challenge response)."""
    if hub_mode == "subscribe" and verify_webhook(hub_verify_token or "", settings.whatsapp_webhook_verify_token):
        return {"hub.challenge": hub_challenge}
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def webhook_message(request: Request):
    """Receive and process incoming WhatsApp messages."""
    payload = await request.json()
    entries = payload.get("entry", [])
    replies = []

    for entry in entries:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for contact in value.get("contacts", []):
                phone = contact.get("wa_id", "")
                messages = value.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "text":
                        text = msg.get("text", {}).get("body", "")
                        reply = await process_incoming(phone, text)
                        replies.append({"phone": phone, "reply": reply})

    if not replies:
        return {"status": "ignored"}

    # In dev, just log replies (sending back via Meta API needs real token)
    import structlog
    logger = structlog.get_logger(__name__)
    for r in replies:
        logger.info("[MOCK WHATSAPP REPLY]", phone=r["phone"], reply=r["reply"])

    return {"status": "received", "processed": len(replies)}
