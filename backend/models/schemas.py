from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    detected_language: str
    ticket_id: Optional[str] = None
    sources: List[str] = []
    session_id: Optional[str] = None


class TicketListItem(BaseModel):
    id: str
    query: str
    language: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    qdrant: str
    openai: str
