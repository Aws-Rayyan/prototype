import { useState } from "react";
import type { ActionItem } from "../types";
import { useUserContext } from "../context/UserContext";

type Props = {
  action: ActionItem;
  onChanged: () => void;
};

export default function ApprovalCard({ action, onChanged }: Props) {
  const { api } = useUserContext();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function review(status: "approved" | "rejected") {
    setBusy(true);
    setError(null);
    try {
      await api.patch(`/api/approvals/${action.id}`, { status });
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <article className="space-y-3 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <header className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="text-xs uppercase text-zinc-500">{action.action_type}</div>
          <h3 className="text-lg font-semibold">{action.title}</h3>
          <div className="text-sm text-zinc-400">
            Created by {action.created_by} · Question {action.question_id}
          </div>
        </div>
      </header>
      <pre className="whitespace-pre-wrap rounded-lg bg-black/50 p-4 text-sm">
        {action.body}
      </pre>
      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          className="rounded bg-emerald-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
          disabled={busy}
          onClick={() => void review("approved")}
        >
          Approve
        </button>
        <button
          type="button"
          className="rounded bg-rose-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
          disabled={busy}
          onClick={() => void review("rejected")}
        >
          Reject
        </button>
      </div>
      {error && <div className="text-sm text-rose-300">{error}</div>}
    </article>
  );
}
