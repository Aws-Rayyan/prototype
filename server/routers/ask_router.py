"""Ask Gaia grounded Q&A."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import require_user
from models import AskRequest, AskResponse
from services.answer_generator import generate_answer
from services.audit_service import append_event
from services.question_service import insert_question
from services.retrieval import search
from users import MockUser

router = APIRouter(tags=["ask"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,
    user: MockUser = Depends(require_user),
) -> AskResponse:
    trimmed = payload.question.strip()
    if not trimmed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question is empty")

    hits, weak = search(trimmed, user.role)
    # weak flag from retrieval plus empty hits
    empty_or_weak = weak or len(hits) == 0
    response = generate_answer(trimmed, hits, empty_or_weak)

    cited_ids = list(dict.fromkeys(c.doc_id for c in response.citations))
    ts = _now_iso()

    insert_question(
        question_id=response.question_id,
        user_id=user.id,
        question=trimmed,
        answer=response.answer,
        confidence=response.confidence,
        cited_doc_ids=cited_ids,
        created_at=ts,
    )

    append_event(
        "question_asked",
        user.id,
        {
            "question_id": response.question_id,
            "question": trimmed,
            "answer_preview": response.answer[:500],
            "confidence": response.confidence,
            "cited_doc_ids": cited_ids,
            "below_threshold": response.retrieved_below_threshold,
            "acting_as": user.role,
            "audit_note": (
                "Only documents permitted for this role contributed to retrieval and citations."
            ),
        },
    )

    return response
