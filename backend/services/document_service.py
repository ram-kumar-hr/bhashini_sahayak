import logging
import re
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

CHUNK_SIZE = 600
CHUNK_OVERLAP = 80
UPLOADS_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf(file_path)
    elif suffix in {".docx", ".doc"}:
        return _extract_docx(file_path)
    elif suffix in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def _extract_pdf(path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def _extract_docx(path: Path) -> str:
    from docx import Document
    doc = Document(str(path))
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _clean(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _chunk(text: str) -> List[str]:
    if len(text) <= CHUNK_SIZE:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if c.strip()]


def build_chunks(text: str, source_name: str) -> List[Dict[str, Any]]:
    """Split extracted text into Qdrant-ready chunk dicts."""
    text = _clean(text)
    raw_chunks = _chunk(text)
    return [
        {
            "id": i,
            "content": f"[{source_name}]\n\n{chunk}",
            "source": source_name,
            "section": "",
        }
        for i, chunk in enumerate(raw_chunks)
    ]
