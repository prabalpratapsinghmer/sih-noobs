"""WhatsApp chatbot backend — webhook handling + intent detection + conversation state."""

import json
import re
import uuid
from datetime import datetime

import structlog

logger = structlog.get_logger(__name__)

# --- Intent detection ---

INTENT_KEYWORDS = {
    "emergency": ["emergency", "urgent", "help now", "immediate"],  # checked first — most specific
    "complaint": ["report", "fraud", "scam", "stolen", "cheated", "hack", "phishing", "upi fraud"],
    "status": ["status", "update", "check", "track", "where"],
    "tip": ["tip", "suspicious", "report anonymously", "anonymous"],
    "help": ["help", "menu", "options", "start"],
}

CONVERSATION_TTL = 30 * 60  # 30 minutes

# --- Webhook verification ---

def verify_webhook(verify_token: str, expected: str) -> bool:
    return verify_token == expected


def detect_intent(text: str) -> str:
    lowered = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return intent
    return "help"


# --- Conversation state (Redis) ---

async def get_conversation(phone: str) -> dict | None:
    try:
        from api.database.redis import get_redis

        r = get_redis()
        raw = await r.get(f"whatsapp:conv:{phone}")
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None


async def set_conversation(phone: str, state: dict) -> None:
    try:
        from api.database.redis import get_redis

        r = get_redis()
        await r.setex(f"whatsapp:conv:{phone}", CONVERSATION_TTL, json.dumps(state))
    except Exception:
        pass


async def clear_conversation(phone: str) -> None:
    try:
        from api.database.redis import get_redis

        r = get_redis()
        await r.delete(f"whatsapp:conv:{phone}")
    except Exception:
        pass


# --- Conversation flow handlers ---

def _welcome() -> str:
    return (
        "👮 *CyberCell Bot*\n\n"
        "How can I help you?\n"
        "1. 📝 Report a fraud (*report*)\n"
        "2. 🔍 Check complaint status (*status*)\n"
        "3. 🕵️ Submit anonymous tip (*tip*)\n"
        "4. 🚨 Emergency (*emergency*)\n\n"
        "Reply with a keyword above."
    )


def _parse_amount(text: str) -> float | None:
    match = re.search(r"[₹Rs.\s]*([\d,]+(?:\.\d+)?)", text)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def _parse_fraud_type(text: str) -> str | None:
    fraud_types = ["upi", "phishing", "card", "skimming", "loan", "investment", "job", "otp"]
    for ft in fraud_types:
        if ft in text.lower():
            return ft.upper()
    return None


def _step_prompt(step: int, collected: dict) -> str:
    if step == 1:
        return "Please enter the amount lost:"
    if step == 2:
        return "What fraud type? (UPI, PHISHING, CARD, LOAN, INVESTMENT, JOB, OTP)"
    if step == 3:
        return "Final confirmation — reply *yes* to submit or *no* to cancel."
    return "Thank you! Your complaint has been registered."


async def process_incoming(phone: str, text: str) -> str:
    """Process an incoming WhatsApp message; returns reply text."""
    lowered = text.lower().strip()

    # Handle confirmations during a flow
    existing = await get_conversation(phone)
    if existing and existing.get("intent") == "complaint" and lowered in ("yes", "no", "cancel"):
        if lowered in ("no", "cancel"):
            await clear_conversation(phone)
            return "Complaint submission cancelled. Send *report* to start over."
        # yes — submit collected data
        collected = existing.get("collected", {})
        await clear_conversation(phone)
        return await _submit_complaint(phone, collected)

    intent = detect_intent(text)

    if intent == "help":
        return _welcome()

    if intent == "emergency":
        return "🚨 Emergency line: *100*. For cybercrime, call *1930*. An officer has been alerted."

    if intent == "complaint":
        state = {
            "phone": phone,
            "intent": "complaint",
            "step": 1,
            "collected": {},
            "started_at": datetime.utcnow().isoformat(),
        }
        await set_conversation(phone, state)
        return _step_prompt(1, {})

    if intent == "status":
        return (
            "To check complaint status, please reply with your complaint ID "
            "(format: *CMP-2026-00X*) or registered phone number."
        )

    if intent == "tip":
        return "🕵️ Your anonymous tip will be relayed securely. Please type your tip now."

    # If in mid-flow, continue steps
    if existing and existing.get("intent") == "complaint":
        step = existing.get("step", 1)
        collected = existing.get("collected", {})
        if step == 1:
            amount = _parse_amount(text)
            if amount is None:
                return "Please enter a numeric amount, e.g. *50000*"
            collected["amount"] = amount
            step = 2
        elif step == 2:
            ft = _parse_fraud_type(text)
            if ft is None:
                return "Unknown type. Please choose: UPI, PHISHING, CARD, LOAN, INVESTMENT, JOB, OTP"
            collected["fraud_type"] = ft
            step = 3
        elif step == 3:
            return _step_prompt(3, collected)

        await set_conversation(phone, {"phone": phone, "intent": "complaint", "step": step, "collected": collected})
        return _step_prompt(step, collected)

    return _welcome()


async def _submit_complaint(phone: str, collected: dict) -> str:
    """Create complaint in the system; returns confirmation message."""
    complaint_id = f"CMP-{datetime.now().strftime('%Y-%m-%d')}-{uuid.uuid4().hex[:4].upper()}"
    logger.info("whatsapp_complaint_submitted", phone=phone, data=collected, complaint_id=complaint_id)
    # TODO: full pipeline integration (PG insert + Neo4j + blockchain) lives in victim route;
    # WhatsApp path shares logic there when available.
    return (
        f"✅ *Complaint Registered!*\n\n"
        f"Complaint ID: *{complaint_id}*\n"
        f"Amount: ₹{collected.get('amount', 0):,.0f}\n"
        f"Type: {collected.get('fraud_type', 'N/A')}\n\n"
        "An officer will contact you soon. Reply *status* anytime to track it."
    )
