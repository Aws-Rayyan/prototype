"""Audit log read API."""

from fastapi import APIRouter, Depends

from dependencies import require_user

from models import AuditEntryOut
from services.audit_service import list_entries
from users import MockUser

router = APIRouter(tags=["audit"])


@router.get("/audit", response_model=list[AuditEntryOut])
async def audit_logs(
    limit: int = 200,
    _: MockUser = Depends(require_user),
) -> list[AuditEntryOut]:
    rows = list_entries(limit=min(limit, 500))
    return [
        AuditEntryOut(
            id=r["id"],
            event_type=r["event_type"],
            user_id=r["user_id"],
            detail=r["detail"],
            created_at=r["created_at"],
        )
        for r in rows
    ]
