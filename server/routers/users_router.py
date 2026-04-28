"""Mock user listing."""

from fastapi import APIRouter

from models import UserOut
from users import MOCK_USERS

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserOut])
async def list_users() -> list[UserOut]:
    """Return configured mock identities (helps front-end stay in sync)."""
    return [
        UserOut(id=u.id, name=u.name, role=u.role) for u in MOCK_USERS.values()
    ]
