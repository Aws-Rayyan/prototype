import type { AuditEntry } from "../types";

type Props = {
  rows: AuditEntry[];
};

export default function AuditTable({ rows }: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-zinc-800">
      <table className="min-w-full divide-y divide-zinc-800 text-sm">
        <thead className="bg-zinc-950/70 text-xs uppercase tracking-wide text-zinc-400">
          <tr>
            <th className="px-4 py-3 text-left">When</th>
            <th className="px-4 py-3 text-left">User</th>
            <th className="px-4 py-3 text-left">Event</th>
            <th className="px-4 py-3 text-left">Detail</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-900">
          {rows.map((entry) => (
            <tr key={entry.id} className="align-top">
              <td className="whitespace-nowrap px-4 py-3 text-zinc-400">
                {new Date(entry.created_at).toLocaleString()}
              </td>
              <td className="whitespace-nowrap px-4 py-3 font-mono text-xs text-teal-300">
                {entry.user_id}
              </td>
              <td className="whitespace-nowrap px-4 py-3 font-semibold text-zinc-200">
                {entry.event_type}
              </td>
              <td className="max-w-xl px-4 py-3">
                <pre className="whitespace-pre-wrap break-words rounded bg-black/40 p-2 text-xs leading-relaxed">
                  {JSON.stringify(entry.detail, null, 2)}
                </pre>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {rows.length === 0 && (
        <p className="px-4 py-6 text-center text-sm text-zinc-500">No audit entries.</p>
      )}
    </div>
  );
}
