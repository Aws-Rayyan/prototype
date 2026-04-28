import { useEffect, useState } from "react";
import type { AskResponse } from "../types";

type Props = {
  open: boolean;
  onClose: () => void;
  lastAnswer?: AskResponse | null;
  onSubmit: (
    draft: Pick<
      { title: string; body: string; action_type: "email" | "note" | "task" },
      "title" | "body" | "action_type"
    >,
  ) => Promise<void>;
};

export default function DraftActionForm({
  open,
  onClose,
  lastAnswer,
  onSubmit,
}: Props) {
  const [actionType, setActionType] = useState<"email" | "note" | "task">(
    "note",
  );
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open && lastAnswer) {
      setTitle(`Follow-up on: ${lastAnswer.question_id}`);
      setBody(lastAnswer.answer);
    }
  }, [open, lastAnswer]);

  if (!open) return null;

  async function submit() {
    setSaving(true);
    try {
      await onSubmit({ title, body, action_type: actionType });
      onClose();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
      <div className="w-full max-w-lg rounded-xl border border-zinc-700 bg-zinc-900 p-6 shadow-2xl">
        <h2 className="text-lg font-semibold">Create draft action</h2>
        <p className="mt-1 text-sm text-zinc-400">
          Drafts are stored server-side and require approval before finalization.
        </p>
        <div className="mt-4 space-y-3">
          <label className="block text-sm">
            <span className="text-zinc-400">Type</span>
            <select
              className="mt-1 w-full rounded border border-zinc-700 bg-zinc-950 px-3 py-2"
              value={actionType}
              onChange={(e) =>
                setActionType(e.target.value as typeof actionType)
              }
            >
              <option value="email">Follow-up email</option>
              <option value="note">Internal note</option>
              <option value="task">Task</option>
            </select>
          </label>
          <label className="block text-sm">
            <span className="text-zinc-400">Title</span>
            <input
              className="mt-1 w-full rounded border border-zinc-700 bg-zinc-950 px-3 py-2"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>
          <label className="block text-sm">
            <span className="text-zinc-400">Body</span>
            <textarea
              className="mt-1 min-h-[160px] w-full rounded border border-zinc-700 bg-zinc-950 px-3 py-2"
              value={body}
              onChange={(e) => setBody(e.target.value)}
            />
          </label>
        </div>
        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            className="rounded border border-zinc-600 px-4 py-2 text-sm"
            onClick={onClose}
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="button"
            className="rounded bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-500 disabled:opacity-50"
            onClick={() => void submit()}
            disabled={saving}
          >
            Save draft
          </button>
        </div>
      </div>
    </div>
  );
}
