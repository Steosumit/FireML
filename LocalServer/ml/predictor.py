import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import numpy as np
from . import model_loader

THRESHOLD = 0.5
SUSPICIOUS_LABELS = {1, "1", "suspicious", "malicious", "phishing", True}


def extract_features(url: str) -> Tuple[List[float], Dict[str, float]]:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    def _average_word_length(value: str) -> float:
        # split on non-alphanumeric characters to approximate word tokens
        tokens = [token for token in re.split(r"[^a-zA-Z0-9]+", value) if token]
        if not tokens:
            return 0.0
        return sum(len(token) for token in tokens) / len(tokens)

    host_len = len(hostname)
    ratio_digits_host = (
        sum(ch.isdigit() for ch in hostname) / host_len if host_len else 0.0
    )
    avg_words_raw = _average_word_length(url)
    avg_word_path = _average_word_length(path)

    features = [
        ratio_digits_host,
        avg_words_raw,
        avg_word_path,
    ]

    feature_map = {
        "ratio_digits_host": ratio_digits_host,
        "avg_words_raw": avg_words_raw,
        "avg_word_path": avg_word_path,
    }

    return features, feature_map


def _model_predict(model, features: List[float]):
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(np.array([features]))[0]
        suspicious_score = probabilities[1] if len(probabilities) > 1 else probabilities[0]
        decision = "suspicious" if suspicious_score >= THRESHOLD else "safe"
        return decision, float(suspicious_score)

    # Fallback for models without predict_proba (use predict instead)
    prediction = model.predict(np.array([features]))[0]
    decision = "suspicious" if prediction in SUSPICIOUS_LABELS else "safe"
    return decision, None


def predict_url(url: str, model=None):
    model = model or model_loader.load_model()
    features, feature_map = extract_features(url)
    decision, score = _model_predict(model, features)
    return {
        "decision": decision,
        "score": score,
        "features": feature_map,
    }
