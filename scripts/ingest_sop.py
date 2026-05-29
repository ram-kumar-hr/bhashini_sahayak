#!/usr/bin/env python3
"""
Ingest SOP markdown files into Qdrant.

Usage (from repo root after activating venv):
    python -m scripts.ingest_sop

Reads all .md files from backend/data/, chunks them, embeds with OpenAI,
and upserts into the configured Qdrant collection.
"""
import sys
import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Any

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from backend.config import config
from backend.services.qdrant_service import QdrantService

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "backend" / "data"
CHUNK_SIZE = 600       # characters per chunk
CHUNK_OVERLAP = 80     # overlap between chunks


# ── Chunking ─────────────────────────────────────────────────────────────────

def _clean(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _split_by_sections(text: str) -> List[Dict[str, str]]:
    """Split markdown by ## headings, then sub-chunk large sections."""
    sections: List[Dict[str, str]] = []
    current_title = "Introduction"
    current_body: List[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_body:
                sections.append(
                    {"title": current_title, "content": "\n".join(current_body).strip()}
                )
            current_title = line.lstrip("#").strip()
            current_body = []
        else:
            current_body.append(line)

    if current_body:
        sections.append(
            {"title": current_title, "content": "\n".join(current_body).strip()}
        )

    return [s for s in sections if s["content"]]


def _chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Slide a window over text to produce overlapping chunks."""
    if len(text) <= size:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def load_and_chunk(filepath: Path) -> List[Dict[str, Any]]:
    source_name = filepath.stem.replace("_", " ").title()
    raw = _clean(filepath.read_text(encoding="utf-8"))

    sections = _split_by_sections(raw)
    all_chunks: List[Dict[str, Any]] = []
    chunk_id = 0

    for section in sections:
        text_chunks = _chunk_text(section["content"])
        for chunk in text_chunks:
            if chunk.strip():
                all_chunks.append(
                    {
                        "id": chunk_id,
                        "content": f"[{source_name} — {section['title']}]\n\n{chunk.strip()}",
                        "source": source_name,
                        "section": section["title"],
                    }
                )
                chunk_id += 1

    logger.info(f"  {filepath.name}: {len(sections)} sections → {len(all_chunks)} chunks")
    return all_chunks


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set. Cannot generate embeddings.")
        sys.exit(1)

    md_files = sorted(DATA_DIR.glob("*.md"))
    if not md_files:
        logger.error(f"No markdown files found in {DATA_DIR}")
        sys.exit(1)

    logger.info(f"Found {len(md_files)} SOP file(s) in {DATA_DIR}")

    all_chunks: List[Dict[str, Any]] = []
    global_id = 0
    for f in md_files:
        chunks = load_and_chunk(f)
        for c in chunks:
            c["id"] = global_id
            global_id += 1
        all_chunks.extend(chunks)

    logger.info(f"Total chunks to embed and store: {len(all_chunks)}")

    svc = QdrantService()
    svc.ensure_collection()

    inserted = svc.upsert_chunks(all_chunks)
    logger.info(f"Done. {inserted} chunks stored in collection '{config.QDRANT_COLLECTION}'.")


if __name__ == "__main__":
    main()
