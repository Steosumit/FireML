# FireML

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license) [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#requirements)

FireML is a browser extension with a local FastAPI server that infer a local ML model and a LLM API to block phishing links

Motivation
--------
How to deploy local models and handle initialization? How to integrate GenAI LLM with local servers?

Features
--------
- Quick response with caching
- Local safe model integration
- GenAI LLM integration

Quick start
-----------
1. Clone the repository
   ```bash
   git clone https://github.com/Steosumit/FireML.git
   cd FireML
   ```

2. Create a Python virtual environment and install dependencies
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cd LocalServer
   python main.py
   ```
   Load the extension separate to your chromium based browser
   
3. Train a model (example)
   Use this code : https://github.com/Steosumit/URL-classifier-cpu-gpu-nb/blob/master/models/score.py.ipynb
   To make a ML model(remember to check the inference parameter list and the parameters you selected for training)

Installation
------------
Minimum recommended setup:
- Python 3.8+
- pip

Install dependencies:
```bash
pip install -r requirements.txt
```

License
-------
This project is provided under the MIT License. See LICENSE file for details.

Contact
-------
Maintainer: Steosumit
Project repository: https://github.com/Steosumit/FireML

Customizing this README
-----------------------
This README is a template. Replace placeholders (configs, scripts, model names) with project-specific details and add examples of real commands, datasets, and expected outputs to make it easier for other contributors to get started.
