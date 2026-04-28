import { NavLink, Route, Routes } from "react-router-dom";
import UserSwitcher from "./components/UserSwitcher";
import ActionsPage from "./pages/ActionsPage";
import ApprovalsPage from "./pages/ApprovalsPage";
import AskPage from "./pages/AskPage";
import AuditPage from "./pages/AuditPage";

export default function App() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800 bg-zinc-900/60 backdrop-blur">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-4 py-4">
          <div>
            <div className="text-sm font-semibold uppercase tracking-wide text-teal-400">
              Gaia
            </div>
            <h1 className="text-lg font-semibold">Permission-aware assistant</h1>
          </div>
          <UserSwitcher />
          <nav className="flex flex-wrap gap-4 text-sm font-medium">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? "text-teal-400" : "text-zinc-400 hover:text-zinc-100"
              }
            >
              Ask Gaia
            </NavLink>
            <NavLink
              to="/actions"
              className={({ isActive }) =>
                isActive ? "text-teal-400" : "text-zinc-400 hover:text-zinc-100"
              }
            >
              My Actions
            </NavLink>
            <NavLink
              to="/approvals"
              className={({ isActive }) =>
                isActive ? "text-teal-400" : "text-zinc-400 hover:text-zinc-100"
              }
            >
              Approvals
            </NavLink>
            <NavLink
              to="/audit"
              className={({ isActive }) =>
                isActive ? "text-teal-400" : "text-zinc-400 hover:text-zinc-100"
              }
            >
              Audit
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-10">
        <Routes>
          <Route path="/" element={<AskPage />} />
          <Route path="/actions" element={<ActionsPage />} />
          <Route path="/approvals" element={<ApprovalsPage />} />
          <Route path="/audit" element={<AuditPage />} />
        </Routes>
      </main>
    </div>
  );
}
