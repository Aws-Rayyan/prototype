## Architecture (one page)

### Frontend (`client/`)

- **Stack:** React 19, Vite 8, TypeScript, Tailwind CSS v4 (`@tailwindcss/vite`), React Router v7.
- **Structure:**
  - `src/pages/*` route-level screens (`AskGaia`, drafts, approvals, audit).
  - `src/components/*` reusable UI (answer card with citations & confidence, draft modal, approval cards, audit table).
  - `src/context/UserContext.tsx` keeps the mock user (`alice` / `bob` / `aws`) in sync with `localStorage` and injects **`X-User-Id`** on every Axios request.
- **Networking:** Axios instance with interceptor; `/api/**` proxied during dev so the browser speaks same-origin to Vite (`vite.config.ts`).

### Backend (`server/`)

- **Stack:** FastAPI + Uvicorn, Python `sqlite3`, Pydantic v2 models (`models.py`).
- **Structure:**
  - `database.py` — connection factory, schema DDL, indexes.
  - `seed.py` — seeds documents once when `documents` is empty on startup (`main.py` lifespan).
  - `services/retrieval.py` — selects **only permitted** documents (`json_each` on `allowed_roles` JSON array), then scores filtered rows with weighted keyword overlap. Forbidden corpora never enter ranking.
  - `services/answer_generator.py` — template + extractive sentences (no external LLM). Emits structured citations and confidence tiers.
  - `services/action_service.py` / `approval` logic — CRUD-ish helpers for drafts + status mutations.
  - `services/audit_service.py` — append-only JSON payloads stored in `audit_log`.
  - `routers/*` — route modules mounted under `/api` in `main.py`.

### Permission model

- Documents carry `allowed_roles` as JSON string arrays (`["sales_manager"]`, shared arrays, engineering-only `[ "engineering_lead" ]`).
- Retrieval filters **at the database/query layer** using `json_each`.
- **Answer generation consumes only retrieved rows**, so inaccessible documents cannot influence summaries, citations, draft suggestions, or audit previews.

### Answer generation approach

1. Keyword tokenization with light stop-word removal (`services/retrieval.py`).
2. Relevance normalization using overlap / sqrt(doc token count) plus substring rescue for phrases.
3. Confidence levels:
   - `well_supported`: strong aggregate score across top hits OR single standout doc score.
   - `partial`: mid scores (explicit caution string appended client-side/backend).
   - `insufficient`: no hits above threshold → safe refusal boilerplate **without** hallucinated citations.
4. Sentence picking chooses sentences sharing query tokens; fallback to clipped body chunk.

### Approvals & audit design

- `actions.status` persisted (`draft → approved/rejected`). Reviewer IDs + timestamps stored on PATCH.
- Each meaningful event logs to `audit_log` (`question_asked`, `action_drafted`, `action_approved|rejected`).
- Audit entries hold structured JSON payloads (question text, previews, citation IDs); full bodies truncated for readability but always derived from authorized retrieval paths.
