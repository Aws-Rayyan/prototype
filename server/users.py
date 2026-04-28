"""Mock users for prototype auth."""

from pydantic import BaseModel


class MockUser(BaseModel):
    id: str
    name: str
    role: str


MOCK_USERS: dict[str, MockUser] = {
    "alice": MockUser(
        id="alice",
        name="Alice Johnson",
        role="sales_manager",
    ),
    "bob": MockUser(
        id="bob",
        name="Bob Smith",
        role="hr_manager",
    ),
    # Role not granted on any seeded document — retrieval yields nothing.
    "aws": MockUser(
        id="aws",
        name="Aws Rayyan",
        role="no_document_access",
    ),
}


def get_user_by_header(user_id: str | None) -> MockUser:
    """Resolve user from X-User-Id header."""
    if not user_id:
        raise ValueError("Missing X-User-Id header")
    uid = user_id.strip().lower()
    if uid not in MOCK_USERS:
        raise ValueError("Unknown user")
    return MOCK_USERS[uid]
