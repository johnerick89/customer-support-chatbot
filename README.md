# Customer Support Chatbot

Prototype for **Meridian Electronics** customer support: sign-in, then a streaming chat that (in the full design) calls a **FastAPI** backend and an **MCP** order/product service.

## Stack

- **Frontend:** Next.js (App Router), Tailwind — `frontend/`
- **API:** FastAPI — `api/`
- **Integrations:** MCP server (Streamable HTTP) for catalog, customers, and orders — see `task.md`

## Documentation

- **[DESIGN.md](DESIGN.md)** — architecture, auth/chat flows, MCP tool surface, and agent guidelines.
- **`task.md`** — assessment brief, constraints, and deliverables.

## Quick start (local)

1. **API** — from `api/`: create a venv, `pip install -r requirements.txt`, then `uvicorn index:app --reload --port 8000`.
2. **Frontend** — from `frontend/`: `npm install`, `npm run dev`. Optional `frontend/.env.local`: `API_ORIGIN=http://127.0.0.1:8000` (default).

The Next dev server rewrites `/auth/verify` and `/api/stream` to the FastAPI origin so the browser stays same-origin.

## Deploy

Set **`API_ORIGIN`** on the Next deployment to your live FastAPI base URL. Repo **`vercel.json`** configures the Next build; align Python routing and env vars with how you host `api/`.
