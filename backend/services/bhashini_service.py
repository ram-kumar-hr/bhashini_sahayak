import logging
from typing import Optional

import requests

from backend.config import config

logger = logging.getLogger(__name__)

# ISO 639-1 codes supported by Bhashini / IndicTrans2
SUPPORTED_LANGUAGES = {
    "hi", "bn", "te", "mr", "ta", "gu", "kn", "ml", "pa", "or", "ur", "as", "en"
}

# langdetect can return these codes which map 1:1 to Bhashini codes for Indian langs
LANGUAGE_NAMES = {
    "hi": "Hindi", "bn": "Bengali", "te": "Telugu", "mr": "Marathi",
    "ta": "Tamil", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
    "pa": "Punjabi", "or": "Odia", "ur": "Urdu", "as": "Assamese", "en": "English",
}


class BhashiniService:
    """Wrapper around Bhashini Dhruva inference API for text translation."""

    def __init__(self):
        self._configured = bool(config.BHASHINI_API_KEY and config.BHASHINI_API_URL)
        if not self._configured:
            logger.warning(
                "Bhashini API key/URL not set. Translation will be skipped "
                "(responses will remain in English)."
            )

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source_lang to target_lang.

        Falls back to the original text if the API is not configured or fails.
        """
        if source_lang == target_lang:
            return text

        if not self._configured:
            logger.debug("Bhashini not configured — returning original text")
            return text

        if source_lang not in SUPPORTED_LANGUAGES or target_lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"Unsupported language pair: {source_lang} → {target_lang}")
            return text

        try:
            return self._call_dhruva(text, source_lang, target_lang)
        except Exception as e:
            logger.error(f"Bhashini translation failed ({source_lang}→{target_lang}): {e}")
            return text  # graceful fallback

    def _call_dhruva(self, text: str, source_lang: str, target_lang: str) -> str:
        """Call the Bhashini Dhruva pipeline inference endpoint."""
        url = f"{config.BHASHINI_API_URL.rstrip('/')}/services/inference/pipeline"

        headers = {
            "Authorization": config.BHASHINI_API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang,
                        },
                        "serviceId": config.BHASHINI_TRANSLATION_SERVICE_ID,
                    },
                }
            ],
            "inputData": {
                "input": [{"source": text}],
                "audio": [],
            },
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()

        data = resp.json()
        pipeline_response = data.get("pipelineResponse", [])
        if not pipeline_response:
            raise ValueError("Empty pipelineResponse from Bhashini API")

        output = pipeline_response[0].get("output", [])
        if not output:
            raise ValueError("No output in Bhashini pipeline response")

        return output[0].get("target", text)
