from django.conf import settings

from .rule_based_provider import RuleBasedFAQProvider


def get_ai_provider():
    """
    Single switch point, mirroring apps.weather.services.service.
    AI_API_KEY blank (the default) => rule-based FAQ provider, which
    never fabricates farming advice — see rule_based_provider.py.
    Set AI_API_KEY to switch to the real LLM provider.
    """
    api_key = getattr(settings, "AI_API_KEY", "")
    if api_key:
        from .llm_provider import LLMProvider
        return LLMProvider(api_key)
    return RuleBasedFAQProvider()
