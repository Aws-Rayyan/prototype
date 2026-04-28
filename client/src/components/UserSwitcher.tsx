import { MOCK_USERS, useUserContext } from "../context/UserContext";

function optionLabel(userId: string): string {
  switch (userId) {
    case "alice":
      return "Alice Johnson (Sales Manager)";
    case "bob":
      return "Bob Smith (HR Manager)";
    case "aws":
      return "Aws Rayyan (no corpus access)";
    default:
      return userId;
  }
}

export default function UserSwitcher() {
  const { user, setUserId } = useUserContext();

  return (
    <div className="flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm">
      <span className="text-zinc-400">Acting as:</span>
      <select
        className="rounded border border-zinc-600 bg-zinc-950 px-2 py-1 text-zinc-100"
        value={user.id}
        onChange={(e) => setUserId(e.target.value)}
        aria-label="Switch mock user"
      >
        {MOCK_USERS.map((u) => (
          <option key={u.id} value={u.id}>
            {optionLabel(u.id)}
          </option>
        ))}
      </select>
    </div>
  );
}
