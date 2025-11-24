"""
Gemini API integration for URL analysis using official Google SDK
"""
import os
import json
from typing import Optional, Dict
import google.generativeai as genai


class GeminiURLChecker:
    """Handles URL checking using Google Gemini API with official SDK"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None

        if self.api_key:
            self._initialize_model()

    def _initialize_model(self):
        """Initialize the Gemini model with API key"""
        genai.configure(api_key=self.api_key)

        # Configure generation settings
        generation_config = {
            "temperature": 0.1,  # Low temperature for consistent results
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 512,
        }

        # Create model instance
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
        )

    def set_api_key(self, api_key: str):
        """Set the Gemini API key and reinitialize model"""
        self.api_key = api_key
        self._initialize_model()

    def check_url(self, url: str, custom_prompt: Optional[str] = None) -> Dict:
        """
        Check if URL is suspicious using Gemini API

        Args:
            url: The raw URL to check (no preprocessing)
            custom_prompt: Optional custom prompt for analysis

        Returns:
            Dict with decision, confidence, and reasoning
        """
        if not self.api_key or not self.model:
            raise ValueError("Gemini API key not configured")

        # Default prompt - PLACEHOLDER FOR USER TO CUSTOMIZE
        if custom_prompt is None:
            custom_prompt = """
# Check suspicious URL - CUSTOMIZE THIS PROMPT

Analyze the following URL and determine if it is suspicious, malicious, or safe.

Consider:
- Phishing patterns (fake login pages, typosquatting)
- Malware distribution sites
- Suspicious domain names
- URL obfuscation techniques
- Known malicious TLDs
- Suspicious URL structure

URL to analyze: {url}

Respond in JSON format:
{{
    "decision": "safe" or "suspicious",
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation",
    "threat_type": "phishing|malware|scam|safe"
}}

# YOUR CUSTOM ANALYSIS LOGIC HERE
# Add your specific rules, patterns, or instructions
"""

        prompt = custom_prompt.format(url=url)

        try:
            print(f"[Gemini SDK] Analyzing URL: {url}")

            # Generate response using SDK
            response = self.model.generate_content(prompt)

            # Extract text from response
            if response.text:
                text_response = response.text
                print(f"[Gemini SDK] Raw response received")

                # Try to parse JSON response
                try:
                    # Extract JSON from markdown code blocks if present
                    if '```json' in text_response:
                        json_str = text_response.split('```json')[1].split('```')[0].strip()
                    elif '```' in text_response:
                        json_str = text_response.split('```')[1].split('```')[0].strip()
                    else:
                        json_str = text_response.strip()

                    parsed_response = json.loads(json_str)

                    print(f"[Gemini SDK] Decision: {parsed_response.get('decision', 'safe')}")

                    return {
                        'decision': parsed_response.get('decision', 'safe').lower(),
                        'confidence': float(parsed_response.get('confidence', 0.5)),
                        'reasoning': parsed_response.get('reasoning', 'No reasoning provided'),
                        'threat_type': parsed_response.get('threat_type', 'unknown'),
                        'source': 'gemini'
                    }

                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    raise ValueError("Failed to parse Gemini API response as JSON")
            else:
                raise ValueError("No text response from Gemini API")

        except Exception as e:
            print(f"[Gemini SDK] Error: {e}")
            raise


# Module-level singleton instance
_gemini_checker: Optional[GeminiURLChecker] = None


def get_gemini_checker(api_key: Optional[str] = None) -> GeminiURLChecker:
    """Get or create Gemini checker instance"""
    global _gemini_checker

    if _gemini_checker is None:
        _gemini_checker = GeminiURLChecker(api_key)
    elif api_key and api_key != _gemini_checker.api_key:
        _gemini_checker.set_api_key(api_key)

    return _gemini_checker


def check_url_with_gemini(url: str, api_key: Optional[str] = None, custom_prompt: Optional[str] = None) -> Dict:
    """
    Convenience function to check URL with Gemini

    Args:
        url: Raw URL to check (no preprocessing)
        api_key: Optional Gemini API key
        custom_prompt: Optional custom prompt template

    Returns:
        Dict with decision and analysis
    """
    checker = get_gemini_checker(api_key)
    return checker.check_url(url, custom_prompt)

