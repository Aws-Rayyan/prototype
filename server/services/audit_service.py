"""Audit logging."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from database import get_connection


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_event(event_type: str, user_id: str, detail: dict[str, Any]) -> str:
    eid = str(uuid.uuid4())
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO audit_log (id, event_type, user_id, detail, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (eid, event_type, user_id, json.dumps(detail, ensure_ascii=False), _now_iso()),
        )
        conn.commit()
    finally:
        conn.close()
    return eid


def list_entries(limit: int = 200) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT id, event_type, user_id, detail, created_at
            FROM audit_log
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        )
        out = []
        for row in cur.fetchall():
            d = dict(row)
            d["detail"] = json.loads(d["detail"])
            out.append(d)
        return out
    finally:
        conn.close()
