# 🔥 FireML

A browser extension + local ML server that detects and blocks suspicious URLs in real-time.

![Demo](FireML_demo(1).gif)

## Quick Start

### 1. Start the Server

```bash
cd LocalServer
pip install -r requirements.txt
python main.py
```

### 2. Load the Extension

1. Go to `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked** → select `BrowserExtension` folder

## Project Structure

```
FireML/
├── BrowserExtension/   # Chrome extension (Manifest V3)
├── LocalServer/        # Python FastAPI backend
│   ├── ml/             # ML prediction engine
│   └── model/          # Trained models (.pkl)
└── Architecture.md     # Detailed docs
```

## API

```bash
# Check a URL
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"check_url": "https://example.com"}'
```

## License

MIT
