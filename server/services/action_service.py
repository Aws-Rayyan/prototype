"""Draft actions."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from database import get_connection


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_question_exists(question_id: str) -> bool:
    conn = get_connection()
    try:
        row = conn.execute("SELECT 1 FROM questions WHERE id = ?", (question_id,)).fetchone()
        return row is not None
    finally:
        conn.close()


def create_action(
    question_id: str,
    created_by: str,
    action_type: str,
    title: str,
    body: str,
) -> dict[str, Any]:
    aid = str(uuid.uuid4())
    ts = _now_iso()
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO actions (id, question_id, created_by, type, title, body, status, reviewed_by,
            reviewed_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'draft', NULL, NULL, ?)
            """,
            (aid, question_id, created_by, action_type, title, body, ts),
        )
        conn.commit()
    finally:
        conn.close()
    return {
        "id": aid,
        "question_id": question_id,
        "created_by": created_by,
        "action_type": action_type,
        "title": title,
        "body": body,
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": ts,
    }


def list_actions_for_user(user_id: str | None = None, status_filter: str | None = None) -> list[dict]:
    conn = get_connection()
    try:
        if user_id and status_filter:
            cur = conn.execute(
                """
                SELECT * FROM actions WHERE created_by = ? AND status = ?
                ORDER BY datetime(created_at) DESC
                """,
                (user_id, status_filter),
            )
        elif user_id:
            cur = conn.execute(
                """
                SELECT * FROM actions WHERE created_by = ?
                ORDER BY datetime(created_at) DESC
                """,
                (user_id,),
            )
        elif status_filter:
            cur = conn.execute(
                """
                SELECT * FROM actions WHERE status = ?
                ORDER BY datetime(created_at) DESC
                """,
                (status_filter,),
            )
        else:
            cur = conn.execute("SELECT * FROM actions ORDER BY datetime(created_at) DESC")
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_action(action_id: str) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM actions WHERE id = ?", (action_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_action_status(
    action_id: str,
    status: str,
    reviewed_by: str,
) -> dict | None:
    ts = _now_iso()
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM actions WHERE id = ?", (action_id,)).fetchone()
        if not row:
            return None
        if dict(row)["status"] != "draft":
            return {"error": "not_draft"}
        conn.execute(
            """
            UPDATE actions SET status = ?, reviewed_by = ?, reviewed_at = ?
            WHERE id = ?
            """,
            (status, reviewed_by, ts, action_id),
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM actions WHERE id = ?", (action_id,)).fetchone()
        return dict(updated) if updated else None
    finally:
        conn.close()
