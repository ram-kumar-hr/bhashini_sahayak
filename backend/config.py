import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    # OpenAI (optional — kept for reference, not used when Gemini is configured)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Google Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
    GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
    GEMINI_EMBEDDING_DIMS: int = 3072

    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "bhashini_sop")

    # Bhashini / Dhruva
    BHASHINI_API_URL: str = os.getenv(
        "BHASHINI_API_URL", "https://dhruva-api.bhashini.gov.in"
    )
    BHASHINI_API_KEY: str = os.getenv("BHASHINI_API_KEY", "")
    BHASHINI_USER_ID: str = os.getenv("BHASHINI_USER_ID", "")
    BHASHINI_TRANSLATION_SERVICE_ID: str = os.getenv(
        "BHASHINI_TRANSLATION_SERVICE_ID",
        "ai4bharat/indictrans-v2-all-gpu--t4",
    )

    # Ticketing
    TICKETING_DB: str = os.getenv("TICKETING_DB", "./tickets.db")

    # Server
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "0.0.0.0")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8000"))

    # RAG
    MIN_RELEVANCE_SCORE: float = float(os.getenv("MIN_RELEVANCE_SCORE", "0.60"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "4"))


config = Config()
