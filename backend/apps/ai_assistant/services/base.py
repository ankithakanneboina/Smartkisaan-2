from abc import ABC, abstractmethod


class AIAssistantProvider(ABC):
    """
    Common interface every AI provider implements (rule-based FAQ now,
    a real LLM later). Views only ever talk to this interface — see
    services/service.py::get_ai_provider() for the single switch point,
    mirroring apps.weather's provider abstraction pattern.
    """

    @abstractmethod
    def respond(self, *, question: str, language: str, context: dict) -> dict:
        """
        Must return a dict shaped like:
        {
            "problem": str,
            "possible_cause": str,
            "recommended_action": str,
            "precautions": str,
            "when_to_contact_expert": str,
            "provider": str,
        }
        `context` may include farmer profile fields (crops_grown, soil_type,
        location) for context-aware answers, per §6.
        """
        raise NotImplementedError
