import logging
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Session

from backend.config import config

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8].upper())
    query = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default="en")
    status = Column(String(20), nullable=False, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)


class TicketService:
    def __init__(self):
        db_url = f"sqlite:///{config.TICKETING_DB}"
        self._engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self._engine)
        logger.info(f"Ticket DB initialised at {config.TICKETING_DB}")

    def create(self, query: str, language: str = "en", session_id: Optional[str] = None) -> str:
        ticket_id = str(uuid.uuid4())[:8].upper()
        with Session(self._engine) as session:
            ticket = Ticket(
                id=ticket_id,
                query=query,
                language=language,
                status="open",
                created_at=datetime.utcnow(),
                session_id=session_id,
            )
            session.add(ticket)
            session.commit()
        logger.info(f"Ticket created: #{ticket_id} (lang={language})")
        return ticket_id

    def list_tickets(self, limit: int = 50) -> List[dict]:
        with Session(self._engine) as session:
            tickets = (
                session.query(Ticket)
                .order_by(Ticket.created_at.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": t.id,
                    "query": t.query,
                    "language": t.language,
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else "",
                    "session_id": t.session_id,
                }
                for t in tickets
            ]

    def close_ticket(self, ticket_id: str) -> bool:
        with Session(self._engine) as session:
            ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return False
            ticket.status = "closed"
            session.commit()
        return True
