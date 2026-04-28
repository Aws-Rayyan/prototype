import { useCallback, useEffect, useState } from "react";
import AuditTable from "../components/AuditTable";
import { useUserContext } from "../context/UserContext";
import type { AuditEntry } from "../types";

export default function AuditPage() {
  const { api } = useUserContext();
  const [rows, setRows] = useState<AuditEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const { data } = await api.get<AuditEntry[]>("/api/audit?limit=200");
      setRows(data);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load audit log");
    }
  }, [api]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Audit log</h2>
        <p className="max-w-2xl text-zinc-400">
          Immutable chronological history of grounded answers and workflow steps. Details include
          previews only — answers always reflect permission-filtered retrieval.
        </p>
      </div>
      <button
        type="button"
        className="rounded border border-zinc-700 px-3 py-1 text-xs text-zinc-300 hover:bg-zinc-900"
        onClick={() => void load()}
      >
        Refresh
      </button>
      {error && <p className="text-sm text-rose-300">{error}</p>}
      <AuditTable rows={rows} />
    </div>
  );
}
