"""WhatsApp Business API webhook handler for SIH26184.

Handles incoming WhatsApp messages, detects intent using the LLM service,
generates appropriate responses, and sends them back through the WhatsApp
Business API.

In production this would be deployed behind a public HTTPS endpoint that
WhatsApp Cloud API calls for webhook verification and message delivery.
"""

import os
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Optional

import httpx
from fastapi import APIRouter, Request, HTTPException, Query
from loguru import logger

from api.llm_integration import get_llm_service

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

# WhatsApp Cloud API settings
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "sih26184_verify")
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")


# In-memory conversation state (use Redis in production)
_conversations: Dict[str, Dict] = {}


# --------------------------------------------------------------------------
# Webhook verification (GET /whatsapp/webhook)
# --------------------------------------------------------------------------

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """WhatsApp webhook verification endpoint.

    Meta sends a GET request with a challenge token during webhook setup.
    We must respond with the challenge to complete verification.
    """
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified successfully")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


# --------------------------------------------------------------------------
# Incoming messages (POST /whatsapp/webhook)
# --------------------------------------------------------------------------

@router.post("/webhook")
async def receive_message(request: Request):
    """Handle incoming WhatsApp messages.

    Processes the webhook payload, extracts the user message, detects intent,
    generates a response, and sends it back.
    """
    body = await request.json()

    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no messages"}

        message = messages[0]
        sender = message.get("from", "")
        msg_type = message.get("type", "")
        msg_body = ""

        if msg_type == "text":
            msg_body = message.get("text", {}).get("body", "")
        elif msg_type == "interactive":
            interactive = message.get("interactive", {})
            msg_body = (
                interactive.get("button_reply", {}).get("title", "")
                or interactive.get("list_reply", {}).get("title", "")
            )
        else:
            msg_body = f"[{msg_type} message received]"

        logger.info(f"WhatsApp message from {sender}: {msg_body}")

        # Process message
        response_text = await _process_message(sender, msg_body)

        # Send reply
        await _send_text_message(sender, response_text)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        return {"status": "error", "detail": str(e)}


# --------------------------------------------------------------------------
# Message processing
# --------------------------------------------------------------------------

async def _process_message(sender: str, message: str) -> str:
    """Process an incoming message and generate a response."""
    llm_service = get_llm_service()

    # Detect intent
    intent, confidence = llm_service.detect_intent(message)
    logger.info(f"Intent: {intent} (confidence: {confidence})")

    # Maintain conversation state
    if sender not in _conversations:
        _conversations[sender] = {
            "started_at": datetime.utcnow().isoformat(),
            "messages": [],
            "current_intent": None,
            "complaint_data": {},
        }

    conversation = _conversations[sender]
    conversation["messages"].append({
        "role": "user",
        "content": message,
        "timestamp": datetime.utcnow().isoformat(),
        "intent": intent,
    })
    conversation["current_intent"] = intent

    # Generate response
    context = {
        "conversation_length": len(conversation["messages"]),
        "current_intent": intent,
        "complaint_data": conversation.get("complaint_data", {}),
    }
    response = llm_service.generate_response(message, intent, context)

    conversation["messages"].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return response


# --------------------------------------------------------------------------
# WhatsApp Cloud API helpers
# --------------------------------------------------------------------------

async def _send_text_message(to: str, text: str) -> bool:
    """Send a text message via WhatsApp Business Cloud API.

    Returns True if sent successfully or if running in mock mode.
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        logger.debug(f"WhatsApp mock reply to {to}: {text[:80]}...")
        return True

    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                logger.info(f"WhatsApp message sent to {to}")
                return True
            logger.error(f"WhatsApp API error: {resp.status_code} — {resp.text}")
            return False
    except Exception as e:
        logger.error(f"WhatsApp send error: {e}")
        return False
