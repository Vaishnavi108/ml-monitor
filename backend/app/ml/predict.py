import numpy as np
from app.ml.model import load_model, FEATURE_NAMES

_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model

def predict(features: dict) -> dict:
    """
    Takes a dict of feature values, returns prediction + confidence.
    """
    model = get_model()
    X = np.array([[features[f] for f in FEATURE_NAMES]])
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]
    confidence = float(proba[pred])

    return {
        "prediction": pred,
        "label": ">50K" if pred == 1 else "<=50K",
        "confidence": round(confidence, 4),
        "probabilities": {
            "<=50K": round(float(proba[0]), 4),
            ">50K": round(float(proba[1]), 4),
        }
    }