# Customer Support Chatbot

Meridian Electronics prototype: **Next.js** UI + **FastAPI** (`backend`) on **Python 3.11**, deployable on **Vercel**.

## Documentation

- **[DESIGN.md](DESIGN.md)** — architecture and flows  
- **[task.md](task.md)** — assessment brief  

## Local development

1. **Python (API)** — from repo root:

   ```bash
   uv sync
   uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Next.js** — in another terminal:

   ```bash
   npm install
   npm run dev
   ```

Next rewrites `/auth/verify` and `/api/stream` to `http://127.0.0.1:8000` by default. Override with **`API_ORIGIN`** in `.env.local` (no trailing slash).

## Deploy on Vercel

- **Same project:** leave **`API_ORIGIN` unset**. Next (see `next.config.ts`) proxies auth and chat to the Python serverless entry **`api/index.py`**, which imports **`backend.main:app`**.  
- **Separate API:** set **`API_ORIGIN`** to that server’s base URL.

Root **`vercel.json`** runs `npm install` / `npm run build` and configures Python **3.11** for `api/**/*.py`.
