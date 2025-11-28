# Code to load model
from pathlib import Path
from threading import Lock
from typing import Optional
import joblib

DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "GradientBoosting_CPU.pkl"
_model: Optional[object] = None
_model_lock = Lock()  # for thread safe operation (read Notes for details)

def load_model(path: Optional[Path] = None):
    """Load the ML model once and cache it for future predictions."""
    global _model

    if _model is not None:
        return _model

    resolved_path = Path(path or DEFAULT_MODEL_PATH).expanduser().resolve()

    with _model_lock:
        if _model is None:
            if not resolved_path.exists():
                raise FileNotFoundError(f"Model file not found at {resolved_path}")
            _model = joblib.load(resolved_path)  # load the model if it is not laoded yet
    return _model


def reload_model(path: Optional[Path] = None):
    """Force reload the model, useful during development/testing."""
    global _model
    _model = None
    return load_model(path)
