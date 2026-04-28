"""Pydantic request/response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Confidence = Literal["well_supported", "partial", "insufficient"]


class Citation(BaseModel):
    doc_id: str
    doc_title: str
    snippet: str
    relevance: float


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    question_id: str
    answer: str
    confidence: Confidence
    citations: list[Citation]
    retrieved_below_threshold: bool = False


class UserOut(BaseModel):
    id: str
    name: str
    role: str


class ActionCreate(BaseModel):
    question_id: str
    action_type: Literal["email", "note", "task"]
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class ActionOut(BaseModel):
    id: str
    question_id: str
    created_by: str
    action_type: str
    title: str
    body: str
    status: str
    reviewed_by: str | None
    reviewed_at: str | None
    created_at: str


class ApprovalUpdate(BaseModel):
    status: Literal["approved", "rejected"]


class AuditEntryOut(BaseModel):
    id: str
    event_type: str
    user_id: str
    detail: dict
    created_at: str
