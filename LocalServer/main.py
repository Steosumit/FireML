from fastapi import FastAPI, HTTPException
from utils.models import PredictRequestModel
from ml.model_loader import load_model
from ml.predictor import predict_url
from utils.validator import validate_request, RequestValidationError

app = FastAPI()

# init_service() - Initialize the ML model
def init_service():
    """Ensure the ML model is loaded and ready."""
    return load_model()


# api_predict(request) - Endpoint to handle prediction requests
@app.post("/predict")
async def api_predict(request: PredictRequestModel):
    try:
        validated_request = validate_request(request)
    except RequestValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    model = init_service()
    prediction = predict_url(str(validated_request.url), model=model)
    return {
        "url": str(validated_request.url),
        "decision": prediction["decision"],
        "score": prediction["score"],
        "features": prediction["features"],
    }

# log_event(url, decision, timestamp) - Endpoint to log events

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)