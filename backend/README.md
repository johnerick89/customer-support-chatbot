# Backend (FastAPI package)

This directory is the importable Python package **`backend`** (`main.py`, `schemas`, `routers/`).

- **Dependencies & lockfile:** use **[uv](https://docs.astral.sh/uv/)** at the **repository root** (`../pyproject.toml`, `../uv.lock`).
- **ASGI entry for Vercel:** `../api/index.py` re-exports `backend.main:app`.

## Local API server

From repository root (after `uv sync`):

```bash
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Or the same app via the thin shim (matches Vercel’s module path):

```bash
uv run uvicorn index:app --reload --host 127.0.0.1 --port 8000 --app-dir api
```

Next.js (`npm run dev`) rewrites `/auth/verify` and `/api/stream` to this server by default.
