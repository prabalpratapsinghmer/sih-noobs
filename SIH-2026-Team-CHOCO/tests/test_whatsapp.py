"""WhatsApp intent detection and conversation flow tests."""

from api.services.whatsapp import _welcome, detect_intent, verify_webhook


def test_intents():
    assert detect_intent("I want to report a fraud") == "complaint"
    assert detect_intent("check my status") == "status"
    assert detect_intent("sus sUSpicious account tip") == "tip"
    assert detect_intent("help me") == "help"
    assert detect_intent("emergency help now") == "emergency"
    assert detect_intent("random chatter") == "help"


def test_webhook_verify():
    assert verify_webhook("abc", "abc")
    assert not verify_webhook("abc", "def")


def test_welcome_mentions_options():
    msg = _welcome()
    for keyword in ["report", "status", "tip", "emergency"]:
        assert keyword in msg.lower()
