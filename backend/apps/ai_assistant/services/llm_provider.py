"""
Real LLM-backed provider — only instantiated when AI_API_KEY is set
(see get_ai_provider() in service.py). Written against Anthropic's
Messages API as the default choice; swap BASE_URL/payload shape here
to use a different vendor — the rest of the app never needs to change.

IMPORTANT: this has NOT been exercised against a live API key in this
environment (none was available to test with) — verify the request/
response handling against your actual provider account before relying
on it in production. The rule-based provider is used automatically
until you do, so nothing here is a runtime risk in the meantime.
"""
import json

import requests
from django.conf import settings

from .base import AIAssistantProvider

SYSTEM_PROMPT = """You are a farming assistant for Indian smallholder farmers.
Always answer ONLY as strict JSON with exactly these keys:
{"problem": "...", "possible_cause": "...", "recommended_action": "...",
 "precautions": "...", "when_to_contact_expert": "..."}
Respond in the requested language (English or Telugu).
Never recommend a specific pesticide/chemical dosage without a safety
precaution. If you are not confident, say so in "possible_cause" and
recommend contacting a local agriculture extension officer."""


class LLMProvider(AIAssistantProvider):
    BASE_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def respond(self, *, question: str, language: str, context: dict) -> dict:
        lang_name = "Telugu" if language == "te" else "English"
        user_content = (
            f"Farmer's question ({lang_name}): {question}\n"
            f"Farmer context: {json.dumps(context)}"
        )

        response = requests.post(
            self.BASE_URL,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 500,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_content}],
            },
            timeout=15,
        )
        response.raise_for_status()
        text = response.json()["content"][0]["text"]
        parsed = json.loads(text)
        parsed["provider"] = "llm"
        parsed["topic"] = "llm_generated"
        return parsed
