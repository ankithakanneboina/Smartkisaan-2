# ml_models/

Standalone Python ML package, deliberately kept **outside** `backend/apps/`
so model code, training scripts and weights are never coupled to Django
request/response cycles — Django apps call into this package through a
thin predictor interface, nothing more.

## Structure

```
ml_models/
├── common/
│   └── predictor_base.py      # shared Predictor interface + result dataclasses
├── crop_recommendation/
│   ├── predictor.py           # CropRecommendationPredictor (NotImplemented for now)
│   └── README.md
├── fertilizer_recommendation/
│   ├── predictor.py
│   └── README.md
└── disease_detection/
    ├── predictor.py
    └── README.md
```

## Status (Phase 1)

No trained models exist yet and none are faked. Each `predictor.py`
defines the exact interface `apps.crops` / `apps.fertilizers` /
`apps.diseases` will call in their respective phases (Phase 3, Phase 3,
Phase 5), and raises `NotImplementedError` until a real model is wired
in. This lets the Django API contracts (serializers, URLs, request
shapes) be built and tested now against a predictable interface,
without ever returning invented predictions to a user.

## Integration pattern (for later phases)

```python
# apps/crops/views.py (Phase 3)
from ml_models.crop_recommendation.predictor import CropRecommendationPredictor

predictor = CropRecommendationPredictor()  # loads weights once, e.g. at app startup
result = predictor.predict(soil_inputs)     # returns a PredictionResult
```

Swapping a rule-based first version for a trained scikit-learn/TensorFlow
model later means editing only the relevant `predictor.py` — the Django
view, serializer and frontend contract do not change.
