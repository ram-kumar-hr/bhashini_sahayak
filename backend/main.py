import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from typing import List

import shutil
import uuid
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.config import config
from backend.models.schemas import ChatRequest, ChatResponse, TicketListItem, HealthResponse
from backend.graph.workflow import SahayakWorkflow
from backend.services.ticket_service import TicketService

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

# Shared state initialised once at startup
_workflow: SahayakWorkflow | None = None
_ticket_svc: TicketService | None = None
_executor = ThreadPoolExecutor(max_workers=4)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _workflow, _ticket_svc
    logger.info("Starting Bhashini Sahayak backend…")
    _ticket_svc = TicketService()
    _workflow = SahayakWorkflow()
    logger.info("Workflow and services ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Bhashini Sahayak API",
    description="CAG platform chatbot — multilingual SOP assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint. Accepts a query, returns a grounded response."""
    if not _workflow:
        raise HTTPException(status_code=503, detail="Service not ready")

    session_id = request.session_id or str(uuid.uuid4())

    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(_executor, _workflow.run, request.query)
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

    return ChatResponse(
        response=result["response"],
        detected_language=result["detected_language"],
        ticket_id=result.get("ticket_id"),
        sources=result.get("sources", []),
        session_id=session_id,
    )


@app.get("/tickets", response_model=List[TicketListItem])
async def list_tickets():
    """Return the most recent support tickets."""
    if not _ticket_svc:
        raise HTTPException(status_code=503, detail="Service not ready")
    return _ticket_svc.list_tickets(limit=50)


@app.patch("/tickets/{ticket_id}/close")
async def close_ticket(ticket_id: str):
    """Mark a ticket as closed."""
    if not _ticket_svc:
        raise HTTPException(status_code=503, detail="Service not ready")
    success = _ticket_svc.close_ticket(ticket_id.upper())
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "closed", "ticket_id": ticket_id.upper()}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (PDF/DOCX/TXT/MD) and ingest it into the knowledge base."""
    from backend.services.document_service import (
        extract_text, build_chunks, SUPPORTED_EXTENSIONS, UPLOADS_DIR
    )
    from backend.services.qdrant_service import QdrantService

    suffix = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {', '.join(SUPPORTED_EXTENSIONS)}",
        )

    # Save to uploads/
    save_path = UPLOADS_DIR / file.filename
    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract → chunk → embed → upsert
    try:
        text = extract_text(save_path)
        if not text.strip():
            raise ValueError("No text could be extracted from the file.")

        source_name = file.filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
        chunks = build_chunks(text, source_name)

        def _ingest():
            svc = QdrantService()
            # Assign IDs that won't clash with existing points
            import time
            base_id = int(time.time() * 1000)
            for i, c in enumerate(chunks):
                c["id"] = base_id + i
            return svc.upsert_chunks(chunks)

        loop = asyncio.get_event_loop()
        inserted = await loop.run_in_executor(_executor, _ingest)

        logger.info(f"Uploaded '{file.filename}': {inserted} chunks ingested")
        return {
            "filename": file.filename,
            "chunks_ingested": inserted,
            "status": "success",
        }
    except Exception as e:
        save_path.unlink(missing_ok=True)
        logger.error(f"Upload failed for '{file.filename}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all uploaded documents."""
    from backend.services.document_service import UPLOADS_DIR, SUPPORTED_EXTENSIONS
    files = [
        {"filename": f.name, "size_kb": round(f.stat().st_size / 1024, 1)}
        for f in sorted(UPLOADS_DIR.iterdir())
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return {"documents": files}


@app.get("/health", response_model=HealthResponse)
async def health():
    """Simple health check."""
    from backend.services.qdrant_service import QdrantService
    qdrant_ok = "ok"
    try:
        QdrantService().collection_exists()
    except Exception:
        qdrant_ok = "unavailable"

    openai_ok = "configured" if config.GEMINI_API_KEY else "not configured"

    return HealthResponse(
        status="ok",
        qdrant=qdrant_ok,
        openai=openai_ok,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=config.SERVICE_HOST,
        port=config.SERVICE_PORT,
        reload=True,
    )
