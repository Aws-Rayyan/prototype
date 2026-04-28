import { useCallback, useEffect, useState } from "react";
import { useUserContext } from "../context/UserContext";
import type { ActionItem } from "../types";

function statusTone(status: string) {
  switch (status) {
    case "draft":
      return "text-amber-300";
    case "approved":
      return "text-emerald-300";
    case "rejected":
      return "text-rose-300";
    default:
      return "text-zinc-300";
  }
}

export default function ActionsPage() {
  const { api } = useUserContext();
  const [items, setItems] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<ActionItem[]>("/api/actions/me");
      setItems(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load actions");
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">My draft actions</h2>
        <p className="text-zinc-400">
          Actions you created from grounded answers remain in Draft until reviewed.
        </p>
      </div>
      <button
        type="button"
        className="rounded border border-zinc-700 px-3 py-1 text-xs text-zinc-300 hover:bg-zinc-900"
        onClick={() => void reload()}
      >
        Refresh
      </button>
      {error && <p className="text-sm text-rose-300">{error}</p>}
      {loading ? (
        <p className="text-sm text-zinc-500">Loading…</p>
      ) : (
        <div className="space-y-4">
          {items.length === 0 && (
            <p className="text-zinc-500">No actions yet.</p>
          )}
          {items.map((a) => (
            <article
              key={a.id}
              className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <div className="text-xs uppercase text-teal-400">{a.action_type}</div>
                  <h3 className="text-lg font-semibold">{a.title}</h3>
                </div>
                <span className={`text-xs font-semibold uppercase ${statusTone(a.status)}`}>
                  {a.status}
                </span>
              </div>
              <pre className="mt-3 whitespace-pre-wrap text-sm">{a.body}</pre>
              <div className="mt-3 text-xs text-zinc-500">
                Question {a.question_id} • {new Date(a.created_at).toLocaleString()}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
