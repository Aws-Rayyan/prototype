"""Gaia assistant API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import actions_router, approvals_router, ask_router, audit_router, users_router
from seed import seed_documents


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_documents()
    yield


app = FastAPI(title="Gaia Assistant API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router.router, prefix="/api")
app.include_router(ask_router.router, prefix="/api")
app.include_router(actions_router.router, prefix="/api")
app.include_router(approvals_router.router, prefix="/api")
app.include_router(audit_router.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
