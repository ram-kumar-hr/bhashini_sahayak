import logging
from typing import Optional

from google import genai
from google.genai import types

from backend.config import config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Bhashini Sahayak, a helpful assistant for the CAG (Common Assistance Group) platform.
You answer questions about platform workflows based strictly on the provided SOP context.

Rules:
1. Only answer based on the provided context — do not invent procedures.
2. If the context does not contain enough information, say so clearly.
3. Be concise and use numbered steps for procedural answers.
4. Refer to roles correctly: CEO, Super Admin, Office Admin, End User.
5. If asked about something outside the SOPs, say you can only help with platform procedures."""


class LLMService:
    def __init__(self):
        self._client: Optional[genai.Client] = None

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(api_key=config.GEMINI_API_KEY)
        return self._client

    def generate(self, query: str, context: str) -> str:
        """Generate a response grounded in the retrieved SOP context."""
        prompt = f"""Context from SOP documents:
{context}

User question: {query}

Answer based only on the context above."""

        try:
            response = self._get_client().models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=800,
                ),
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise
