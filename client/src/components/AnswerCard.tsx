import type { AskResponse } from "../types";

function confidenceLabel(c: AskResponse["confidence"]): string {
  if (c === "well_supported") return "Well-supported";
  if (c === "partial") return "Partial evidence";
  return "Insufficient evidence";
}

function confidenceStyle(c: AskResponse["confidence"]) {
  if (c === "well_supported")
    return "bg-emerald-500/15 text-emerald-300 border-emerald-700";
  if (c === "partial")
    return "bg-amber-500/15 text-amber-200 border-amber-700";
  return "bg-rose-500/15 text-rose-200 border-rose-700";
}

export default function AnswerCard({
  result,
}: {
  result: AskResponse;
}) {
  return (
    <div className="space-y-6 rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Answer</h2>
        <span
          className={`rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${confidenceStyle(
            result.confidence,
          )}`}
        >
          {confidenceLabel(result.confidence)}
        </span>
      </div>
      {result.retrieved_below_threshold && (
        <p className="text-sm text-amber-300">
          Retrieval did not surface strong enough trusted matches for this role.
          Inaccessible documents were not used.
        </p>
      )}
      <article className="whitespace-pre-wrap text-sm leading-relaxed text-zinc-200">
        {result.answer}
      </article>
      {result.citations.length > 0 && (
        <div>
          <h3 className="mb-2 font-semibold text-zinc-300">Cited evidence</h3>
          <ul className="space-y-3">
            {result.citations.map((c, idx) => (
              <li
                key={`${c.doc_id}-${idx}`}
                className="rounded-lg border border-zinc-800 bg-black/40 p-4 text-sm"
              >
                <div className="mb-1 text-xs uppercase tracking-wide text-teal-400">
                  {c.doc_title}
                  <span className="text-zinc-500"> ({c.doc_id})</span>
                </div>
                <blockquote className="text-zinc-200">{c.snippet}</blockquote>
                <div className="mt-2 text-xs text-zinc-500">
                  Relevance score: {c.relevance.toFixed(4)}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
