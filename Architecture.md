# Architecture 1 — Modules & Function Descriptions

## 1. Browser Extension Module

### 1.1 URL Interceptor
**`intercept_url(url)`**  
Captures every URL the user attempts to visit using browser **webRequest** or **tabs** APIs.

### 1.2 API Communicator
**`send_to_api(url)`**  
Sends the intercepted URL to the local Python server for prediction.

### 1.3 Decision Handler
**`handle_decision(requestId, decision)`**  
If the decision is **"suspicious"**, blocks the request; if **"safe"**, allows it.

### 1.4 UI Notifier
**`show_alert(decision, url)`**  
Displays a popup or warning banner to the user.

### 1.5 Cache Manager
check_cache(url)  # Check if URL was recently analyzed
store_cache(url, decision, ttl=3600)  # Cache results temporarily


---

## 2. Local Python Service Module

### 2.1 Model Loader
**`load_model(path)`**  
Loads the ML model once at startup using joblib.

### 2.2 Prediction Engine
**`predict_url(url)`**  
Takes a URL, extracts features, runs model prediction, and returns **"safe"** or **"suspicious"**.

### 2.3 REST API Layer
**`api_predict(request)`**  
Flask/FastAPI endpoint that accepts a URL from the extension and responds with the prediction.

### 2.4 Logging Module
**`log_event(url, decision, timestamp)`**  
Records the URL, prediction result, and timestamp for auditing.

### 2.5 Request Validator
**`validate_request(url)`**  
Ensures URL format is correct before passing it to the model.

### 2.6 Response Builder
**`build_response(decision)`**  
Wraps the prediction into a minimal JSON response for the extension.

### 2.7 Init 
**`init_service()`**

---

## Summary Structure

### **Extension**
- `intercept_url()`
- `send_to_api()`
- `handle_decision()`
- `show_alert()`

### **Python Service**
- `load_model()`
- `predict_url()`
- `api_predict()`
- `log_event()`

### **Internal Helpers**
- `validate_request()`
- `build_response()`

---

## API Endpoints
- **`POST /predict`**: Accepts a URL and returns prediction.
