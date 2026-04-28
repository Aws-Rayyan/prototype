"""FastAPI dependencies."""

from typing import Annotated

from fastapi import Header, HTTPException, status

from users import MockUser, get_user_by_header


async def require_user(
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
) -> MockUser:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header is required",
        )
    try:
        return get_user_by_header(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown user",
        ) from None
