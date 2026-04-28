"""Rule-based grounded answer generation."""

from __future__ import annotations

import re
import uuid
from typing import Literal

from models import AskResponse, Citation
from services.retrieval import RetrievedDoc


Confidence = Literal["well_supported", "partial", "insufficient"]

# Tunable thresholds (simple keyword scorer)
PARTIAL_MIN = 0.12
STRONG_DOC = 0.32


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [p.strip() for p in parts if len(p.strip()) > 40]


def _best_snippets(doc: RetrievedDoc, query: str, limit: int = 2) -> list[str]:
    q_terms = set(re.findall(r"[a-z0-9']+", query.lower()))
    sentences = _split_sentences(doc.content)
    ranked: list[tuple[int, int, str]] = []
    for sent in sentences:
        st = set(re.findall(r"[a-z0-9']+", sent.lower()))
        overlap = len(q_terms & st)
        if overlap:
            ranked.append((overlap, len(sent), sent))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    snippets = [r[2] for r in ranked[:limit]]
    if not snippets and doc.content.strip():
        snippets = [doc.content.strip()[:400] + ("…" if len(doc.content) > 400 else "")]
    return snippets


def generate_answer(
    question: str,
    retrieved: list[RetrievedDoc],
    empty_or_weak: bool,
    *,
    question_id: str | None = None,
) -> AskResponse:
    """
    Produce grounded answer and confidence from retrieved chunks.
    `empty_or_weak`: True when retrieval found nothing usable.
    """
    qid = question_id or str(uuid.uuid4())

    if empty_or_weak or not retrieved:
        return AskResponse(
            question_id=qid,
            answer=(
                "I don't have enough evidence in the documents you're allowed to access to answer "
                "this question confidently. Try rephrasing with specific policy names or timeframes, "
                "or verify you have permission to the relevant corpus."
            ),
            confidence="insufficient",
            citations=[],
            retrieved_below_threshold=True,
        )

    top = retrieved[0]
    top_two = retrieved[:2]
    avg_two = sum(d.score for d in top_two) / len(top_two)

    if len(retrieved) >= 2 and avg_two >= STRONG_DOC:
        confidence: Confidence = "well_supported"
    elif top.score >= STRONG_DOC:
        confidence = "well_supported"
    elif top.score >= PARTIAL_MIN or avg_two >= PARTIAL_MIN * 0.85:
        confidence = "partial"
    else:
        return AskResponse(
            question_id=qid,
            answer=(
                "There is insufficient evidence in your accessible documents to support a reliable "
                "answer about this topic. Matches were too weak to ground citations safely."
            ),
            confidence="insufficient",
            citations=[],
            retrieved_below_threshold=True,
        )

    citations: list[Citation] = []
    parts: list[str] = []

    for doc in retrieved[: min(3, len(retrieved))]:
        snippets = _best_snippets(doc, question)
        for snip in snippets:
            if not snip:
                continue
            citations.append(
                Citation(
                    doc_id=doc.doc_id,
                    doc_title=doc.title,
                    snippet=snip[:600],
                    relevance=doc.score,
                )
            )

    seen: set[tuple[str, str]] = set()
    deduped: list[Citation] = []
    for c in citations:
        key = (c.doc_id, c.snippet[:120])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(c)
    citations = deduped[:5]

    if confidence == "well_supported":
        intro = (
            "Based on the accessible internal documents listed below, the following summarizes what we "
            "can ground with cited evidence:"
        )
    else:
        intro = (
            "Below is the best-supported answer from partial matches in documents you're allowed to read. "
            "Interpret cautiously:"
        )

    parts_body: list[str] = []
    for c in citations:
        parts_body.append(f"[{c.doc_title}] {c.snippet}")

    answer_body = intro + "\n\n" + "\n\n".join(parts_body)
    if confidence == "partial":
        answer_body += "\n\nEvidence is partial — confirm with stakeholders or additional sources."

    return AskResponse(
        question_id=qid,
        answer=answer_body.strip(),
        confidence=confidence,
        citations=citations,
        retrieved_below_threshold=False,
    )
