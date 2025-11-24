from typing import Mapping, Union
from urllib.parse import urlparse, urlunparse
from pydantic import ValidationError
from .models import PredictRequestModel

ALLOWED_SCHEMES = {"http", "https"}  # scheme check in normalise url
MAX_URL_LENGTH = 2048  # length check in normalise url


class RequestValidationError(ValueError):
    """Raised when the incoming request payload is not usable."""

def _coerce_request(payload: Union[PredictRequestModel, str, Mapping]) -> PredictRequestModel:
    if isinstance(payload, PredictRequestModel):
        return payload
    if isinstance(payload, str):
        payload = {"check_url": payload}  # convert to dict format and put to the BaseModel
        return PredictRequestModel(**payload)
    elif isinstance(payload, Mapping):
        data = dict(payload)
        return PredictRequestModel(**data)
    else:
        raise RequestValidationError("Unsupported payload type for validation")


def normalize_url(raw_url: str) -> str:
    if not raw_url:
        raise RequestValidationError("URL is required")
    if len(raw_url) > MAX_URL_LENGTH:
        raise RequestValidationError("URL exceeds maximum length")

    parsed = urlparse(raw_url.strip())
    scheme = parsed.scheme.lower()  # find the scheme
    if scheme not in ALLOWED_SCHEMES:
        raise RequestValidationError("Only HTTP/HTTPS URLs are allowed")
    if not parsed.netloc:
        raise RequestValidationError("URL missing host component")

    cleaned = parsed._replace(fragment="", params="", query=parsed.query.strip())
    return cleaned.geturl()


def validate_request(payload: Union[PredictRequestModel, str, Mapping]) -> PredictRequestModel:
    """Validate and normalize the incoming payload before inference."""
    try:
        request = _coerce_request(payload)  # check the format
    except ValidationError as exc:
        raise RequestValidationError(str(exc)) from exc

    normalized_url = normalize_url(str(request.url))  # normalize the url length
    return request.copy(update={"url": normalized_url})
