import logging
from typing import List, Dict, Any, Optional

from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    ScoredPoint,
)

from backend.config import config

logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self):
        self._client: Optional[QdrantClient] = None
        self._genai_client: Optional[genai.Client] = None

    def _get_client(self) -> QdrantClient:
        if self._client is None:
            url = f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}"
            kwargs: Dict[str, Any] = {"url": url}
            if config.QDRANT_API_KEY:
                kwargs["api_key"] = config.QDRANT_API_KEY
            self._client = QdrantClient(**kwargs)
        return self._client

    def _get_genai(self) -> genai.Client:
        if self._genai_client is None:
            self._genai_client = genai.Client(api_key=config.GEMINI_API_KEY)
        return self._genai_client

    def _embed(self, text: str, task_type: str = "retrieval_document") -> List[float]:
        result = self._get_genai().models.embed_content(
            model=config.GEMINI_EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        return result.embeddings[0].values

    def _embed_batch(self, texts: List[str], task_type: str = "retrieval_document") -> List[List[float]]:
        result = self._get_genai().models.embed_content(
            model=config.GEMINI_EMBEDDING_MODEL,
            contents=texts,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        return [e.values for e in result.embeddings]

    def collection_exists(self) -> bool:
        try:
            collections = self._get_client().get_collections().collections
            return any(c.name == config.QDRANT_COLLECTION for c in collections)
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            return False

    def ensure_collection(self) -> None:
        client = self._get_client()
        if not self.collection_exists():
            client.create_collection(
                collection_name=config.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=config.GEMINI_EMBEDDING_DIMS,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(
                f"Created Qdrant collection '{config.QDRANT_COLLECTION}' "
                f"(dim={config.GEMINI_EMBEDDING_DIMS})"
            )

    def upsert_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Store text chunks with Gemini embeddings. Returns count inserted."""
        self.ensure_collection()
        client = self._get_client()

        if not chunks:
            return 0

        # Batch embed in groups of 100 (Gemini free-tier limit per request)
        BATCH_SIZE = 100
        all_embeddings: List[List[float]] = []
        texts = [c["content"] for c in chunks]
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i : i + BATCH_SIZE]
            try:
                all_embeddings.extend(self._embed_batch(batch, task_type="retrieval_document"))
            except Exception as e:
                logger.error(f"Batch embedding failed at offset {i}: {e}")
                return len(all_embeddings)  # return however many succeeded

        points: List[PointStruct] = []
        for chunk, embedding in zip(chunks, all_embeddings):
            points.append(
                PointStruct(
                    id=chunk.get("id", len(points)),
                    vector=embedding,
                    payload={
                        "content": chunk["content"],
                        "source": chunk.get("source", "SOP"),
                        "section": chunk.get("section", ""),
                    },
                )
            )

        client.upsert(collection_name=config.QDRANT_COLLECTION, points=points)
        logger.info(f"Upserted {len(points)} chunks into Qdrant")
        return len(points)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Semantic search; returns list of {content, source, score} dicts."""
        if not self.collection_exists():
            logger.warning("Qdrant collection not found — returning empty results")
            return []
        try:
            query_vector = self._embed(query, task_type="retrieval_query")
            results = self._get_client().query_points(
                collection_name=config.QDRANT_COLLECTION,
                query=query_vector,
                limit=config.TOP_K_RESULTS,
                score_threshold=config.MIN_RELEVANCE_SCORE,
            ).points
            return [
                {
                    "content": r.payload.get("content", ""),
                    "source": r.payload.get("source", "SOP"),
                    "section": r.payload.get("section", ""),
                    "score": r.score,
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Qdrant search error: {e}")
            return []
