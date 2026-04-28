import { useState } from "react";
import AnswerCard from "../components/AnswerCard";
import DraftActionForm from "../components/DraftActionForm";
import { useUserContext } from "../context/UserContext";
import type { AskResponse } from "../types";

export default function AskPage() {
  const { api, user } = useUserContext();
  const [question, setQuestion] = useState(
    "What discount approvals are required for enterprise deals?",
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AskResponse | null>(null);
  const [showDraft, setShowDraft] = useState(false);

  async function ask() {
    setLoading(true);
    setError(null);
    try {
      const trimmed = question.trim();
      const { data } = await api.post<AskResponse>("/api/ask", {
        question: trimmed,
      });
      setResult(data);
    } catch (e: unknown) {
      setResult(null);
      if (typeof e === "object" && e !== null && "response" in e) {
        const err = e as {
          response?: { data?: { detail?: unknown } };
        };
        const det = err.response?.data?.detail;
        setError(typeof det === "string" ? det : JSON.stringify(det));
      } else {
        setError(e instanceof Error ? e.message : "Request failed");
      }
    } finally {
      setLoading(false);
    }
  }

  async function saveDraft(payload: {
    title: string;
    body: string;
    action_type: "email" | "note" | "task";
  }) {
    if (!result) return;
    await api.post("/api/actions", {
      question_id: result.question_id,
      action_type: payload.action_type,
      title: payload.title,
      body: payload.body,
    });
  }

  return (
    <div className="space-y-10">
      <section className="space-y-2">
        <h2 className="text-2xl font-semibold">Ask Gaia</h2>
        <p className="max-w-2xl text-zinc-400">
          Questions are grounded only in documents permitted for{" "}
          <span className="font-semibold text-zinc-200">{user.role}</span>. Other
          corpora are hidden from retrieval, answers, citations, and downstream
          actions.
        </p>
      </section>

      <section className="space-y-3">
        <label className="block text-sm font-medium text-zinc-300">
          Your question
        </label>
        <textarea
          className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm outline-none ring-teal-500/40 focus:ring"
          rows={4}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          type="button"
          className="rounded-lg bg-teal-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-teal-500 disabled:opacity-60"
          onClick={() => void ask()}
          disabled={loading || !question.trim()}
        >
          {loading ? "Thinking…" : "Ask Gaia"}
        </button>
        {error && <p className="text-sm text-rose-300">{error}</p>}
      </section>

      {result && (
        <>
          <AnswerCard result={result} />
          {result.confidence !== "insufficient" && (
            <div>
              <button
                type="button"
                className="rounded border border-teal-500 px-5 py-2 text-sm font-semibold text-teal-200 hover:bg-teal-500/15"
                onClick={() => setShowDraft(true)}
              >
                Create draft action from this answer
              </button>
            </div>
          )}
        </>
      )}

      <DraftActionForm
        open={showDraft}
        lastAnswer={result}
        onClose={() => setShowDraft(false)}
        onSubmit={async (draft) => {
          await saveDraft(draft);
        }}
      />

      <section className="rounded-lg border border-dashed border-zinc-800 bg-zinc-950/70 p-4 text-xs text-zinc-500">
        Tip: Compare behavior by switching users — Alice (sales docs), Bob (HR docs), Aws Rayyan (no seeded
        corpus → always insufficient evidence), engineering-only content never surfaces for Alice or Bob.
      </section>
    </div>
  );
}
