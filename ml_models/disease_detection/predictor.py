from ml_models.common.predictor_base import BasePredictor, PredictionResult


class DiseaseDetectionPredictor(BasePredictor):
    """
    Built in Phase 5 alongside apps.diseases. Will load a
    TensorFlow/PyTorch image-classification model from ./weights/ once
    trained. Expected `inputs` keys:
        image_path (or image bytes), crop (optional hint)

    Until a real model is trained, apps.diseases must present this
    clearly as "detection unavailable" in the API/UI rather than
    inventing a diagnosis — see spec section 8.
    """

    def predict(self, inputs: dict) -> list[PredictionResult]:
        raise NotImplementedError(
            "DiseaseDetectionPredictor is not implemented yet — "
            "this is built in Phase 5 alongside apps.diseases."
        )
