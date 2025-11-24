from fastapi import FastAPI, HTTPException, Header
from typing import Optional
from utils.models import PredictRequestModel
from ml.model_loader import load_model
from ml.predictor import predict_url, predict_url_with_ml, predict_url_with_gemini
from utils.validator import validate_request, RequestValidationError

app = FastAPI(title="FireML API", version="2.0.0")

# init_service() - Initialize the ML model
def init_service():
    """Ensure the ML model is loaded and ready."""
    return load_model()


# api_predict(request) - Endpoint to handle prediction requests
@app.post("/predict")
async def api_predict(
    request: PredictRequestModel,
    use_gemini: bool = False,
    x_gemini_api_key: Optional[str] = Header(None, alias="X-Gemini-API-Key")
):
    """
    Predict if URL is suspicious using ML model or Gemini API

    Parameters:
    - request: URL to check
    - use_gemini: Use Gemini API instead of ML model (query param)
    - X-Gemini-API-Key: Gemini API key (HTTP header)

    Returns:
    - decision: "safe" or "suspicious"
    - score: confidence score
    - Additional metadata based on method used
    """
    try:
        validated_request = validate_request(request)
    except RequestValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    url = str(validated_request.url)

    # Check if Gemini is requested but no API key provided
    if use_gemini and not x_gemini_api_key:
        raise HTTPException(
            status_code=400,
            detail="Gemini API key required"
        )

    try:
        if use_gemini:
            # Use only Gemini API
            prediction = predict_url_with_gemini(
                url,
                api_key=x_gemini_api_key
            )
            return {
                "url": url,
                "decision": prediction["decision"],
                "score": prediction.get("score"),
                "source": prediction["source"]
            }

        elif not use_gemini:
            # Use only ML model (default)
            model = init_service()
            prediction = predict_url_with_ml(url, model=model)
            return {
                "url": url,
                "decision": prediction["decision"],
                "score": prediction["score"],
                "features": prediction.get("features"),
                "source": prediction["source"]
            }

        else:
            print("[API] No choice error")
    except Exception as e:
        print(f"[API] Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ml_model": "loaded" if init_service() else "not loaded",
        "gemini_support": "enabled"
    }


# log_event(url, decision, timestamp) - Endpoint to log events

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)