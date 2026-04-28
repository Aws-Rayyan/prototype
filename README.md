# Gaia prototype — permission-aware grounded assistant

One-day prototype of an enterprise assistant with mock login, permission-aware retrieval, grounded answers with citations, draft actions, approval workflow, and an audit trail.

## Prerequisites

- **Python** 3.11+
- **Node.js** 18+ (npm)

## Quick start

### 1. Backend (FastAPI)

```powershell
cd server
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API base: `http://127.0.0.1:8002`
- Health: `GET http://127.0.0.1:8002/health`

On first run, the SQLite database file `server/gaia.db` is created and seeded with ~12 internal documents tagged by allowed roles (`sales_manager`, `hr_manager`, engineering-only demo doc).

### 2. Frontend (Vite + React)

```powershell
cd client
npm install
npm run dev
```

Open `http://localhost:5173`.

The dev server proxies `/api` and `/health` to the FastAPI process (`client/vite.config.ts`). Every API call sends the mock identity via `X-User-Id: alice|bob|aws`.

## Mock identities

| ID    | Role                              | Typical docs                                                            |
| ----- | --------------------------------- | ----------------------------------------------------------------------- |
| alice | Sales Manager                     | Pipeline, territories, discounts, SPIFFs, shared policies               |
| bob   | HR Manager                        | Benefits, hiring, incidents, shared policies                            |
| aws   | `no_document_access` (Aws Rayyan) | **None** — not listed on any seeded document; retrieval is always empty |

Engineering-only seeded content is **never** visible to Alice or Bob; asking about it should return **insufficient evidence**. Aws Rayyan has no corpus permissions at all, so every question resolves to **insufficient evidence** with no citations.

## Product flows

1. **Ask Gaia** — ask a question; answer is built only from docs your role may read. Citations quote accessible snippets. Low confidence shows an explicit insufficient-evidence message.
2. **Create draft action** — email / note / task with body prefilled from the last answer (blocked when confidence is insufficient).
3. **Approvals** — review draft payloads; approve or reject (state stored in SQLite, not UI-only).
4. **My actions** — list actions you created with current status.
5. **Audit log** — chronological JSON events for questions, drafts, approvals/rejections.

## Tradeoffs (intentional)

- **No real auth** — header-based mock user switcher; focus is on server-side permission correctness.
- **Keyword retrieval** instead of vectors — fast for a prototype and easy to reason about.
- **Rule-based “LLM”** — template + extractive snippets; assignment allows this and rewards grounding.
- **SQLite file DB** — zero ops, easy for reviewers; adequate for demo scale.
- **Single approval queue** — any logged-in mock user can approve drafts to keep the demo frictionless.

## Repo layout

```
gaia/
├── server/           # FastAPI + SQLite
├── client/           # React + Vite + Tailwind v4
├── README.md
└── ARCHITECTURE.md
```
