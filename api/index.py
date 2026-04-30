import hashlib
import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()


class VerifyRequest(BaseModel):
    email: str = Field(min_length=1)
    pin: str = Field(min_length=1)


@app.post("/auth/verify")
async def verify(body: VerifyRequest):
    """
    Prototype: accept any non-empty email + PIN so you can exercise the UI
    against a local or deployed API without real MCP credentials.
    """
    email = body.email.strip()
    if not email or not body.pin:
        raise HTTPException(status_code=400, detail="Email and PIN are required")

    local = email.split("@", 1)[0].replace(".", " ").strip() or "Customer"
    name = local.title()
    digest = hashlib.sha256(email.encode()).hexdigest()[:12]

    return {
        "id": f"cust-{digest}",
        "email": email,
        "pin": "",
        "name": name,
    }


@app.post("/stream")
async def stream():
    async def generator():
        for word in ["Hello", " from", " your", " chatbot"]:
            yield word
            time.sleep(0.3)

    return StreamingResponse(generator(), media_type="text/plain")
