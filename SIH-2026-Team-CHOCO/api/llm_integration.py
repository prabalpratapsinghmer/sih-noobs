"""LLM Integration module for SIH26184.

Provides an LLM-powered service for:
- Complaint intent detection (COMPLAINT, STATUS, TIP, HELP, EMERGENCY)
- Natural language complaint summarization
- Multi-language support (English, Hindi, Hinglish)
- WhatsApp chatbot response generation

Uses LangChain + OpenAI GPT-4 when available, with a rule-based fallback
for environments without an API key.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from loguru import logger


# Intent categories
INTENTS = ["COMPLAINT", "STATUS", "TIP", "HELP", "EMERGENCY"]

# Keyword-based fallback patterns for intent detection
_INTENT_PATTERNS = {
    "COMPLAINT": [
        r"\b(fraud|scam|cheated|stolen|deducted|lost money|complaint|report)\b",
        r"\b(धोखाधड़ी|शिकायत|ठगी|पैसे कटे|फ्रॉड)\b",
    ],
    "STATUS": [
        r"\b(status|update|progress|track|where is|complaint number)\b",
        r"\b(स्टेटस|अपडेट|कहाँ तक)\b",
    ],
    "TIP": [
        r"\b(tip|advice|protect|safety|prevent|how to)\b",
        r"\b(सुझाव|सलाह|बचाव|सुरक्षा)\b",
    ],
    "HELP": [
        r"\b(help|guide|what can|how do|contact|support)\b",
        r"\b(मदद|सहायता|कैसे)\b",
    ],
    "EMERGENCY": [
        r"\b(urgent|emergency|happening now|right now|immediately|just happened)\b",
        r"\b(तुरंत|अभी|जल्दी|इमरजेंसी)\b",
    ],
}


class LLMService:
    """LLM-powered service for chatbot and complaint processing."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        """Initialize LLM provider (OpenAI via LangChain)."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set — using rule-based fallback")
            return

        try:
            from langchain_openai import ChatOpenAI

            self.llm = ChatOpenAI(
                model=self.config.get("model", "gpt-4"),
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 1000),
                api_key=api_key,
            )
            logger.info("✓ LLM initialized (OpenAI GPT-4)")
        except ImportError:
            logger.warning("langchain_openai not installed — using rule-based fallback")
        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")

    @property
    def is_available(self) -> bool:
        return self.llm is not None

    # ------------------------------------------------------------------
    # Intent detection
    # ------------------------------------------------------------------
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect the user's intent from a message.

        Returns:
            (intent_label, confidence)
        """
        if self.llm:
            return self._detect_intent_llm(message)
        return self._detect_intent_rules(message)

    def _detect_intent_llm(self, message: str) -> Tuple[str, float]:
        """Use the LLM to classify intent."""
        try:
            prompt = (
                "Classify the following message into exactly one of these intents: "
                "COMPLAINT, STATUS, TIP, HELP, EMERGENCY.\n\n"
                f"Message: \"{message}\"\n\n"
                "Respond with ONLY the intent label."
            )
            response = self.llm.invoke(prompt)
            intent = response.content.strip().upper()
            if intent in INTENTS:
                return intent, 0.95
            return "HELP", 0.5
        except Exception as e:
            logger.error(f"LLM intent detection failed: {e}")
            return self._detect_intent_rules(message)

    def _detect_intent_rules(self, message: str) -> Tuple[str, float]:
        """Rule-based intent detection using keyword patterns."""
        msg_lower = message.lower()
        scores = {}

        for intent, patterns in _INTENT_PATTERNS.items():
            count = sum(
                len(re.findall(pattern, msg_lower, re.IGNORECASE))
                for pattern in patterns
            )
            scores[intent] = count

        if max(scores.values()) == 0:
            return "HELP", 0.3

        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 3.0, 1.0)
        return best_intent, round(confidence, 2)

    # ------------------------------------------------------------------
    # Response generation
    # ------------------------------------------------------------------
    def generate_response(self, message: str, intent: str, context: Optional[Dict] = None) -> str:
        """Generate a chatbot response based on intent and context."""
        if self.llm:
            return self._generate_response_llm(message, intent, context)
        return self._generate_response_template(intent, context)

    def _generate_response_llm(self, message: str, intent: str, context: Optional[Dict]) -> str:
        """Use the LLM to generate a contextual response."""
        try:
            system_prompt = (
                "You are a helpful assistant for the National Cyber Crime Reporting Portal (NCRP). "
                "You help victims of cybercrime file complaints, check status, and get safety tips. "
                "Be empathetic, concise, and provide actionable guidance. "
                "Support English, Hindi, and Hinglish."
            )
            user_prompt = (
                f"Intent: {intent}\n"
                f"User message: {message}\n"
                f"Context: {context or 'None'}\n\n"
                "Generate an appropriate, helpful response."
            )

            from langchain.schema import HumanMessage, SystemMessage

            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ])
            return response.content.strip()
        except Exception as e:
            logger.error(f"LLM response generation failed: {e}")
            return self._generate_response_template(intent, context)

    def _generate_response_template(self, intent: str, context: Optional[Dict] = None) -> str:
        """Fallback template-based responses."""
        templates = {
            "COMPLAINT": (
                "I'm sorry to hear about the fraud. To file a complaint, please provide:\n"
                "1. Your name and phone number\n"
                "2. Amount lost (₹)\n"
                "3. Type of fraud (UPI/Investment/KYC/Loan)\n"
                "4. Fraudster details (UPI ID, phone, account)\n\n"
                "You can also call 1930 (National Cybercrime Helpline) for immediate assistance."
            ),
            "STATUS": (
                "To check your complaint status, please share your complaint ID "
                "(format: C followed by numbers, e.g., C1001).\n\n"
                "You can also check at https://cybercrime.gov.in"
            ),
            "TIP": (
                "🔒 Safety Tips:\n"
                "• Never share OTP, PIN, or CVV with anyone\n"
                "• Verify UPI requests before approving\n"
                "• Don't click suspicious links in SMS/WhatsApp\n"
                "• Use official banking apps only\n"
                "• Report fraud within 2 hours for best recovery chances"
            ),
            "HELP": (
                "I can help you with:\n"
                "1. 📝 Filing a cybercrime complaint\n"
                "2. 🔍 Checking complaint status\n"
                "3. 💡 Cybersecurity tips and prevention\n"
                "4. 🚨 Emergency assistance\n\n"
                "What would you like to do?"
            ),
            "EMERGENCY": (
                "🚨 EMERGENCY: If a fraud is happening RIGHT NOW:\n\n"
                "1. Call 1930 (National Cybercrime Helpline) IMMEDIATELY\n"
                "2. Call your bank's 24/7 helpline to freeze your account\n"
                "3. Do NOT share any OTP or approve any transaction\n"
                "4. File an FIR at your nearest police station\n\n"
                "Time is critical — act within 2 hours for best recovery."
            ),
        }
        return templates.get(intent, templates["HELP"])

    # ------------------------------------------------------------------
    # Complaint summarization
    # ------------------------------------------------------------------
    def summarize_complaint(self, complaint_data: Dict) -> str:
        """Generate a human-readable summary of a complaint."""
        if self.llm:
            try:
                prompt = (
                    "Summarize this cybercrime complaint in 2-3 sentences:\n\n"
                    f"{complaint_data}\n\n"
                    "Include: fraud type, amount, key details, and urgency level."
                )
                response = self.llm.invoke(prompt)
                return response.content.strip()
            except Exception as e:
                logger.error(f"LLM summarization failed: {e}")

        # Fallback
        amount = complaint_data.get("amount", "unknown")
        fraud_type = complaint_data.get("fraud_type", "unknown")
        return (
            f"Cybercrime complaint: {fraud_type} fraud involving ₹{amount}. "
            f"Status: {complaint_data.get('status', 'SUBMITTED')}."
        )


# Singleton
_service: Optional[LLMService] = None


def get_llm_service(config: Optional[Dict] = None) -> LLMService:
    """Get or create the global LLM service instance."""
    global _service
    if _service is None:
        _service = LLMService(config)
    return _service
