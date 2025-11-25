# 🔥 FireML - AI-Powered URL Threat Detection

<div align="center">

![FireML Banner](FireML_demo(1).gif)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A real-time browser security solution that uses Machine Learning and Gemini AI to detect and block suspicious URLs before you visit them.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Reference](#-api-reference) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## ✨ Features

- 🛡️ **Real-time URL Protection** - Automatically intercepts and analyzes every URL before navigation
- 🤖 **Dual AI Detection** - Choose between local ML model (RandomForest/LightGBM) or Google Gemini AI
- ⚡ **Lightning Fast** - Local ML predictions in milliseconds with smart caching
- 🔒 **Privacy First** - All ML processing happens locally on your machine
- 🎨 **Modern UI** - Clean, intuitive browser extension interface
- 🔄 **Smart Caching** - Reduces redundant API calls with configurable TTL
- 📊 **Confidence Scores** - See how confident the model is in its predictions
- 🎯 **Feature Extraction** - Intelligent URL analysis including domain patterns, path analysis, and more

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome or Chromium-based browser
- (Optional) Google Gemini API key for AI-powered analysis

### Step 1: Clone the Repository

```bash
git clone https://github.com/Steosumit/FireML.git
cd FireML
```

### Step 2: Set Up the Local Server

```bash
# Navigate to the LocalServer directory
cd LocalServer

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The server will start at `http://localhost:8000`

### Step 3: Install the Browser Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right)
3. Click **Load unpacked**
4. Select the `BrowserExtension` folder from the cloned repository
5. The FireML icon should appear in your browser toolbar

## 💡 Usage

### Basic Usage

Once installed, FireML automatically monitors all your web navigation:

1. **Navigate normally** - FireML works in the background
2. **Safe URLs** - Allowed through seamlessly
3. **Suspicious URLs** - Blocked with a warning page displaying threat details

### Extension Settings

Click the FireML icon in your toolbar to access settings:

- **Enable/Disable ML Model** - Toggle local machine learning detection
- **Enable Gemini AI** - Use Google's Gemini AI for advanced analysis
- **Configure API Key** - Add your Gemini API key for AI-powered detection

### Choosing Detection Method

| Method | Pros | Cons |
|--------|------|------|
| **ML Model (Default)** | Fast, works offline, privacy-focused | May miss novel threats |
| **Gemini AI** | Advanced analysis, reasoning provided | Requires API key, network dependent |

## 📡 API Reference

The local server exposes a REST API for URL analysis:

### Predict URL

```http
POST /predict
```

**Request Body:**
```json
{
  "check_url": "https://example.com/suspicious-path"
}
```

**Query Parameters:**
- `use_gemini` (boolean): Use Gemini AI instead of ML model

**Headers (for Gemini):**
- `X-Gemini-API-Key`: Your Gemini API key

**Response (ML Model):**
```json
{
  "url": "https://example.com/suspicious-path",
  "decision": "safe",
  "score": 0.15,
  "features": {
    "ratio_digits_host": 0.0,
    "avg_words_raw": 5.2,
    "avg_word_path": 4.8
  },
  "source": "ml_model"
}
```

**Response (Gemini AI):**
```json
{
  "url": "https://example.com/suspicious-path",
  "decision": "suspicious",
  "score": 0.95,
  "source": "gemini_api"
}
```

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "ml_model": "loaded",
  "gemini_support": "enabled"
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Browser Extension                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ URL          │  │ Cache        │  │ UI Notifier          │   │
│  │ Interceptor  │──▶│ Manager      │  │ (Alert/Warning)      │   │
│  └──────┬───────┘  └──────────────┘  └──────────────────────┘   │
│         │                                        ▲               │
│         ▼                                        │               │
│  ┌──────────────┐  ┌──────────────┐              │               │
│  │ API          │──▶│ Decision     │──────────────┘               │
│  │ Communicator │  │ Handler      │                              │
│  └──────┬───────┘  └──────────────┘                              │
└─────────┼───────────────────────────────────────────────────────┘
          │ HTTP POST /predict
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Local Python Server                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ FastAPI      │──▶│ Request      │──▶│ Model Loader         │   │
│  │ Endpoint     │  │ Validator    │  │ (RandomForest/LGBM)  │   │
│  └──────────────┘  └──────────────┘  └──────────┬───────────┘   │
│                                                  │               │
│  ┌──────────────┐  ┌──────────────┐              ▼               │
│  │ Response     │◀─│ Prediction   │◀─────────────────────────    │
│  │ Builder      │  │ Engine       │                              │
│  └──────────────┘  └──────────────┘                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Gemini AI Checker (Optional)                              │   │
│  │ - Custom prompt templates                                  │   │
│  │ - Advanced threat analysis                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend (LocalServer)
- **FastAPI** - High-performance async web framework
- **Uvicorn** - Lightning-fast ASGI server
- **Scikit-learn** - Machine learning models (RandomForest, LightGBM)
- **Pydantic** - Data validation
- **Google Generative AI** - Gemini API integration

### Frontend (BrowserExtension)
- **Manifest V3** - Latest Chrome extension standard
- **Chrome APIs** - webNavigation, storage, tabs
- **Vanilla JavaScript** - No framework dependencies

## 🔍 How It Works

1. **URL Interception**: The browser extension intercepts every HTTP/HTTPS navigation
2. **Cache Check**: Checks if the URL was recently analyzed
3. **Feature Extraction**: Extracts URL features (domain patterns, path structure, etc.)
4. **ML Prediction**: Runs the URL through the trained model
5. **Decision Making**: Returns "safe" or "suspicious" based on confidence threshold (0.5)
6. **Action**: Safe URLs proceed; suspicious URLs are blocked with a warning page

### Feature Extraction

The ML model analyzes:
- **Ratio of digits in hostname** - Phishing sites often use numeric domains
- **Average word length in URL** - Obfuscated URLs tend to have unusual patterns
- **Average word length in path** - Detects suspicious path structures

## 📁 Project Structure

```
FireML/
├── BrowserExtension/          # Chrome extension
│   ├── background/            # Service worker
│   ├── ui/                    # Alert/warning pages
│   ├── utils/                 # API communication
│   ├── manifest.json          # Extension manifest
│   ├── popup.html             # Settings popup
│   └── popup.js               # Popup logic
├── LocalServer/               # Python backend
│   ├── ml/                    # ML components
│   │   ├── model_loader.py    # Model loading
│   │   ├── predictor.py       # Prediction engine
│   │   └── gemini_checker.py  # Gemini AI integration
│   ├── model/                 # Trained models
│   │   ├── url_classifier_RandomForest_CPU.pkl
│   │   └── url_classifier_LightGBM_GPU_latest.pkl
│   ├── utils/                 # Utilities
│   │   ├── models.py          # Pydantic models
│   │   └── validator.py       # Request validation
│   ├── tests/                 # Test suite
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── Architecture.md            # Detailed architecture docs
└── README.md                  # This file
```

## 🧪 Testing

Run the test suite:

```bash
cd LocalServer
pytest tests/ -v
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/FireML.git

# Install development dependencies
cd LocalServer
pip install -r requirements.txt
pip install pytest httpx

# Run tests
pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for safer browsing
- Powered by Google Gemini AI
- ML models trained on publicly available phishing URL datasets

---

<div align="center">

**[⬆ Back to Top](#-fireml---ai-powered-url-threat-detection)**

Made with 🔥 by the FireML Team

</div>
