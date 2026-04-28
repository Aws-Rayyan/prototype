"""Approve or reject draft actions."""

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import require_user
from models import ActionOut, ApprovalUpdate
from services.action_service import get_action, list_actions_for_user, update_action_status
from services.audit_service import append_event
from users import MockUser

router = APIRouter(tags=["approvals"])


@router.get("/approvals/pending", response_model=list[ActionOut])
async def pending_actions(_user: MockUser = Depends(require_user)) -> list[ActionOut]:
    """List all draft actions (visible to reviewers; prototype simplifies RBAC here)."""
    rows = list_actions_for_user(status_filter="draft")
    return [_to_out(r) for r in rows]


@router.patch("/approvals/{action_id}", response_model=ActionOut)
async def review_action(
    action_id: str,
    payload: ApprovalUpdate,
    user: MockUser = Depends(require_user),
) -> ActionOut:
    prev = get_action(action_id)
    if not prev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")

    result = update_action_status(action_id, payload.status, user.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")
    if result.get("error") == "not_draft":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Action is not in draft")

    evt = (
        "action_approved"
        if payload.status == "approved"
        else "action_rejected"
    )
    append_event(
        evt,
        user.id,
        {
            "action_id": action_id,
            "status": payload.status,
            "action_title": prev["title"],
            "creator": prev["created_by"],
            "reviewed_by_role": user.role,
        },
    )

    return _to_out(result)


def _to_out(r: dict) -> ActionOut:
    return ActionOut(
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
