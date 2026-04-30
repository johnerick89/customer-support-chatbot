"""
ASGI entry for Vercel (`api/index.py` → serverless) and local `uvicorn index:app`.

Imports the FastAPI app from the `backend` package at the repository root.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from backend.main import app  # noqa: E402

__all__ = ["app"]
