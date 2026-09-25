from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PredictionResult:
    """Common envelope every predictor returns, regardless of domain."""
    label: str                      # e.g. crop name, disease name, fertilizer type
    confidence: float               # 0.0–1.0
    details: dict = field(default_factory=dict)  # domain-specific extra fields
    model_version: str = "unversioned"


class BasePredictor(ABC):
    """
    Every predictor (crop, fertilizer, disease, ...) implements this.
    Django views depend only on this interface, never on a specific
    model implementation — see ml_models/README.md.
    """

    @abstractmethod
    def predict(self, inputs: dict[str, Any]) -> list[PredictionResult]:
        """Return one or more ranked PredictionResult objects."""
        raise NotImplementedError

    def is_ready(self) -> bool:
        """False until a real trained model/weights file is loaded."""
        return False
