"""Permission-aware document retrieval."""

from __future__ import annotations

import json
import math
import re
import sqlite3
from dataclasses import dataclass

from database import get_connection


@dataclass
class RetrievedDoc:
    doc_id: str
    title: str
    content: str
    department: str
    score: float


_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "must",
    "can",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 1]


def fetch_accessible_documents_for_role(role: str) -> list[dict]:
    """Return docs the role may access using SQLite json_each, with fallback."""
    conn = get_connection()
    try:
        try:
            cur = conn.execute(
                """
                SELECT DISTINCT d.id, d.title, d.content, d.department, d.allowed_roles
                FROM documents d, json_each(d.allowed_roles) AS je
                WHERE je.value = ?
                """,
                (role,),
            )
            rows = [dict(r) for r in cur.fetchall()]
            return rows
        except sqlite3.OperationalError:
            cur = conn.execute(
                "SELECT id, title, content, department, allowed_roles FROM documents",
            )
            out = []
            for r in cur.fetchall():
                row = dict(r)
                roles = json.loads(row["allowed_roles"])
                if role in roles:
                    out.append(row)
            return out
    finally:
        conn.close()


def search(query: str, role: str, top_k: int = 5) -> tuple[list[RetrievedDoc], bool]:
    """
    Retrieve documents filtered by permission, then ranked by keyword overlap.
    Returns (results, retrieved_below_threshold) where the second indicates all scores were unusably low.
    """
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return [], True

    accessible = fetch_accessible_documents_for_role(role)
    scored: list[RetrievedDoc] = []

    for row in accessible:
        doc_tokens = _tokenize(row["content"] + " " + row["title"])
        if not doc_tokens:
            continue
        overlap = len(query_tokens & set(doc_tokens))
        # Normalize: overlap relative to sqrt of doc size to avoid mega-docs dominating
        denom = math.sqrt(max(len(doc_tokens), 1))
        score = overlap / denom
        if overlap == 0:
            # Loose partial: substring matches for hyphenated/acronyms
            qtxt = query.lower().strip()
            if len(qtxt) >= 4 and qtxt in row["content"].lower():
                score = 0.15
                overlap = 1
        scored.append(
            RetrievedDoc(
                doc_id=row["id"],
                title=row["title"],
                content=row["content"].strip(),
                department=row["department"],
                score=score,
            )
        )

    scored.sort(key=lambda d: -d.score)
    top = scored[:top_k]

    # Heuristic: signal "no useful hit" — no overlap at all on top docs
    if not top or all(d.score <= 0.001 for d in top):
        return [], True

    return top, False
