"""Draft actions."""

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import require_user
from models import ActionCreate, ActionOut
from services.action_service import create_action, ensure_question_exists, list_actions_for_user
from services.audit_service import append_event
from users import MockUser

router = APIRouter(tags=["actions"])


@router.post("/actions", response_model=ActionOut, status_code=status.HTTP_201_CREATED)
async def post_action(payload: ActionCreate, user: MockUser = Depends(require_user)) -> ActionOut:
    if not ensure_question_exists(payload.question_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown question id; ask a question first.",
        )

    row = create_action(
        question_id=payload.question_id,
        created_by=user.id,
        action_type=payload.action_type,
        title=payload.title.strip(),
        body=payload.body.strip(),
    )

    append_event(
        "action_drafted",
        user.id,
        {
            "action_id": row["id"],
            "question_id": row["question_id"],
            "type": row["action_type"],
            "title": row["title"],
            "body_preview": row["body"][:500],
            "creator_role": user.role,
        },
    )

    return ActionOut(
        id=row["id"],
        question_id=row["question_id"],
        created_by=row["created_by"],
        action_type=row["action_type"],
        title=row["title"],
        body=row["body"],
        status=row["status"],
        reviewed_by=row["reviewed_by"],
        reviewed_at=row["reviewed_at"],
        created_at=row["created_at"],
    )


@router.get("/actions/me", response_model=list[ActionOut])
async def my_actions(user: MockUser = Depends(require_user)) -> list[ActionOut]:
    rows = list_actions_for_user(user_id=user.id)
    return [
        ActionOut(
            id=r["id"],
            question_id=r["question_id"],
            created_by=r["created_by"],
            action_type=r["type"],
            title=r["title"],
            body=r["body"],
            status=r["status"],
            reviewed_by=r["reviewed_by"],
            reviewed_at=r["reviewed_at"],
            created_at=r["created_at"],
        )
        for r in rows
    ]
