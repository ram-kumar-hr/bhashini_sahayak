"""LangGraph orchestration for Bhashini Sahayak.

Flow:
  detect_language
    ├─(non-English)→ translate_to_english → retrieve_docs
    └─(English)────────────────────────→ retrieve_docs
                                              ↓
                                       generate_response
                                         ├─(ticket needed)──→ create_ticket → END
                                         ├─(non-English)────→ translate_response → END
                                         └─(English, ok)────→ END
"""
import logging
from typing import TypedDict, Optional, List

from langgraph.graph import StateGraph, END

from backend.services.bhashini_service import BhashiniService, SUPPORTED_LANGUAGES
from backend.services.qdrant_service import QdrantService
from backend.services.llm_service import LLMService
from backend.services.ticket_service import TicketService

logger = logging.getLogger(__name__)


# ── State ────────────────────────────────────────────────────────────────────

class WorkflowState(TypedDict):
    original_query: str
    detected_language: str
    english_query: str
    context: str
    sources: List[str]
    response: str
    final_response: str
    needs_ticket: bool
    ticket_id: Optional[str]
    error: Optional[str]


# ── Node factories ────────────────────────────────────────────────────────────

def _make_detect_language():
    def detect_language(state: WorkflowState) -> dict:
        query = state["original_query"]
        try:
            from langdetect import detect, LangDetectException
            lang = detect(query)
            if lang not in SUPPORTED_LANGUAGES:
                lang = "en"
        except Exception:
            lang = "en"
        return {
            "detected_language": lang,
            "english_query": query if lang == "en" else "",
        }
    return detect_language


def _make_translate_to_english(bhashini: BhashiniService):
    def translate_to_english(state: WorkflowState) -> dict:
        try:
            translated = bhashini.translate(
                state["original_query"],
                state["detected_language"],
                "en",
            )
            return {"english_query": translated}
        except Exception as e:
            logger.warning(f"Query translation failed, using original: {e}")
            return {"english_query": state["original_query"]}
    return translate_to_english


def _make_retrieve_docs(qdrant: QdrantService):
    def retrieve_docs(state: WorkflowState) -> dict:
        try:
            results = qdrant.search(state["english_query"])
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            results = []

        if not results:
            return {
                "context": "",
                "sources": [],
                "needs_ticket": True,
            }

        context = "\n\n---\n\n".join(r["content"] for r in results)
        sources = list({r["source"] for r in results})
        return {
            "context": context,
            "sources": sources,
            "needs_ticket": False,
        }
    return retrieve_docs


def _make_generate_response(llm: LLMService):
    def generate_response(state: WorkflowState) -> dict:
        if state.get("needs_ticket"):
            return {
                "response": (
                    "I couldn't find relevant information in the knowledge base "
                    "to answer your query. A support ticket has been created for you."
                )
            }
        try:
            answer = llm.generate(state["english_query"], state["context"])
            return {"response": answer}
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "response": "I encountered an error generating a response. A support ticket will be created.",
                "needs_ticket": True,
            }
    return generate_response


def _make_translate_response(bhashini: BhashiniService):
    def translate_response(state: WorkflowState) -> dict:
        try:
            translated = bhashini.translate(
                state["response"],
                "en",
                state["detected_language"],
            )
            return {"final_response": translated}
        except Exception as e:
            logger.warning(f"Response translation failed, using English: {e}")
            return {"final_response": state["response"]}
    return translate_response


def _make_create_ticket(ticket_svc: TicketService):
    def create_ticket(state: WorkflowState) -> dict:
        try:
            ticket_id = ticket_svc.create(
                query=state["original_query"],
                language=state["detected_language"],
            )
            base = state.get("final_response") or state.get("response", "")
            final = f"{base}\n\n📋 Support ticket created — ID: **#{ticket_id}**"
            return {"ticket_id": ticket_id, "final_response": final}
        except Exception as e:
            logger.error(f"Ticket creation failed: {e}")
            return {"ticket_id": None, "final_response": state.get("response", "")}
    return create_ticket


# ── Routing ──────────────────────────────────────────────────────────────────

def _route_after_detect(state: WorkflowState) -> str:
    return "translate_query" if state["detected_language"] != "en" else "retrieve_docs"


def _route_after_generate(state: WorkflowState) -> str:
    if state.get("needs_ticket"):
        return "create_ticket"
    if state["detected_language"] != "en":
        return "translate_response"
    return END


def _route_after_translate_response(state: WorkflowState) -> str:
    return "create_ticket" if state.get("needs_ticket") else END


# ── Graph builder ─────────────────────────────────────────────────────────────

class SahayakWorkflow:
    def __init__(self):
        self._bhashini = BhashiniService()
        self._qdrant = QdrantService()
        self._llm = LLMService()
        self._ticket = TicketService()
        self._graph = self._build()

    def _build(self):
        wf = StateGraph(WorkflowState)

        wf.add_node("detect_language", _make_detect_language())
        wf.add_node("translate_query", _make_translate_to_english(self._bhashini))
        wf.add_node("retrieve_docs", _make_retrieve_docs(self._qdrant))
        wf.add_node("generate_response", _make_generate_response(self._llm))
        wf.add_node("translate_response", _make_translate_response(self._bhashini))
        wf.add_node("create_ticket", _make_create_ticket(self._ticket))

        wf.set_entry_point("detect_language")

        wf.add_conditional_edges(
            "detect_language",
            _route_after_detect,
            {"translate_query": "translate_query", "retrieve_docs": "retrieve_docs"},
        )
        wf.add_edge("translate_query", "retrieve_docs")
        wf.add_edge("retrieve_docs", "generate_response")
        wf.add_conditional_edges(
            "generate_response",
            _route_after_generate,
            {
                "translate_response": "translate_response",
                "create_ticket": "create_ticket",
                END: END,
            },
        )
        wf.add_conditional_edges(
            "translate_response",
            _route_after_translate_response,
            {"create_ticket": "create_ticket", END: END},
        )
        wf.add_edge("create_ticket", END)

        return wf.compile()

    def run(self, query: str) -> dict:
        initial: WorkflowState = {
            "original_query": query,
            "detected_language": "",
            "english_query": "",
            "context": "",
            "sources": [],
            "response": "",
            "final_response": "",
            "needs_ticket": False,
            "ticket_id": None,
            "error": None,
        }
        result = self._graph.invoke(initial)
        return {
            "response": result.get("final_response") or result.get("response", ""),
            "detected_language": result.get("detected_language", "en"),
            "ticket_id": result.get("ticket_id"),
            "sources": result.get("sources", []),
        }
