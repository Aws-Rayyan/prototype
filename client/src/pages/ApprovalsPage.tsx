import { useCallback, useEffect, useState } from "react";
import ApprovalCard from "../components/ApprovalCard";
import { useUserContext } from "../context/UserContext";
import type { ActionItem } from "../types";

export default function ApprovalsPage() {
  const { user, api } = useUserContext();
  const [items, setItems] = useState<ActionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<ActionItem[]>("/api/approvals/pending");
      setItems(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load drafts");
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold">Approvals queue</h2>
        <p className="text-zinc-400">
          Review drafts with full payloads. Approvals mutate server state (
          <span className="text-zinc-200">{user.name}</span> signing each decision).
          Prototype: any logged-in reviewer can approve for demo clarity.
        </p>
      </div>
      {error && <p className="text-sm text-rose-300">{error}</p>}
      {loading ? (
        <p className="text-sm text-zinc-500">Loading draft actions…</p>
      ) : items.length === 0 ? (
        <p className="text-zinc-500">No draft actions awaiting review.</p>
      ) : (
        <div className="space-y-6">
          {items.map((action) => (
            <ApprovalCard key={action.id} action={action} onChanged={load} />
          ))}
        </div>
      )}
    </div>
  );
}
