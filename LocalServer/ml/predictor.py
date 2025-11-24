import re
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import numpy as np
from . import model_loader
from .gemini_checker import check_url_with_gemini

THRESHOLD = 0.5
SUSPICIOUS_LABELS = {1, "1", "suspicious", "malicious", "phishing", True}


# ============================================================================
# ML MODEL PREDICTION CLUSTER
# ============================================================================

def extract_features(url: str) -> Tuple[List[float], Dict[str, float]]:
    """Extract features from URL for ML model"""
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


def _model_predict(model, features: List[float]) -> Tuple[str, Optional[float]]:
    """Run ML model prediction"""
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(np.array([features]))[0]
        suspicious_score = probabilities[1] if len(probabilities) > 1 else probabilities[0]
        decision = "suspicious" if suspicious_score >= THRESHOLD else "safe"
        return decision, float(suspicious_score)

    # Fallback for models without predict_proba (use predict instead)
    prediction = model.predict(np.array([features]))[0]
    decision = "suspicious" if prediction in SUSPICIOUS_LABELS else "safe"
    return decision, None


def predict_url_with_ml(url: str, model=None) -> Dict:
    """
    Predict URL using ML model only

    Args:
        url: URL to analyze (will be preprocessed into features)
        model: Optional pre-loaded model

    Returns:
        Dict with decision, score, features, and source
    """
    model = model or model_loader.load_model()
    features, feature_map = extract_features(url)
    decision, score = _model_predict(model, features)
    return {
        "decision": decision,
        "score": score,
        "features": feature_map,
        "source": "ml_model"
    }


# ============================================================================
# GEMINI API PREDICTION CLUSTER
# ============================================================================

def predict_url_with_gemini(url: str, api_key: Optional[str] = None, custom_prompt: Optional[str] = None) -> Dict:
    """
    Predict URL using Gemini API

    Args:
        url: Raw URL to check (NO preprocessing)
        api_key: Gemini API key
        custom_prompt: Custom prompt template for analysis

    Returns:
        Dict with decision, confidence, reasoning, threat_type, and source
    """
    try:
        result = check_url_with_gemini(url, api_key, custom_prompt)
        return {
            "decision": result['decision'],
            "score": result.get('confidence'),
            "reasoning": result.get('reasoning'),
            "threat_type": result.get('threat_type'),
            "source": "gemini_api"
        }
    except Exception as e:
        print(f"[Gemini] Error checking URL: {e}")
        # Fallback to safe if Gemini fails
        return {
            "decision": "safe",
            "score": 0.0,
            "reasoning": f"Gemini API error: {str(e)}",
            "threat_type": "error",
            "source": "gemini_api_fallback"
        }


# ============================================================================
# UNIFIED PREDICTION INTERFACE
# ============================================================================

def predict_url(
    url: str,
    model=None,
    use_gemini: bool = False,
    gemini_api_key: Optional[str] = None,
    gemini_prompt: Optional[str] = None
) -> Dict:
    """
    Unified URL prediction interface

    Args:
        url: URL to analyze
        model: Optional ML model instance
        use_gemini: Whether to use Gemini API
        gemini_api_key: Gemini API key (if using Gemini)
        gemini_prompt: Custom prompt for Gemini

    Returns:
        Dict with prediction results
    """

    # Use Gemini API if requested
    if use_gemini:
        return predict_url_with_gemini(url, gemini_api_key, gemini_prompt)

    # Use ML model (default behavior)
    return predict_url_with_ml(url, model)


# Backward compatibility - keep original function name
# This maintains compatibility with existing code
def predict_url_legacy(url: str, model=None):
    """Legacy function for backward compatibility"""
    return predict_url_with_ml(url, model)
