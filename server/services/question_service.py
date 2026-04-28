"""Persist questions."""

import json

from database import get_connection


def insert_question(
    question_id: str,
    user_id: str,
    question: str,
    answer: str,
    confidence: str,
    cited_doc_ids: list[str],
    created_at: str,
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO questions (id, user_id, question, answer, confidence, cited_doc_ids, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                question_id,
                user_id,
                question,
                answer,
                confidence,
                json.dumps(cited_doc_ids),
                created_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()
